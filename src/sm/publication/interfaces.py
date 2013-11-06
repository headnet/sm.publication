# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope import schema

from sm.publication.i18n import MessageFactory as _
from sm.publication.utils import number_vocabulary


class IOrderFormStorage(Interface):
    """ Marker interface for OrderFormStorage """


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

    country = schema.TextLine(
        title=u'Land',
        required=False,
        default=u'Danmark',
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

    email_receiver_email = schema.TextLine(
        title=_(u"Notification email: Receiver email"),
        description=_(u"Please fill in the receiver email address here"),
        required=False,
        default=u'',
    )

    email_receiver_name = schema.TextLine(
        title=_(u"Notification email: Receiver name"),
        description=_(u"Please fill in the name of the receiver here"),
        required=False,
        default=u'',
    )

    email_subject = schema.TextLine(
        title=_(u"Notification email: Subject"),
        description=_(u"Please fill in the subject of the notification mail"),
        required=False,
        default=u"",
    )

    email_text = schema.Text(
        title=_(u"Notification email: Text"),
        description=_(u"Please fill in the introductionary text of "
                      u"the notification mail"),
        required=False,
        default=u"",
    )
