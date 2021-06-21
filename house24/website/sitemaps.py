from django.contrib.sitemaps import Sitemap

from db.models.pages import MainPage, AboutPage, ContactsPage, ServicesPage


class MainPageSitemap(Sitemap):
    def items(self):
        return [MainPage.load(), ]

    def title(self):
        return MainPage.load().title


class AboutPageSitemap(Sitemap):
    def items(self):
        return [AboutPage.load(), ]


class ContactPageSitemap(Sitemap):
    def items(self):
        return [ContactsPage.load(), ]


class ServicesPageSitemap(Sitemap):
    def items(self):
        return [ServicesPage.load(), ]
