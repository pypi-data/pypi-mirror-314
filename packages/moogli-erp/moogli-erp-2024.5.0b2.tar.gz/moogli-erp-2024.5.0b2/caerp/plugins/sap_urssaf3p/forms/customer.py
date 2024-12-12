from types import MethodType
import colander
from colanderalchemy import SQLAlchemySchemaNode
from caerp_base.consts import CIVILITE_OPTIONS
from caerp.consts.insee_countries import COUNTRIES
from caerp.consts.insee_departments import DEPARTMENTS
from caerp import forms
from caerp.forms.third_party.customer import get_individual_customer_schema
from caerp.plugins.sap_urssaf3p.models.customer import UrssafCustomerData
from caerp.utils.colanderalchemy import patched_objectify
import schwifty


def get_urssaf_data_schema() -> SQLAlchemySchemaNode:
    result = SQLAlchemySchemaNode(UrssafCustomerData)

    result.objectify = MethodType(patched_objectify, result)
    return result


def iban_validator(node, values):
    """
    validator for iban strings. Raise a colander.Invalid exception
    when the value is not a valid IBAN.
    """
    try:
        schwifty.IBAN(values, validate_bban=True)
    except schwifty.exceptions.SchwiftyException:
        raise colander.Invalid(node, "Veuillez saisir un IBAN valide")


def bic_validator(node, values):
    "Veuillez saisir un BIC valide"
    try:
        schwifty.BIC(values, allow_invalid=False)
    except schwifty.exceptions.SchwiftyException:
        raise colander.Invalid(node, "Veuillez saisir un BIC valide")


def get_urssaf_individual_customer_schema() -> SQLAlchemySchemaNode:
    """
    Build the customer form schema specific to Urssaf related data
    """
    schema = get_individual_customer_schema()
    schema.objectify = MethodType(patched_objectify, schema)
    schema["urssaf_data"] = get_urssaf_data_schema()

    for field in (
        "civilite",
        "firstname",
        "email",
        "mobile",
        "city",
        "city_code",
        "zip_code",
        "address",
    ):
        schema[field].missing = colander.required

    schema["civilite"].validator = colander.OneOf(
        [opt[0] for opt in CIVILITE_OPTIONS[1:]]
    )
    schema["mobile"].validator = colander.Regex(
        r"^(0|\+33)[6-7]([0-9]{2}){4}$",
        msg=(
            "Veuillez saisir un numéro de mobile valide sans espace "
            "(0610111213 ou  +33610111213)"
        ),
    )

    schema["firstname"].label = "Prénom(s)"
    schema[
        "firstname"
    ].description = "Prénom(s) d'usage du client séparés par des espaces"

    for field in (
        "street_type",
        "birthdate",
        "birthplace_city",
        "birthplace_country_code",
        "bank_account_bic",
        "bank_account_iban",
        "bank_account_owner",
    ):
        schema["urssaf_data"][field].missing = colander.required

    schema["urssaf_data"]["street_number_complement"].validator = colander.OneOf(
        ["", "B", "T", "Q", "C"]
    )
    schema["urssaf_data"]["birthplace_country_code"].widget = forms.get_select(
        [(country["code_insee"], country["name"]) for country in COUNTRIES]
    )
    schema["urssaf_data"]["birthplace_department_code"].widget = forms.get_select(
        [(dept["code_insee"], dept["name"]) for dept in DEPARTMENTS]
    )
    schema["urssaf_data"]["bank_account_bic"].validator = bic_validator
    schema["urssaf_data"]["bank_account_iban"].validator = iban_validator

    return schema
