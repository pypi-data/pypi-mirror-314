import logging
import colander

from caerp.consts.permissions import PERMISSIONS
from sqlalchemy import desc

from caerp_base.models.base import DBSESSION
from caerp.export.utils import write_file_to_request
from caerp.export.excel import XlsExporter
from caerp.export.ods import OdsExporter
from caerp.forms.management.treasuries import get_list_schema
from caerp.models.accounting.treasury_measures import TreasuryMeasureGrid
from caerp.models.company import Company
from caerp.views import BaseListView
from caerp.views.accounting.treasury_measures import TreasuryGridCompute


logger = logging.getLogger(__name__)


class TreasuriesManagementView(BaseListView):
    """
    Tableau de suivi des trésoreries
    """

    title = "Suivi des trésoreries de la CAE"
    schema = get_list_schema()
    use_paginate = False

    def get_last_treasury_date(self):
        last_grid = (
            DBSESSION()
            .query(TreasuryMeasureGrid)
            .order_by(desc(TreasuryMeasureGrid.date))
            .first()
        )
        return last_grid.date if last_grid else None

    def query(self):
        return (
            TreasuryMeasureGrid.query()
            .join(Company)
            .filter(TreasuryMeasureGrid.date == self.get_last_treasury_date())
            .order_by(Company.name)
        )

    def filter_follower_id(self, query, appstruct):
        follower_id = appstruct.get("follower_id")
        if follower_id not in (None, colander.null):
            if follower_id == -2:
                # -2 means no follower configured
                query = query.filter(Company.follower_id == None)
            else:
                query = query.filter(Company.follower_id == follower_id)
        return query

    def filter_antenne_id(self, query, appstruct):
        antenne_id = appstruct.get("antenne_id")
        if antenne_id not in (None, colander.null):
            if antenne_id == -2:
                # -2 means no antenne configured
                query = query.filter(Company.antenne_id == None)
            else:
                query = query.filter(Company.antenne_id == antenne_id)
        return query

    def filter_active(self, query, appstruct):
        active_only = appstruct.get("active")
        if active_only not in (None, colander.null, False):
            query = query.filter(Company.active == True)
        return query

    def filter_internal(self, query, appstruct):
        no_internal = appstruct.get("internal")
        if no_internal not in (None, colander.null, False):
            query = query.filter(Company.internal == False)
        return query

    def get_treasury_headers(self, treasury_grids):
        treasury_headers = []
        if treasury_grids.count() > 0:
            computed_grid = TreasuryGridCompute(treasury_grids[0])
            for row in computed_grid.rows:
                treasury_headers.append(row[0].label)
        return treasury_headers

    def compute_treasury_grid_values(self, grid):
        values = []
        for row in TreasuryGridCompute(grid).rows:
            values.append(row[1])
        return values

    def _build_return_value(self, schema, appstruct, query):
        last_treasury_date = self.get_last_treasury_date()
        treasury_grids = query

        treasury_headers = self.get_treasury_headers(treasury_grids)

        treasury_data = []
        for grid in treasury_grids:
            treasury_data.append(
                (grid.company, self.compute_treasury_grid_values(grid))
            )

        if schema is not None:
            if self.error is not None:
                form_object = self.error
                form_render = self.error.render()
            else:
                form = self.get_form(schema)
                if appstruct and "__formid__" in self.request.GET:
                    form.set_appstruct(appstruct)
                form_object = form
                form_render = form.render()

        return dict(
            title=self.title,
            form_object=form_object,
            form=form_render,
            nb_results=treasury_grids.count(),
            treasuries_date=last_treasury_date,
            treasury_headers=treasury_headers,
            treasury_data=treasury_data,
            export_xls_url=self.request.route_path(
                "management_treasuries_export",
                extension="xls",
                _query=self.request.GET,
            ),
            export_ods_url=self.request.route_path(
                "management_treasuries_export",
                extension="ods",
                _query=self.request.GET,
            ),
        )


class TreasuriesManagementXlsView(TreasuriesManagementView):
    """
    Export du tableau de suivi des trésoreries au format XLS
    """

    _factory = XlsExporter

    @property
    def filename(self):
        return "suivi_tresoreries_{}.{}".format(
            self.get_last_treasury_date(),
            self.request.matchdict["extension"],
        )

    def _build_return_value(self, schema, appstruct, query):
        writer = self._factory()
        writer._datas = []
        # Récupération des données
        treasury_grids = query
        treasury_headers = self.get_treasury_headers(treasury_grids)
        treasury_data = []
        for grid in treasury_grids:
            treasury_data.append(
                (grid.company, self.compute_treasury_grid_values(grid))
            )
        # En-têtes
        headers = treasury_headers
        headers.insert(0, "Enseigne")
        writer.add_headers(headers)
        # Données des enseignes
        for company, treasury_values in treasury_data:
            row_data = [
                company.name,
            ]
            for value in treasury_values:
                row_data.append(value)
            writer.add_row(row_data)
        # Génération du fichier d'export
        write_file_to_request(self.request, self.filename, writer.render())
        return self.request.response


class TreasuriesManagementOdsView(TreasuriesManagementXlsView):
    """
    Export du tableau de suivi des trésoreries au format ODS
    """

    _factory = OdsExporter


def includeme(config):
    config.add_route(
        "management_treasuries",
        "management/treasuries",
    )
    config.add_route(
        "management_treasuries_export", "management/treasuries.{extension}"
    )
    config.add_view(
        TreasuriesManagementView,
        route_name="management_treasuries",
        renderer="management/treasuries.mako",
        permission=PERMISSIONS["global.view_company"],
    )
    config.add_view(
        TreasuriesManagementXlsView,
        route_name="management_treasuries_export",
        match_param="extension=xls",
        permission=PERMISSIONS["global.view_company"],
    )
    config.add_view(
        TreasuriesManagementOdsView,
        route_name="management_treasuries_export",
        match_param="extension=ods",
        permission=PERMISSIONS["global.view_company"],
    )
    config.add_admin_menu(
        parent="management",
        order=0,
        label="Trésoreries",
        href="/management/treasuries",
    )
