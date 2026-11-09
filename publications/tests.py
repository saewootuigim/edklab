from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Publication


def create_publication(**fields):
    defaults = {'type': 'Article', 'authors': 'Kim E', 'journal': 'Journal', 'doi': 'https://doi.org/10.1000/1'}
    return Publication.objects.create(**{**defaults, **fields})


class PublicationListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_publication(
            title='Older paper', authors='Kim E, Doe J', year=2023, month=11, journal='Plant Cell',
            volume=35, issue=2, pages='10-20', doi='https://doi.org/10.1000/older')
        create_publication(title='Undated paper', type='Review', year=2025)
        create_publication(title='May paper', year=2025, month=5)
        create_publication(title='November paper', year=2025, month=11)
        create_publication(title='My thesis', type='Dissertation', year=2015)

    def get(self, url):
        return self.client.get(url, secure=True)

    def test_lists_newest_first_without_dissertations(self):
        response = self.get(reverse('publication_list'))
        self.assertTemplateUsed(response, 'publications/publication_list.html')
        html = response.content.decode()
        # Newest year first; within a year, latest month first and no month last.
        positions = [html.index(title) for title in ['November paper', 'May paper', 'Undated paper', 'Older paper']]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn('My thesis', html)
        self.assertEqual(html.count('<li class="list-group-item pb-3"'), 4)

    def test_entry_format(self):
        html = self.get(reverse('publication_list')).content.decode()
        self.assertIn('<h3>Publications</h3>', html)
        self.assertIn('<ol class="custom-counter" id="search-scope">', html)
        # The author-highlighting script looks for authors in ".list-group-item span".
        self.assertIn('<span>Kim E, Doe J</span> (2023)<br/>', html)
        self.assertIn('<a href="https://doi.org/10.1000/older" target="_blank">Older paper</a><br/>', html)
        self.assertIn('<em>Plant Cell</em><br/>', html)
        self.assertIn('vol. 35, issue 2, pp. 10-20', ' '.join(html.split()))

    def test_no_heading_without_publications(self):
        Publication.objects.all().delete()
        self.assertNotContains(self.get(reverse('publication_list')), '<h3>Publications</h3>')

    def test_author_publication_url_shows_the_same_page(self):
        self.assertEqual(
            self.get('/publications/Eun/Kim/Kim E/').content,
            self.get(reverse('publication_list')).content)

    def test_incomplete_author_publication_url_is_not_found(self):
        self.assertEqual(self.get('/publications/Eun/Kim/').status_code, 404)


class PublicationModelTests(TestCase):
    def test_type_choices(self):
        self.assertEqual(Publication._meta.get_field('type').choices, [
            ('Article', 'Article'), ('Review', 'Review'), ('Protocol', 'Protocol'),
            ('Patent', 'Patent'), ('Dissertation', 'Dissertation')])

    def test_str_is_title(self):
        self.assertEqual(str(Publication(title='On Engines')), 'On Engines')

    def test_doi_must_be_a_url(self):
        publication = Publication(type='Article', title='T', authors='A', year=2025, journal='J', doi='not a url')
        with self.assertRaises(ValidationError) as cm:
            publication.full_clean()
        self.assertEqual(list(cm.exception.message_dict), ['doi'])
        publication.doi = 'https://doi.org/10.1000/xyz'
        publication.full_clean()


class PublicationAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = get_user_model().objects.create_superuser('admin', 'admin@example.com', 'pw')
        cls.old = create_publication(title='Old paper', year=2020, journal='Cell')
        cls.new = create_publication(title='New paper', year=2025, month=1, journal='Nature')

    def setUp(self):
        self.client.force_login(self.admin)

    def changelist(self, query=''):
        response = self.client.get(reverse('admin:publications_publication_changelist') + query, secure=True)
        self.assertEqual(response.status_code, 200)
        return list(response.context['cl'].result_list)

    def test_changelist_is_newest_first(self):
        self.assertEqual(self.changelist(), [self.new, self.old])

    def test_changelist_search_and_filters(self):
        self.assertEqual(self.changelist('?q=Old'), [self.old])
        self.assertEqual(self.changelist('?year=2025'), [self.new])
        self.assertEqual(self.changelist('?journal=Cell'), [self.old])

    def test_add_change_and_delete_pages_render(self):
        for url in [
            reverse('admin:publications_publication_add'),
            reverse('admin:publications_publication_change', args=[self.old.pk]),
            reverse('admin:publications_publication_delete', args=[self.old.pk]),
        ]:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url, secure=True).status_code, 200)
