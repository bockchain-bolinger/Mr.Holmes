from Core.Support.HttpClient import Client


def test_session_is_singleton_instance():
    Client.reset_session()
    first = Client.session()
    second = Client.session()

    assert first is second


def test_reset_session_recreates_instance():
    Client.reset_session()
    first = Client.session()
    Client.reset_session()
    second = Client.session()

    assert first is not second


def test_post_uses_default_timeout_when_missing(monkeypatch):
    calls = {}

    class DummySession:
        def post(self, **kwargs):
            calls.update(kwargs)
            return object()

    monkeypatch.setattr(Client, "session", staticmethod(lambda: DummySession()))

    Client.post(url="https://example.com", headers={"a": "b"}, data={"k": "v"})

    assert calls["timeout"] == Client.DEFAULT_TIMEOUT
    assert calls["url"] == "https://example.com"
