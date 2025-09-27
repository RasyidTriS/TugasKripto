from caesar_cipher import CaesarCipher
from vigenere_cipher import VigenereCipher
from modern_ciphers import ModernCipher1, ModernCipher2


class SuperEncryption:
    """
    Super Encryption class that combines all 4 encryption algorithms.
    Applies encryption in sequence: Caesar -> Vigenère -> Modern1 -> Modern2
    """
    
    def __init__(self):
        self.caesar = CaesarCipher()
        self.vigenere = VigenereCipher()
        self.modern1 = ModernCipher1()
        self.modern2 = ModernCipher2()
    
    def encrypt(self, plaintext, caesar_shift, vigenere_key, modern1_key, modern2_key):
        """
        Encrypt plaintext using all 4 algorithms in sequence.
        
        Args:
            plaintext (str): Text to encrypt
            caesar_shift (int): Shift value for Caesar cipher
            vigenere_key (str): Key for Vigenère cipher
            modern1_key (str): Key for Modern Cipher 1
            modern2_key (str): Key for Modern Cipher 2
            
        Returns:
            str: Super encrypted text
        """
        if not plaintext:
            return ""
        
        # Step 1: Caesar Cipher
        step1 = self.caesar.encrypt(plaintext, caesar_shift)
        
        # Step 2: Vigenère Cipher
        step2 = self.vigenere.encrypt(step1, vigenere_key)
        
        # Step 3: Modern Cipher 1
        step3 = self.modern1.encrypt(step2, modern1_key)
        
        # Step 4: Modern Cipher 2
        step4 = self.modern2.encrypt(step3, modern2_key)
        
        return step4
    
    def decrypt(self, ciphertext, caesar_shift, vigenere_key, modern1_key, modern2_key):
        """
        Decrypt ciphertext using all 4 algorithms in reverse sequence.
        
        Args:
            ciphertext (str): Text to decrypt
            caesar_shift (int): Shift value for Caesar cipher
            vigenere_key (str): Key for Vigenère cipher
            modern1_key (str): Key for Modern Cipher 1
            modern2_key (str): Key for Modern Cipher 2
            
        Returns:
            str: Decrypted text
        """
        if not ciphertext:
            return ""
        
        # Step 1: Modern Cipher 2 (reverse)
        step1 = self.modern2.decrypt(ciphertext, modern2_key)
        
        # Step 2: Modern Cipher 1 (reverse)
        step2 = self.modern1.decrypt(step1, modern1_key)
        
        # Step 3: Vigenère Cipher (reverse)
        step3 = self.vigenere.decrypt(step2, vigenere_key)
        
        # Step 4: Caesar Cipher (reverse)
        step4 = self.caesar.decrypt(step3, caesar_shift)
        
        return step4
    
    def get_encryption_steps(self, plaintext, caesar_shift, vigenere_key, modern1_key, modern2_key):
        """
        Get all intermediate steps of the encryption process for demonstration.
        
        Args:
            plaintext (str): Text to encrypt
            caesar_shift (int): Shift value for Caesar cipher
            vigenere_key (str): Key for Vigenère cipher
            modern1_key (str): Key for Modern Cipher 1
            modern2_key (str): Key for Modern Cipher 2
            
        Returns:
            dict: Dictionary containing all encryption steps
        """
        steps = {
            "Original": plaintext,
            "After Caesar": "",
            "After Vigenère": "",
            "After Modern 1": "",
            "After Modern 2": ""
        }
        
        if not plaintext:
            return steps
        
        # Step 1: Caesar Cipher
        step1 = self.caesar.encrypt(plaintext, caesar_shift)
        steps["After Caesar"] = step1
        
        # Step 2: Vigenère Cipher
        step2 = self.vigenere.encrypt(step1, vigenere_key)
        steps["After Vigenère"] = step2
        
        # Step 3: Modern Cipher 1
        step3 = self.modern1.encrypt(step2, modern1_key)
        steps["After Modern 1"] = step3
        
        # Step 4: Modern Cipher 2
        step4 = self.modern2.encrypt(step3, modern2_key)
        steps["After Modern 2"] = step4
        
        return steps
    
    def get_decryption_steps(self, ciphertext, caesar_shift, vigenere_key, modern1_key, modern2_key):
        """
        Get all intermediate steps of the decryption process for demonstration.
        
        Args:
            ciphertext (str): Text to decrypt
            caesar_shift (int): Shift value for Caesar cipher
            vigenere_key (str): Key for Vigenère cipher
            modern1_key (str): Key for Modern Cipher 1
            modern2_key (str): Key for Modern Cipher 2
            
        Returns:
            dict: Dictionary containing all decryption steps
        """
        steps = {
            "Encrypted": ciphertext,
            "After Modern 2 Decrypt": "",
            "After Modern 1 Decrypt": "",
            "After Vigenère Decrypt": "",
            "After Caesar Decrypt": ""
        }
        
        if not ciphertext:
            return steps
        
        # Step 1: Modern Cipher 2 (reverse)
        step1 = self.modern2.decrypt(ciphertext, modern2_key)
        steps["After Modern 2 Decrypt"] = step1
        
        # Step 2: Modern Cipher 1 (reverse)
        step2 = self.modern1.decrypt(step1, modern1_key)
        steps["After Modern 1 Decrypt"] = step2
        
        # Step 3: Vigenère Cipher (reverse)
        step3 = self.vigenere.decrypt(step2, vigenere_key)
        steps["After Vigenère Decrypt"] = step3
        
        # Step 4: Caesar Cipher (reverse)
        step4 = self.caesar.decrypt(step3, caesar_shift)
        steps["After Caesar Decrypt"] = step4
        
        return steps
