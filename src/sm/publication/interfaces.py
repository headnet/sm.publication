# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope import schema

from sm.publication.i18n import MessageFactory as _
from sm.publication.utils import number_vocabulary


class IPublicationFolder(Interface):
    """ Marker interface for publication folder """


class IOrderFormStorage(Interface):
    """ Interface for OrderFormStorage utility """

    def __init__(self):
        """ Constructor """

    def getData(self, min_timestamp, max_timestamp):
        """ Returns data stored in the utility, to be
            called from a view """

    def addToIndex(self, index, key, value):
        """ Adds key to a given index, the utlity provides
            basic catalog """

    def addOrder(self, order, title, uid):
        """ Adds a order to be stored in the utility. """


class IOrderForm(Interface):
    """ Order form, rendered from OrderFormViewlet """

    name = schema.TextLine(
        title=_(u'Name'),
        required=True
    )

    organization = schema.TextLine(
        title=_(u'Organization'),
        required=False
    )

    street = schema.TextLine(
        title=_(u'Street'),
        required=True
    )

    zipcode = schema.Int(
        title=_(u'Zipcode'),
        required=True
    )

    city = schema.TextLine(
        title=_(u'City'),
        required=True
    )

    country = schema.TextLine(
        title=_(u'Country'),
        required=False,
        default=u'Danmark',
    )

    number_of_items = schema.Choice(
        title=_(u'How many copies do you wish?'),
        vocabulary=number_vocabulary,
        required=True
    )

    email = schema.TextLine(
        title=_(u"Email"),
        required=True
    )


class IPublicationSettings(Interface):
    """ Publication module settings, to be edited using the
        controlpanel """

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
