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

    ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alpha = ALPHA.lower()
    ciphertext = ''

    for i in range(len(plaintext)):

        ch = plaintext[i]
        shift = ALPHA.index(keyword[i])

        if ch in alpha:
            ciphertext += alpha[(alpha.index(ch) + shift) % 26]

        elif ch in ALPHA:
            ciphertext += ALPHA[(ALPHA.index(ch) + shift) % 26]

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

    N_ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ALPHA = 'ZYXWVUTSRQPONMLKJIHGFEDCBA'
    alpha = ALPHA.lower()
    plaintext = ''

    for i in range(len(ciphertext)):

        ch = ciphertext[i]
        shift = N_ALPHA.index(keyword[i])

        if ch in alpha:
            plaintext += alpha[(alpha.index(ch) + shift) % 26]

        elif ch in ALPHA:
            plaintext += ALPHA[(ALPHA.index(ch) + shift) % 26]

        else:
            plaintext += ch

    return plaintext
