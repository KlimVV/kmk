from tabnanny import verbose
from django.db import models
from django.db.models import Count
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.models import Page, Orderable
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.admin.panels import FieldPanel, FieldRowPanel
from wagtail.admin.panels import InlinePanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from wagtail.search.models import Query
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag as TaggitTag
from taggit.models import TaggedItemBase

from datetime import date


class HomePage(Page):
    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)

        search_query = request.GET.get("query", None)
        tag = request.GET.get("tag", None)
        auth_id = request.GET.get("auth_id", None)
        year = request.GET.get("year", None)

        additional_get_str = ""

        if search_query:
            all_articles = ArticlePage.objects.search(search_query, partial_match=False)
            sub_title = "Статті по запиту < {0} >".format(search_query)
            additional_get_str = "&query={0}".format(search_query)
        elif tag:
            all_articles = ArticlePage.objects.filter(tags__name__exact=tag)
            sub_title = "Статті з тегом < {0} >".format(tag)
            additional_get_str = "&tag={0}".format(tag)
        elif auth_id:
            all_articles = ArticlePage.objects.filter(kmkauthors__auth__id=auth_id)
            sub_title = "Статті автора/соавтора < {0} >".format(
                Author.objects.get(pk=auth_id)
            )
            additional_get_str = "&auth_id={0}".format(auth_id)
        elif year:
            all_articles = ArticlePage.objects.filter(pubdate__year=year)
            sub_title = "Статті за < {0} > рік".format(year)
            additional_get_str = "&year={0}".format(year)
        else:
            # search_results = Page.objects.none()
            all_articles = ArticlePage.objects.live().public().order_by("-pubdate")
            sub_title = "Усі статті"

        paginator = Paginator(all_articles, 5)

        try:
            page = request.GET.get("page")
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context["additional_get_str"] = additional_get_str
        context["arts"] = articles
        context["page"] = page
        context["top_authors"] = (
            Author.objects.all()
            .annotate(num_art=Count("articles"))
            .order_by("-num_art")[:5]
        )
        context["top_tags"] = ArticlePage.tags.most_common()[:10]
        context["sub_title"] = sub_title
        context["year_list"] = range(2021, date.today().year + 1)
        return context


@register_snippet
class Author(index.Indexed, models.Model):
    name = models.CharField("Ім'я", max_length=25)
    fname = models.CharField("По батькові", max_length=25, null=True, blank=True)
    surname = models.CharField("Прізвище", max_length=25)
    academic_degree = models.CharField(max_length=100, null=True, blank=True)
    personal_photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="photo",
    )
    search_name = models.CharField("TransName", max_length=25, null=True, blank=True)

    panels = [
        FieldPanel("name"),
        # FieldPanel('search_name'),
        FieldPanel("fname"),
        FieldPanel("surname"),
        FieldPanel("academic_degree"),
        FieldPanel("personal_photo"),
    ]

    search_fields = [
        # index.SearchField('search_name'),
        index.AutocompleteField("surname"),
    ]

    def __str__(self):
        return self.surname + " " + self.name[0] + "." + self.fname[0] + "."

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True


class ArticlePage(Page):
    team = models.CharField("Усі автори", max_length=1024)
    pubtitle = models.CharField("Повна назва публікації", max_length=1024)
    annotation = RichTextField("Анотація", blank=True)
    article_body = StreamField(
        [
            ("linetext", blocks.CharBlock()),
            ("mtext", blocks.TextBlock()),
            ("richtext", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("table", TableBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    issue = models.CharField("Де опубліковано", max_length=512, null=True, blank=True)
    event = models.CharField(
        "Захід (конференція, видання тощо)", max_length=1024, null=True, blank=True
    )
    pubdate = models.DateField("Дата публікації", null=True, blank=True)
    link_to_hard_copy = models.URLField(blank=True)

    tags = ClusterTaggableManager(through="ArticlePageTag", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("team"),
        FieldPanel("pubtitle"),
        FieldPanel("annotation"),
        FieldPanel("article_body"),
        FieldPanel("issue"),
        FieldPanel("event"),
        FieldPanel("pubdate"),
        FieldRowPanel(
            [InlinePanel("kmkauthors")],
            heading="Наши Автори",
        ),
        FieldPanel("link_to_hard_copy"),
        FieldPanel("tags"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("pubtitle", partial_match=True),
        index.SearchField("team", partial_match=True),
        index.SearchField("annotation", partial_match=True),
        index.SearchField("issue", partial_match=True),
    ]

    def __str__(self):
        return self.pubtitle[:64] + "..."

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["top_authors"] = (
            Author.objects.all()
            .annotate(num_art=Count("articles"))
            .order_by("-num_art")[:5]
        )
        context["top_tags"] = ArticlePage.tags.most_common()[:10]
        context["year_list"] = range(2021, date.today().year + 1)
        return context

    def getAnnotation(self):
        for i, b in enumerate(self.article_body):
            if i == 0:
                return b


STATUS_CHOICES = [
    (None, ""),
    ("ZO", "з.о."),
    ("ZVO", "з.в.о."),
]


class ArticleToAuthor(Orderable):
    page = ParentalKey(
        "ArticlePage", on_delete=models.CASCADE, related_name="kmkauthors"
    )
    auth = models.ForeignKey(
        "Author", on_delete=models.CASCADE, related_name="articles"
    )
    status = models.CharField(
        max_length=4, choices=STATUS_CHOICES, null=True, blank=True, default=None
    )

    panels = [
        FieldPanel("auth"),
        FieldPanel("status"),
    ]

    class Meta:
        unique_together = ("page", "auth")


class ArticlePageTag(TaggedItemBase):
    content_object = ParentalKey("ArticlePage", related_name="article_tags")
