# Library Management System
A simple flask app to manage users along with mysql (now postgresql) service

![Libray Management App - Flask](https://github.com/hamzaavvan/library-management-system/blob/master/ss/ss2.JPG?raw=true)

5026231100 - Defita Aulia Syarif

5026231171 - Redo Adika Dharmawan

5026231209 - Adityo Rafi Wardhana

5026231217 - Rahmadhona Elokpribadi Kusmawan


# 📚 Library Management System (DevOps CI/CD Pipeline)

[![CI/CD Staging](https://github.com/Axegass/library-management-system-master/actions/workflows/staging.yml/badge.svg)](https://github.com/Axegass/library-management-system-master/actions)
[![CI/CD Production](https://github.com/Axegass/library-management-system-master/actions/workflows/production.yml/badge.svg)](https://github.com/Axegass/library-management-system-master/actions)

Sebuah aplikasi web manajemen perpustakaan berbasis pola arsitektur **MVC (Model-View-Controller)** yang dirancang untuk membantu pengguna mengoleksi dan mendokumentasikan daftar buku mereka dengan rapi. Proyek ini difokuskan sebagai implementasi praktik **DevOps** dengan otomatisasi **CI/CD menggunakan GitHub Actions** dan dideploy ke **Google Cloud Platform (GCP)**.

---

## 🛠️ Tech Stack & Arsitektur

* **Backend Framework:** Python (Flask v2.3.2)
* **Frontend Component:** Server-Side Rendering (SSR) via HTML, Jinja2 Template Engine, & Bootstrap CSS
* **Database:** PostgreSQL (Relational Database)
* **Package Manager:** pip (`requirements.txt`)
* **CI/CD Automation:** GitHub Actions
* **Cloud Infrastructure:** Google Cloud Platform (GCP)

---

## 🚀 Fitur Utama (CRUD Aplikasi)

Aplikasi ini memiliki antarmuka (UI) intuitif yang mendukung pengelolaan dokumentasi data buku:
* **Tambah Buku (Create):** Menambahkan data buku baru yang dipinjam atau dikoleksi ke dalam sistem perpustakaan.
* **Lihat Daftar (Read):** Menampilkan katalog daftar buku secara rapi yang ditarik langsung dari database.
* **Edit Data (Update):** Memperbarui detail informasi buku jika terdapat penyesuaian status.
* **Hapus Buku (Delete):** Menghapus catatan buku yang sudah tidak relevan dari daftar dokumentasi.

---

## 🔄 Alur Pipeline CI/CD (Staging & Production)

Otomatisasi deployment dibagi menjadi 2 tahap lingkungan (*environment*) terpisah demi menjaga integritas dan keamanan aplikasi:

```text
[Developer] -> Push ke Branch 'staging' -> [CI Stage: Linting & Unit Test]
                                                 |
                                            (Jika Hijau)
                                                 v
                                       [CD Stage: Deploy Staging (GCP)] -> [Smoke Test]
                                                 |
                                         (Manual Merge ke 'main')
                                                 v
                                       [CD Stage: Deploy Production (GCP)] -> LIVE!
