def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    keyword = keyword.upper()
    i = 0
    while len(keyword) < len(plaintext):
        keyword += keyword[i]
        i += 1

    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphabet = ALPHABET.lower()
    ciphertext = ''

    for i in range(len(plaintext)):

        ch = plaintext[i]
        k = keyword[i]

        if ch in alphabet:
            ciphertext += alphabet[(alphabet.index(ch)+ALPHABET.index(k))%26]

        elif ch in ALPHABET:
            ciphertext += ALPHABET[(ALPHABET.index(ch)+ALPHABET.index(k))%26]

        else:
            ciphertext += ch


    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    keyword = keyword.upper()
    i = 0
    while len(keyword) < len(ciphertext):
        keyword += keyword[i]
        i += 1

    N_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ALPHABET = 'ZYXWVUTSRQPONMLKJIHGFEDCBA'
    alphabet = ALPHABET.lower()
    plaintext = ''

    for i in range(len(ciphertext)):

        ch = ciphertext[i]
        k = keyword[i]

        if ch in alphabet:
            plaintext += alphabet[(alphabet.index(ch)+N_ALPHABET.index(k))%26]

        elif ch in ALPHABET:
            plaintext += ALPHABET[(ALPHABET.index(ch)+N_ALPHABET.index(k))%26]

        else:
            plaintext += ch


    return plaintext