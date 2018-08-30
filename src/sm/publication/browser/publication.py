from Products.Five.browser import BrowserView


class PublicationView(BrowserView):

    @property
    def relative_download_link(self):
        relative_link = '/'.join(self.context.getPhysicalPath()[2:])
        relative_link += '/@@download/publication'
        return '/' + relative_link

    @property
    def analytics_script(self):
        return """
            _gaq.push(['_trackEvent', 'Downloads', 'PDF',
            '%s'])
        """ % (self.relative_download_link, )

    @property
    def download_link(self):
        download_link = self.context.absolute_url() + '/@@download/publication'
        return download_link
