from caerp.consts.permissions import PERMISSIONS
from caerp.views.estimations.rest_api import EstimationRestView
from ..mixins import SAPTaskRestViewMixin


class SAPEstimationRestView(SAPTaskRestViewMixin, EstimationRestView):
    def _more_form_sections(self, sections):
        sections = EstimationRestView._more_form_sections(self, sections)
        sections["composition"]["classic"]["lines"]["date"] = {"edit": True}
        # Pas de configuration de la présentation (affichage ttc ou affichage du détail en mode SAP)
        sections["display_options"] = {}
        return sections


def add_views(config):
    config.add_view(
        SAPEstimationRestView,
        attr="form_config",
        route_name="/api/v1/estimations/{id}",
        renderer="json",
        request_param="form_config",
        permission=PERMISSIONS["company.view"],
    )


def includeme(config):
    add_views(config)
