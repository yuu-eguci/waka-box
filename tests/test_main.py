import json

import pytest

import main


def test_run_keeps_its_name_and_docstring():
    assert main.run.__name__ == 'run'
    assert main.run.__doc__.startswith('メインメソッドです。')


def test_bar_chart_for_zero_percent_is_empty():
    assert main._generate_bar_chart(0, 15) == '░' * 15


def test_bar_chart_always_has_given_size():
    for percent in (0, 0.01, 6.67, 50, 99.99, 100):
        assert len(main._generate_bar_chart(percent, 15)) == 15


class FakeResponse:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self.ok = status_code < 400
        self.text = json.dumps(payload)


STATS = {'data': {'languages': [
    {'name': 'Python', 'text': '1 hr', 'percent': 100.0}]}}
GIST = {'files': {'file': {'content': 'x'}}}


@pytest.fixture
def env(monkeypatch):
    monkeypatch.setenv('WAKATIME_SECRET_API_KEY', 'dummy-key')
    monkeypatch.setenv('GITHUB_ACCESS_TOKEN', 'dummy-token')
    monkeypatch.setenv('GIST_ID', 'dummy-gist')
    monkeypatch.delenv('DRY_RUN', raising=False)
    monkeypatch.setattr(main.dotenv, 'load_dotenv', lambda *a, **k: None)


def test_run_raises_when_wakatime_fails_without_leaking_key(env, monkeypatch):
    monkeypatch.setattr(main.requests, 'get',
                        lambda *a, **k: FakeResponse(401, {'error': 'x'}))
    monkeypatch.setattr(main.requests, 'patch', pytest.fail)
    with pytest.raises(main.ApiRequestError, match='401') as e:
        main.run()
    assert 'dummy-key' not in str(e.value)


def test_run_raises_when_gist_update_fails(env, monkeypatch):
    monkeypatch.setattr(main.requests, 'get',
                        lambda *a, **k: FakeResponse(200, STATS))
    monkeypatch.setattr(main.requests, 'patch',
                        lambda *a, **k: FakeResponse(404, {'message': 'x'}))
    with pytest.raises(main.ApiRequestError, match='404'):
        main.run()


def test_run_updates_gist_with_patch_and_timeouts(env, monkeypatch):
    calls = []

    def fake(method, payload):
        def _request(url, **kwargs):
            calls.append((method, url, kwargs))
            return FakeResponse(200, payload)
        return _request

    monkeypatch.setattr(main.requests, 'get', fake('get', STATS))
    monkeypatch.setattr(main.requests, 'patch', fake('patch', GIST))
    main.run()
    assert [(m, u) for m, u, _ in calls] == [
        ('get', 'https://wakatime.com/api/v1/users/current/stats/last_7_days'
                '?api_key=dummy-key'),
        ('patch', 'https://api.github.com/gists/dummy-gist'),
    ]
    assert all(kwargs.get('timeout') for _, _, kwargs in calls)
