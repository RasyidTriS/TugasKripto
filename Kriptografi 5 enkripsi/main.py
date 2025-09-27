import streamlit as st
from caesar_cipher import CaesarCipher
from vigenere_cipher import VigenereCipher
from modern_ciphers import ModernCipher1, ModernCipher2
from super_encryption import SuperEncryption

# Konfigurasi halaman - ini buat set judul dan icon
st.set_page_config(
    page_title="KriptoGrafi Kelompok 11",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inisialisasi instance cipher - bikin objek untuk setiap algoritma
caesar = CaesarCipher()
vigenere = VigenereCipher()
modern1 = ModernCipher1()
modern2 = ModernCipher2()
super_encryption = SuperEncryption()

# Judul utama aplikasi
st.title("🔐 Aplikasi Enkripsi dan Dekripsi")
st.markdown("Praktik dengan algoritma enkripsi tradisional dan modern!")

# Buat tab-tab - ini buat navigasi antar algoritma
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Caesar Cipher", 
    "Vigenère Cipher", 
    "Stream Cipher (XOR + FSR)", 
    "Block Cipher (SPN)", 
    "Super Encryption"
])

# Tab Caesar Cipher - algoritma paling sederhana
with tab1:
    st.header("Caesar Cipher")
    st.markdown("Cipher substitusi dimana setiap huruf digeser dengan jumlah posisi yang tetap.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Encryption")
        caesar_plaintext = st.text_area("Masukkan text yang mau di-encrypt:", height=100, key="caesar_plaintext")
        caesar_shift = st.slider("Nilai shift:", 0, 25, 3, key="caesar_shift")
        
        if st.button("Encrypt", key="caesar_encrypt_btn"):
            if caesar_plaintext:
                caesar_encrypted = caesar.encrypt(caesar_plaintext, caesar_shift)
                st.success("Text ter-encrypt:")
                st.code(caesar_encrypted)
            else:
                st.warning("Masukkan text dulu.")
    
    with col2:
        st.subheader("Decryption")
        caesar_ciphertext = st.text_area("Masukkan text yang mau di-decrypt:", height=100, key="caesar_ciphertext")
        caesar_decrypt_shift = st.slider("Nilai shift:", 0, 25, 3, key="caesar_decrypt_shift")
        
        if st.button("Decrypt", key="caesar_decrypt_btn"):
            if caesar_ciphertext:
                caesar_decrypted = caesar.decrypt(caesar_ciphertext, caesar_decrypt_shift)
                st.success("Text ter-decrypt:")
                st.code(caesar_decrypted)
            else:
                st.warning("Masukkan text dulu.")
    
    # Brute force attack - coba semua kemungkinan shift
    st.subheader("Brute Force Attack")
    caesar_brute_text = st.text_input("Masukkan encrypted text untuk brute force attack:", key="caesar_brute_text")
    
    if st.button("Brute Force Decrypt", key="caesar_brute_btn"):
        if caesar_brute_text:
            brute_results = caesar.brute_force_decrypt(caesar_brute_text)
            st.success("Semua kemungkinan decrypt:")
            for shift, decrypted in brute_results:
                st.text(f"Shift {shift:2d}: {decrypted}")
        else:
            st.warning("Masukkan text dulu.")

# Tab Vigenère Cipher - lebih aman dari Caesar
with tab2:
    st.header("Vigenère Cipher")
    st.markdown("Cipher substitusi polyalphabetic yang pakai keyword buat tentuin shift-nya.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Encryption")
        vigenere_plaintext = st.text_area("Masukkan text yang mau di-encrypt:", height=100, key="vigenere_plaintext")
        vigenere_key = st.text_input("Masukkan encryption key:", key="vigenere_key")
        
        if st.button("Encrypt", key="vigenere_encrypt_btn"):
            if vigenere_plaintext and vigenere_key:
                vigenere_encrypted = vigenere.encrypt(vigenere_plaintext, vigenere_key)
                st.success("Text ter-encrypt:")
                st.code(vigenere_encrypted)
            else:
                st.warning("Masukkan text dan key dulu.")
    
    with col2:
        st.subheader("Decryption")
        vigenere_ciphertext = st.text_area("Masukkan text yang mau di-decrypt:", height=100, key="vigenere_ciphertext")
        vigenere_decrypt_key = st.text_input("Masukkan decryption key:", key="vigenere_decrypt_key")
        
        if st.button("Decrypt", key="vigenere_decrypt_btn"):
            if vigenere_ciphertext and vigenere_decrypt_key:
                vigenere_decrypted = vigenere.decrypt(vigenere_ciphertext, vigenere_decrypt_key)
                st.success("Text ter-decrypt:")
                st.code(vigenere_decrypted)
            else:
                st.warning("Masukkan text dan key dulu.")
    
    # # Frequency analysis attack - ini di-comment karena ga dipake
    # st.subheader("Frequency Analysis Attack")
    # vigenere_freq_text = st.text_input("Enter encrypted text for frequency analysis:", key="vigenere_freq_text")
    
    # if st.button("Analyze Frequency", key="vigenere_freq_btn"):
    #     if vigenere_freq_text:
    #         freq_result = vigenere.frequency_analysis_attack(vigenere_freq_text)
    #         st.success(freq_result)
    #     else:
    #         st.warning("Please enter text for frequency analysis.")

# Tab Modern Cipher 1 - Stream Cipher dengan FSR
with tab3:
    st.header("Stream Cipher (XOR + FSR)")
    st.markdown("Stream cipher yang pakai operasi XOR dengan Feedback Shift Register (FSR) buat generate keystream.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Encryption")
        modern1_plaintext = st.text_area("Masukkan text yang mau di-encrypt:", height=100, key="modern1_plaintext")
        modern1_key = st.text_input("Masukkan encryption key (FSR seed):", key="modern1_key")
        
        if st.button("Encrypt", key="modern1_encrypt_btn"):
            if modern1_plaintext and modern1_key:
                modern1_encrypted = modern1.encrypt(modern1_plaintext, modern1_key)
                st.success("Encrypted text (Binary):")
                st.code(modern1_encrypted)
                
                # Tampilkan keystream yang dipake
                keystream = modern1.get_keystream(modern1_key, len(modern1_encrypted))
                st.info(f"Keystream yang dipake: {keystream[:50]}{'...' if len(keystream) > 50 else ''}")
            else:
                st.warning("Masukkan text dan key dulu.")
    
    with col2:
        st.subheader("Decryption")
        modern1_ciphertext = st.text_area("Masukkan binary text yang mau di-decrypt:", height=100, key="modern1_ciphertext")
        modern1_decrypt_key = st.text_input("Masukkan decryption key (FSR seed):", key="modern1_decrypt_key")
        
        if st.button("Decrypt", key="modern1_decrypt_btn"):
            if modern1_ciphertext and modern1_decrypt_key:
                modern1_decrypted = modern1.decrypt(modern1_ciphertext, modern1_decrypt_key)
                st.success("Decrypted text:")
                st.code(modern1_decrypted)
            else:
                st.warning("Masukkan binary text dan key dulu.")
    
    # Section analisis FSR keystream
    st.subheader("FSR Keystream Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        analysis_key_stream = st.text_input("Masukkan key untuk analisis:", key="analysis_key_stream")
        analysis_length = st.slider("Panjang keystream:", 50, 500, 100, key="analysis_length")
        
        if st.button("Analisis Keystream", key="analyze_btn"):
            if analysis_key_stream:
                analysis = modern1.analyze_keystream(analysis_key_stream, analysis_length)
                st.success("Hasil Analisis Keystream:")
                st.json(analysis)
            else:
                st.warning("Masukkan key dulu.")
    
    with col2:
        st.subheader("FSR Properties")
        st.markdown("""
        **Feedback Shift Register (FSR) Features:**
        - Pakai taps di posisi 0, 2, 3, 5
        - Generate pseudo-random keystream
        - Operasi XOR buat encrypt/decrypt
        - Key yang sama dipake buat encrypt dan decrypt
        """)
        
        # Tampilkan proses generate keystream
        if analysis_key_stream:
            keystream_sample = modern1.get_keystream(analysis_key_stream, 32)
            st.info(f"Keystream sample (32 bits): {keystream_sample}")
    
    # Informasi edukasi - ini buat jelasin gimana cara kerjanya
    with st.expander("Gimana Stream Cipher dengan FSR Bekerja"):
        st.markdown("""
        **Proses Stream Cipher:**
        1. **Text to Binary**: Convert input text jadi binary
        2. **FSR Keystream**: Generate pseudo-random keystream pakai FSR
        3. **XOR Operation**: Lakukan bitwise XOR antara text dan keystream
        4. **Result**: Encrypted binary output
        
        **FSR Keystream Generation:**
        - Pakai key sebagai initial seed
        - Shift bits ke kanan dan hitung feedback
        - Feedback adalah XOR dari tap positions tertentu
        - Output satu bit per iterasi
        
        **Security Features:**
        - Keystream yang sama dipake buat encrypt dan decrypt
        - Key menentukan seluruh sequence keystream
        - Operasi XOR bisa dibalik
        """)

# Modern Cipher 2 Tab
with tab4:
    st.header("Block Cipher (SPN)")
    st.markdown("Block cipher menggunakan substitusi-permutasi network dengan Feistel structure.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Encryption")
        modern2_plaintext = st.text_area("Masukkan text yang mau di-encrypt:", height=100, key="modern2_plaintext")
        modern2_key = st.text_input("Masukkan encryption key:", key="modern2_key")
        
        if st.button("Encrypt", key="modern2_encrypt_btn"):
            if modern2_plaintext and modern2_key:
                modern2_encrypted = modern2.encrypt(modern2_plaintext, modern2_key)
                st.success("Encrypted text (Binary):")
                st.code(modern2_encrypted)
                
                # Tampilkan analisis block structure
                analysis = modern2.analyze_block_structure(modern2_plaintext, modern2_key)
                st.info(f"Jumlah block: {analysis['number_of_blocks']}, Block size: {analysis['block_size']} bit")
            else:
                st.warning("Masukkan text dan key dulu.")
    
    with col2:
        st.subheader("Decryption")
        modern2_ciphertext = st.text_area("Masukkan binary text yang mau di-decrypt:", height=100, key="modern2_ciphertext")
        modern2_decrypt_key = st.text_input("Masukkan decryption key:", key="modern2_decrypt_key")
        
        if st.button("Decrypt", key="modern2_decrypt_btn"):
            if modern2_ciphertext and modern2_decrypt_key:
                modern2_decrypted = modern2.decrypt(modern2_ciphertext, modern2_decrypt_key)
                st.success("Decrypted text:")
                st.code(modern2_decrypted)
            else:
                st.warning("Masukkan binary text dan key dulu.")
    
    # Block Cipher Analysis Section
    st.subheader("Block Cipher Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        analysis_text = st.text_input("Masukkan text untuk analisis:", key="analysis_text")
        analysis_key_block = st.text_input("Masukkan key untuk analisis:", key="analysis_key_block")
        
        if st.button("Analisis Block Structure", key="analyze_block_btn"):
            if analysis_text and analysis_key_block:
                analysis = modern2.analyze_block_structure(analysis_text, analysis_key_block)
                st.success("Hasil Analisis Block Cipher:")
                st.json(analysis)
            else:
                st.warning("Masukkan text dan key dulu.")
        
        # Test button buat debug
        if st.button("Test Encrypt/Decrypt", key="test_block_btn"):
            if analysis_text and analysis_key_block:
                test_result = modern2.test_encrypt_decrypt(analysis_text, analysis_key_block)
                st.success("Hasil Test Encrypt/Decrypt:")
                st.json(test_result)
                
                if test_result["success"]:
                    st.success("✅ Encrypt/Decrypt berhasil!")
                else:
                    st.error("❌ Encrypt/Decrypt gagal!")
            else:
                st.warning("Masukkan text dan key dulu.")
    
    with col2:
        st.subheader("Block Cipher Properties")
        st.markdown("""
        **Substitusi-Permutasi Network:**
        - S-box untuk substitusi
        - P-box untuk permutasi
        - Feistel network structure
        - 4 rounds encryption
        """)
        
        # Tampilkan round keys
        if analysis_key_block:
            round_keys = modern2._generate_round_keys(analysis_key_block, 4)
            st.info("Round Keys:")
            for i, key in enumerate(round_keys):
                st.text(f"Round {i+1}: {key}")
    
    # Educational Information
    with st.expander("Gimana Block Cipher Bekerja"):
        st.markdown("""
        **Proses Block Cipher:**
        1. **Text to Binary**: Convert text jadi binary
        2. **Padding**: Tambah padding biar kelipatan block size
        3. **Block Processing**: Bagi jadi block-block 8-bit
        4. **Feistel Rounds**: 4 round substitusi-permutasi
        5. **Result**: Encrypted binary output
        
        **Feistel Network:**
        - Bagi block jadi left dan right
        - F function: S-box + P-box + XOR key
        - new_left = right, new_right = left XOR F(right)
        - Round keys berbeda untuk setiap round
        
        **Security Features:**
        - Substitusi membuat confusion
        - Permutasi membuat diffusion
        - Multiple rounds meningkatkan security
        """)

# Tab Super Encryption - gabungin semua algoritma
with tab5:
    st.header("Super Encryption")
    st.markdown("Gabungin semua 4 algoritma enkripsi secara berurutan buat keamanan maksimal.")
    
    # Section input
    st.subheader("Input")
    super_plaintext = st.text_area("Masukkan text yang mau di-encrypt:", height=100, key="super_plaintext")
    
    # Input key-key untuk setiap algoritma
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.subheader("Caesar Cipher")
        caesar_shift_super = st.slider("Nilai shift:", 0, 25, 3, key="caesar_shift_super")
    
    with col2:
        st.subheader("Vigenère Cipher")
        vigenere_key_super = st.text_input("Key:", key="vigenere_key_super")
    
    with col3:
        st.subheader("Stream Cipher")
        modern1_key_super = st.text_input("Key:", key="modern1_key_super")
    
    with col4:
        st.subheader("Block Cipher")
        modern2_key_super = st.text_input("Key:", key="modern2_key_super")
    
    # Tombol encrypt/decrypt
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Super Encrypt", key="super_encrypt_btn"):
            if super_plaintext:
                super_encrypted = super_encryption.encrypt(
                    super_plaintext, 
                    caesar_shift_super, 
                    vigenere_key_super, 
                    modern1_key_super, 
                    modern2_key_super
                )
                st.success("Super Encrypted text:")
                st.code(super_encrypted)
                
                # Tampilkan langkah-langkah enkripsi
                st.subheader("Langkah-langkah Enkripsi")
                steps = super_encryption.get_encryption_steps(
                    super_plaintext, 
                    caesar_shift_super, 
                    vigenere_key_super, 
                    modern1_key_super, 
                    modern2_key_super
                )
                for step_name, step_text in steps.items():
                    st.text(f"{step_name}: {step_text}")
            else:
                st.warning("Masukkan text dulu.")
    
    with col2:
        super_ciphertext = st.text_area("Masukkan text yang mau di-decrypt:", height=100, key="super_ciphertext")
        
        if st.button("Super Decrypt", key="super_decrypt_btn"):
            if super_ciphertext:
                super_decrypted = super_encryption.decrypt(
                    super_ciphertext, 
                    caesar_shift_super, 
                    vigenere_key_super, 
                    modern1_key_super, 
                    modern2_key_super
                )
                st.success("Super Decrypted text:")
                st.code(super_decrypted)
                
                # Tampilkan langkah-langkah dekripsi
                st.subheader("Langkah-langkah Dekripsi")
                steps = super_encryption.get_decryption_steps(
                    super_ciphertext, 
                    caesar_shift_super, 
                    vigenere_key_super, 
                    modern1_key_super, 
                    modern2_key_super
                )
                for step_name, step_text in steps.items():
                    st.text(f"{step_name}: {step_text}")
            else:
                st.warning("Masukkan text dulu.")

# Informasi sidebar - ini buat navigasi dan info tambahan
with st.sidebar:
    st.header("Daftar Algoritma")
    st.markdown("""
    
    **Algoritma Traditional:**
    - Caesar Cipher
    - Vigenère Cipher
    
    **Algoritma Modern:**
    - Stream Cipher (XOR + FSR)
    - Block Cipher (SPN)
    
    **Super Enkripsi:**
    - Gabungin semua algoritma di atas
    """)
    
    st.header("Fitur Stream Cipher")
    st.markdown("""
    **FSR Keystream Generator:**
    - Feedback Shift Register
    - Operasi XOR
    - Binary encryption
    - Analisis keystream
    """)
    
    st.header("Fitur Block Cipher")
    st.markdown("""
    **Substitusi-Permutasi Network:**
    - S-box dan P-box
    - Feistel network
    - 4 rounds encryption
    - Block processing
    """)

# Footer - ini di bawah halaman
st.markdown("---")
st.markdown("🔐 **Aplikasi Enkripsi dan Dekripsi Kelompok 11** - Dibuat dengan Streamlit")