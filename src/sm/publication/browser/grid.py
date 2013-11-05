from Products.Five import BrowserView

from sm.publication.interfaces import IOrderFormStorage

from zope.component import getUtility, getMultiAdapter


class GridView(BrowserView):

    @property
    def results(self):
        plone_view = getMultiAdapter(
            (self.context, self.request),
            name="plone"
        )
        utility = getUtility(IOrderFormStorage)

        data = utility.getData()
        for item in data:
            if item.get('timestamp', None):
                item['formatted_timestamp'] = plone_view.toLocalizedTime(
                    item['timestamp'], long_format=True
                )
        return data
