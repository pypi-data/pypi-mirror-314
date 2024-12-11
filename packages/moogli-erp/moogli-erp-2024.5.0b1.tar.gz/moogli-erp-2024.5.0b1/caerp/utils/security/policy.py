from typing import List, Optional

from pyramid.authorization import Authenticated, Everyone, ACLHelper
from pyramid.authentication import SessionAuthenticationHelper
from caerp.services.company import find_company_id_from_model, get_company_by_id

from caerp.models.user import User
from .identity import get_identity


def get_user_principals(request, context, user: User) -> List[str]:
    """
    Compute the principals for the current authenticated user
    """
    principals = [Everyone]
    principals.append(Authenticated)
    principals.append(user.login.login)
    principals.append(f"user:{user.id}")
    principals.append(f"login:{user.login.id}")
    for group in user.login._groups:
        principals.append(f"group:{group.name}")
        for access_right in group.access_rights:
            principals.append(f"access_right:{access_right.name}")
    for company in user.companies:
        if company.active:
            principals.append(f"company:{company.id}")
    return principals


def global_permits(request, context, identity: Optional[User], permission: str) -> bool:
    """
    Check if the user has globally access to the given permission
    The permission should be in the form "global.<permission>"
    """
    if identity:
        if permission == "global.authenticated":
            return True
        for group in identity.login._groups:
            for access_right in group.access_rights:
                if permission in access_right.global_permissions:
                    return True
    return False


def company_permits(request, context, identity: Optional[User]) -> bool:
    """
    Check if the user has the permission needed on the context regarding his companies

    permission should be in the form "company.<permission>"
    """
    if identity:
        # Si on a les droits pour voir toutes les enseignes on renvoie True
        if global_permits(request, context, identity, "global.view_company"):
            return True
        company_id = find_company_id_from_model(request, context)
        if company_id is None:
            raise Exception(
                f"Check permission 'company.view' : Can't retrieve the company_id "
                f"for the current context.{context} with id {context.id}"
            )
        for company in identity.companies:
            if company.id == company_id:
                return True
    return False


class SessionSecurityPolicy:
    def __init__(self):
        self.helper = SessionAuthenticationHelper()

    def identity(self, request):
        """Return app-specific user object."""
        userid = self.helper.authenticated_userid(request)
        if userid is None:
            return None

        if getattr(request, "_cached_identity", None) is None:
            request._cached_identity = get_identity(request, userid)
        return request._cached_identity

    def authenticated_userid(self, request):
        """Return a string ID for the user."""

        identity = self.identity(request)

        if identity is None:
            return None

        return str(identity.id)

    def permits(self, request, context, permission):
        """Allow access to everything if signed in."""
        identity = self.identity(request)

        if permission.startswith("global."):
            return global_permits(request, context, identity, permission)

        if permission == "company.view":
            return company_permits(request, context, identity)

        # La permission est relative à la company du contexte
        if permission.startswith("company."):
            # On retrouve la company,
            company_id = find_company_id_from_model(request, context)
            context = get_company_by_id(request, company_id)
            # on renomme la permission qui est désormais relative au contexte
            permission = permission.replace("company.", "context.")

        if identity is not None:
            principals = get_user_principals(request, context, identity)
        else:
            principals = [Everyone]

        return ACLHelper().permits(context, principals, permission)

    def remember(self, request, userid, **kw):
        return self.helper.remember(request, userid, **kw)

    def forget(self, request, **kw):
        # Clean le cache
        if hasattr(request, "_cached_identity"):
            del request._cached_identity
        return self.helper.forget(request, **kw)
