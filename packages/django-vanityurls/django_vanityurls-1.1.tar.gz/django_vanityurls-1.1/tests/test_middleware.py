"""
Tests for django-vanityurls middleware
"""
from mock import Mock

from django.http.response import HttpResponse
from django.test import TestCase

from vanityurls.middleware import VanityUrlsMiddleware


class MiddlewareTest(TestCase):

    fixtures = ['basic-db.json']

    def setUp(self):

        self.mock_response = Mock(spec=HttpResponse)

        self.middleware = VanityUrlsMiddleware(lambda x : self.mock_response)
        self.request = Mock()
        self.request.META = {
                'REQUEST_METHOD': 'GET',
        }
        self.request.path = '/testURL/'

    def test_when_request_not_404(self):
        self.mock_response.status_code = 200
        response = self.middleware(self.request)
        self.assertEqual(response, self.mock_response)

    # '/testURL/' doesn't exist in the fixture
    def test_when_request_is_404_with_bad_vanity_url(self):
        self.mock_response.status_code = 404
        response = self.middleware(self.request)
        self.assertEqual(response, self.mock_response)

    # but '/shorturl' does, and maps to '/longurl'
    def test_when_request_is_404_with_good_vanity_url(self):
        self.request.path = '/shorturl'
        self.mock_response.status_code = 404
        response = self.middleware(self.request)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.headers['Location'], '/longurl')
