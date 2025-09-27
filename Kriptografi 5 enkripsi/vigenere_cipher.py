class VigenereCipher:
    """
    Vigenère Cipher implementation for encryption and decryption.
    Uses a keyword to determine the shift for each letter.
    """
    
    def __init__(self):
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'
    
    def _prepare_key(self, key, length):
        """
        Prepare the key by repeating it to match the length of the text.
        
        Args:
            key (str): The encryption key
            length (int): Length of the text to encrypt/decrypt
            
        Returns:
            str: Prepared key with same length as text
        """
        if not key:
            return ""
        
        # Remove non-alphabetic characters and convert to uppercase
        clean_key = ''.join(c.upper() for c in key if c.isalpha())
        if not clean_key:
            return ""
        
        # Repeat key to match text length
        repeated_key = (clean_key * ((length // len(clean_key)) + 1))[:length]
        return repeated_key
    
    def encrypt(self, plaintext, key):
        """
        Encrypt plaintext using Vigenère cipher with given key.
        
        Args:
            plaintext (str): Text to encrypt
            key (str): Encryption key
            
        Returns:
            str: Encrypted text
        """
        if not plaintext or not key:
            return plaintext
        
        result = ""
        key_index = 0
        clean_key = ''.join(c.upper() for c in key if c.isalpha())
        
        if not clean_key:
            return plaintext
        
        for char in plaintext:
            if char.isupper():
                # Handle uppercase letters
                index = self.alphabet.find(char)
                if index != -1:
                    key_char = clean_key[key_index % len(clean_key)]
                    key_shift = self.alphabet.find(key_char)
                    new_index = (index + key_shift) % 26
                    result += self.alphabet[new_index]
                    key_index += 1
                else:
                    result += char  # Keep non-alphabetic characters
            elif char.islower():
                # Handle lowercase letters
                index = self.alphabet_lower.find(char)
                if index != -1:
                    key_char = clean_key[key_index % len(clean_key)]
                    key_shift = self.alphabet.find(key_char)
                    new_index = (index + key_shift) % 26
                    result += self.alphabet_lower[new_index]
                    key_index += 1
                else:
                    result += char  # Keep non-alphabetic characters
            else:
                # Keep non-alphabetic characters as they are
                result += char
        
        return result
    
    def decrypt(self, ciphertext, key):
        """
        Decrypt ciphertext using Vigenère cipher with given key.
        
        Args:
            ciphertext (str): Text to decrypt
            key (str): Decryption key
            
        Returns:
            str: Decrypted text
        """
        if not ciphertext or not key:
            return ciphertext
        
        result = ""
        key_index = 0
        clean_key = ''.join(c.upper() for c in key if c.isalpha())
        
        if not clean_key:
            return ciphertext
        
        for char in ciphertext:
            if char.isupper():
                # Handle uppercase letters
                index = self.alphabet.find(char)
                if index != -1:
                    key_char = clean_key[key_index % len(clean_key)]
                    key_shift = self.alphabet.find(key_char)
                    new_index = (index - key_shift) % 26
                    result += self.alphabet[new_index]
                    key_index += 1
                else:
                    result += char  # Keep non-alphabetic characters
            elif char.islower():
                # Handle lowercase letters
                index = self.alphabet_lower.find(char)
                if index != -1:
                    key_char = clean_key[key_index % len(clean_key)]
                    key_shift = self.alphabet.find(key_char)
                    new_index = (index - key_shift) % 26
                    result += self.alphabet_lower[new_index]
                    key_index += 1
                else:
                    result += char  # Keep non-alphabetic characters
            else:
                # Keep non-alphabetic characters as they are
                result += char
        
        return result
    
    # def frequency_analysis_attack(self, ciphertext):
    #     """
    #     Attempt to break Vigenère cipher using frequency analysis.
    #     This is a simplified version for educational purposes.
        
    #     Args:
    #         ciphertext (str): Text to analyze
            
    #     Returns:
    #         str: Suggested key based on frequency analysis
    #     """
    #     # This is a simplified frequency analysis
    #     # In practice, this would be much more complex
    #     ciphertext_clean = ''.join(c.upper() for c in ciphertext if c.isalpha())
        
    #     if len(ciphertext_clean) < 10:
    #         return "Text too short for analysis"
        
    #     # English letter frequencies
    #     english_freq = {
    #         'E': 12.02, 'T': 9.10, 'A': 8.12, 'O': 7.68, 'I': 6.97,
    #         'N': 6.95, 'S': 6.28, 'H': 6.09, 'R': 5.99, 'D': 4.25,
    #         'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
    #         'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29,
    #         'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10,
    #         'Z': 0.07
    #     }
        
    #     # Count letter frequencies in ciphertext
    #     letter_count = {}
    #     for char in ciphertext_clean:
    #         letter_count[char] = letter_count.get(char, 0) + 1
        
    #     total_chars = len(ciphertext_clean)
    #     cipher_freq = {char: count/total_chars * 100 for char, count in letter_count.items()}
        
    #     # Find the most frequent letter
    #     most_frequent = max(cipher_freq.items(), key=lambda x: x[1])
    #     most_frequent_letter = most_frequent[0]
        
    #     # Assume it corresponds to 'E' (most frequent in English)
    #     # Calculate the shift
    #     e_index = self.alphabet.find('E')
    #     cipher_index = self.alphabet.find(most_frequent_letter)
    #     shift = (cipher_index - e_index) % 26
        
    #     # Convert shift to letter
    #     suggested_key = self.alphabet[shift]
        
    #     return f"Suggested key: {suggested_key} (based on frequency analysis)"
