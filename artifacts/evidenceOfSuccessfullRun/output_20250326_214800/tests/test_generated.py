import pytest
import requests

@pytest.mark.parametrize('username, password, redirect', [('standard_user', 'secret_sauce', 'product_catalog')])
def test_successful_login(username, password, redirect):
    response = requests.post('/login', data={'username': username, 'password': password})
    assert response.status_code == 200
    assert response.json()['redirect'] == redirect

@pytest.mark.parametrize('username, password, error_message', [('standard_user', 'wrong_password', 'Invalid credentials')])
def test_unsuccessful_login(username, password, error_message):
    response = requests.post('/login', data={'username': username, 'password': password})
    assert response.status_code == 401
    assert response.json()['error_message'] == error_message

@pytest.mark.parametrize('username, password, error_message', [('locked_out_user', 'secret_sauce', 'Account locked')])
def test_locked_user_login(username, password, error_message):
    response = requests.post('/login', data={'username': username, 'password': password})
    assert response.status_code == 403
    assert response.json()['error_message'] == error_message

@pytest.mark.parametrize('product_list', [('visible')])
def test_product_catalog_visibility(product_list):
    response = requests.get('/product_catalog')
    assert response.status_code == 200
    assert response.json()['product_list'] == product_list

@pytest.mark.parametrize('product_id, action, cart_count', [('valid_product_id', 'add', 'increased')])
def test_add_product_to_cart(product_id, action, cart_count):
    response = requests.post('/add_to_cart', data={'product_id': product_id, 'action': action})
    assert response.status_code == 200
    assert response.json()['cart_count'] == cart_count