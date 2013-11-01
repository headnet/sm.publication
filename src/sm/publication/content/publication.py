# -*- coding: utf-8 -*-
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import Interface, implements
from zope.component import adapts
from plone.z3cform.fieldsets.extensible import FormExtender
from plone.z3cform.fieldsets.interfaces import IFormExtender
from plone.dexterity.content import Item

from z3c.form.interfaces import IEditForm


class IPublication(Interface):
    """ Publication """


class Publication(Item):
    implements(IPublication)


class EffectiveDateRequired(FormExtender):
    implements(IFormExtender)
    adapts(Interface, IDefaultBrowserLayer, IEditForm)

    def __init__(self, context, request, form):
        self.context = context
        self.request = request
        self.form = form

    def update(self):
        for group in self.form.groups:
            if 'IDublinCore.effective' in group.fields:
                field = group.fields['IDublinCore.effective'].field
                field.required = (self.context.portal_type == 'Publication')
