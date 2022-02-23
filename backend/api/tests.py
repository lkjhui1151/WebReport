def myFunc(e):
    return e['risk']


cars = [
    {
        "address": "10.20.33.199\n10.20.80.50\n10.20.80.65\n10.20.80.74\n10.20.80.141\n10.20.90.56\n10.20.121.210\n10.90.10.111\n10.90.10.182\n10.90.20.113\n10.90.20.118\n10.90.30.150\n10.100.10.132\n10.100.10.137\n10.100.10.187\n10.100.10.191\n10.100.40.151",
        "name": "SSH Server CBC Mode Ciphers Enabled\n\n- The SSH server is configured to support Cipher Block Chaining (CBC)\nencryption.  This may allow an attacker to recover the plaintext message\nfrom the ciphertext. \nNote that this plugin only checks for the options of the SSH server and\ndoes not check for vulnerable software versions.",
        "remask": "Contact the vendor or consult product documentation to disable CBC mode\ncipher encryption, and enable CTR or GCM cipher mode encryption.",
        "color": "#23B800",
        "risk": 1
    },
    {
        "address": "10.20.33.199\n10.20.80.50\n10.20.80.65\n10.20.80.74\n10.20.80.141\n10.20.90.56\n10.20.121.210\n10.90.10.111\n10.90.10.182\n10.90.20.113\n10.90.20.118\n10.90.30.150\n10.100.10.132\n10.100.10.137\n10.100.10.187\n10.100.10.191\n10.100.40.151",
        "name": "SSH Server CBC Mode Ciphers Enabled\n\n- The SSH server is configured to support Cipher Block Chaining (CBC)\nencryption.  This may allow an attacker to recover the plaintext message\nfrom the ciphertext. \nNote that this plugin only checks for the options of the SSH server and\ndoes not check for vulnerable software versions.",
        "remask": "Contact the vendor or consult product documentation to disable CBC mode\ncipher encryption, and enable CTR or GCM cipher mode encryption.",
        "color": "#23B800",
        "risk": 3
    },
    {
        "address": "10.20.33.199\n10.20.80.50\n10.20.80.65\n10.20.80.74\n10.20.80.141\n10.20.90.56\n10.20.121.210\n10.90.10.111\n10.90.10.182\n10.90.20.113\n10.90.20.118\n10.90.30.150\n10.100.10.132\n10.100.10.137\n10.100.10.187\n10.100.10.191\n10.100.40.151",
        "name": "SSH Server CBC Mode Ciphers Enabled\n\n- The SSH server is configured to support Cipher Block Chaining (CBC)\nencryption.  This may allow an attacker to recover the plaintext message\nfrom the ciphertext. \nNote that this plugin only checks for the options of the SSH server and\ndoes not check for vulnerable software versions.",
        "remask": "Contact the vendor or consult product documentation to disable CBC mode\ncipher encryption, and enable CTR or GCM cipher mode encryption.",
        "color": "#23B800",
        "risk": 2
    },
    {
        "address": "10.20.33.199\n10.20.80.50\n10.20.80.65\n10.20.80.74\n10.20.80.141\n10.20.90.56\n10.20.121.210\n10.90.10.111\n10.90.10.182\n10.90.20.113\n10.90.20.118\n10.90.30.150\n10.100.10.132\n10.100.10.137\n10.100.10.187\n10.100.10.191\n10.100.40.151",
        "name": "SSH Server CBC Mode Ciphers Enabled\n\n- The SSH server is configured to support Cipher Block Chaining (CBC)\nencryption.  This may allow an attacker to recover the plaintext message\nfrom the ciphertext. \nNote that this plugin only checks for the options of the SSH server and\ndoes not check for vulnerable software versions.",
        "remask": "Contact the vendor or consult product documentation to disable CBC mode\ncipher encryption, and enable CTR or GCM cipher mode encryption.",
        "color": "#23B800",
        "risk": 4
    },
]

cars.sort(key=myFunc, reverse=True)

print(cars)
