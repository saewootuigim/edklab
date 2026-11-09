import re

from django.test import TestCase
from django.urls import reverse

# URL name -> page title.
PAGES = {
    'main_page': 'KimLab | home',
    'people_list': 'KimLab | people',
    'publication_list': 'KimLab | publication',
    'lab_update': 'KimLab | lab update',
    'opportunity': 'KimLab | Opportunities',
    'contact': 'KimLab | Contact',
}


def active_nav_links(html):
    """Return the hrefs of the navbar links marked as active."""
    return re.findall(r'<a class="nav-link[^"]*\bactive\b[^"]*" href="([^"]*)"', html)


class SiteLayoutTests(TestCase):
    def get(self, url):
        # secure=True: with DEBUG off, SECURE_SSL_REDIRECT redirects plain HTTP.
        return self.client.get(url, secure=True)

    def test_every_page_renders_with_the_base_layout_and_its_title(self):
        for name, title in PAGES.items():
            with self.subTest(page=name):
                response = self.get(reverse(name))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'base.html')
                page_title = re.search(r'<title>(.*?)</title>', response.content.decode(), re.S)[1]
                self.assertEqual(' '.join(page_title.split()), title)

    def test_navbar_highlights_only_the_current_page(self):
        for name in PAGES:
            with self.subTest(page=name):
                html = self.get(reverse(name)).content.decode()
                self.assertEqual(active_nav_links(html), [reverse(name)])

    def test_navbar_highlights_publications_on_author_publication_urls(self):
        html = self.get('/publications/Eun/Kim/Kim E/').content.decode()
        self.assertEqual(active_nav_links(html), [reverse('publication_list')])

    def test_footer_links_to_every_page(self):
        html = self.get(reverse('main_page')).content.decode()
        footer = html[html.index('<footer'):html.index('</footer>')]
        for name in PAGES:
            self.assertIn(f'href="{reverse(name)}"', footer)

    def test_static_files_are_linked_under_static_url(self):
        response = self.get(reverse('main_page'))
        self.assertContains(response, 'src="/static/syracuse-arts-sciences.svg"')
        self.assertContains(response, 'src="/static/icons/copy_button.svg"')

    def test_unknown_url_is_not_found(self):
        self.assertEqual(self.get('/no-such-page/').status_code, 404)


class HomePageTests(TestCase):
    def test_shows_carousel_and_welcome_text(self):
        response = self.client.get(reverse('main_page'), secure=True)
        self.assertTemplateUsed(response, 'main/main_page.html')
        html = response.content.decode()
        self.assertEqual(html.count('class="carousel-item'), 9)
        for image in ['1.png', '2.png', '3.png', '4.png', '5.png', '72.png', '82.png', '92.png']:
            self.assertIn(f'src="/static/carousel/{image}"', html)
        self.assertIn('<source src="/static/carousel/6.mp4" type="video/mp4">', html)
        self.assertIn('Welcome to Kim Lab', html)
