# encoding: utf-8
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from sm.publication.i18n import MessageFactory as _

from plone.app.portlets.browser import z3cformhelper
from plone.app.portlets.portlets import base
from plone.memoize import instance
from plone.portlets.interfaces import IPortletDataProvider

from z3c.form import field

from zope import schema
from zope.interface import implements

from sm.publication.interfaces import IPublicationFolder


class INavigationPortlet(IPortletDataProvider):

    header = schema.TextLine(
        title=_(u"Portlet header"),
        description=_(u"Header of the rendered portlet"),
        required=False)


class Assignment(base.Assignment):
    implements(INavigationPortlet)

    def __init__(self, **kwargs):
        for (key, value) in kwargs.items():
            setattr(self, key, value)

    @property
    def title(self):
        return self.header


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('navigation_portlet.pt')

    @property
    def header(self):
        return self.data.header

    @property
    def header_link(self):
        return self.publication_folder.absolute_url()

    @property
    @instance.memoize
    def publication_folder(self):
        """ Finds the folder that provides the IPublicationFolder
            marker interface by searching backwards in the acqusition
            chain """

        obj = self

        while obj:
            if IPublicationFolder.providedBy(obj):
                return obj

            try:
                obj = obj.__parent__
            except AttributeError:
                return None

    @property
    def items(self):
        """ Searches the catalog to find all collections stored in the
            publication folder (that provides IPublicationFolder)
            """

        results = []
        current_class = 'navTreeCurrentNode navTreeCurrentItem'
        catalog_tool = self.context.portal_catalog
        publication_folder = self.publication_folder
        for brain in catalog_tool.searchResults(
            portal_type='Collection',
            review_status='published',
            path='/'.join(publication_folder.getPhysicalPath())
        ):
            if brain.exclude_from_nav:
                continue

            current = brain.getURL() == self.context.absolute_url()

            results.append({
                'id': brain.id,
                'url': brain.getURL(),
                'title': brain.Title,
                'description': brain.Description,
                'current': current and current_class or ''
            })

        return results


class AddForm(z3cformhelper.AddForm):
    fields = field.Fields(INavigationPortlet)
    label = _(u"Add Navigation Portlet (Publications)")
    description = _(u"ONLY to be used in publication section")

    def create(self, data):
        return Assignment(**data)


class EditForm(z3cformhelper.EditForm):
    fields = field.Fields(INavigationPortlet)
    label = _(u"Edit Navigation portlet (Publication)")
    description = _(u"ONLY to be used in publication section")
