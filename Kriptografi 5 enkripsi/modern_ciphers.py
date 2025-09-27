class ModernCipher1:
    """
    Stream Cipher using XOR with Feedback Shift Register (FSR) keystream generator.
    This implements a stream cipher where the keystream is generated using FSR.
    """
    
    def __init__(self):
        self.name = "Stream Cipher (XOR + FSR)"
        self.description = "Stream cipher using XOR operation with FSR keystream generator"
    
    def _text_to_binary(self, text):
        """
        Convert text to binary string.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Binary representation
        """
        binary = ""
        for char in text:
            # Convert character to 8-bit binary
            binary += format(ord(char), '08b')
        return binary
    
    def _binary_to_text(self, binary):
        """
        Convert binary string to text.
        
        Args:
            binary (str): Binary string (must be multiple of 8)
            
        Returns:
            str: Converted text
        """
        text = ""
        for i in range(0, len(binary), 8):
            if i + 8 <= len(binary):
                byte = binary[i:i+8]
                char_code = int(byte, 2)
                if 32 <= char_code <= 126:  # Printable ASCII range
                    text += chr(char_code)
                else:
                    text += '?'  # Replace non-printable characters
        return text
    
    def _fsr_keystream_generator(self, seed, length):
        """
        Generate keystream using Feedback Shift Register (FSR).
        
        Args:
            seed (str): Initial seed for FSR
            length (int): Length of keystream to generate
            
        Returns:
            str: Generated keystream
        """
        if not seed:
            return "0" * length
        
        # Convert seed to binary if it's text
        if len(seed) > 0 and ord(seed[0]) > 1:  # If it's text, not binary
            seed_binary = self._text_to_binary(seed)
        else:
            seed_binary = seed
        
        # Ensure seed is at least 8 bits
        if len(seed_binary) < 8:
            seed_binary = seed_binary.ljust(8, '0')
        
        # Initialize FSR with seed
        fsr = list(seed_binary)
        keystream = ""
        
        for _ in range(length):
            # Extract output bit (rightmost bit)
            output_bit = fsr[-1]
            keystream += output_bit
            
            # Calculate feedback (XOR of specific positions)
            # Using taps at positions 0, 2, 3, 5 (common LFSR configuration)
            feedback = int(fsr[0]) ^ int(fsr[2]) ^ int(fsr[3]) ^ int(fsr[5])
            
            # Shift right and insert feedback at the beginning
            fsr = [str(feedback)] + fsr[:-1]
        
        return keystream
    
    def _xor_operation(self, text_binary, keystream):
        """
        Perform XOR operation between text and keystream.
        
        Args:
            text_binary (str): Binary representation of text
            keystream (str): Binary keystream
            
        Returns:
            str: Result of XOR operation
        """
        result = ""
        min_length = min(len(text_binary), len(keystream))
        
        for i in range(min_length):
            result += str(int(text_binary[i]) ^ int(keystream[i]))
        
        # Pad with remaining text if keystream is shorter
        if len(text_binary) > len(keystream):
            result += text_binary[len(keystream):]
        
        return result
    
    def encrypt(self, plaintext, key):
        """
        Encrypt plaintext using Stream Cipher with FSR.
        
        Args:
            plaintext (str): Text to encrypt
            key (str): Encryption key (used as FSR seed)
            
        Returns:
            str: Encrypted text (in binary format)
        """
        if not plaintext:
            return ""
        
        # Convert plaintext to binary
        plaintext_binary = self._text_to_binary(plaintext)
        
        # Generate keystream using FSR
        keystream = self._fsr_keystream_generator(key, len(plaintext_binary))
        
        # Perform XOR operation
        ciphertext_binary = self._xor_operation(plaintext_binary, keystream)
        
        return ciphertext_binary
    
    def decrypt(self, ciphertext, key):
        """
        Decrypt ciphertext using Stream Cipher with FSR.
        
        Args:
            ciphertext (str): Encrypted text (in binary format)
            key (str): Decryption key (used as FSR seed)
            
        Returns:
            str: Decrypted text
        """
        if not ciphertext:
            return ""
        
        # Generate keystream using FSR
        keystream = self._fsr_keystream_generator(key, len(ciphertext))
        
        # Perform XOR operation (same as encryption for stream cipher)
        plaintext_binary = self._xor_operation(ciphertext, keystream)
        
        # Convert binary back to text
        plaintext = self._binary_to_text(plaintext_binary)
        
        return plaintext
    
    def get_keystream(self, key, length):
        """
        Get the keystream generated by FSR for demonstration.
        
        Args:
            key (str): FSR seed
            length (int): Length of keystream
            
        Returns:
            str: Generated keystream
        """
        return self._fsr_keystream_generator(key, length)
    
    def analyze_keystream(self, key, length=100):
        """
        Analyze the keystream properties for educational purposes.
        
        Args:
            key (str): FSR seed
            length (int): Length of keystream to analyze
            
        Returns:
            dict: Analysis results
        """
        keystream = self._fsr_keystream_generator(key, length)
        
        # Count 0s and 1s
        zeros = keystream.count('0')
        ones = keystream.count('1')
        
        # Calculate frequency
        zero_freq = zeros / length if length > 0 else 0
        one_freq = ones / length if length > 0 else 0
        
        # Check for patterns (simple analysis)
        pattern_analysis = {
            "total_bits": length,
            "zeros": zeros,
            "ones": ones,
            "zero_frequency": round(zero_freq, 4),
            "one_frequency": round(one_freq, 4),
            "balance": "Good" if 0.4 <= zero_freq <= 0.6 else "Poor",
            "keystream_sample": keystream[:50] + "..." if len(keystream) > 50 else keystream
        }
        
        return pattern_analysis


class ModernCipher2:
    """
    Block Cipher implementation using substitution-permutation network.
    Ini adalah block cipher sederhana yang pakai substitusi dan permutasi.
    """
    
    def __init__(self):
        self.name = "Block Cipher (SPN)"
        self.description = "Block cipher menggunakan substitusi-permutasi network"
        self.block_size = 8  # ukuran block dalam bit
    
    def _text_to_binary(self, text):
        """
        Ubah text jadi binary string.
        Ini fungsi helper buat convert text ke binary.
        
        Args:
            text (str): Text yang mau diubah
            
        Returns:
            str: Binary representation
        """
        binary = ""
        for char in text:
            # convert setiap karakter jadi 8-bit binary
            binary += format(ord(char), '08b')
        return binary
    
    def _binary_to_text(self, binary):
        """
        Ubah binary string jadi text.
        Ini kebalikan dari fungsi di atas.
        
        Args:
            binary (str): Binary string (harus kelipatan 8)
            
        Returns:
            str: Text hasil convert
        """
        text = ""
        for i in range(0, len(binary), 8):
            if i + 8 <= len(binary):
                byte = binary[i:i+8]
                char_code = int(byte, 2)
                if 32 <= char_code <= 126:  # range ASCII yang bisa diprint
                    text += chr(char_code)
                else:
                    text += '?'  # ganti karakter yang ga bisa diprint
        return text
    
    def _pad_text(self, text, block_size):
        """
        Tambah padding ke text biar panjangnya kelipatan block_size.
        Ini penting banget buat block cipher.
        
        Args:
            text (str): Text yang mau di-pad
            block_size (int): Ukuran block
            
        Returns:
            str: Text yang sudah di-pad
        """
        # hitung berapa bit yang kurang
        remainder = len(text) % block_size
        if remainder != 0:
            # tambah padding dengan '0' sebanyak yang kurang
            padding_needed = block_size - remainder
            text += '0' * padding_needed
        return text
    
    def _remove_padding(self, text):
        """
        Hapus padding dari text.
        Ini buat pas decrypt, biar hasilnya bersih.
        
        Args:
            text (str): Text yang ada padding-nya
            
        Returns:
            str: Text tanpa padding
        """
        # hapus '0' di akhir, tapi hati-hati jangan hapus '0' yang asli
        # cuma hapus padding yang ditambah di encrypt
        if text.endswith('0'):
            # cek berapa banyak '0' di akhir
            padding_count = 0
            for i in range(len(text) - 1, -1, -1):
                if text[i] == '0':
                    padding_count += 1
                else:
                    break
            
            # hapus maksimal 7 '0' (karena block size 8, padding max 7)
            if padding_count <= 7:
                return text.rstrip('0')
        
        return text
    
    def _substitution_box(self, block):
        """
        S-box untuk substitusi.
        Ini ganti setiap 4-bit dengan 4-bit lain sesuai tabel.
        
        Args:
            block (str): Block 8-bit yang mau di-substitute
            
        Returns:
            str: Block hasil substitusi
        """
        # S-box sederhana (4-bit input, 4-bit output)
        sbox = {
            '0000': '1110', '0001': '0100', '0010': '1101', '0011': '0001',
            '0100': '0010', '0101': '1111', '0110': '1011', '0111': '1000',
            '1000': '0011', '1001': '1010', '1010': '0110', '1011': '1100',
            '1100': '0101', '1101': '1001', '1110': '0000', '1111': '0111'
        }
        
        # bagi block jadi 2 bagian 4-bit
        left_half = block[:4]
        right_half = block[4:]
        
        # substitusi pakai S-box
        substituted_left = sbox.get(left_half, left_half)
        substituted_right = sbox.get(right_half, right_half)
        
        return substituted_left + substituted_right
    
    def _inverse_substitution_box(self, block):
        """
        Inverse S-box buat decrypt.
        Ini kebalikan dari S-box di atas.
        
        Args:
            block (str): Block yang mau di-inverse substitute
            
        Returns:
            str: Block hasil inverse substitusi
        """
        # Inverse S-box (kebalikan dari S-box)
        inverse_sbox = {
            '1110': '0000', '0100': '0001', '1101': '0010', '0001': '0011',
            '0010': '0100', '1111': '0101', '1011': '0110', '1000': '0111',
            '0011': '1000', '1010': '1001', '0110': '1010', '1100': '1011',
            '0101': '1100', '1001': '1101', '0000': '1110', '0111': '1111'
        }
        
        # bagi block jadi 2 bagian 4-bit
        left_half = block[:4]
        right_half = block[4:]
        
        # inverse substitusi pakai inverse S-box
        inverse_left = inverse_sbox.get(left_half, left_half)
        inverse_right = inverse_sbox.get(right_half, right_half)
        
        return inverse_left + inverse_right
    
    def _permutation_box(self, block):
        """
        P-box untuk permutasi.
        Ini acak-acak posisi bit dalam block.
        
        Args:
            block (str): Block 8-bit yang mau di-permute
            
        Returns:
            str: Block hasil permutasi
        """
        # P-box sederhana (8-bit input, 8-bit output)
        # posisi bit baru: [7,3,1,5,0,4,2,6] (dari posisi lama)
        pbox = [7, 3, 1, 5, 0, 4, 2, 6]
        
        # pastikan block panjangnya 8 bit
        if len(block) < 8:
            block = block.ljust(8, '0')  # tambah '0' di kanan kalau kurang
        elif len(block) > 8:
            block = block[:8]  # potong kalau lebih dari 8
        
        result = ""
        for pos in pbox:
            if pos < len(block):  # cek dulu posisi ada atau ga
                result += block[pos]
            else:
                result += '0'  # default ke '0' kalau posisi ga ada
        
        return result
    
    def _inverse_permutation_box(self, block):
        """
        Inverse P-box buat decrypt.
        Ini kebalikan dari P-box di atas.
        
        Args:
            block (str): Block yang mau di-inverse permute
            
        Returns:
            str: Block hasil inverse permutasi
        """
        # Inverse P-box (kebalikan dari P-box)
        # posisi bit lama: [4,2,6,1,5,3,7,0] (dari posisi baru)
        inverse_pbox = [4, 2, 6, 1, 5, 3, 7, 0]
        
        # pastikan block panjangnya 8 bit
        if len(block) < 8:
            block = block.ljust(8, '0')  # tambah '0' di kanan kalau kurang
        elif len(block) > 8:
            block = block[:8]  # potong kalau lebih dari 8
        
        result = ""
        for pos in inverse_pbox:
            if pos < len(block):  # cek dulu posisi ada atau ga
                result += block[pos]
            else:
                result += '0'  # default ke '0' kalau posisi ga ada
        
        return result
    
    def _generate_round_keys(self, key, num_rounds):
        """
        Generate round keys dari master key.
        Ini buat setiap round punya key yang beda.
        
        Args:
            key (str): Master key
            num_rounds (int): Jumlah round
            
        Returns:
            list: List of round keys
        """
        # convert key jadi binary dulu
        key_binary = self._text_to_binary(key)
        
        # pastikan key minimal 8 bit
        if len(key_binary) < 8:
            key_binary = key_binary.ljust(8, '0')
        
        round_keys = []
        for i in range(num_rounds):
            # generate round key dengan shift dan XOR
            shifted_key = key_binary[i:] + key_binary[:i]
            round_key = ""
            for j in range(8):
                # XOR dengan posisi bit
                round_key += str(int(shifted_key[j]) ^ (i + j) % 2)
            round_keys.append(round_key)
        
        return round_keys
    
    def _feistel_round(self, left, right, round_key):
        """
        Satu round Feistel network.
        Ini inti dari block cipher, pakai Feistel structure.
        
        Args:
            left (str): Left half of block
            right (str): Right half of block
            round_key (str): Round key
            
        Returns:
            tuple: (new_left, new_right)
        """
        # F function: substitusi + permutasi + XOR dengan key
        f_result = self._substitution_box(right)
        f_result = self._permutation_box(f_result)
        
        # XOR dengan round key
        f_result_xor = ""
        for i in range(len(f_result)):
            f_result_xor += str(int(f_result[i]) ^ int(round_key[i % len(round_key)]))
        
        # pastikan f_result_xor panjangnya sama dengan left
        if len(f_result_xor) < len(left):
            f_result_xor = f_result_xor.ljust(len(left), '0')
        elif len(f_result_xor) > len(left):
            f_result_xor = f_result_xor[:len(left)]
        
        # Feistel operation: new_left = right, new_right = left XOR F(right)
        new_left = right
        new_right = ""
        for i in range(len(left)):
            new_right += str(int(left[i]) ^ int(f_result_xor[i]))
        
        return new_left, new_right
    
    def encrypt(self, plaintext, key):
        """
        Encrypt plaintext pakai Block Cipher.
        Ini fungsi utama buat encrypt.
        
        Args:
            plaintext (str): Text yang mau di-encrypt
            key (str): Encryption key
            
        Returns:
            str: Encrypted text (binary format)
        """
        if not plaintext or not key:
            return ""
        
        # convert text jadi binary
        plaintext_binary = self._text_to_binary(plaintext)
        
        # tambah padding biar kelipatan block_size
        padded_text = self._pad_text(plaintext_binary, self.block_size)
        
        # generate round keys
        num_rounds = 4  # 4 round aja, biar ga terlalu ribet
        round_keys = self._generate_round_keys(key, num_rounds)
        
        encrypted_blocks = []
        
        # proses setiap block
        for i in range(0, len(padded_text), self.block_size):
            block = padded_text[i:i + self.block_size]
            
            # pastikan block panjangnya 8 bit
            if len(block) < self.block_size:
                block = block.ljust(self.block_size, '0')
            
            # bagi jadi left dan right
            left = block[:4]
            right = block[4:]
            
            # lakukan Feistel rounds
            for round_num in range(num_rounds):
                left, right = self._feistel_round(left, right, round_keys[round_num])
            
            # gabung hasil
            encrypted_block = left + right
            encrypted_blocks.append(encrypted_block)
        
        return ''.join(encrypted_blocks)
    
    def decrypt(self, ciphertext, key):
        """
        Decrypt ciphertext pakai Block Cipher.
        Ini kebalikan dari encrypt.
        
        Args:
            ciphertext (str): Encrypted text (binary format)
            key (str): Decryption key
            
        Returns:
            str: Decrypted text
        """
        if not ciphertext or not key:
            return ""
        
        # generate round keys (sama kayak encrypt)
        num_rounds = 4
        round_keys = self._generate_round_keys(key, num_rounds)
        
        decrypted_blocks = []
        
        # proses setiap block
        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i + self.block_size]
            
            # pastikan block panjangnya 8 bit
            if len(block) < self.block_size:
                block = block.ljust(self.block_size, '0')
            
            # bagi jadi left dan right
            left = block[:4]
            right = block[4:]
            
            # lakukan Feistel rounds (dalam urutan terbalik)
            for round_num in range(num_rounds - 1, -1, -1):
                # untuk decrypt, pakai round keys dalam urutan terbalik
                # tapi Feistel round-nya sama kayak encrypt
                left, right = self._feistel_round(left, right, round_keys[round_num])
            
            # gabung hasil
            decrypted_block = left + right
            decrypted_blocks.append(decrypted_block)
        
        # gabung semua block dan convert ke text
        decrypted_binary = ''.join(decrypted_blocks)
        decrypted_text = self._binary_to_text(self._remove_padding(decrypted_binary))
        
        return decrypted_text
    
    def test_encrypt_decrypt(self, text, key):
        """
        Test function buat debug encrypt/decrypt.
        Ini buat cek apakah encrypt dan decrypt bekerja dengan benar.
        
        Args:
            text (str): Text yang mau ditest
            key (str): Key yang dipakai
            
        Returns:
            dict: Hasil test
        """
        if not text or not key:
            return {"error": "Text dan key harus ada"}
        
        # test encrypt
        encrypted = self.encrypt(text, key)
        
        # test decrypt
        decrypted = self.decrypt(encrypted, key)
        
        # cek apakah hasil decrypt sama dengan text asli
        success = (decrypted == text)
        
        return {
            "original_text": text,
            "encrypted": encrypted,
            "decrypted": decrypted,
            "success": success,
            "key": key
        }
    
    def analyze_block_structure(self, text, key):
        """
        Analisis struktur block cipher.
        Ini buat edukasi, biar tau gimana block cipher bekerja.
        
        Args:
            text (str): Text yang mau dianalisis
            key (str): Key yang dipakai
            
        Returns:
            dict: Hasil analisis
        """
        if not text or not key:
            return {"error": "Text dan key harus ada"}
        
        # convert ke binary
        text_binary = self._text_to_binary(text)
        padded_text = self._pad_text(text_binary, self.block_size)
        
        # hitung jumlah block
        num_blocks = len(padded_text) // self.block_size
        
        # generate round keys
        round_keys = self._generate_round_keys(key, 4)
        
        analysis = {
            "original_text": text,
            "binary_length": len(text_binary),
            "padded_length": len(padded_text),
            "number_of_blocks": num_blocks,
            "block_size": self.block_size,
            "round_keys": round_keys,
            "padding_added": len(padded_text) - len(text_binary)
        }
        
        return analysis
