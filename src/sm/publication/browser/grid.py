import csv
from time import time

from StringIO import StringIO

from Products.CMFPlone.PloneBatch import Batch
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.memoize import ram

from sm.publication.interfaces import IOrderFormStorage

from zope.component import getUtility, getMultiAdapter


def _results_cachekey(method, self):
    return time() // (60)


class GridView(BrowserView):

    @ram.cache(_results_cachekey)
    def results(self):
        sortabledata_fmt = 'sortabledata-%04d-%02d-%02d-%02d-%02d-%02d'

        portal_object = self.context.portal_url.getPortalObject()
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
                item['sort_class_name'] = sortabledata_fmt % (
                    item['timestamp'].year(),
                    item['timestamp'].month(),
                    item['timestamp'].day(),
                    item['timestamp'].hour(),
                    item['timestamp'].minute(),
                    item['timestamp'].second()
                )

            if item.get('uid', None):
                item['url'] = portal_object.absolute_url() +\
                    '/resolveuid/' + item['uid']

        # Newest first
        data.reverse()
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

        for item in self.results():
            csv_writer.writerow([
                item.get('formatted_timestamp', ''),
                item.get('title', ''),
                item.get('number_of_items', ''),
                item.get('organization', ''),
                item.get('name', ''),
                item.get('street', ''),
                item.get('zipcode', ''),
                item.get('city', ''),
                item.get('country', ''),
                item.get('email', '')
            ])

        return fh.getvalue()


class HtmlGridView(GridView):
    """ """

    @property
    def results(self):
        b_size = self.context.REQUEST.get('b_size', 10)
        b_start = self.context.REQUEST.get('b_start', 0)

        results = GridView.results(self)
        batched_results = Batch(results, int(b_size), int(b_start), orphan=0)

        return batched_results

    def __call__(self):
        page_template = ViewPageTemplateFile('grid.pt')
        return page_template(self)
