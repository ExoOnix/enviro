from django.db import models
from django.conf import settings
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.search import index
from wagtail.images.models import Image

class BlogIndexPage(Page):
    intro = models.CharField(max_length=250)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
    ]

    def get_context(self, request):
        # Get all live blog posts that are children of this index page, ordered by date descending
        blogpages = BlogPage.objects.live().descendant_of(self).order_by('-date')

        # Update context to include blog posts
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context
    

class BlogPage(Page):
    date = models.DateField("Post date")
    header_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='blog_posts'
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('author'),
        FieldPanel('date'),
        FieldPanel('header_image'),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
