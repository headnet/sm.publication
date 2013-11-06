# encoding: utf-8
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.person import MessageFactory as _

from plone.app.portlets.browser import z3cformhelper
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from z3c.form import field

from zope import schema
from zope.interface import implements


class IPublicationPortlet(IPortletDataProvider):

    header = schema.TextLine(
        title=_(u"Portlet header"),
        description=_(u"Header of the rendered portlet"),
        required=False)


class Assignment(base.Assignment):
    implements(IPublicationPortlet)

    def __init__(self, **kwargs):
        for (key, value) in kwargs.items():
            setattr(self, key, value)

    @property
    def title(self):
        return self.header


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('publication_portlet.pt')

    @property
    def publication_year(self):
        context = self.context.aq_base
        effective = context.effective()
        return effective.year()

    @property
    def publication_subjects(self):
        results = []
        context = self.context.aq_base

        if not hasattr(context, 'taxonomy_publication_subjects'):
            return []

        subjects = context.taxonomy_publication_subjects

        if not subjects:
            return []

        for subject in subjects:
            translation = self.context.translate(
                subject,
                domain='collective.taxonomy.publication_subjects'
            )
            results.append(translation)

        return results


class AddForm(z3cformhelper.AddForm):
    fields = field.Fields(IPublicationPortlet)
    label = _(u"Add Publication Portlet")

    def create(self, data):
        return Assignment(**data)


class EditForm(z3cformhelper.EditForm):
    fields = field.Fields(IPublicationPortlet)
    label = _(u"Edit Publication portlet")
