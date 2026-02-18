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
