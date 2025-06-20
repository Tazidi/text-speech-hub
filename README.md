# 🎧 Text ↔ Speech Converter (Streamlit App)

Aplikasi berbasis **Streamlit** yang memungkinkan konversi dua arah antara **teks ke suara (Text-to-Speech)** dan **suara ke teks (Speech-to-Text)**.  
Dilengkapi dengan pengaturan bahasa, gender suara, kecepatan bicara, dan volume output.  
Mendukung input dari **file teks, dokumen, PDF, link website**, serta **rekaman mikrofon atau upload file audio**.

---

## 🚀 Fitur Utama

### 🗣️ Text to Speech
- ✅ Masukkan teks langsung, atau
- 📂 Upload file `.txt`, `.docx`, atau `.pdf`
- 🌐 Ambil teks langsung dari **URL website**
- 🎙️ Konversi teks ke suara menggunakan **Google Cloud Text-to-Speech**
- ⚙️ Atur bahasa (Indonesia/Inggris), gender suara, kecepatan bicara, dan volume
- 🔊 Putar hasil audio langsung di browser
- 💾 Unduh hasil suara dalam format `.mp3`

### 🎤 Speech to Text
- 🎙️ Rekam dari mikrofon, atau
- 📁 Upload file audio (`.mp3` / `.wav`)
- 🔎 Transkripsi ucapan ke teks menggunakan **Google Speech Recognition**
- 💬 Tampilkan hasil transkripsi dan simpan ke file `.txt`

---

## 📦 Instalasi

### 1. Clone Repository & Buat Virtual Environment (Opsional tapi disarankan)

```bash
[git clone https://github.com/username/nama-repo-kamu.git](https://github.com/Tazidi/text-speech-hub.git)
cd text-speech-hub
python -m venv env
# Aktifkan virtual environment:
# Windows
env\Scripts\activate
```

### 2. Install Libraries yang Diperlukan

Sebelum menjalankan aplikasi, pastikan kamu menginstal semua pustaka Python yang digunakan dalam proyek ini. Jalankan perintah berikut:

```bash
pip install streamlit google-cloud-texttospeech pydub SpeechRecognition python-docx pymupdf requests beautifulsoup4
```

Tentu! Berikut adalah **lanjutan panduan installasi FFmpeg di GitHub README** kamu dengan **format yang sama** seperti sebelumnya:

---

### 3. Install FFmpeg (Wajib untuk Audio Processing)

Aplikasi ini menggunakan pustaka `pydub`, yang memerlukan **FFmpeg** untuk memproses file audio seperti `.mp3` dan `.wav`.

#### 🪟 Windows

1. Unduh FFmpeg dari [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)
2. Pilih versi **"Release full"**, lalu ekstrak ke lokasi seperti: `C:\ffmpeg`
3. Tambahkan path berikut ke **Environment Variables**:

   ```
   C:\ffmpeg\bin
   ```
4. Cek apakah sudah berhasil dengan mengetik di Command Prompt:

   ```bash
   ffmpeg -version
   ```

### 4. Jalankan Aplikasi

Setelah semua dependensi dan FFmpeg terpasang, jalankan aplikasi dengan perintah berikut:

```bash
streamlit run 152022027_152022047_152022261.py
```

> Gantilah `152022027_152022047_152022261.py` dengan nama file utama Python kamu, misalnya `app.py`, `main.py`, atau `tts_app.py`.

---


