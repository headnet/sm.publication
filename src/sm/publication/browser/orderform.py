# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.layout.viewlets.common import ViewletBase
from plone.directives import form
from plone.z3cform.interfaces import IWrappedForm

from z3c.form import button

from zope import schema
from zope.interface import Interface
from zope.interface import alsoProvides

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


def _createNumberVocabulary():
    return [SimpleTerm(number) for number in range(1, 6)]


number_vocabulary = SimpleVocabulary(list(_createNumberVocabulary()))


class IOrderForm(Interface):
    name = schema.TextLine(
        title=u'Navn',
        required=True
    )

    organization = schema.TextLine(
        title=u'Organisation',
        required=False
    )

    street = schema.TextLine(
        title=u'Vej',
        required=True
    )

    zipcode = schema.Int(
        title=u'Postnummer',
        required=True
    )

    city = schema.TextLine(
        title=u'By',
        required=True
    )

    number_of_items = schema.Choice(
        title=u'Hvor mange eksemplarer ønsker du?',
        vocabulary=number_vocabulary,
        required=True
    )

    email = schema.TextLine(
        title=u"Email",
        required=True
    )


class OrderForm(form.SchemaForm):
    schema = IOrderForm
    ignoreContext = True

    @button.buttonAndHandler(u'Bestil')
    def handleApply(self, action):
        data, errors = self.extractData()

        if errors:
            self.status = self.formErrorsMessage
            return

        return self.context.REQUEST.RESPONSE.redirect(
            self.context.absolute_url() + '/@@thank-you'
        )


class OrderFormViewlet(ViewletBase):
    template = ViewPageTemplateFile('orderform_viewlet.pt')

    def update(self):
        self.form = OrderForm(self.context, self.context.REQUEST)
        self.form.update()
        alsoProvides(self.form, IWrappedForm)

    def index(self):
        context = self.context
        if context.free_printed_edition:
            return self.template()
        return ''

