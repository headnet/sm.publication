from Products.Five.browser import BrowserView


class PublicationView(BrowserView):

    @property
    def image_tag(self):
        scale = self.context.restrictedTraverse('@@images')
        return scale.scale('image').tag(css_class='publication_image')

    @property
    def download_link(self):
        return self.context.absolute_url() + '/@@download/publication'


