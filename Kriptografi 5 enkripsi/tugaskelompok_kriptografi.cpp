#include <iostream>
#include <iomanip>
#include <sstream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <cctype>
#include <cstdlib>
#include <limits>

using namespace std;

// ---------- Utilities ----------
string toHex(const string &s) {
    ostringstream oss;
    oss << hex << setfill('0');
    for (unsigned char c : s) oss << setw(2) << (int)c;
    return oss.str();
}

string fromHex(const string &hexs) {
    string out;
    out.reserve(hexs.size()/2);
    for (size_t i=0; i+1 < hexs.size(); i += 2) {
        string byte = hexs.substr(i,2);
        char chr = (char) (int) strtol(byte.c_str(), nullptr, 16);
        out.push_back(chr);
    }
    return out;
}

string showPrintableOrHex(const string &raw) {
    bool printable = true;
    for (unsigned char c : raw) if (c < 32 || c > 126) { printable = false; break; }
    if (printable) return raw;
    return "[HEX] " + toHex(raw);
}

// ---------- Safe input helpers ----------
string promptLine(const string &prompt) {
    cout << prompt;
    cout.flush();
    string line;
    if (!getline(cin, line)) {
        cout << "\n(input stream closed) exiting...\n";
        exit(0);
    }
    return line;
}

int promptInt(const string &prompt, int minVal = INT_MIN, int maxVal = INT_MAX) {
    while (true) {
        string s = promptLine(prompt);
        try {
            size_t pos;
            int v = stoi(s, &pos);
            if (pos != s.size()) throw invalid_argument("extra");
            if (v < minVal || v > maxVal) {
                cout << "Masukan di luar rentang. Coba lagi.\n";
                continue;
            }
            return v;
        } catch (...) {
            cout << "Input tidak valid. Masukkan angka bulat.\n";
        }
    }
}

char promptChar(const string &prompt) {
    string s = promptLine(prompt);
    if (s.empty()) return '\0';
    return s[0];
}

// ---------- Ciphers ----------
string caesarEncrypt(const string &text, int key) {
    string result; result.reserve(text.size());
    key = ((key % 26) + 26) % 26;
    for (char c : text) {
        if (isalpha((unsigned char)c)) {
            char base = isupper((unsigned char)c) ? 'A' : 'a';
            result += char((c - base + key) % 26 + base);
        } else result += c;
    }
    return result;
}

string caesarDecrypt(const string &text, int key) { 
    return caesarEncrypt(text, 26 - (key % 26)); 
}

string vigenereEncrypt(const string &text, const string &key) {
    string result; result.reserve(text.size());
    if (key.empty()) return text;
    int j = 0;
    for (char c : text) {
        if (isalpha((unsigned char)c)) {
            char base = isupper((unsigned char)c) ? 'A' : 'a';
            char k = toupper((unsigned char)key[j % key.size()]) - 'A';
            result += char((c - base + k) % 26 + base);
            j++;
        } else result += c;
    }
    return result;
}

string vigenereDecrypt(const string &text, const string &key) {
    string result; result.reserve(text.size());
    if (key.empty()) return text;
    int j = 0;
    for (char c : text) {
        if (isalpha((unsigned char)c)) {
            char base = isupper((unsigned char)c) ? 'A' : 'a';
            char k = toupper((unsigned char)key[j % key.size()]) - 'A';
            result += char((c - base - k + 26) % 26 + base);
            j++;
        } else result += c;
    }
    return result;
}

string xorEncrypt(const string &text, const string &key) {
    if (key.empty()) return text;
    string result; result.resize(text.size());
    for (size_t i = 0; i < text.size(); ++i) result[i] = char(text[i] ^ key[i % key.size()]);
    return result;
}

string xorDecrypt(const string &text, const string &key) { 
    return xorEncrypt(text, key); 
}

string vernamEncrypt(const string &text, const string &key) {
    if (key.size() != text.size()) {
        cerr << "Kunci Vernam harus sama panjang dengan plaintext!\n";
        return "";
    }
    string result; result.resize(text.size());
    for (size_t i = 0; i < text.size(); ++i) result[i] = char(text[i] ^ key[i]);
    return result;
}

string vernamDecrypt(const string &text, const string &key) { 
    return vernamEncrypt(text, key); 
}

// Fungsi super encrypt yang mengembalikan juga setiap tahapan
vector<string> superEncryptWithSteps(const string &text, int caesarKey, const string &vigKey, const string &xorKey, const string &verKey) {
    vector<string> steps;
    
    string s1 = caesarEncrypt(text, caesarKey);
    steps.push_back("Caesar: " + showPrintableOrHex(s1));
    
    string s2 = vigenereEncrypt(s1, vigKey);
    steps.push_back("Vigenere: " + showPrintableOrHex(s2));
    
    string s3 = xorEncrypt(s2, xorKey);
    steps.push_back("XOR: " + showPrintableOrHex(s3));
    
    string s4 = vernamEncrypt(s3, verKey);
    steps.push_back("Vernam: " + showPrintableOrHex(s4));
    
    steps.push_back(s4); // hasil akhir di index terakhir
    return steps;
}

string superEncrypt(const string &text, int caesarKey, const string &vigKey, const string &xorKey, const string &verKey) {
    auto steps = superEncryptWithSteps(text, caesarKey, vigKey, xorKey, verKey);
    return steps.back(); // return hasil akhir
}

string superDecrypt(const string &text, int caesarKey, const string &vigKey, const string &xorKey, const string &verKey) {
    string s1 = vernamDecrypt(text, verKey);
    string s2 = xorDecrypt(s1, xorKey);
    string s3 = vigenereDecrypt(s2, vigKey);
    string s4 = caesarDecrypt(s3, caesarKey);
    return s4;
}

// ---------- Storage ----------
struct Record { 
    int algo; 
    string cipherHex;
    string cipherDisplay; // untuk menampilkan cipher dalam bentuk yang bisa dibaca
};

vector<Record> storeCipher;

// ---------- Clue/analysis functions ----------
map<char,int> frequency(const string &s) {
    map<char,int> f;
    for (unsigned char c : s) f[c]++;
    return f;
}

double indexOfCoincidence(const string &s) {
    auto freq = frequency(s);
    double N = (double)s.size(); if (N <= 1) return 0.0;
    double sum = 0;
    for (auto &p : freq) sum += (double)p.second * (p.second - 1);
    return sum / (N * (N - 1));
}

void showCluesForCaesar(const string &cipher) {
    cout << "=== CLUE UNTUK CAESAR CIPHER ===\n";
    cout << "Panjang ciphertext: " << cipher.size() << "\n";
    cout << "Index of Coincidence: " << fixed << setprecision(4) << indexOfCoincidence(cipher) << "\n";
    
    auto freq = frequency(cipher);
    vector<pair<int,char>> v;
    for (auto &p : freq) if (isalpha((unsigned char)p.first)) v.push_back({p.second, p.first});
    sort(v.rbegin(), v.rend());
    
    if (!v.empty()) {
        cout << "Huruf paling sering: ";
        for (size_t i=0;i<min((size_t)3,v.size());++i) 
            cout << v[i].second << "(" << v[i].first << "x) ";
        cout << "\n";
        
        cout << "Saran shift yang dicoba:\n";
        for (size_t i=0;i<min((size_t)3,v.size());++i) {
            char commonChar = tolower(v[i].second);
            // Coba map ke 'e' dan 'a' (huruf paling umum dalam bahasa Indonesia/Inggris)
            int shiftToE = (commonChar - 'e' + 26) % 26;
            int shiftToA = (commonChar - 'a' + 26) % 26;
            cout << "  - Jika '" << v[i].second << "' adalah 'e': shift = " << shiftToE << "\n";
            cout << "  - Jika '" << v[i].second << "' adalah 'a': shift = " << shiftToA << "\n";
        }
    } else {
        cout << "Tidak ditemukan huruf alfabet dalam ciphertext.\n";
    }
    cout << "----------------------------------------\n";
}

void showCluesForVigenere(const string &cipher) {
    cout << "=== CLUE UNTUK VIGENERE CIPHER ===\n";
    cout << "Panjang ciphertext: " << cipher.size() << "\n";
    cout << "Index of Coincidence: " << fixed << setprecision(4) << indexOfCoincidence(cipher) << "\n";
    
    // Analisis Kasiski sederhana - cari substring yang berulang
    map<string, vector<int>> positions;
    for (int len = 3; len <= 5; len++) {
        for (int i = 0; i <= (int)cipher.size() - len; i++) {
            string substr = cipher.substr(i, len);
            positions[substr].push_back(i);
        }
    }
    
    cout << "Substring yang berulang (petunjuk panjang kunci):\n";
    bool found = false;
    for (auto &p : positions) {
        if (p.second.size() > 1) {
            cout << "  '" << p.first << "' muncul di posisi: ";
            for (size_t i = 0; i < p.second.size(); i++) {
                cout << p.second[i];
                if (i < p.second.size() - 1) cout << ", ";
            }
            cout << " -> jarak: ";
            for (size_t i = 1; i < p.second.size(); i++) {
                cout << (p.second[i] - p.second[0]);
                if (i < p.second.size() - 1) cout << ", ";
            }
            cout << "\n";
            found = true;
        }
    }
    if (!found) cout << "  Tidak ditemukan substring berulang yang signifikan.\n";
    
    cout << "Saran: Coba panjang kunci 3, 5, 7, atau faktor dari jarak yang ditemukan.\n";
    cout << "----------------------------------------\n";
}

void showCluesForXor(const string &cipher) {
    cout << "=== CLUE UNTUK XOR CIPHER ===\n";
    cout << "Panjang ciphertext: " << cipher.size() << " bytes\n";
    cout << "Hex: " << toHex(cipher) << "\n";
    
    // Untuk XOR dengan kunci pendek, cari pola
    cout << "Analisis frekuensi karakter:\n";
    auto freq = frequency(cipher);
    vector<pair<int,char>> v;
    for (auto &p : freq) v.push_back({p.second, p.first});
    sort(v.rbegin(), v.rend());
    
    for (size_t i=0;i<min((size_t)5,v.size());++i) {
        cout << "  Karakter " << showPrintableOrHex(string(1, v[i].second)) 
             << ": " << v[i].first << " kemunculan\n";
    }
    
    cout << "Saran: Coba kunci pendek (1-10 karakter), spasi (0x20) adalah karakter umum.\n";
    cout << "----------------------------------------\n";
}

void showCluesForVernam(const string &cipher) {
    cout << "=== CLUE UNTUK VERNAM CIPHER ===\n";
    cout << "Panjang ciphertext: " << cipher.size() << " bytes\n";
    cout << "Hex: " << toHex(cipher) << "\n";
    cout << "Vernam/OTP yang benar TIDAK BISA dipecahkan tanpa kunci.\n";
    cout << "Jika kunci digunakan ulang, sistem menjadi rentan.\n";
    cout << "----------------------------------------\n";
}

void showCluesForSuper(const string &cipher) {
    cout << "=== CLUE UNTUK SUPER CIPHER ===\n";
    cout << "Panjang ciphertext: " << cipher.size() << " bytes\n";
    cout << "Hex: " << toHex(cipher) << "\n";
    cout << "Urutan enkripsi: Caesar -> Vigenere -> XOR -> Vernam\n";
    cout << "Urutan dekripsi: Vernam -> XOR -> Vigenere -> Caesar\n";
    cout << "Strategi:\n";
    cout << "1. Coba tebak panjang kunci Vernam (sama dengan panjang plaintext)\n";
    cout << "2. Analisis pola setelah melepas lapisan Vernam dan XOR\n";
    cout << "3. Gunakan teknik Vigenere dan Caesar pada lapisan dalam\n";
    cout << "----------------------------------------\n";
}

// ---------- Menus ----------
int chooseAlgoMenu() {
    cout << "1. Caesar\n2. Vigenere\n3. XOR\n4. Vernam\n5. Super\n";
    return promptInt("Pilih algoritma (1-5): ", 1, 5);
}

void listStored() {
    if (storeCipher.empty()) { 
        cout << "Belum ada ciphertext tersimpan.\n"; 
        return; 
    }
    cout << "--- Stored Ciphertexts ---\n";
    for (size_t i=0;i<storeCipher.size();++i) {
        cout << i << ". Algo=" << storeCipher[i].algo << " Display=" << storeCipher[i].cipherDisplay;
        if (storeCipher[i].cipherDisplay.find("[HEX]") == string::npos) {
            cout << " (Hex=" << storeCipher[i].cipherHex << ")";
        }
        cout << "\n";
    }
}

// ---------- Main ----------
int main() {
    while (true) {
        cout << "===== SISTEM KRIPTO =====\n";
        cout << "1. Enkripsi\n2. Dekripsi\n3. Percobaan Pembobolan (Clue)\n4. Keluar\n";
        int mainChoice = promptInt("Pilih: ", 1, 4);

        if (mainChoice == 4) { 
            cout << "Keluar...\n"; 
            break; 
        }

        if (mainChoice == 1) {
            int algo = chooseAlgoMenu();
            string plaintext = promptLine("Masukkan plaintext: ");
            string cipherRaw;
            string displayText;
            
            if (algo == 1) {
                int shift = promptInt("Masukkan shift (int): ");
                cipherRaw = caesarEncrypt(plaintext, shift);
                displayText = showPrintableOrHex(cipherRaw);
                cout << "Ciphertext: " << displayText << "\n";
                storeCipher.push_back({1, toHex(cipherRaw), displayText});
            } 
            else if (algo == 2) {
                string key = promptLine("Masukkan kunci Vigenere: ");
                cipherRaw = vigenereEncrypt(plaintext, key);
                displayText = showPrintableOrHex(cipherRaw);
                cout << "Ciphertext: " << displayText << "\n";
                storeCipher.push_back({2, toHex(cipherRaw), displayText});
            } 
            else if (algo == 3) {
                string key = promptLine("Masukkan kunci XOR: ");
                cipherRaw = xorEncrypt(plaintext, key);
                displayText = showPrintableOrHex(cipherRaw);
                cout << "Ciphertext: " << displayText << "\n";
                storeCipher.push_back({3, toHex(cipherRaw), displayText});
            } 
            else if (algo == 4) {
                string key;
                while (true) {
                    key = promptLine("Masukkan kunci Vernam (sama panjang dengan plaintext): ");
                    if (key.size() != plaintext.size()) 
                        cout << "Panjang kunci salah. plaintext panjang=" << plaintext.size() << "\n";
                    else break;
                }
                cipherRaw = vernamEncrypt(plaintext, key);
                displayText = showPrintableOrHex(cipherRaw);
                cout << "Ciphertext: " << displayText << "\n";
                storeCipher.push_back({4, toHex(cipherRaw), displayText});
            } 
            else { // super
                cout << "Super: Caesar -> Vigenere -> XOR -> Vernam\n";
                int shift = promptInt("Masukkan kunci Caesar (int): ");
                string vkey = promptLine("Masukkan kunci Vigenere: ");
                string xkey = promptLine("Masukkan kunci XOR: ");
                string verkey;
                while (true) {
                    verkey = promptLine("Masukkan kunci Vernam (sama panjang dengan plaintext): ");
                    if (verkey.size() != plaintext.size()) 
                        cout << "Panjang kunci salah.\n"; 
                    else break;
                }
                
                // Tampilkan setiap tahapan
                auto steps = superEncryptWithSteps(plaintext, shift, vkey, xkey, verkey);
                cout << "\n=== URUTAN ENKRIPSI ===\n";
                for (size_t i = 0; i < steps.size() - 1; i++) {
                    cout << steps[i] << "\n";
                }
                cout << "Hasil akhir: " << steps.back() << "\n";
                
                cipherRaw = steps.back();
                displayText = showPrintableOrHex(cipherRaw);
                storeCipher.push_back({5, toHex(cipherRaw), displayText});
            }
            cout << "Cipher disimpan.\n";
            promptLine("Tekan Enter untuk melanjutkan...");
        }
        else if (mainChoice == 2) {
            int algo = chooseAlgoMenu();
            cout << "1. Dekripsi ciphertext tersimpan\n2. Dekripsi ciphertext baru\n";
            int mode = promptInt("Pilih mode (1/2): ", 1, 2);
            string cipherHex;
            string displayText;
            
            if (mode == 1) {
                if (storeCipher.empty()) { 
                    cout << "Belum ada ciphertext.\n"; 
                    continue; 
                }
                listStored();
                int idx = promptInt("Masukkan index ciphertext: ", 0, (int)storeCipher.size()-1);
                if (storeCipher[idx].algo != algo) {
                    char c = promptChar("WARNING: Algoritma berbeda dari yang digunakan saat enkripsi. Lanjutkan? (y/n): ");
                    if (c != 'y' && c != 'Y') continue;
                }
                cipherHex = storeCipher[idx].cipherHex;
                displayText = storeCipher[idx].cipherDisplay;
            } else {
                string in = promptLine("Masukkan ciphertext (hex atau teks printable): ");
                bool maybeHex = !in.empty() && (in.size()%2==0);
                for (char ch : in) if (!isxdigit((unsigned char)ch)) { maybeHex = false; break; }
                if (maybeHex) {
                    cipherHex = in;
                    displayText = "[HEX] " + in;
                } else {
                    cipherHex = toHex(in);
                    displayText = in;
                }
            }

            cout << "Ciphertext yang akan didekripsi: " << displayText << "\n";
            string cipherRaw = fromHex(cipherHex);
            string plain;
            
            if (algo == 1) {
                int shift = promptInt("Masukkan shift (kunci Caesar): ");
                plain = caesarDecrypt(cipherRaw, shift);
                cout << "Plaintext: " << plain << "\n";
            } 
            else if (algo == 2) {
                string k = promptLine("Masukkan kunci Vigenere: ");
                plain = vigenereDecrypt(cipherRaw, k);
                cout << "Plaintext: " << plain << "\n";
            } 
            else if (algo == 3) {
                string k = promptLine("Masukkan kunci XOR: ");
                plain = xorDecrypt(cipherRaw, k);
                cout << "Plaintext: " << showPrintableOrHex(plain) << "\n";
            } 
            else if (algo == 4) {
                string k = promptLine("Masukkan kunci Vernam (sama panjang): ");
                if (k.size() != cipherRaw.size()) 
                    cout << "Panjang kunci salah.\n";
                else { 
                    plain = vernamDecrypt(cipherRaw, k); 
                    cout << "Plaintext: " << plain << "\n"; 
                }
            } 
            else {
                cout << "Super dekripsi (Vernam -> XOR -> Vigenere -> Caesar)\n";
                string vkey = promptLine("Masukkan kunci Vernam (sama panjang): ");
                if (vkey.size() != cipherRaw.size()) { 
                    cout << "Panjang Vernam salah.\n"; 
                }
                else {
                    string xkey = promptLine("Masukkan kunci XOR: ");
                    string vigen = promptLine("Masukkan kunci Vigenere: ");
                    int shift = promptInt("Masukkan kunci Caesar (int): ");
                    plain = superDecrypt(cipherRaw, shift, vigen, xkey, vkey);
                    cout << "Plaintext: " << plain << "\n";
                }
            }
            promptLine("Tekan Enter untuk melanjutkan...");
        }
        else if (mainChoice == 3) {
            cout << "=== PEMBOBOLAN / CLUE ===\n";
            
            // Pilih algoritma yang ingin dicoba bobol
            int algo = chooseAlgoMenu();
            
            cout << "1. Gunakan ciphertext tersimpan\n2. Masukkan ciphertext baru\n";
            int mode = promptInt("Pilih mode (1/2): ", 1, 2);
            string cipherHex;
            string displayText;
            string cipherRaw;
            
            if (mode == 1) {
                if (storeCipher.empty()) { 
                    cout << "Belum ada ciphertext.\n"; 
                    continue; 
                }
                listStored();
                int idx = promptInt("Masukkan index ciphertext: ", 0, (int)storeCipher.size()-1);
                cipherHex = storeCipher[idx].cipherHex;
                displayText = storeCipher[idx].cipherDisplay;
                cipherRaw = fromHex(cipherHex);
                
                if (storeCipher[idx].algo != algo) {
                    cout << "PERHATIAN: Ciphertext ini dibuat dengan algoritma " << storeCipher[idx].algo;
                    cout << ", tetapi Anda memilih algoritma " << algo << " untuk pembobolan.\n";
                    char c = promptChar("Lanjutkan? (y/n): ");
                    if (c != 'y' && c != 'Y') continue;
                }
            } else {
                string in = promptLine("Masukkan ciphertext (hex atau teks printable): ");
                bool maybeHex = !in.empty() && (in.size()%2==0);
                for (char ch : in) if (!isxdigit((unsigned char)ch)) { maybeHex = false; break; }
                if (maybeHex) {
                    cipherHex = in;
                    displayText = "[HEX] " + in;
                } else {
                    cipherHex = toHex(in);
                    displayText = in;
                }
                cipherRaw = fromHex(cipherHex);
            }

            cout << "\nCiphertext yang akan dibobol: " << displayText << "\n";
            
            // Tampilkan clue berdasarkan algoritma
            cout << "\n";
            if (algo == 1) showCluesForCaesar(cipherRaw);
            else if (algo == 2) showCluesForVigenere(cipherRaw);
            else if (algo == 3) showCluesForXor(cipherRaw);
            else if (algo == 4) showCluesForVernam(cipherRaw);
            else showCluesForSuper(cipherRaw);

            // Sekarang beri opsi untuk mencoba dekripsi dengan kunci tebakan
            cout << "\n=== COBA TEBAK KUNCI ===\n";
            string plain;
            
            if (algo == 1) {
                int shift = promptInt("Masukkan shift yang dicoba: ");
                plain = caesarDecrypt(cipherRaw, shift);
                cout << "Hasil: " << plain << "\n";
            } 
            else if (algo == 2) {
                string k = promptLine("Masukkan kunci Vigenere yang dicoba: ");
                plain = vigenereDecrypt(cipherRaw, k);
                cout << "Hasil: " << plain << "\n";
            } 
            else if (algo == 3) {
                string k = promptLine("Masukkan kunci XOR yang dicoba: ");
                plain = xorDecrypt(cipherRaw, k);
                cout << "Hasil: " << showPrintableOrHex(plain) << "\n";
            } 
            else if (algo == 4) {
                string k = promptLine("Masukkan kunci Vernam yang dicoba: ");
                if (k.size() != cipherRaw.size()) 
                    cout << "Panjang kunci salah.\n";
                else { 
                    plain = vernamDecrypt(cipherRaw, k); 
                    cout << "Hasil: " << plain << "\n"; 
                }
            } 
            else {
                cout << "Super dekripsi (Vernam -> XOR -> Vigenere -> Caesar)\n";
                string vkey = promptLine("Masukkan kunci Vernam: ");
                if (vkey.size() != cipherRaw.size()) { 
                    cout << "Panjang Vernam salah.\n"; 
                }
                else {
                    string xkey = promptLine("Masukkan kunci XOR: ");
                    string vigen = promptLine("Masukkan kunci Vigenere: ");
                    int shift = promptInt("Masukkan kunci Caesar: ");
                    plain = superDecrypt(cipherRaw, shift, vigen, xkey, vkey);
                    cout << "Hasil: " << plain << "\n";
                }
            }
            
            promptLine("Tekan Enter untuk melanjutkan...");
        }
    }

    return 0;
}