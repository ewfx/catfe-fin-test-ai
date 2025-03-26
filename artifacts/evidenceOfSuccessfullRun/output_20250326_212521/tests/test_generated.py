import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        self.driver.find_element(By.ID, 'id_username').send_keys(username)
        self.driver.find_element(By.ID, 'id_password').send_keys(password)
        self.driver.find_element(By.ID, 'id_login').click()


class HomePage:
    def __init__(self, driver):
        self.driver = driver

    def is_product_catalog_visible(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'id_product_catalog')))

    def add_product_to_cart(self, product_id):
        self.driver.find_element(By.ID, product_id).click()
        self.driver.find_element(By.ID, 'id_add_to_cart').click()


def test_successful_login(driver):
    LoginPage(driver).login('standard_user', 'secret_sauce')
    assert 'product_catalog' in driver.current_url

def test_invalid_login(driver):
    LoginPage(driver).login('invalid_user', 'invalid_password')
    assert 'Invalid username or password' in driver.page_source

def test_locked_user_login(driver):
    LoginPage(driver).login('locked_out_user', 'secret_sauce')
    assert 'Your account has been locked' in driver.page_source

def test_product_catalog_visibility(driver):
    LoginPage(driver).login('standard_user', 'secret_sauce')
    assert HomePage(driver).is_product_catalog_visible()

def test_add_product_to_cart(driver):
    LoginPage(driver).login('standard_user', 'secret_sauce')
    HomePage(driver).add_product_to_cart('id_product_1')
    assert '1' in driver.find_element(By.ID, 'id_cart_count').text