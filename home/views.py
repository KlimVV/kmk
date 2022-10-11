from wagtail.admin.views.reports import PageReportView
from wagtail.admin.filters import DateRangePickerWidget, WagtailFilterSet
from wagtail.models import Page

from home.models import ArticlePage
import django_filters
from django.contrib.auth import get_user_model


class LockedPagesReportFilterSet(WagtailFilterSet):
    pubdate = django_filters.DateFromToRangeFilter(widget=DateRangePickerWidget)

    class Meta:
        model = Page
        fields = ["pubdate", "live"]


class ArticlesReportView(PageReportView):

    header_icon = "doc-empty-inverse"
    list_export = PageReportView.list_export + ["pubdate", "pubtitle", "event"]

    filterset_class = LockedPagesReportFilterSet
    # export_headings = dict(last_published_at='Last Published', **PageReportView.export_headings)

    def get_queryset(self):
        return ArticlePage.objects.all()
