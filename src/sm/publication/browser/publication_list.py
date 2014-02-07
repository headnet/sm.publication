# -*- coding: utf-8 -*-

from copy import deepcopy
from Acquisition import aq_inner
from DateTime import DateTime

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

from plone.memoize.view import memoize
from plone.app.querystring.querybuilder import QueryBuilder

START_YEAR = 1990


class PublicationListSearchView(BrowserView):
    has_search = True

    def subject_to_text(self, subjects):
        results = []

        if not subjects:
            return []

        for subject in subjects:
            translation = self.context.translate(
                subject,
                domain='collective.taxonomy.publication_subjects'
            )
            results.append(translation)

        return results

    @property
    @memoize
    def all_years(self):
        current_year = DateTime().year()

        year_list = range(START_YEAR, current_year + 1)
        year_list.reverse()

        return year_list

    @property
    @memoize
    def all_subjects(self):
        subjects = []

        catalog_tool = getToolByName(self.context, 'portal_catalog')
        index = catalog_tool._catalog.indexes['taxonomy_publication_subjects']

        for key in index.uniqueValues():
            subjects.append(key)

        result = zip(subjects, self.subject_to_text(subjects))
        result.sort(key=lambda (id, value,): value)

        return result

    def user_has_searched(self):
        return self.request.get('searchable', None) or \
            self.request.get('subject', None) or \
            self.request.get('year', None)

    @memoize
    def results(self, batch=True, b_start=0, b_size=None):
        sort_on = 'effective'
        sort_order = 'reverse'
        context = aq_inner(self.context)
        query = context.getQuery()

        searchable = self.request.get("searchable", "")
        if searchable:
            query = deepcopy(query)
            row = {}
            row['i'] = "SearchableText"
            row['o'] = "plone.app.querystring.operation.string.contains"
            row['v'] = searchable
            query.append(row)

        subject = self.request.get("subject", "")
        if subject:
            query = deepcopy(query)
            row = {}
            row['i'] = "taxonomy_publication_subjects"
            row['o'] = "plone.app.querystring.operation.string.is"
            row['v'] = subject
            query.append(row)

        year = self.request.get("year", "")
        if year:
            query = deepcopy(query)
            row = {}
            row['i'] = "effective"
            row['o'] = "plone.app.querystring.operation.date.between"
            row['v'] = [DateTime(int(year), 01, 01, 0, 0, 0),
                        DateTime(int(year), 12, 31, 23, 59, 59)]
            query.append(row)

        querybuilder = QueryBuilder(context, self.request)

        size = b_size or context.item_count or self.default_bsize
        results = querybuilder(
            query=query, batch=batch, b_start=b_start,
            b_size=size, sort_on=sort_on, sort_order=sort_order,
            limit=context.limit
        )
        return results


class PublicationListView(PublicationListSearchView):
    has_search = False
