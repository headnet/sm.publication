import csv

from StringIO import StringIO

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

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


class CsvGridView(GridView):

    def __call__(self):
        response = self.context.REQUEST.RESPONSE

        response.setHeader('Content-Type',
                           'text/csv')
        response.setHeader('Content-disposition',
                           'attachment;filename=export.csv')

        fh = StringIO()

        csv_writer = csv.writer(fh)

        for item in self.results:
            csv_writer.writerow([
                item.get('formatted_timestamp', ''),
                item.get('title', ''),
                item.get('number_of_items', ''),
                item.get('organization', ''),
                item.get('name', ''),
                item.get('street', ''),
                item.get('zipcode', ''),
                item.get('city', ''),
                item.get('email', '')
            ])

        return fh.getvalue()


class HtmlGridView(GridView):
    """ """

    def __call__(self):
        page_template = ViewPageTemplateFile('grid.pt')
        return page_template(self)
