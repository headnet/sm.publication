from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.app.registry.browser import controlpanel
from plone.z3cform import layout

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from z3c.form import field

from zope import schema
from zope.interface import Interface

from sm.publication.i18n import MessageFactory as _
from sm.publication.interfaces import IPublicationSettings


class ControlPanelEditForm(controlpanel.RegistryEditForm):
    label = _(u"Configure publication module")
    description = _(
        u"This form lets you configure the settings for "
        u"the publication module."
    )

    schema = IPublicationSettings
    fields = field.Fields(IPublicationSettings)
    fields['thank_you_page'].widgetFactory = WysiwygFieldWidget


ControlPanel = layout.wrap_form(
    ControlPanelEditForm,
    controlpanel.ControlPanelFormWrapper,
    index=ViewPageTemplateFile('controlpanel.pt')
)
