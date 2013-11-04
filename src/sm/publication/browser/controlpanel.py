from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.app.registry.browser import controlpanel
from plone.z3cform import layout

from z3c.form import field

from zope import schema
from zope.interface import Interface

from sm.publication.i18n import MessageFactory as _


class IPublicationSettings(Interface):
    thank_you_heading = schema.TextLine(
        title=_(u"Thank-you page heading"),
        required=True,
        default=u'',
    )

    thank_you_page = schema.Text(
        title=_(u"Thank-you page"),
        description=_(u"The text here will be used on the "
                      u"thank-you page for publication ordering"),
        required=False,
        default=u'',
    )


class ControlPanelEditForm(controlpanel.RegistryEditForm):
    label = _(u"Configure publication module")
    description = _(
        u"This form lets you configure the settings for the publication module."
    )

    schema = IPublicationSettings
    fields = field.Fields(IPublicationSettings)
    fields['thank_you_page'].widgetFactory = WysiwygFieldWidget


ControlPanel = layout.wrap_form(
    ControlPanelEditForm,
    controlpanel.ControlPanelFormWrapper
)
