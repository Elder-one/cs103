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
    # PUT YOUR CODE HERE
    return plaintext
