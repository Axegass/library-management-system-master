// Urusan konfigurasi URL dasar (BASE_URL) di Cypress biasanya diatur di file cypress.config.js,
// namun kita bisa mendefinisikannya langsung atau menggunakan Cypress.config().
const BASE_URL = Cypress.env('LIVE_STAGING_URL') || 'http://localhost:5000';

describe('Library Management System - Automated Testing', () => {

  // ==============================================================================
  // 1. SMOKE TEST: MEMASTIKAN TIDAK ADA HALAMAN YANG EROR 500
  // ==============================================================================
  it('Smoke Test: Memastikan rute-rute utama aman dari error 500', () => {
    const routesToCheck = ['/', '/signin', '/signup', '/books/'];

    routesToCheck.forEach((route) => {
      // cy.request digunakan untuk menembak status HTTP secara cepat tanpa me-render visual UI
      cy.request({
        url: `${BASE_URL}${route}`,
        failOnStatusCode: false // Agar Cypress tidak langsung crash jika ada status error, kita handle manual di bawah
      }).then((response) => {
        expect(response.status).to.be.lessThan(500);
      });
    });
  });

  // ==============================================================================
  // 2. FITUR ADMIN: TAMBAH, EDIT, DAN HAPUS BUKU
  // ==============================================================================
  it('Admin Fitur: Siklus Hidup Buku (Tambah, Edit, Hapus Buku)', () => {
    
    // --- STEP A: LOGIN ADMIN ---
    cy.visit(`${BASE_URL}/admin/signin`);
    cy.get("input[name='email']").type('hamza@gmail.com');
    cy.get("input[name='password']").type('admin'); // Memakai password "admin" teks biasa
    cy.get("button[type='submit']").click();

    // Memastikan dialihkan ke dashboard admin
    cy.url().should('eq', `${BASE_URL}/admin/`);

    // --- STEP B: TAMBAH BUKU ---
    cy.visit(`${BASE_URL}/admin/books/add`);
    cy.get("input[name='name']").type('Buku Testing Playwright');
    cy.get("textarea[name='desc']").type('Deskripsi buku untuk otomasi testing menggunakan Playwright.');
    cy.get("input[name='author']").type('Tim DevOps Kelompok 15');
    cy.get("input[name='edition']").type('1');
    cy.get("input[name='count']").type('5');
    cy.get("button[type='submit']").click();

    // Pastikan buku baru muncul di daftar views admin (Bisa memakai selektor .card.book kalian)
    cy.visit(`${BASE_URL}/admin/books/`);
    cy.contains('Buku Testing Playwright').should('be.visible');

    // --- STEP C: EDIT BUKU ---
    // Mencari card pembungkus buku yang berisi teks, lalu klik tautan 'Edit' di dalamnya
    cy.get('.card.book')
      .contains('Buku Testing Playwright')
      .parents('.card.book')
      .find("a[href*='edit/']")
      .click();

    cy.get("input[name='count']").clear().type('10'); // Clear dulu isian lama, baru ketik '10'
    cy.get("button[type='submit']").click();

    // Verifikasi perubahan stok sukses terbaca angka 10
    cy.visit(`${BASE_URL}/admin/books/`);
    cy.get('.card.book')
      .contains('Buku Testing Playwright')
      .parents('.card.book')
      .should('contain.text', '10');

    // --- STEP D: HAPUS BUKU ---
    cy.get('.card.book')
      .contains('Buku Testing Playwright')
      .parents('.card.book')
      .find("a[href*='delete/']")
      .click();

    // Pastikan buku sudah musnah dan hilang dari daftar
    cy.visit(`${BASE_URL}/admin/books/`);
    cy.contains('Buku Testing Playwright').should('not.exist');
  });

});