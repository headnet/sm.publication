from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import Invalid
from Products.CMFCore.utils import getToolByName
from Products.validation import validation

from sm.publication.i18n import MessageFactory as _


def _validateEmail(value):
    validator_function = validation.validatorFor('isEmail')

    if validator_function(str(value)) != 1:
        raise Invalid(_(u'The email entered is not valid'))

    return True


def _sendMail(context, mail_text):
    host = getToolByName(context, 'MailHost')
    return host.send(mail_text, immediate=True)


def _createNumberVocabulary():
    return [SimpleTerm(number) for number in range(1, 6)]

number_vocabulary = SimpleVocabulary(list(_createNumberVocabulary()))
