import colander

from caerp.consts.permissions import PERMISSIONS
from caerp.forms.user import contractor_choice_node_factory
from caerp.models.competence import CompetenceDeadline


def restrict_user_id(form, kw):
    """
    Restrict the user selection to the current user
    """
    if not kw["request"].has_permission(PERMISSIONS["admin_competence"]):
        current_user = kw["request"].identity
        form["contractor_id"].validator = colander.OneOf((current_user.id,))


@colander.deferred
def deferred_deadline_id_validator(node, kw):
    return colander.OneOf([c[0] for c in CompetenceDeadline.query("id").all()])


class _CompetenceGridQuerySchema(colander.Schema):
    contractor_id = contractor_choice_node_factory()
    deadline = colander.SchemaNode(
        colander.Integer(),
        validator=deferred_deadline_id_validator,
        missing=colander.drop,
    )


CompetenceGridQuerySchema = _CompetenceGridQuerySchema(after_bind=restrict_user_id)
