# Encryption/Decryption Practice App

A comprehensive Streamlit application for practicing various encryption and decryption algorithms.

## Features

### Traditional Algorithms
1. **Caesar Cipher** - Simple substitution cipher with shift values
2. **Vigenère Cipher** - Polyalphabetic substitution cipher using keywords

### Modern Algorithms (Placeholders)
3. **Modern Cipher 1** - Placeholder for future modern encryption algorithm
4. **Modern Cipher 2** - Placeholder for future modern encryption algorithm

### Super Encryption
5. **Super Encryption** - Combines all 4 algorithms in sequence for maximum security

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run main.py
```

## Usage

The app provides 5 tabs, each dedicated to a specific encryption algorithm:

### Caesar Cipher
- Enter text to encrypt/decrypt
- Adjust shift value (0-25)
- Brute force attack feature to try all possible shifts

### Vigenère Cipher
- Enter text and encryption key
- Frequency analysis attack feature
- Supports both uppercase and lowercase letters

### Modern Ciphers
- Placeholder interfaces for future modern algorithms
- Same encryption/decryption interface as traditional ciphers

### Super Encryption
- Combines all 4 algorithms in sequence
- Shows step-by-step encryption/decryption process
- Requires keys for all algorithms

## File Structure

```
├── main.py                 # Main Streamlit application
├── caesar_cipher.py        # Caesar Cipher implementation
├── vigenere_cipher.py      # Vigenère Cipher implementation
├── modern_ciphers.py       # Placeholder modern cipher classes
├── super_encryption.py     # Super encryption combining all algorithms
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Algorithm Details

### Caesar Cipher
- Shifts each letter by a fixed number of positions in the alphabet
- Supports both uppercase and lowercase letters
- Preserves non-alphabetic characters

### Vigenère Cipher
- Uses a keyword to determine the shift for each letter
- More secure than Caesar cipher due to multiple shift patterns
- Key is repeated to match the length of the text

### Super Encryption
- Applies encryption in sequence: Caesar → Vigenère → Modern1 → Modern2
- Decryption applies algorithms in reverse order
- Provides maximum security through multiple encryption layers

## Educational Features

- Interactive encryption/decryption with real-time results
- Brute force attack demonstration on Caesar cipher
- Frequency analysis attack on Vigenère cipher
- Step-by-step process visualization for super encryption
- Clean, user-friendly interface with comprehensive documentation

## Future Enhancements

The modern cipher placeholders can be replaced with actual modern encryption algorithms such as:
- AES (Advanced Encryption Standard)
- RSA (Rivest-Shamir-Adleman)
- Blowfish
- Twofish
- Or any other modern cryptographic algorithm

## Requirements

- Python 3.7+
- Streamlit 1.28.0+

## License

This project is for educational purposes only.
