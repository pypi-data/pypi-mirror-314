import deform
import colander

from caerp.forms.lists import BaseListsSchema
from caerp.forms.user import (
    antenne_filter_node_factory,
    follower_filter_node_factory,
)
from caerp.models.company import CompanyActivity


def get_list_schema():
    schema = BaseListsSchema().clone()
    del schema["search"]
    del schema["page"]
    del schema["items_per_page"]

    schema.add(
        follower_filter_node_factory(
            name="follower_id",
            title="Accompagnateur",
        )
    )
    schema.add(
        antenne_filter_node_factory(
            name="antenne_id",
            title="Antenne",
        )
    )
    schema.add(
        colander.SchemaNode(
            colander.Boolean(),
            name="active",
            label="Masquer les enseignes désactivées",
            arialabel="Activer pour afficher seulement les enseignes actives",
            default=True,
            missing=colander.drop,
        )
    )
    schema.add(
        colander.SchemaNode(
            colander.Boolean(),
            name="internal",
            label="Masquer les enseignes internes",
            arialabel="Activer pour afficher seulement les enseignes non-internes",
            default=True,
            missing=colander.drop,
        )
    )

    return schema
