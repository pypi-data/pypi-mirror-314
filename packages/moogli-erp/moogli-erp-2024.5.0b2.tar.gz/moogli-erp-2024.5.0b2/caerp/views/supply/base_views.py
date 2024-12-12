import datetime

import colander

from caerp.models.third_party.supplier import Supplier


class SupplierDocListTools:
    """
    Filtering tools common to SupplierInvoice and SupplierOrder

    Inheriting child must define those attributes:

    - model_class: target model class (that model_class must define a
      filter_by_year() method)
    """

    sort_columns = {
        "company_id": "company_id",
        "date": "date",
        "name": "name",
        "supplier": "supplier_id",
        "created_at": "created_at",
    }

    default_sort = "created_at"
    default_direction = "desc"

    def filter_name(self, records, appstruct):
        search = appstruct.get("search")
        if search:
            records = records.join("supplier")
            return records.filter(
                self.model_class.name.like("%{}%".format(search))
                | Supplier.company_name.like("%{}%".format(search))
            )
        else:
            return records

    def filter_supplier(self, records, appstruct):
        supplier_id = appstruct.get("supplier_id")
        if supplier_id:
            return records.filter(
                self.model_class.supplier_id == supplier_id,
            )
        else:
            return records

    def filter_company(self, query, appstruct):
        company_id = appstruct.get("company_id")
        if company_id:
            query = query.filter_by(company_id=company_id)
        return query

    def filter_status(self, query, appstruct):
        status = appstruct.get("status")
        if status and (status != "all"):
            query = query.filter(
                self.model_class.status == status,
            )
        return query

    def filter_year(self, query, appstruct):
        year = appstruct.get("year")
        if year and year not in (-1, colander.null):
            query = self.model_class.filter_by_year(query, year)
            self.year = year
        else:
            self.year = datetime.date.today().year
        return query

    def filter_doctype(self, query, appstruct):
        type_ = appstruct.get("doctype")
        if type_ in (
            "supplier_invoice",
            "internalsupplier_invoice",
            "supplier_order",
            "internalsupplier_order",
        ):
            query = query.filter(self.model_class.type_ == type_)
        return query
