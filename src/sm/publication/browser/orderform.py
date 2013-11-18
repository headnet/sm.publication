# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


from plone.app.layout.viewlets.common import ViewletBase
from plone.directives import form
from plone.z3cform.interfaces import IWrappedForm
from plone.registry.interfaces import IRegistry

from sm.publication.interfaces import IOrderFormStorage
from sm.publication.interfaces import IPublicationSettings

from z3c.form import button, validator

from zope.component import getUtility
from zope.interface import alsoProvides

from sm.publication.interfaces import IOrderForm
from sm.publication.utils import _sendMail, _validateEmail


class OrderFormSuccessView(BrowserView):

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
        email_from_name = portal_object.getProperty('email_from_name')
        email_from_addr = portal_object.getProperty('email_from_address')

        settings_registry = self.settings_registry
        email_to_name = settings_registry.email_receiver_name
        email_to_addr = settings_registry.email_receiver_email
        email_subject = settings_registry.email_subject
        email_text = settings_registry.email_text

        title = self.context.Title()
        url = self.context.absolute_url()

        mail_template = ViewPageTemplateFile('mail_template.pt')
        mail_text = mail_template(
            self,
            email_from_name=email_from_name,
            email_from_addr=email_from_addr,
            email_to_name=email_to_name,
            email_to_addr=email_to_addr,
            email_subject=email_subject,
            email_text=email_text,
            title=title,
            url=url,
            data=data
        )

        _sendMail(self, mail_text)

    def saveData(self, data):
        utility = getUtility(IOrderFormStorage)
        utility.addOrder(
            data,
            title=self.context.Title(),
            uid=self.context.UID()
        )

    @button.buttonAndHandler(u'Bestil')
    def handleApply(self, action):
        data, errors = self.extractData()

        if errors:
            self.status = self.formErrorsMessage
            return

        self.saveData(data)
        self.sendMail(data)

        return self.context.REQUEST.RESPONSE.redirect(
            self.context.absolute_url() + '/@@orderform-success'
        )


class EmailValidator(validator.SimpleFieldValidator):
    def validate(self, value):
        return _validateEmail(value)


validator.WidgetValidatorDiscriminators(
    EmailValidator,
    field=IOrderForm['email']
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
