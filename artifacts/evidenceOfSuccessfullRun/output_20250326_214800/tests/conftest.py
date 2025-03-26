import pytest

@pytest.fixture(scope='session')
def test_session():
    print('Setting up test session')
    yield
    print('Tearing down test session')