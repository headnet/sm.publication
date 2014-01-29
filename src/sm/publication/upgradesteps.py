from plone.dexterity.interfaces import IDexterityFTI

from zope.component import getUtility


def addPublicationCollectionViews(tool):
    fti = getUtility(IDexterityFTI, name='Collection')
    fti.view_methods = fti.view_methods + (
        'publication-collection-view',
        'publication-collection-search-view',
    )
