import logging
from datetime import (
    date,
    timedelta,
)
from typing import (
    Iterable,
    List,
    Optional,
    Tuple,
)

from sqlalchemy import func

from caerp.models.activity import (
    Activity,
    ActivityType,
    Attendance,
    Event,
)
from caerp.models.career_path import MotifSortieOption
from caerp.models.user import (
    User,
    Login,
)
from caerp.models.user.userdatas import (
    STATUS_OPTIONS,
    SocialDocTypeOption,
    UserDatas,
    UserDatasSocialDocTypes,
)
from caerp.models.user.utils import (
    get_all_userdatas_active_on_period,
    get_epci_label,
    get_userdatas_exit,
    get_user_analytical_accounts,
    get_tuple_option_label,
    get_social_statuses_label,
    get_userdatas_cae_situation,
    get_userdatas_last_step,
    get_userdatas_steps_on_period,
    get_num_hours_worked,
)
from caerp.dataqueries.base import BaseDataQuery
from caerp.utils.dataqueries import dataquery_class

logger = logging.getLogger(__name__)


def _is_equipe(login: Login):
    return login.account_type == "equipe_appui"


def social_status_to_flags(social_status_label) -> Tuple[str, str, str, str]:
    # Les booléens successifs correspondent à, dans l'ordre:
    # Chômeurs moins de 2 ans (OUI / NON)
    # Chômeurs de longue durée (OUI / NON)
    # Personnes inactives (OUI / NON)
    # Personne exerçant un emploi, y compris les indépendants (OUI / NON)

    _map = {
        "Salarié.e - Temps plein": (False, False, False, True),
        "Salarié.e - Temps partiel": (False, False, False, True),
        "Demandeur.e d'emploi (plus de 2 ans) - Non indemnisé.e": (
            False,
            True,
            True,
            False,
        ),
        "Demandeur.e d'emploi (plus de 2 ans) - Indemnisé.e": (
            False,
            True,
            True,
            False,
        ),
        "Demandeur.e d'emploi (entre 1 et 2 ans) - Non indemnisé.e": (
            True,
            False,
            True,
            False,
        ),
        "Demandeur.e d'emploi (entre 1 et 2 ans) - Indemnisé.e": (
            True,
            False,
            True,
            False,
        ),
        "Demandeur.e d'emploi (moins de 1 an) - Non indemnisé.e": (
            True,
            False,
            True,
            False,
        ),
        "Demandeur.e d'emploi (moins de 1 an) - Indemnisé.e": (
            True,
            False,
            True,
            False,
        ),
        "Étudiant.e": (False, False, False, False),
        # "RSA": [],
    }
    try:
        return _map[social_status_label]
    except KeyError:
        return ("INCONNU",) * 4


def exit_type_to_flags(
    all_motifs: List[MotifSortieOption], motif: MotifSortieOption
) -> List[bool]:
    flags = []

    for existing_motif in all_motifs:
        if motif == existing_motif:
            flags.append(True)
        else:
            flags.append(False)

    return flags


def doctypes_to_flags(userdatas: UserDatas, docs_to_show: List[str]) -> List[bool]:
    """
    Returns a flag for each of the social doc types we have interest in.

    :param userdatas:
    :param docs_to_show: the list of docs to be shown
    :return: True/False for each doctype listed in docs_to_show, in same order as docs_to_show
    """
    docs = (
        UserDatasSocialDocTypes.query()
        .join(UserDatasSocialDocTypes.doctype)
        .filter(
            UserDatasSocialDocTypes.userdatas == userdatas,
            SocialDocTypeOption.label.in_(docs_to_show),
        )
    )
    db_dict = {doc.doctype.label: doc.status for doc in docs.all()}
    return [db_dict.get(k, False) for k in docs_to_show]


def get_activity_date(
    user: User, after_date: date, activity_type: str
) -> Optional[date]:
    q = Attendance.query()
    q = q.join(Activity, Attendance.user, User.userdatas, ActivityType)
    q = q.filter(
        Attendance.status.in_(("registered", "attended")),
        ActivityType.label == activity_type,
        Activity.datetime >= after_date,  # ,UserDatas.parcours_date_info_coll,
        User.id == user.id,
    )
    activity = q.first()
    if activity is not None:
        return activity.event.datetime.date()
    else:
        return None


@dataquery_class()
class OBActiveOrSupportedESQuery(BaseDataQuery):
    name = "ob_porteurs_actifs_ou_accompagnes_periode"
    label = (
        "[OUVRE-BOITES] Requête stats financeurs (porteurs actifs et/ou accompagnés)"
    )
    description = """
    <p>
        Liste de tous les porteurs de projets actifs sur la période choisie avec les informations nécessaires pour les financeurs BPI/FSE.
    </p>
    <p>
        Requête taillée pour les besoins et la config de l'<a href="https://ouvre-boites.coop">Ouvre-Boites</a> sur la base des requêtes existantes « porteurs actifs » et « porteurs accompagnés ».
    </p>
    <br/>
    <ul>
        <li>Un porteur est considéré <strong>actif</strong> si il est présent sur au moins une partie de la période (présent signifie <em>entré</em> et pas encore <em>sorti</em> au regard des étapes de parcours).</li>
        <li>Un porteur est considéré <strong>accompagné</strong> s'il a eu un rendez-vous 
    d'accompagnement ou a participé à un atelier (en étant présent) sur la période.</li>
    </ul>
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cached just the time of the query generation
        self._cached_exit_types = MotifSortieOption.query().all()
        self._docs_to_show = [
            "Avis situation Pôle Emploi",
            "Déclaration Minimis",
            "Attestation RQTH",
            "Questionnaire FSE",
        ]

    def default_dates(self):
        self.start_date = self.date_tools.year_start()
        self.end_date = self.date_tools.year_end()

    def headers(self):
        headers = [
            "Identifiant enDI",
            "Code(s) analytique(s)",
            "Civilité",
            "Nom",
            "Nom de naissance",
            "Prénom",
            "E-mail 1",
            "Tél. fixe",
            "Tél. mobile",
            "Adresse",
            "Code postal",
            "Ville",
            # Désactivé pour l'instant, lent, aurait plus sa place dans une autre requete de vérif de données
            # "EPCI (auto depuis geo.api.gouv)",
            "Zone d'habitation (infos manquantes complétées depuis geo.api.gouv)",  # EPCI et quartier
            "QPV ?",
            f"Situation dans la CAE (au {self.end_date:%d/%m/%Y})",
            "Sociétaire (OUI/NON)",
            "",  # SECTION : Statut social à l'entrée
            # "Statut social à l'entrée",
            "Chômeurs moins de 2 ans (OUI / NON / INCONNU)",
            "Chômeurs de longue durée (OUI / NON / INCONNU)",
            "Personne inactive  (OUI / NON / INCONNU)",
            "Personne exerçant un emploi, y compris les indépendants (OUI / NON / INCONNU)",
            "Antenne de rattachement",
            "Accompagnateur",
            "Prescripteur",
            "Sexe",
            "Date de naissance",
            "Code postal lieu de naissance",
            "Nationalité",
            "Fin de validité de la carte de séjour",
            "Reconnaissance RQTH (OUI/NON)",
            "Numéro de sécurité sociale",
            "Situation familiale",
            "Nombre d'enfants",
            "Niveau d'études",
            "",  # SECTION : Parcours
            "Date info coll",
            "Date 1er RDV",
            "Date signature CAPE",
            "Date CESA",
            "Date d'entrée au sociétariat",
            f"Nombre d'heure contractuel au {self.start_date:%d/%m/%Y}",
            "Nombre d'heures calculées + projetée sur période",
            "Sortie (OUI/NON)",
            "Date de sortie",
            "Type de sortie",  # Ajout Jocelyn, il me semble que ça pouvait être utile
            # "Exerce une activité d'indépendant (OUI / NON)",
            # "Exerce un emploi durable (CDI ou CDD) (OUI / N   ON)",
            # "Exerce un emploi temporaire (OUI / NON)",
            # "Exerce un emploi aidé (OUI / NON)", ## TODO: voir pour éventuellement la rajouter, demande un paramétrage enDI
            # "Est en formation (OUI / NON)",
            # "Recherche activement un emploi (OUI / NON)",
            # Cette ligne correspond aux options du dessus
            *[f"{motif.label} (OUI/NON)" for motif in self._cached_exit_types],
            "",  # SECTION : Justificatifs FSE
            *[f"{i} (OUI/NON)" for i in self._docs_to_show],
            # "Statut social à l'entrée",
            # "Statut social actuel",
            "Date de fin de droit",
            "Typologie d'activité principale",
            "Équipe d'appui",
            "Raison de retenue dans les données",
        ]

        return headers

    def data(self):
        data = []
        active_users: Iterable[UserDatas] = get_all_userdatas_active_on_period(
            self.start_date, self.end_date
        )
        user_ids_in_request = set()

        for u in active_users:
            data_row = self.data_row_from_userdatas(u)
            data.append(data_row + ["Porteur actif"])
            user_ids_in_request.add(u.user.id)

        supported_users = (
            User.query()
            .join(Attendance)
            .join(Event)
            .outerjoin(UserDatas, User.id == UserDatas.user_id)  # backport ?
            .where(Event.datetime.between(self.start_date, self.end_date))
            .where(Attendance.status == "attended")
            # On exclut tous les workshop qui ne sont pas des infocol
            .where(
                (Event.type_ != "workshop")
                | func.lower(Event.name).contains("collective")
            )
            .distinct()
            .order_by(User.lastname, User.firstname)
        )
        for user in supported_users:
            if (
                not user.login.account_type == "entrepreneur" and user.userdatas is None
            ) or (user.id in user_ids_in_request):
                continue
            else:
                if user.userdatas:
                    data_row = self.data_row_from_userdatas(user.userdatas)
                else:
                    # Should not happen in OB context (and if so, this is likely garbage data)
                    logger.warning("Ignoring user #{user.id} without userdatas")
                data.append(data_row + ["Porteur accompagné"])
                user_ids_in_request.add(user.id)

        return data

    def data_row_from_userdatas(self, u: UserDatas):
        cae_situation = get_userdatas_cae_situation(u.id, self.end_date)

        if cae_situation:
            cae_situation_label = cae_situation.label
        elif u.parcours_date_info_coll and (u.parcours_date_info_coll <= self.end_date):
            # À l'OB, l'étape de parcours infocol n'est pas forcément remplie, on fallback
            cae_situation_label = "Candidat"
        else:
            cae_situation_label = ""
        social_status_flags = social_status_to_flags(
            get_social_statuses_label(u.social_statuses)
        )
        # Dernière sortie en date (si on a eu plusieurs parcours)
        latest_exit_ = get_userdatas_exit(u.id, before_date=self.end_date)
        # Première étape hors sortie du parcours (il peut y avoir eu plusieurs parcours
        # Si c'est le cas dans la période, on ne considère que le dernier en date
        # Dans certain cas limites, c'est un choix qui peut fausser
        # (cas de plusieurs parcours au sein de la même période, mais rarissime)
        current_parcours_steps = get_userdatas_steps_on_period(
            u.id,
            period_end_date=self.end_date,
            period_start_date=latest_exit_.start_date if latest_exit_ else None,
            stage_type_exclude=["exit"],
        )
        if len(current_parcours_steps) > 0:
            first_step = current_parcours_steps[0]

        date_premier_rdv_diag = (
            get_activity_date(
                u.user,
                after_date=u.parcours_date_info_coll,
                activity_type="1er RDV diag",
            )
            if u.parcours_date_info_coll
            else None
        )
        # Contrat CESA ou avenant, dernier en date
        dernier_cesa_ou_avenant = get_userdatas_last_step(
            u.id,
            limit_date=self.end_date,
            # À l'OB ça qualifie une signature de CESA
            stage_type_filter=["contract", "amendment"],
        )

        # Contrat CAPE, dernier en date
        # en cas d'entrée/sortie, on veut la dernière entrée en date
        last_cape_step = get_userdatas_last_step(
            u.id,
            limit_date=self.end_date,
            # À l'OB ça qualifie une signature de CAPE
            stage_type_filter=["entry"],
        )

        # Contrat CESA, dernier en date
        # en cas d'entrée/sortie, on veut la dernière entrée en date
        last_cesa_step = get_userdatas_last_step(
            u.id,
            limit_date=self.end_date,
            # À l'OB ça qualifie une signature de CESA
            stage_type_filter=["contract"],
        )
        user_data = [
            u.user_id,
            # u.coordonnees_identifiant_interne,
            get_user_analytical_accounts(u.user_id),
            u.coordonnees_civilite,
            u.coordonnees_lastname,
            u.coordonnees_ladies_lastname,
            u.coordonnees_firstname,
            u.coordonnees_email1,
            u.coordonnees_tel,
            u.coordonnees_mobile,
            u.coordonnees_address,
            u.coordonnees_zipcode,
            u.coordonnees_city,
            # Désactivé pour l'instant, lent, aurait plus sa place dans une autre requete de vérif de données
            # get_epci_label(u.coordonnees_zipcode, u.coordonnees_city),
            # TODO: ici on voudrait bien requêter la BDD de l'ANCT plutôt
            # que de faire une saisie manuelle…
            # Demande envoyée le 13/3 https://sig.ville.gouv.fr/page/174
            # Requête api.geo.gouv pour les champs non remplis
            u.coordonnees_zone.label
            if u.coordonnees_zone
            else get_epci_label(u.coordonnees_zipcode, u.coordonnees_city),
            u.coordonnees_zone_qual.label  # et celui-ci
            if u.coordonnees_zone_qual
            else "",
            cae_situation_label,
            "OUI" if u.situation_societariat_entrance else "NON",
            "",  # SECTION : Statut social à l'entrée
            # get_social_statuses_label(u.social_statuses),
            *("OUI" if i else "NON" for i in social_status_flags),  # x 4
            u.situation_antenne.label if u.situation_antenne else "",
            u.situation_follower.label if u.situation_follower else "",
            u.parcours_prescripteur.label if u.parcours_prescripteur else "",
            u.coordonnees_sex,
            self.date_tools.format_date(u.coordonnees_birthday),
            u.coordonnees_birthplace_zipcode,
            u.coordonnees_nationality,
            self.date_tools.format_date(u.coordonnees_resident),
            # ça veut dire que même si on a 1J d'AAH, c'est considéré RQTH:
            "OUI"
            if (
                u.statut_handicap_allocation_expiration
                and u.statut_handicap_allocation_expiration > self.start_date
            )
            else "NON",
            str(u.coordonnees_secu),
            get_tuple_option_label(STATUS_OPTIONS, u.coordonnees_family_status),
            u.coordonnees_children,
            u.coordonnees_study_level.label if u.coordonnees_study_level else "",
            "",  # SECTION : Parcours
            self.date_tools.format_date(u.parcours_date_info_coll),
            self.date_tools.format_date(date_premier_rdv_diag),
            self.date_tools.format_date(last_cape_step.start_date)
            if last_cape_step
            else "",
            self.date_tools.format_date(last_cesa_step.start_date)
            if last_cesa_step
            else "",
            self.date_tools.format_date(u.situation_societariat_entrance),
            dernier_cesa_ou_avenant.num_hours if dernier_cesa_ou_avenant else "",
            get_num_hours_worked(u, self.start_date, self.end_date + timedelta(days=1)),
            "OUI" if latest_exit_ else "NON",
            self.date_tools.format_date(latest_exit_.start_date)
            if latest_exit_
            else "",
            latest_exit_.type_sortie.label
            if latest_exit_ and latest_exit_.type_sortie
            else "",
            *(
                (
                    "OUI" if bool_flag else "NON"
                    for bool_flag in exit_type_to_flags(
                        self._cached_exit_types,
                        latest_exit_.motif_sortie,
                    )
                )
                if latest_exit_
                else (("",) * len(self._cached_exit_types))
            ),
            "",
            *(
                "OUI" if bool_flag else "NON"
                for bool_flag in doctypes_to_flags(u, self._docs_to_show)
            ),
            self.date_tools.format_date(u.statut_end_rights_date),
            u.activity_typologie.label if u.activity_typologie else "",
            ("OUI" if _is_equipe(u.user.login) else "NON") if u.user.login else "NON",
        ]
        return user_data
