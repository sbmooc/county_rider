from unittest import TestCase
import mock
from requests_oauthlib import OAuth2Session
import county_rider


class FlaskTests(TestCase):

    @mock.patch('requests_oauthlib.OAuth2Session')
    def test_collect_activities(self, mock_session):

        mock_session.return_value = OAuth2Session()

        print(county_rider.collect_activities())

        a = 'a'