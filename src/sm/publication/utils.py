from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.CMFCore.utils import getToolByName


def _sendMail(context, mail_text):
    host = getToolByName(context, 'MailHost')
    return host.send(mail_text, immediate=True)


def _createNumberVocabulary():
    return [SimpleTerm(number) for number in range(1, 6)]

number_vocabulary = SimpleVocabulary(list(_createNumberVocabulary()))
