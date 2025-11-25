# tests/test_parabank.py
import time
import pytest
from playwright.sync_api import sync_playwright

BASE = "https://parabank.parasoft.com/parabank"

@pytest.fixture(scope="session")
def pw():
    with sync_playwright() as p:
        yield p

@pytest.fixture
def page(pw, tmp_path):
    browser = pw.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
    browser.close()

def save_ss(page, name):
    path = f"artifacts/{name}.png"
    page.screenshot(path=path, full_page=True)
    return path

def test_login_valido(page):
    page.goto(f"{BASE}/index.htm")
    page.fill('input[name="username"]', "john")
    page.fill('input[name="password"]', "demo")
    start = time.time()
    page.click('input[value="Log In"]')
    page.wait_for_selector("text=Accounts Overview", timeout=7000)
    elapsed = time.time()-start
    save_ss(page, "TC-01_login_valido")
    assert page.is_visible("text=Accounts Overview")

def test_login_invalido(page):
    page.goto(f"{BASE}/index.htm")
    page.fill('input[name="username"]', "no_user")
    page.fill('input[name="password"]', "badpass")
    page.click('input[value="Log In"]')
    page.wait_for_selector("div[class*='error']", timeout=5000)
    save_ss(page, "TC-02_login_invalido")
    assert page.is_visible("div[class*='error']")

def test_consulta_saldo(page):
    page.goto(f"{BASE}/index.htm")
    page.fill('input[name="username"]', "john")
    page.fill('input[name="password"]', "demo")
    page.click('input[value="Log In"]')
    page.wait_for_selector("text=Accounts Overview", timeout=7000)
    save_ss(page, "TC-03_accounts_overview")
    assert page.is_visible("text=Accounts Overview")

def test_transferencia_valida(page):
    page.goto(f"{BASE}/index.htm")
    page.fill('input[name="username"]', "john")
    page.fill('input[name="password"]', "demo")
    page.click('input[value="Log In"]')
    page.wait_for_selector("text=Accounts Overview", timeout=7000)
    page.click('text=Transfer Funds')
    page.fill('input[name="amount"]', "5")
    page.select_option('select[name="fromAccountId"]', index=0)
    page.select_option('select[name="toAccountId"]', index=1)
    page.click('input[value="Transfer"]')
    page.wait_for_selector("text=Transfer Complete", timeout=7000)
    save_ss(page, "TC-04_transferencia_valida")
    assert page.is_visible("text=Transfer Complete")

def test_logout(page):
    page.goto(f"{BASE}/index.htm")
    page.fill('input[name="username"]', "john")
    page.fill('input[name="password"]', "demo")
    page.click('input[value="Log In"]')
    page.wait_for_selector("text=Accounts Overview", timeout=7000)
    page.click('text=Log Out')
    page.wait_for_selector('text=Customer Login', timeout=5000)
    save_ss(page, "TC-06_logout")
    assert page.is_visible('text=Customer Login')
