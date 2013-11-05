# -*- coding: utf-8 -*-

from BTrees.IOBTree import IOBTree
from BTrees.OOBTree import OOBTree

from DateTime import DateTime

from Persistence import Persistent

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from plone.app.layout.viewlets.common import ViewletBase
from plone.directives import form
from plone.z3cform.interfaces import IWrappedForm
from plone.registry.interfaces import IRegistry

from sm.publication.interfaces import IOrderFormStorage
from sm.publication.browser.controlpanel import IPublicationSettings

from z3c.form import button

from zope import schema
from zope.component import getUtility
from zope.interface import Interface, alsoProvides, implements
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


def _sendMail(context, mail_text):
    host = getToolByName(context, 'MailHost')
    return host.send(mail_text, immediate=True)


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


class OrderFormStorage(Persistent):
    implements(IOrderFormStorage)

    def __init__(self):
        self.storage = IOBTree()
        self.indeces = OOBTree()

    def getData(self, min_timestamp=None, max_timestamp=None):
        if min_timestamp and max_timestamp:
            indeces = self.indeces['timestamp'].keys(
                min=min_timestamp,
                max=max_timestamp
            )
        else:
            indeces = []

        result = []
        for i in indeces or self.storage.keys():
            data = self.storage[i]
            data.update({'id': i})

            result.append(data)

        return result

    def addToIndex(self, index, key, value):
        if index not in self.indeces:
            self.indeces[index] = OOBTree()

        self.indeces[index][key] = value

    def addOrder(self, order):
        if len(self.storage) == 0:
            new_key = 0
        else:
            new_key = self.storage.maxKey()
            new_key += 1

        new_dict = {}

        for key in order.keys():
            new_dict[key] = order[key]

        new_dict['timestamp'] = DateTime()

        self.storage[new_key] = order

        self.addToIndex('timestamp', new_key, new_dict['timestamp'])


class ThankYouView(BrowserView):

    @property
    def registry(self):
        return getUtility(IRegistry).forInterface(IPublicationSettings)

    @property
    def heading(self):
        return self.registry.thank_you_heading

    @property
    def page(self):
        return self.registry.thank_you_page


class OrderForm(form.SchemaForm):
    schema = IOrderForm
    ignoreContext = True

    @property
    def settings_registry(self):
        return getUtility(IRegistry).forInterface(IPublicationSettings)

    @property
    def portal_object(self):
        portal_url = getToolByName(self, 'portal_url')
        portal = portal_url.getPortalObject()
        return portal

    def sendMail(self, data):
        portal_object = self.portal_object
        settings_registry = self.settings_registry
        title = self.context.Title()
        mail_template = ViewPageTemplateFile('mail_template.pt')
        mail_text = mail_template(
            self,
            email_from_name=portal_object.getProperty('email_from_name'),
            email_from_addr=portal_object.getProperty('email_from_address'),
            email_to_name=settings_registry.email_reciever_name,
            email_to_addr=settings_registry.email_reciever_email,
            email_subject=settings_registry.email_subject,
            email_text=settings_registry.email_text,
            title=title,
            data=data
        )
        _sendMail(self, mail_text)

    def saveData(self, data):
        utility = getUtility(IOrderFormStorage)
        utility.addOrder(data)

    @button.buttonAndHandler(u'Bestil')
    def handleApply(self, action):
        data, errors = self.extractData()

        if errors:
            self.status = self.formErrorsMessage
            return

        self.saveData(data)
        self.sendMail(data)

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
