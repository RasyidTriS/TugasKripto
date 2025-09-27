class CaesarCipher:
    """
    Caesar Cipher implementation for encryption and decryption.
    Shifts each letter by a fixed number of positions in the alphabet.
    """
    
    def __init__(self):
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'
    
    def encrypt(self, plaintext, shift):
        if not plaintext:
            return ""
        
        result = ""
        shift = shift % 26  # Menyesuaikan shift dengan jumlah alphabet
        
        for char in plaintext:
            if char.isupper():
                # samakan kecil dan besar
                index = self.alphabet.find(char)
                if index != -1:
                    new_index = (index + shift) % 26
                    result += self.alphabet[new_index]
                else:
                    result += char  # Tetap simpan karater non-alphabetic
            elif char.islower():
                # samakan kecil dan besar
                index = self.alphabet_lower.find(char)
                if index != -1:
                    new_index = (index + shift) % 26
                    result += self.alphabet_lower[new_index]
                else:
                    result += char  # Keep non-alphabetic characters
            else:
                # Keep non-alphabetic characters as they are
                result += char
        
        return result
    
    def decrypt(self, ciphertext, shift):
        """
        Decrypt ciphertext using Caesar cipher with given shift value.
        
        Args:
            ciphertext (str): Text to decrypt
            shift (int): Number of positions the letters were shifted during encryption
            
        Returns:
            str: Decrypted text
        """
        if not ciphertext:
            return ""
        
        result = ""
        shift = shift % 26  # Ensure shift is within 0-25 range
        
        for char in ciphertext:
            if char.isupper():
                # Handle uppercase letters
                index = self.alphabet.find(char)
                if index != -1:
                    new_index = (index - shift) % 26
                    result += self.alphabet[new_index]
                else:
                    result += char  # Keep non-alphabetic characters
            elif char.islower():
                # Handle lowercase letters
                index = self.alphabet_lower.find(char)
                if index != -1:
                    new_index = (index - shift) % 26
                    result += self.alphabet_lower[new_index]
                else:
                    result += char  # Keep non-alphabetic characters
            else:
                # Keep non-alphabetic characters as they are
                result += char
        
        return result
    
    def brute_force_decrypt(self, ciphertext):
        """
        Attempt to decrypt ciphertext by trying all possible shift values.
        
        Args:
            ciphertext (str): Text to decrypt
            
        Returns:
            list: List of tuples (shift_value, decrypted_text) for all possible shifts
        """
        results = []
        for shift in range(26):
            decrypted = self.decrypt(ciphertext, shift)
            results.append((shift, decrypted))
        return results
