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

# ==============================================================================
# 2. FITUR ADMIN: TAMBAH, EDIT, DAN HAPUS BUKU
# ==============================================================================
def test_admin_book_lifecycle(browser_context):
    page = browser_context.new_page()
    
    # --- STEP A: LOGIN ADMIN ---
    page.goto(f"{BASE_URL}/admin/signin/")
    page.fill("input[name='email']", "hamza@gmail.com") # Sesuai dummy data lms.sql
    page.fill("input[name='password']", "admin") 
    page.click("button[type='submit']")
    
    # Pastikan dialihkan ke dashboard admin
    expect(page).to_have_url(f"{BASE_URL}/admin/")
    
    # --- STEP B: TAMBAH BUKU ---
    page.goto(f"{BASE_URL}/admin/books/add")
    page.fill("input[name='name']", "Buku Testing Playwright")
    page.fill("textarea[name='desc']", "Deskripsi buku untuk otomasi testing menggunakan Playwright.")
    page.fill("input[name='author']", "Tim DevOps Kelompok 15")
    page.fill("input[name='edition']", "1")
    page.fill("input[name='count']", "5")
    page.click("button[type='submit']")
    
    # Pastikan buku baru muncul di daftar views admin
    page.goto(f"{BASE_URL}/admin/books/")
    expect(page.get_by_text("Buku Testing Playwright")).to_be_visible()
    
    # --- STEP C: EDIT BUKU ---
    # Pakai .card.book sebagai container, bukan div biasa
    # filter() dengan has_text lalu ambil first supaya tidak ambiguous
    page.locator(".card.book").filter(
        has_text="Buku Testing Playwright"
    ).first.locator("a[href*='edit/']").click()

    page.fill("input[name='count']", "10")
    page.click("button[type='submit']")

    # Verifikasi stok berubah
    page.goto(f"{BASE_URL}/admin/books/")
    expect(
        page.locator(".card.book").filter(has_text="Buku Testing Playwright").first
    ).to_contain_text("10")

    # --- STEP D: HAPUS BUKU ---
    page.locator(".card.book").filter(
        has_text="Buku Testing Playwright"
    ).first.locator("a[href*='delete/']").click()

    # Pastikan buku hilang
    page.goto(f"{BASE_URL}/admin/books/")
    expect(page.get_by_text("Buku Testing Playwright")).not_to_be_visible()
    page.close()