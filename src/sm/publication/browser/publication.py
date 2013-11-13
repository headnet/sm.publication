from Products.Five.browser import BrowserView


class PublicationView(BrowserView):
    @property
    def image_tag(self):
        scale = self.context.restrictedTraverse('@@images')
        return scale.scale('image', scale='publication_image').tag(
            css_class='publication_image'
        )

    @property
    def relative_download_link(self):
        relative_link = '/'.join(self.context.getPhysicalPath()[2:])
        relative_link += '/@@download/publication'
        return '/' + relative_link

    @property
    def download_link(self):
        download_link = self.context.absolute_url() + '/@@download/publication'
        return download_link
