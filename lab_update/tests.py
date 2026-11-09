from datetime import UTC, datetime, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Post


class LabUpdatePageTests(TestCase):
    def get_page(self):
        return self.client.get(reverse('lab_update'), secure=True)

    def test_shows_placeholder_without_posts(self):
        response = self.get_page()
        self.assertTemplateUsed(response, 'lab_update/post_list.html')
        self.assertContains(response, 'No updates yet.')

    def test_shows_newest_post_first(self):
        Post.objects.create(title='Spring post', image='spring.jpg', posted_at=datetime(2026, 3, 1, tzinfo=UTC))
        Post.objects.create(title='Fall post', image='fall.jpg', posted_at=datetime(2026, 10, 1, tzinfo=UTC))
        html = self.get_page().content.decode()
        self.assertLess(html.index('Fall post'), html.index('Spring post'))
        self.assertNotIn('No updates yet.', html)

    def test_post_shows_local_time_image_and_caption(self):
        Post.objects.create(
            title='Lab retreat', image='retreat 2026.jpg', body='Day one\nDay two',
            posted_at=datetime(2026, 9, 2, 17, 10, tzinfo=UTC))
        response = self.get_page()
        self.assertContains(response, '<h4 class="mb-1">Lab retreat</h4>')
        self.assertContains(response, 'September 2, 2026, 1:10 p.m.')  # America/New_York
        self.assertContains(response, 'src="/static/lab_update/retreat 2026.jpg"')
        self.assertContains(response, '<p class="mt-3" style="white-space: pre-line;">Day one\nDay two</p>')

    def test_caption_is_optional(self):
        Post.objects.create(title='Photo only', image='photo.jpg')
        self.assertNotContains(self.get_page(), 'white-space: pre-line')


class PostModelTests(TestCase):
    def test_posted_at_defaults_to_now_and_str_is_title(self):
        post = Post.objects.create(title='Hello', image='hello.jpg')
        self.assertLess(abs(timezone.now() - post.posted_at), timedelta(seconds=10))
        self.assertEqual(str(post), 'Hello')


class PostAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = get_user_model().objects.create_superuser('admin', 'admin@example.com', 'pw')
        cls.retreat = Post.objects.create(title='Lab retreat', image='retreat.jpg', body='Fun')
        cls.seminar = Post.objects.create(title='Seminar', image='seminar.jpg')

    def setUp(self):
        self.client.force_login(self.admin)

    def test_changelist_columns_and_search(self):
        url = reverse('admin:lab_update_post_changelist')
        changelist = self.client.get(url, secure=True).context['cl']
        self.assertEqual(changelist.list_display, ['action_checkbox', 'title', 'posted_at', 'image'])
        self.assertEqual(list(changelist.result_list), [self.seminar, self.retreat])
        found = self.client.get(url + '?q=retreat', secure=True).context['cl'].result_list
        self.assertEqual(list(found), [self.retreat])

    def test_add_change_and_delete_pages_render(self):
        for url in [
            reverse('admin:lab_update_post_add'),
            reverse('admin:lab_update_post_change', args=[self.retreat.pk]),
            reverse('admin:lab_update_post_delete', args=[self.retreat.pk]),
        ]:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url, secure=True).status_code, 200)
