import pytest
import os
from playwright.sync_api import sync_playwright, expect

# Setel URL dasar aplikasi (sesuaikan jika running lokal atau staging)
BASE_URL = os.environ.get("LIVE_STAGING_URL", "http://localhost:5000")

@pytest.fixture(scope="session")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()

# ==============================================================================
# 1. SMOKE TEST: MEMASTIKAN TIDAK ADA HALAMAN YANG EROR 500
# ==============================================================================
def test_smoke_pages_no_500(browser_context):
    page = browser_context.new_page()
    
    # Daftar rute penting yang harus dicek statusnya
    routes_to_check = ["/", "/signin", "/signup", "/books/", "/admin/signin/"]
    
    for route in routes_to_check:
        response = page.goto(f"{BASE_URL}{route}")
        # Memastikan response sukses (200) dan bukan eror internal server (500)
        assert response.status < 500, f"Smoke Test Gagal! Rute {route} mengembalikan status {response.status}"
    page.close()
