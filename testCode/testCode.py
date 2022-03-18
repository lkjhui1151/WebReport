# Hash a single string with hashlib.sha256
import hashlib

with open("D:/github/WebReport/testCode/hash.txt", 'rb') as f:
    for line in f:
        hashed_line = hashlib.sha512(line).hexdigest()
        print(hashed_line)

"49ec55bd83fcd67838e3d385ce831669e3f815a7f44b7aa5f8d52b5d42354c46d89c8b9d06e47a797ae4fbd22291be15bcc35b07735c4a6f92357f93d5a33d9b"
"49ec55bd83fcd67838e3d385ce831669e3f815a7f44b7aa5f8d52b5d42354c46d89c8b9d06e47a797ae4fbd22291be15bcc35b07735c4a6f92357f93d5a33d9b"