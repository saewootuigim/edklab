import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Education, Person


def create_person(first_name, last_name, **fields):
    defaults = {'email': f'{first_name.lower()}@example.com', 'title': 'Member', 'year_start': 2020}
    return Person.objects.create(first_name=first_name, last_name=last_name, **{**defaults, **fields})


def normalized(text):
    return ' '.join(text.split())


class PeoplePageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.pi = create_person(
            'Eun-Deok', 'Kim', priority=1, year_start=2020,
            google_scholar='https://scholar.google.com/kim', orcid='0000-0001-2345-6789',
            linkedin='https://linkedin.com/in/kim', pubmed='https://pubmed.gov/kim',
            personal_website='https://kim.example.com')
        Education.objects.create(person=cls.pi, degree='Ph.D.', school='Univ A', year_earned=2010)
        Education.objects.create(person=cls.pi, degree='B.S.', school='Univ B', year_earned=2002)
        create_person('Bob', 'Smith', priority=4, year_start=2022)
        create_person('Alice', 'Jones', priority=4, year_start=2022)
        create_person('Zed', 'Brown', priority=4, year_start=2021)
        create_person('Carol', 'Lee', middle_name='Ann', priority=2, year_start=2023)
        create_person('Nora', 'Norole', year_start=2024)  # no role
        old = create_person(
            'Old', 'Timer', priority=4, year_start=2010, year_finish=2015, position_after_finish='Professor at X')
        Education.objects.create(person=old, degree='M.S.', school='Alumni Univ', year_earned=2012)
        create_person('Recent', 'Grad', priority=6, year_start=2018, year_finish=2022)
        create_person('Same', 'Year', priority=2, year_start=2016, year_finish=2022)

    def get_html(self):
        response = self.client.get(reverse('people_list'), secure=True)
        self.assertTemplateUsed(response, 'people/people_list.html')
        self.assertTemplateUsed(response, 'people/card.html')
        return response.content.decode()

    def test_lists_current_members_then_alumni(self):
        names = re.findall(r'<h5 class="card-title mb-1">(.*?)</h5>', self.get_html(), re.S)
        self.assertEqual([normalized(name) for name in names], [
            # Current members: by role, then start year, then first name. No role sorts first.
            'Nora Norole', 'Eun-Deok Kim', 'Carol Ann Lee', 'Zed Brown', 'Alice Jones', 'Bob Smith',
            # Alumni: latest finish year first, then by role.
            'Same Year', 'Recent Grad', 'Old Timer',
        ])

    def test_role_headings(self):
        headings = re.findall(r'<h5 class="py-2 mb-0 fw-bold"[^>]*>(.*?)</h5>', self.get_html(), re.S)
        # One heading per role among current members, plural when the role has several
        # people. A member without a role gets an empty heading. Alumni get none.
        self.assertEqual(
            [normalized(heading) for heading in headings],
            ['', 'Principal Investigator', 'Postdoctoral Researcher', 'Graduate Students'])

    def test_alumni_section_only_when_there_are_alumni(self):
        self.assertIn('<h2 class="text-center py-4">Lab Alumni</h2>', self.get_html())
        Person.objects.filter(year_finish__isnull=False).delete()
        self.assertNotIn('Lab Alumni', self.get_html())

    def test_card_details(self):
        html = self.get_html()
        self.assertIn('src="/static/people/Eun-Deok Kim.jpg"', html)
        self.assertIn('2020 - present', html)
        self.assertIn('2010 - 2015', html)
        self.assertIn('now Professor at X', html)
        self.assertIn('id="Eun-DeokKim"', html)
        self.assertIn("onclick=\"copyToClipboard('Eun-DeokKim')\">eun-deok@example.com</span>", html)
        self.assertIn('href="https://orcid.org/0000-0001-2345-6789"', html)
        for url in ['https://scholar.google.com/kim', 'https://linkedin.com/in/kim', 'https://pubmed.gov/kim']:
            self.assertIn(f'href="{url}" target="_blank"', html)
        self.assertIn(
            '<a href="https://kim.example.com" target="_blank" class="btn btn-secondary" '
            'style="margin-left: -15px;">Personal Website</a>', html)
        # Links only appear for people who have them.
        self.assertEqual(html.count('alt="orcid logo"'), 1)
        self.assertEqual(html.count('Personal Website'), 1)

    def test_education_shown_for_current_members_only(self):
        html = self.get_html()
        self.assertIn('<td><strong>Ph.D.</strong></td>', html)
        self.assertIn('<td>Univ A</td>', html)
        self.assertIn('<td><strong>B.S.</strong></td>', html)
        self.assertNotIn('Alumni Univ', html)
        self.assertEqual(html.count('<table'), 6)  # one per current member


class PersonModelTests(TestCase):
    def test_str(self):
        person = create_person('Ada', 'Lovelace')
        self.assertEqual(str(person), 'Ada Lovelace')
        education = Education(person=person, degree='Ph.D.', school='Cambridge', year_earned=1840)
        self.assertEqual(str(education), 'Ph.D. Cambridge (1840)')

    def test_priority_choices(self):
        self.assertEqual(Person._meta.get_field('priority').choices, [
            (1, 'supervisor'), (2, 'postdoc'), (3, 'visiting scholar'),
            (4, 'grad student'), (5, 'research technician'), (6, 'undergrad')])

    def test_link_fields_must_be_urls(self):
        for field in ['personal_website', 'google_scholar', 'linkedin', 'pubmed']:
            with self.subTest(field=field):
                person = Person(
                    first_name='Ada', last_name='Lovelace', email='ada@example.com', title='PI',
                    year_start=2020, **{field: 'not a url'})
                with self.assertRaises(ValidationError) as cm:
                    person.full_clean()
                self.assertEqual(list(cm.exception.message_dict), [field])


class PersonAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = get_user_model().objects.create_superuser('admin', 'admin@example.com', 'pw')
        cls.current_a = create_person('Ada', 'Kim')
        cls.alum_2019 = create_person('Bea', 'Lee', year_finish=2019)
        cls.alum_2021 = create_person('Cy', 'Park', year_finish=2021)
        cls.current_b = create_person('Dan', 'Choi')
        Education.objects.create(person=cls.current_a, degree='Ph.D.', school='Univ A', year_earned=2010)

    def setUp(self):
        self.client.force_login(self.admin)

    def changelist(self, query=''):
        response = self.client.get(reverse('admin:people_person_changelist') + query, secure=True)
        self.assertEqual(response.status_code, 200)
        return list(response.context['cl'].result_list)

    def test_changelist_lists_current_members_first_then_alumni_by_finish_year(self):
        # Ties are broken by the most recently added person first.
        self.assertEqual(self.changelist(), [self.current_b, self.current_a, self.alum_2021, self.alum_2019])

    def test_changelist_search_and_filters(self):
        self.assertEqual(self.changelist('?q=Kim'), [self.current_a])
        self.assertEqual(self.changelist('?year_finish=2019'), [self.alum_2019])

    def test_add_change_and_delete_pages_render(self):
        for url in [
            reverse('admin:people_person_add'),
            reverse('admin:people_person_change', args=[self.current_a.pk]),
            reverse('admin:people_person_delete', args=[self.current_a.pk]),
        ]:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url, secure=True).status_code, 200)

    def test_change_page_has_education_inline_with_one_blank_row(self):
        response = self.client.get(reverse('admin:people_person_change', args=[self.current_a.pk]), secure=True)
        self.assertEqual(response.context['inline_admin_formsets'][0].formset.total_form_count(), 2)

    def test_add_person_with_education(self):
        response = self.client.post(reverse('admin:people_person_add'), {
            'priority': '2', 'first_name': 'Grace', 'last_name': 'Hopper', 'email': 'grace@example.com',
            'title': 'Postdoc', 'year_start': '2021', 'personal_website': 'example.com',
            'educations-TOTAL_FORMS': '1', 'educations-INITIAL_FORMS': '0',
            'educations-MIN_NUM_FORMS': '0', 'educations-MAX_NUM_FORMS': '1000',
            'educations-0-degree': 'Ph.D.', 'educations-0-school': 'Yale', 'educations-0-year_earned': '1934',
        }, secure=True)
        self.assertEqual(response.status_code, 302)
        grace = Person.objects.get(first_name='Grace')
        self.assertEqual(grace.educations.get().school, 'Yale')
        # URLs typed without a scheme get https:// (Django 6 default).
        self.assertEqual(grace.personal_website, 'https://example.com')
