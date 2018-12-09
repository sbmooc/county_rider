from unittest import TestCase
import mock
from requests_oauthlib import OAuth2Session
import endpoints


class FlaskTests(TestCase):

    @mock.patch('requests_oauthlib.OAuth2Session')
    def test_collect_activities(self, mock_session):

        mock_session.return_value = OAuth2Session()

        print(endpoints.collect_activities())

        a = 'a'