# 15-puzzle-solver
Disusun untuk memenuhi Tugas Kecil 3 IF2211 Strategi Algoritma "Penyelesaian Persoalan 15-Puzzle dengan Algoritma *Branch and Bound*"

## Daftar Isi
* [Deskripsi Singkat Program](#deskripsi-singkat-program)
* [Struktur Program](#struktur-program)
* [Requirement Program](#requirement-program)
* [Cara Menyiapkan *Environment*](#cara-menyiapkan-environment)
* [Cara Menjalankan Program](#cara-menjalankan-program)
* [Cara Menggunakan Program](#cara-menggunakan-program)
* [Author](#author)

## Deskripsi Singkat Program

## Struktur Program
```bash
.
│   .gitignore
│   README.md
│   requirements.txt
│   
├───doc
│   
├───src
│   │   app.py
│   │   puzzle.py
│   │   
│   ├───static
│   │   ├───images
│   │   │       loading.gif
│   │   │       logo.png
│   │   │       
│   │   ├───js
│   │   │       index.js
│   │   │       view.js
│   │   │       
│   │   └───styles
│   │           stylesheet.css
│   │           
│   └───templates
│           index.html
│           view.html
│
│           
└───test
        bisa1.txt
        bisa2.txt
        bisa3.txt
        tidakbisa1.txt
        tidakbisa2.txt
```

## Requirement Program
* Python versi 3.8.5 atau lebih baru. Pastikan pula terdapat package PyPi (PIP) pada Python Anda.
* Flask versi 2.0.3 atau lebih baru.
* NumPy versi 1.22.3 atau lebih baru.
* PyFladesk versi 1.1 atau lebih baru.
* Google CDN jQuery versi 3.6.0 atau lebih baru.

## Cara Menyiapkan *Environment*
1. Pastikan Python versi 3.8.5 atau lebih baru sudah terpasang pada komputer (Anda dapat mengecek versi Python dengan menjalankan *command* `py --version` pada *command prompt*).
2. Lakukan instalasi semua *library* yang digunakan pada program. Anda dapat menginstalasi seluruh *library* yang digunakan pada program ini dengan menjalankan *command* `pip install -r requirements.txt` pada *command prompt*.
3. Jika seluruh *library* berhasil diinstalasi, maka akan terdapat pemberitahuan pada *command prompt*.

## Cara Menjalankan Program
1. Pastikan sudah menyiapkan *environment* program serta mesin eksekusi terhubung dengan internet.
2. Jalankan program `app.py` dengan menjalankan perintah `py app.py` pada *command prompt* pada folder `src`.
3. Jika berhasil dijalankan, maka akan terdapat *window* Python pada komputer.

## Cara Menggunakan Program
1. *Upload* file `.txt` sesuai dengan format yang terdapat pada folder `test` atau menggantinya secara manual pada program.
2. Tekan tombol *Calculate* pada program.
3. Tunggu hingga program berhasil menemukan jawaban dari *puzzle*.
4. Kemudian, program akan menunjukkan *step-by-step* yang dibutuhkan untuk mendapatkan solusi.

## Author
* Nama: Rayhan Kinan Muhannad
* NIM: 13520065
* Prodi/Jurusan: STEI/Teknik Informatika
* Profile GitHub: [rayhankinan](https://github.com/rayhankinan)