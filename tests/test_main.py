import os

from dotenv import load_dotenv
from starlette.testclient import TestClient

from main import app, send_webhook

client = TestClient(app)
json_boi = {'action': 'created',
            'sponsorship': {'node_id': 'S_kwDAX"OAD9fc84ASDAasf', 'created_at': '2022-11-23T12:57:58+00:00',
                            'sponsorable': {'login': 'TheLovinator1', 'id': 4153203, 'node_id': 'MDQ61asXasjQxNTMyMDM=',
                                            'avatar_url': 'https://avatars.githubusercontent.com/u/4153203?v=4',
                                            'gravatar_id': '', 'url': 'https://api.github.com/users/TheLovinator1',
                                            'html_url': 'https://github.com/TheLovinator1',
                                            'followers_url': 'https://api.github.com/users/TheLovinator1/followers',
                                            'following_url': 'https://api.github.com/users/TheLovinator1/following{'
                                                             '/other_user}',
                                            'gists_url': 'https://api.github.com/users/TheLovinator1/gists{/gist_id}',
                                            'starred_url': 'https://api.github.com/users/TheLovinator1/starred{'
                                                           '/owner}{/repo}',
                                            'subscriptions_url':
                                                'https://api.github.com/users/TheLovinator1/subscriptions',
                                            'organizations_url': 'https://api.github.com/users/TheLovinator1/orgs',
                                            'repos_url': 'https://api.github.com/users/TheLovinator1/repos',
                                            'events_url': 'https://api.github.com/users/TheLovinator1/events{/privacy}',
                                            'received_events_url':
                                                'https://api.github.com/users/TheLovinator1/received_events',
                                            'type': 'User', 'site_admin': False},
                            'maintainer': {'login': 'TheLovinator1', 'id': 4153203, 'node_id': 'MDQ61asXasjQxNTMyMDM=',
                                           'avatar_url': 'https://avatars.githubusercontent.com/u/4153203?v=4',
                                           'gravatar_id': '', 'url': 'https://api.github.com/users/TheLovinator1',
                                           'html_url': 'https://github.com/TheLovinator1',
                                           'followers_url': 'https://api.github.com/users/TheLovinator1/followers',
                                           'following_url': 'https://api.github.com/users/TheLovinator1/following{'
                                                            '/other_user}',
                                           'gists_url': 'https://api.github.com/users/TheLovinator1/gists{/gist_id}',
                                           'starred_url': 'https://api.github.com/users/TheLovinator1/starred{'
                                                          '/owner}{/repo}',
                                           'subscriptions_url':
                                               'https://api.github.com/users/TheLovinator1/subscriptions',
                                           'organizations_url': 'https://api.github.com/users/TheLovinator1/orgs',
                                           'repos_url': 'https://api.github.com/users/TheLovinator1/repos',
                                           'events_url': 'https://api.github.com/users/TheLovinator1/events{/privacy}',
                                           'received_events_url':
                                               'https://api.github.com/users/TheLovinator1/received_events',
                                           'type': 'User', 'site_admin': False},
                            'sponsor': {'login': 'testing', 'id': 1, 'node_id': 'U_kgDOBwX9RA',
                                        'avatar_url': 'https://avatars.githubusercontent.com/u/1?v=4',
                                        'gravatar_id': '', 'url': 'https://api.github.com/users/testing',
                                        'html_url': 'https://github.com/testing',
                                        'followers_url': 'https://api.github.com/users/testing/followers',
                                        'following_url': 'https://api.github.com/users/testing/following{/other_user}',
                                        'gists_url': 'https://api.github.com/users/testing/gists{/gist_id}',
                                        'starred_url': 'https://api.github.com/users/testing/starred{/owner}{/repo}',
                                        'subscriptions_url': 'https://api.github.com/users/testing/subscriptions',
                                        'organizations_url': 'https://api.github.com/users/testing/orgs',
                                        'repos_url': 'https://api.github.com/users/testing/repos',
                                        'events_url': 'https://api.github.com/users/testing/events{/privacy}',
                                        'received_events_url': 'https://api.github.com/users/testing/received_events',
                                        'type': 'User', 'site_admin': False}, 'privacy_level': 'public',
                            'tier': {'node_id': 'ST_kwDOAD9fc84AAiB5', 'created_at': '2022-03-02T23:11:37Z',
                                     'description': '- Buy me coffee.\r\n\r\nMore coffee = more code.\r\n',
                                     'monthly_price_in_cents': 100, 'monthly_price_in_dollars': 1,
                                     'name': '$1 one time', 'is_one_time': True, 'is_custom_amount': False}},
            'sender': {'login': 'testing', 'id': 1, 'node_id': 'U_kasfafwX9RA',
                       'avatar_url': 'https://avatars.githubusercontent.com/u/1?v=4', 'gravatar_id': '',
                       'url': 'https://api.github.com/users/testing', 'html_url': 'https://github.com/testing',
                       'followers_url': 'https://api.github.com/users/testing/followers',
                       'following_url': 'https://api.github.com/users/testing/following{/other_user}',
                       'gists_url': 'https://api.github.com/users/testing/gists{/gist_id}',
                       'starred_url': 'https://api.github.com/users/testing/starred{/owner}{/repo}',
                       'subscriptions_url': 'https://api.github.com/users/testing/subscriptions',
                       'organizations_url': 'https://api.github.com/users/testing/orgs',
                       'repos_url': 'https://api.github.com/users/testing/repos',
                       'events_url': 'https://api.github.com/users/testing/events{/privacy}',
                       'received_events_url': 'https://api.github.com/users/testing/received_events', 'type': 'User',
                       'site_admin': False}}


def test_send_webhook():
    load_dotenv(verbose=True)
    webhook_url = os.environ.get("WEBHOOK_URL", default=None)
    hook = send_webhook(json_boi, webhook_url)
    assert hook.ok
    assert hook.status_code == 200


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
