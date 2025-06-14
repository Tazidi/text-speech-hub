import streamlit as st
from google.cloud import texttospeech
from pydub import AudioSegment
from io import BytesIO
import tempfile
import os
from datetime import datetime
import base64
import speech_recognition as sr
from docx import Document
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup

# ========== Konfigurasi Google Cloud ==========
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ttscc.json"

# ====== Konfigurasi Halaman ======
st.set_page_config(page_title="Text to Speech & Speech to Text", page_icon="🎧", layout="centered")

# ====== Styling UI Sederhana ======
st.markdown("""
    <style>
    body {
        background-color: #f7f9fc;
        font-family: 'Segoe UI', sans-serif;
    }
    textarea, .stTextInput>div>div>input {
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ====== Inisialisasi Riwayat ======
if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

# ====== Header ======
st.title("🎧 Text ↔ Speech Converter")
st.markdown("Konversi **teks ke suara** dan **suara ke teks** dalam bahasa Indonesia/Inggris dengan pengaturan kecepatan, volume, dan gender suara.")

tab1, tab2 = st.tabs(["🗣️ Text to Speech", "🎤 Speech to Text"])

# ========== TAB 1: TEXT TO SPEECH ==========
with tab1:
    uploaded_file = st.file_uploader("📂 Upload File (.txt, .docx, .pdf) [Opsional]", type=["txt", "docx", "pdf"])
    initial_text = ""

    def extract_text_from_file(uploaded_file):
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext == ".txt":
            return uploaded_file.read().decode("utf-8")
        elif ext == ".docx":
            doc = Document(uploaded_file)
            return "\n".join([para.text for para in doc.paragraphs])
        elif ext == ".pdf":
            text = ""
            with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text()
            return text
        return ""

    # Ekstrak teks dari file jika ada
    if uploaded_file is not None:
        initial_text = extract_text_from_file(uploaded_file)
        st.caption(f"📄 Teks dari file: `{uploaded_file.name}` berhasil dimuat.")
    
    st.markdown("### 🌐 Ambil Teks dari Website (Opsional)")
    url_input = st.text_input("Masukkan URL Website (berita, artikel, dsb)", placeholder="https://contoh.com/artikel")

    if url_input:
        try:
            response = requests.get(url_input, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Gabungkan semua <p> tag sebagai isi artikel
            paragraphs = soup.find_all('p')
            website_text = "\n".join([p.get_text() for p in paragraphs if p.get_text().strip() != ""])

            if website_text.strip():
                initial_text = website_text.strip()
                st.success("✅ Teks dari website berhasil dimuat ke kotak teks.")
            else:
                st.warning("⚠️ Tidak ditemukan isi teks yang relevan dari URL.")
        except Exception as e:
            st.error(f"❌ Gagal mengambil data dari URL: {e}")

    teks = st.text_area("📝 Masukkan Teks", value=initial_text, height=150)
    bahasa = st.selectbox("🌐 Pilih Bahasa", options=[("Indonesia", "id-ID"), ("English", "en-US")], format_func=lambda x: x[0])
    gender = st.selectbox("👤 Pilih Gender Suara", ["Perempuan", "Laki-laki"])
    kecepatan = st.selectbox("⚡ Kecepatan Suara", ["Normal", "Cepat", "Lambat"])
    volume_db = st.slider("🔊 Volume Output (dB)", min_value=-20, max_value=10, value=0)

    gender_map = {
        "Perempuan": texttospeech.SsmlVoiceGender.FEMALE,
        "Laki-laki": texttospeech.SsmlVoiceGender.MALE
    }

    rate_map = {
        "Normal": 1.0,
        "Cepat": 1.3,
        "Lambat": 0.7
    }

    if st.button("🎙️ Konversi Sekarang"):
        if not teks.strip():
            st.warning("❗ Teks tidak boleh kosong.")
        elif len(teks.encode('utf-8')) > 5000:
            st.error("❗ Teks terlalu panjang untuk dikonversi (maksimal 5000 karakter). Silakan potong teks menjadi bagian yang lebih kecil.")
        else:
            st.info("⏳ Sedang mengonversi...")

            try:
                client = texttospeech.TextToSpeechClient()

                input_text = texttospeech.SynthesisInput(text=teks)

                voice = texttospeech.VoiceSelectionParams(
                    language_code=bahasa[1],
                    ssml_gender=gender_map[gender]
                )

                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3,
                    speaking_rate=rate_map[kecepatan]
                )

                response = client.synthesize_speech(
                    input=input_text,
                    voice=voice,
                    audio_config=audio_config
                )

                audio = AudioSegment.from_file(BytesIO(response.audio_content), format="mp3")
                audio += volume_db

                buffer = BytesIO()
                audio.export(buffer, format="mp3")
                buffer.seek(0)

                audio_base64 = base64.b64encode(buffer.getvalue()).decode()
                audio_html = f"""
                <audio controls>
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                    Your browser does not support the audio element.
                </audio>
                """
                st.markdown(audio_html, unsafe_allow_html=True)

                now = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"tts_output_{now}.mp3"
                st.download_button("⬇️ Unduh Audio", data=buffer, file_name=filename, mime="audio/mp3")

                st.session_state.riwayat.append({"teks": teks, "waktu": now})
                st.success(f"✅ Konversi selesai! File `{filename}` siap diunduh.")
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan saat mengonversi: {e}")

    with st.expander("📜 Riwayat Pembacaan (5 Terakhir)"):
        if st.session_state.riwayat:
            for item in reversed(st.session_state.riwayat[-5:]):
                st.markdown(f"🕒 `{item['waktu']}` - {item['teks'][:80]}{'...' if len(item['teks']) > 80 else ''}")
        else:
            st.info("Belum ada riwayat pembacaan.")

# ========== TAB 2: SPEECH TO TEXT ==========
with tab2:
    recognizer = sr.Recognizer()
    input_mode = st.radio("Pilih Sumber Audio", ["🎙️ Mikrofon", "📁 Upload File Audio (.wav/.mp3)"])
    st.markdown("Bahasa pengenalan ucapan akan mengikuti pilihan di tab pertama.")

    recognized_text = ""

    if input_mode == "🎙️ Mikrofon":
        st.info("Tekan tombol di bawah untuk mulai merekam dari mikrofon.")
        if st.button("🎧 Mulai Rekaman"):
            try:
                with sr.Microphone() as source:
                    st.info("Silakan bicara... (maks. 5 detik)")
                    audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                    st.success("✅ Rekaman selesai, sedang memproses...")

                    recognized_text = recognizer.recognize_google(audio_data, language=bahasa[1])
                    st.text_area("📝 Hasil Transkripsi", recognized_text, height=100)

            except sr.WaitTimeoutError:
                st.error("❗ Waktu habis. Tidak ada suara terdeteksi. Coba lagi dan pastikan mikrofon aktif.")
            except sr.UnknownValueError:
                st.error("❌ Tidak bisa mengenali ucapan.")
            except sr.RequestError as e:
                st.error(f"❌ Terjadi kesalahan saat mengakses API: {e}")
            except Exception as e:
                st.error(f"❌ Mikrofon tidak tersedia atau ada masalah lain: {e}")

    elif input_mode == "📁 Upload File Audio (.wav/.mp3)":
        audio_file = st.file_uploader("Upload File Audio", type=["wav", "mp3"])
        if audio_file is not None:
            # Simpan file audio sementara
            audio_ext = os.path.splitext(audio_file.name)[1].lower()
            audio_bytes = audio_file.read()

            with tempfile.NamedTemporaryFile(delete=False, suffix=audio_ext) as tmp_in:
                tmp_in.write(audio_bytes)
                tmp_in_path = tmp_in.name

            # Konversi ke .wav jika diperlukan
            audio_wav_path = tmp_in_path
            if audio_ext != ".wav":
                sound = AudioSegment.from_file(tmp_in_path)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
                    sound.export(tmp_wav.name, format="wav")
                    audio_wav_path = tmp_wav.name

            # Transkripsi menggunakan SpeechRecognition
            with sr.AudioFile(audio_wav_path) as source:
                audio_data = recognizer.record(source)
                try:
                    recognized_text = recognizer.recognize_google(audio_data, language=bahasa[1])
                    st.text_area("📝 Hasil Transkripsi", recognized_text, height=100)
                except sr.UnknownValueError:
                    st.error("❌ Tidak bisa mengenali ucapan.")
                except sr.RequestError as e:
                    st.error(f"❌ Terjadi kesalahan: {e}")

            st.markdown("🔊 **Putar Audio**")
            st.audio(audio_bytes, format="audio/" + audio_ext.strip("."))

            # Tombol unduh hasil transkripsi jika tersedia
            if recognized_text:
                txt_buffer = BytesIO()
                txt_buffer.write(recognized_text.encode("utf-8"))
                txt_buffer.seek(0)
                filename_txt = f"transkripsi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                st.download_button("💾 Simpan sebagai .txt", data=txt_buffer, file_name=filename_txt, mime="text/plain")

            # Bersihkan file sementara
            os.remove(tmp_in_path)
            if audio_ext != ".wav":
                os.remove(audio_wav_path)