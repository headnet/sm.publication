# -*- coding: utf-8 -*-

from copy import deepcopy
from Acquisition import aq_inner

from Products.Five.browser import BrowserView

from plone.memoize.view import memoize
from plone.app.querystring.querybuilder import QueryBuilder


class PublicationListView(BrowserView):
    """
    """

    @memoize
    def results(self, batch=True, b_start=0, b_size=None):
        """
        """
        sort_on = 'portal_type'
        context = aq_inner(self.context)
        query = context.getQuery()
        searchable = self.request.get("SearchableText", "")
        if searchable:
            query = deepcopy(query)
            row = {}
            row['i'] = "SearchableText"
            row['o'] = "plone.app.querystring.operation.string.contains"
            row['v'] = searchable
            query.append(row)

        # sorry!
        querybuilder = QueryBuilder(context, self.request)
        sort_order = 'reverse' if context.sort_reversed else 'ascending'

        size = b_size or context.item_count or self.default_bsize
        results = querybuilder(
            query=query, batch=batch, b_start=b_start,
            b_size=size, sort_on=sort_on, sort_order=sort_order,
            limit=context.limit
        )
        return results
