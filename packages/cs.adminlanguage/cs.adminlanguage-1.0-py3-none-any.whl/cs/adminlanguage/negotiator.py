"""
    Override user interface language setting: taken from silvuple:
    https://github.com/miohtama/silvuple/blob/master/silvuple/negotiator.py
"""

from AccessControl import getSecurityManager
from cs.adminlanguage.interfaces import ICsAdminlanguageLayer
from cs.adminlanguage.settings import ISettings
from plone.registry.interfaces import IRegistry
from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.interfaces import IFolderish
from zope.component import ComponentLookupError
from zope.component import getUtility
from zope.i18n.translationdomain import TranslationDomain

import logging


logger = logging.getLogger("cs.languageadmin")


def find_context(request):
    """Find the context from the request
    http://stackoverflow.com/questions/10489544/getting-published-content-item-out-of-requestpublished-in-plone
    """
    published = request.get("PUBLISHED", None)
    context = getattr(published, "__parent__", None)
    if context is None:
        context = request.PARENTS[0]
    return context


def _get_editor_language(request):
    """Get editor language override if cs.adminlanguage is installed.

    This is the uncached version.
    """
    if not ICsAdminlanguageLayer.providedBy(request):
        # Add on is not active
        return None

    context = find_context(request)

    # Filter out CSS and other non-sense
    # IFolderish check includes site root
    if not (IContentish.providedBy(context) or IFolderish.providedBy(context)):
        # Early terminate
        return None

    # Check if we are the editor
    if not getSecurityManager().checkPermission(
        "cs.adminlanguage: ViewinAdminLanguage", context
    ):
        # Anon visitor, normal language ->
        return None

    try:

        # Will raise an exception if plone.app.registry is not quick installed
        registry = getUtility(IRegistry)

        # Will raise exception if your product add-on installer
        # has not been run
        settings = registry.forInterface(ISettings, prefix="admin_language")
    except (KeyError, ComponentLookupError):
        # Registry schema and actual values do not match
        # Quick installer has not been run or need to rerun
        # to update registry.xml values to database
        return None

    # Read language from settings
    return settings.adminLanguage


_cache_attribute_name = "_cached_admin_language"
_marker = object()


def get_editor_language(request):
    """Get editor language override if cs.adminlanguage is installed.

    This is the cached version.
    """
    language = getattr(request, _cache_attribute_name, _marker)
    if language is _marker:
        language = _get_editor_language(request)
        setattr(request, _cache_attribute_name, language)
    return language


def is_editor_language_domain(domain):
    """
    Filter to check which gettext domains will get forced to be in
    english always.
    """
    return (
        domain.startswith("plone")
        or domain.startswith("collective")
        or domain == "linguaplone"
    )


_unpatched_translate = None


def _patched_translate(
    self,
    msgid,
    mapping=None,
    context=None,
    target_language=None,
    default=None,
    msgid_plural=None,
    default_plural=None,
    number=None,
):
    """TranslationDomain.translate() patched for editor language support

    :param context: HTTPRequest object

    This patch overrides the target_language keyword argument if needed.

    These three were added in zope.i18n 4.5:
    msgid_plural=None, default_plural=None, number=None

    I tried to pass them on when needed by accepting **kwargs and passing those
    along, but this would still result in an error in Plone 6:

    TypeError: _patched_translate() takes from 2 to 6 positional arguments but
               9 were given

    So: accept them, but only pass them along when set.
    """

    # Override translation language?
    try:
        if is_editor_language_domain(self.domain):
            language = get_editor_language(context)
            if language:
                target_language = language
    except Exception as e:
        # Some defensive programming here
        logger.error("Admin language force patch failed")
        logger.exception(e)

    if (
        msgid_plural is not None or default_plural is not None or number is not None
    ):  # noqa: E501
        extra = dict(
            msgid_plural=msgid_plural,
            default_plural=default_plural,
            number=number,
        )
    else:
        extra = {}

    return _unpatched_translate(
        self, msgid, mapping, context, target_language, default, **extra
    )


_unpatched_translate = TranslationDomain.translate
TranslationDomain.translate = _patched_translate
