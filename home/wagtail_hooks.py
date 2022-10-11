from django.urls import path, reverse

from wagtail.admin.menu import AdminOnlyMenuItem, MenuItem
from wagtail import hooks

from .views import ArticlesReportView


@hooks.register("register_reports_menu_item")
def register_articles_report_menu_item():
    return AdminOnlyMenuItem(
        "Articles Page",
        reverse("articles_report"),
        classnames="icon icon-" + ArticlesReportView.header_icon,
        order=700,
    )


@hooks.register("register_admin_urls")
def register_articles_report_url():
    return [
        path("reports/articles/", ArticlesReportView.as_view(), name="articles_report"),
    ]
