import json
import logging

from datetime import date
from dateutil.relativedelta import relativedelta
from functools import lru_cache
from typing import (
    Optional,
    Union,
    List,
    Tuple,
    Iterable,
)

import requests
from caerp_base.models.base import DBSESSION
from caerp.models.activity import (
    Event,
    Attendance,
    Activity,
)
from caerp.models.config import Config
from caerp.models.career_path import CareerPath
from caerp.models.user.userdatas import (
    User,
    UserDatas,
    UserDatasCustomFields,
    CaeSituationOption,
)
from caerp.models.workshop import Timeslot
from caerp.utils.colanderalchemy import get_model_columns_list


logger = logging.getLogger(__name__)


def get_userdatas_first_step(
    userdatas_id: int, limit_date: date = None, stage_type_filter: List[str] = None
) -> Union[CareerPath, None]:
    """
    Return the first CareerPath with a stage type of the user
    after the given date if specified
    with the given stage types if specified

    :param userdatas_id: id of the userdatas concerned
    :param limit_date: Optional limit date, we want the first step after this date
    :param stage_type_filter: Optional list of the stage types we want
        eg: ['exit'], ['entry','contract']

    :returns: A CareerPath (the first step) or None
    """
    first_step_query = (
        DBSESSION()
        .query(CareerPath)
        .filter(CareerPath.userdatas_id == userdatas_id)
        .filter(CareerPath.stage_type != None)
    )
    if limit_date:
        first_step_query = first_step_query.filter(CareerPath.start_date >= limit_date)
    if stage_type_filter:
        first_step_query = first_step_query.filter(
            CareerPath.stage_type.in_(stage_type_filter)
        )
    first_step_query = first_step_query.order_by(CareerPath.start_date)
    return first_step_query.first()


def get_userdatas_last_step(
    userdatas_id: int, limit_date: date = None, stage_type_filter: List[str] = None
) -> Union[CareerPath, None]:
    """
    Return the last CareerPath with a stage type of the user
    before the given date if specified
    with the given stage types if specified

    :param userdatas_id: id of the userdatas concerned
    :param limit_date: Optional limit date, we want the last step before this date
    :param stage_type_filter: Optional list of the stage types we want
        eg: ['exit'], ['entry','contract']

    :returns: A CareerPath (the last step) or None
    """
    last_step_query = (
        DBSESSION()
        .query(CareerPath)
        .filter(CareerPath.userdatas_id == userdatas_id)
        .filter(CareerPath.stage_type != None)  # noqa: E711
    )
    if limit_date:
        last_step_query = last_step_query.filter(CareerPath.start_date <= limit_date)
    if stage_type_filter:
        last_step_query = last_step_query.filter(
            CareerPath.stage_type.in_(stage_type_filter)
        )
    last_step_query = last_step_query.order_by(CareerPath.start_date.desc())
    return last_step_query.first()


def get_userdatas_steps_on_period(
    userdatas_id: int,
    period_start_date: Optional[date],
    period_end_date: date,
    stage_type_only: List[str] = None,
    stage_type_exclude: List[str] = None,
    sort_descending: bool = False,
) -> List[CareerPath]:
    """
    Return all the CareerPath with a stage type of the user between two dates
    with the given stage types if specified

    :param userdatas_id: id of the userdatas concerned
    :param period_start_date: The period start date, we want the steps after this date
    :param period_end_date: The period end date, we want the steps before this date
    :param stage_type_only: Optional list of the stage types we want
        eg: ['exit'], ['entry','contract','amendment']
    :param stage_type_exclude: Optional list of the stage types we do not want
    :param sort_descending: True if we want the steps sorted from last to first

    :returns: A list of CareerPath (the steps)
    """
    steps_query = (
        DBSESSION()
        .query(CareerPath)
        .filter(CareerPath.userdatas_id == userdatas_id)
        .filter(CareerPath.start_date <= period_end_date)
        .filter(CareerPath.stage_type != None)
    )
    if period_start_date:
        steps_query = steps_query.filter(CareerPath.start_date >= period_start_date)

    if stage_type_only:
        steps_query = steps_query.filter(CareerPath.stage_type.in_(stage_type_only))
    if stage_type_exclude:
        steps_query = steps_query.filter(
            CareerPath.stage_type.notin_(stage_type_exclude)
        )
    if sort_descending:
        steps_query = steps_query.order_by(CareerPath.start_date.desc())
    else:
        steps_query = steps_query.order_by(CareerPath.start_date)
    return steps_query.all()


def get_userdatas_entry_date(userdatas_id: int) -> Union[date, None]:
    """
    Compute the entry date of the user
    This is the start date of the first CareerPath with a stage
    of type 'entry' or 'contract'
    """
    first_entry = get_userdatas_first_step(
        userdatas_id, stage_type_filter=["entry", "contract"]
    )
    return first_entry.start_date if first_entry else None


def get_userdatas_contract_date(userdatas_id: int) -> Union[date, None]:
    """
    Compute the first contract date of the user
    This is the start date of the first CareerPath with a stage
    of type 'contract'
    """
    first_contract = get_userdatas_first_step(
        userdatas_id,
        stage_type_filter=["contract"],
    )
    return first_contract.start_date if first_contract else None


def get_userdatas_exit_date(
    userdatas_id: int, before_date: date = None
) -> Union[date, None]:
    """
    Compute the exit date of the user
    This is the date of the last CareerPath with a stage type if the type is 'exit'

    NB : User can exit and come back, this return the exit date only if the last
    typed step is an exit

    :param before_date: if set, ignore any exit occurring strictly after this date.
    """
    exit_date = None
    last_step = get_userdatas_last_step(userdatas_id, before_date)
    if last_step:
        if last_step.stage_type == "exit":
            exit_date = last_step.start_date
    return exit_date


def get_userdatas_exit(
    userdatas_id: int, before_date: date = None
) -> Union[CareerPath, None]:
    """
    Return the exit object of given user
    This is the last CareerPath with a stage type if the type is 'exit'

    NB : User can exit and come back, this return the exit only if the last
    typed step is an exit

    :param before_date: if set, ignore any exit occurring strictly after this date.

    :returns: A CareerPath or None
    """
    last_step = get_userdatas_last_step(userdatas_id, before_date)
    if last_step:
        if last_step.stage_type == "exit":
            return last_step
    return None


def get_userdatas_seniority(user_id: int, date_ref: date = None) -> int:
    """
    Return the seniority (in months) of the given user in the CAE calculated
    from entry date to the earliest date between given date, exit date, and today
    """
    entry_date = get_userdatas_entry_date(user_id)
    exit_date = get_userdatas_exit_date(user_id)
    end_date = min(d for d in [date_ref, exit_date, date.today()] if d is not None)
    td = relativedelta(end_date, entry_date)
    return (td.years * 12) + td.months


def is_userdatas_active_on_period(userdatas_id: int, start: date, end: date) -> bool:
    """
    Returns whether the user was active during the given period

    This means that he has an entry before the period ends and
    no exit or an exit after the period start

    NB : User can exit and come back, the period can be on the absence
    and this function should return False in this case

    :returns: True if active else False
    """
    is_active = False
    entry_date = get_userdatas_entry_date(userdatas_id)
    if entry_date and entry_date <= end:
        exit_date = get_userdatas_exit_date(userdatas_id)
        if exit_date == None or exit_date >= start:
            is_active = True
            # Globally active, check for absences on the period
            last_step = get_userdatas_last_step(userdatas_id, start)
            if last_step:
                if last_step.career_stage.stage_type == "exit" and start < end:
                    period_steps = get_userdatas_steps_on_period(
                        userdatas_id,
                        start,
                        end,
                        stage_type_only=["entry", "contract", "amendment"],
                    )
                    if not period_steps:
                        # Exit just before the period and no return during the period
                        is_active = False
    return is_active


def get_all_userdatas_active_on_period(start: date, end: date) -> List[UserDatas]:
    """
    Returns all the UserDatas active on the given period

    This means all users that has an entry before the period ends and
    no exit or an exit after the period start

    :returns: A list of UserDatas
    """
    all = (
        UserDatas.query()
        .join(CareerPath)
        .filter(CareerPath.stage_type.in_(["entry", "contract", "amendment"]))
        .all()
    )
    actives = []
    for pp in all:
        if is_userdatas_active_on_period(pp.id, start, end):
            actives.append(pp)
    logger.debug(
        f"{len(actives)} actives user on period {start.strftime('%d/%m/%Y')} \
            to {end.strftime('%d/%m/%Y')} for {len(all)} entered users"
    )
    return actives


def get_user_analytical_accounts(user_id: int, only_active: bool = False) -> str:
    """
    Return a string with the analytical accounts of the given user
    """
    compta_str = ""
    user = User.get(user_id)
    for c in user.companies:
        if c.code_compta and c.code_compta not in compta_str:
            if c.active or not only_active:
                compta_str += f"{c.code_compta}, "
    if len(compta_str) > 0:
        compta_str = compta_str[:-2]
    return compta_str


def get_tuple_option_label(options_tuple: tuple, key: str) -> str:
    """
    Return label associated to a given key in a tuple of options '(key, label)'
    """
    try:
        label = [
            option_label
            for option_key, option_label in options_tuple
            if option_key == key
        ][0]
    except IndexError:
        label = ""
    return label


def get_social_statuses_label(social_statuses) -> str:
    """
    Return a string with the social statuses of the given user
    """
    if len(social_statuses) > 1:
        social_statuses_label = ""
        for social_status in social_statuses:
            social_statuses_label += f"{social_status.social_status.label} ; "
        social_statuses_label = social_statuses_label[:-3]
    elif len(social_statuses) == 1:
        social_statuses_label = social_statuses[0].social_status.label
    else:
        social_statuses_label = ""
    return social_statuses_label


def get_active_custom_fields() -> List[str]:
    """
    Returns the names of all active custom fields
    """
    return json.loads(Config.get_value("userdatas_active_custom_fields", "[]"))


def get_active_custom_fields_labels() -> List[str]:
    """
    Returns the labels of all active custom fields
    """
    active_custom_fields_labels = []
    for field in get_model_columns_list(UserDatasCustomFields):
        if field.name in get_active_custom_fields():
            active_custom_fields_labels.append(field.info["colanderalchemy"]["title"])
    return active_custom_fields_labels


def get_custom_field_value_string(userdatas: UserDatas, custom_field: str) -> str:
    """
    Return string value of the given custom field of the given userdatas

    Used for dataqueries exports
    """
    value = ""
    if userdatas.custom_fields:
        value = str(getattr(userdatas.custom_fields, custom_field))
    if value == "True":
        value = "Oui"
    return value


def get_userdatas_cae_situation(
    userdatas_id: int, date_ref: date = None
) -> Union[CaeSituationOption, None]:
    """
    Return the CaeSituationOption of the user
    before the given date if specified

    :param userdatas_id: id of the userdatas concerned
    :param date_ref: Optional limit date, we want the CAE situation before this date

    :returns: A CaeSituationOption (the CAE situation) or None
    """
    last_situation_step_query = (
        DBSESSION()
        .query(CareerPath)
        .filter(CareerPath.userdatas_id == userdatas_id)
        .filter(CareerPath.cae_situation_id != None)
    )
    if date_ref:
        last_situation_step_query = last_situation_step_query.filter(
            CareerPath.start_date <= date_ref
        )
    last_situation_step_query = last_situation_step_query.order_by(
        CareerPath.start_date.desc()
    )
    last_situation_step = last_situation_step_query.first()
    if last_situation_step:
        return CaeSituationOption.get(last_situation_step.cae_situation_id)
    else:
        return None


def get_user_accompaniment_stats(
    user_id: int, start: date, end: date
) -> Tuple[int, float, Union[date, None], str, int, float, Union[date, None], str]:
    """
    Return statistics on the accompaniment of the given user on the given period :
    - Number of appointments attended
    - Number of hours of appointments attended
    - Date of the last appointment attended
    - Type of the last appointment attended
    - Number of workshops attended
    - Number of hours of workshops attended
    - Date of the last workshop attended
    - Title of the last workshop attended
    """
    nb_rdvs = 0
    nb_h_rdvs = 0
    last_rdv_date = None
    last_rdv_name = ""
    nb_ateliers = 0
    nb_h_ateliers = 0
    last_atelier_date = None
    last_atelier_name = ""
    query = (
        Event.query()
        .join(Attendance)
        .where(Event.datetime.between(start, end))
        .where(Attendance.status == "attended")
        .where(Attendance.account_id == user_id)
        .order_by(Event.datetime.desc())
    )
    for event in query.all():
        if isinstance(event, Activity):
            nb_rdvs += 1
            if event.duration:
                nb_h_rdvs += int(event.duration) / 60
            if not last_rdv_date:
                last_rdv_date = event.datetime.date()
                last_rdv_name = event.type_object.label
        elif isinstance(event, Timeslot):
            nb_ateliers += 1
            time_delta = event.end_time - event.start_time
            nb_h_ateliers += time_delta.seconds / 3600
            if not last_atelier_date:
                last_atelier_date = event.datetime.date()
                last_atelier_name = event.workshop.title
        else:
            logger.error(f"Unexpected event type : {type(event)}")
    nb_h_rdvs = round(nb_h_rdvs, 2)
    nb_h_ateliers = round(nb_h_ateliers, 2)
    return (
        nb_rdvs,
        nb_h_rdvs,
        last_rdv_date,
        last_rdv_name,
        nb_ateliers,
        nb_h_ateliers,
        last_atelier_date,
        last_atelier_name,
    )


def get_user_companies_names(user_id: int, only_active: bool = False) -> str:
    """
    Return a string with the name of active companies of the given user
    """
    user = User.get(user_id)
    companies_names_str = ""
    if only_active:
        companies = user.active_companies
    else:
        companies = user.companies
    if len(companies) == 1:
        companies_names_str = f"{companies[0].name}"
    elif len(companies) > 1:
        for c in companies:
            companies_names_str += f"- {c.name}\r\n"
        companies_names_str = companies_names_str[:-2]
    return companies_names_str


def get_user_companies_goals(user_id: int, only_active: bool = False) -> str:
    """
    Return a string with the goals of active companies of the given user
    """
    user = User.get(user_id)
    companies_goals_str = ""
    if only_active:
        companies = user.active_companies
    else:
        companies = user.companies
    if len(companies) == 1:
        companies_goals_str = f"{companies[0].goal}"
    elif len(companies) > 1:
        for c in companies:
            companies_goals_str += f"- {c.goal}\r\n"
        companies_goals_str = companies_goals_str[:-2]
    return companies_goals_str


def get_user_companies_activities(
    user_id: int, only_main: bool = False, only_active: bool = False
) -> str:
    """
    Return a string with the activities of the active companies of the given user

    Option "only_main" will return only the main (first) activity of each company
    """
    user = User.get(user_id)
    companies_activities = []
    companies_activities_str = ""
    if only_active:
        companies = user.active_companies
    else:
        companies = user.companies
    for c in companies:
        if only_main:
            companies_activities.append(c.main_activity)
        else:
            for a in c.activities:
                if a not in companies_activities:
                    companies_activities.append(a.label)
    if len(companies_activities) == 1:
        companies_activities_str = f"{companies_activities[0]}"
    elif len(companies_activities) > 1:
        for activity in companies_activities:
            companies_activities_str += f"- {activity}\r\n"
        companies_activities_str = companies_activities_str[:-2]
    return companies_activities_str


def get_user_turnover(
    user_id: int, start: date, end: date, only_active: bool = False
) -> int:
    """
    Return the global turnover of the actives companies of the given user
    on the given period

    For multi-employees companies turnover is equally split by employee
    """
    user = User.get(user_id)
    user_turnover = 0
    if only_active:
        companies = user.active_companies
    else:
        companies = user.companies
    for c in companies:
        company_turnover = c.get_turnover(start, end)
        if len(c.employees) > 1:
            nb_employees = 0
            for e in c.employees:
                if e.userdatas and is_userdatas_active_on_period(
                    e.userdatas.id, start, end
                ):
                    nb_employees += 1
            user_turnover += round(company_turnover / max(1, nb_employees), 2)
        else:
            user_turnover += company_turnover
    return user_turnover


@lru_cache(maxsize=200)  # memoize
def get_epci_label(postcode: str, city: str) -> str:
    """
    From a postcode, gets EPCI (« Communauté de commune ») from geo.api.gouv.fr name

    Result is fetched from API and cached in RAM to avoid spamming the API

    :return a str (starting with "Inconnu" if no result was found)
    """
    base_url = "https://geo.api.gouv.fr"
    if not postcode or len(postcode) != 5:
        return ""
    postcode_resp = requests.get(
        f"{base_url}/communes",
        params=dict(codePostal=postcode, fields="epci"),
    )

    try:
        postcode_resp.raise_for_status()
        json_resp = postcode_resp.json()
        if not json_resp:
            raise KeyError("Code postal inconnu")

        epcis = set(i["epci"]["nom"] for i in json_resp)
        if len(epcis) == 1:
            epci_label = epcis.pop()
        else:
            # There may be >1 EPCI per postcode, another request will help
            # Using api adresse first as it allows fuzzy match
            # (/communes require exact match on name..)
            city_code_resp = requests.get(
                "https://api-adresse.data.gouv.fr/search/",
                params=dict(q=city, type="municipality", postcode=postcode, limit=1),
            )
            city_code_resp.raise_for_status()
            found_cities = city_code_resp.json()["features"]
            if len(found_cities) < 1:
                raise KeyError("Combinaison Commune/CP inconnue")
            city_insee_code = found_cities[0]["properties"]["citycode"]

            city_resp = requests.get(
                f"{base_url}/communes/{city_insee_code}",
                params=dict(fields="epci"),
            )
            city_resp.raise_for_status()
            epci_label = city_resp.json()["epci"]["nom"]

    except (requests.HTTPError, requests.ConnectionError) as e:
        logger.warning(f"Erreur en requêtant {e.request.url} : {e}")
        return "INCONNU (pas de réponse API)"

    except KeyError as e:
        return f"INCONNU ({e})"
    else:
        return epci_label


def iter_hours_change(ud: UserDatas) -> Iterable[Tuple[date, float]]:
    """
    Yields all hours change with its date

    Iterate career steps and yield the date and new hour count each time a step
    introduce a change in num_hours.
    """
    career_steps = (CareerPath.query().filter(CareerPath.userdatas == ud)).all()
    # Cannot manage to SQL-sort it, don't know why…
    career_steps.sort(key=lambda x: x.start_date)
    for step in career_steps:
        if step.num_hours:
            hours_per_day = step.num_hours * 12 / 365
            yield step.start_date, hours_per_day
        elif step.stage_type == "exit":
            yield step.start_date, 0


def get_num_hours_worked(ud: UserDatas, start_date, end_date) -> int:
    """
    Returns the number of hours worked within a time period

    Based on the contract hours number across time.
    If end_date is in the future, result is a projection.

    :param start_date: inclusive (the worked hours for the start date are counted)
    :param end_date: exclusive (the worked hours for the end date are not counted, you
       may want to add +1 day to this arg)
    """
    total_hours = 0
    current_hours_per_day = 0
    period_start_date = start_date
    for effect_date, new_hours_per_day in iter_hours_change(ud):
        if effect_date < end_date:
            if effect_date >= start_date:
                nb_days = (effect_date - period_start_date).days
                hours_to_add = current_hours_per_day * nb_days
                assert hours_to_add >= 0
                total_hours += hours_to_add
            # Start a new period
            current_hours_per_day = new_hours_per_day
            period_start_date = max(effect_date, start_date)

    if period_start_date < end_date:
        nb_days = (end_date - period_start_date).days
        hours_to_add = current_hours_per_day * nb_days
        assert hours_to_add >= 0
        total_hours += hours_to_add

    return int(total_hours)
