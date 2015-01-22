# -*- coding: utf-8 -*-

from copy import deepcopy

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import Interface, implements
from zope.component import adapts
from plone.z3cform.fieldsets.extensible import FormExtender
from plone.z3cform.fieldsets.interfaces import IFormExtender
from plone.dexterity.content import Item

from z3c.form.field import Fields
from z3c.form.interfaces import IEditForm, IAddForm


class IPublication(Interface):
    """ Publication """


class Publication(Item):
    implements(IPublication)


class EffectiveDateRequired(FormExtender):
    def __init__(self, context, request, form):
        self.context = context
        self.request = request
        self.form = form

    def update(self):
        categorization_group = None
        effective_group = None

        for group in self.form.groups:
            if 'IDublinCore.effective' in group.fields:
                effective_group = group
            if 'IDublinCore.subjects' in group.fields:
                categorization_group = group

        if not effective_group or not categorization_group:
            return

        # Moving effective to main fields and making it
        # required

        field = deepcopy(effective_group.fields['IDublinCore.effective'])
        field.field.required = True

        self.form.fields += Fields(field)
        effective_group.fields = effective_group.fields.omit(
            'IDublinCore.effective'
        )

        # Moving publication subjects to the main fields

        field = categorization_group.fields[
            'publication_subjects.taxonomy_publication_subjects'
        ]
        self.form.fields += Fields(field)

        categorization_group.fields = categorization_group.fields.omit(
            'publication_subjects.taxonomy_publication_subjects'
        )

        # Omitting subject and related items ..

        categorization_group.fields = categorization_group.fields.omit(
            'IDublinCore.subjects'
        )
        categorization_group.fields = categorization_group.fields.omit(
            'IRelatedItems.relatedItems'
        )


class EffectiveDateRequiredAddForm(EffectiveDateRequired):
    implements(IFormExtender)
    adapts(Interface, IDefaultBrowserLayer, IAddForm)

    def update(self):
        if self.form.portal_type == 'Publication':
            super(EffectiveDateRequiredAddForm, self).update()


class EffectiveDateRequiredEditForm(EffectiveDateRequired):
    implements(IFormExtender)
    adapts(IPublication, IDefaultBrowserLayer, IEditForm)
