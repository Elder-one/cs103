def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphabet = ALPHABET.lower()
    ciphertext = ''

    for ch in plaintext:

        if ch in alphabet:
            ciphertext += alphabet[(alphabet.index(ch) + 3) % 26]

        elif ch in ALPHABET:
            ciphertext += ALPHABET[(ALPHABET.index(ch) + 3) % 26]

        else:
            ciphertext += ch

    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    ALPHABET = 'ZYXWVUTSRQPONMLKJIHGFEDCBA'
    alphabet = ALPHABET.lower()
    plaintext = ''

    for ch in ciphertext:

        if ch in alphabet:
            plaintext += alphabet[(alphabet.index(ch) + 3) % 26]

        elif ch in ALPHABET:
            plaintext += ALPHABET[(ALPHABET.index(ch) + 3) % 26]

        else:
            plaintext += ch

    return plaintext
