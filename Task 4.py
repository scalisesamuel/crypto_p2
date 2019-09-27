import os
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes


def file_generator(file_name, file_size):

    """Generates random binary files of a certain Byte size"""

    f = open(file_name, 'wb')
    f.write(os.urandom(file_size))
    f.close()
    return


def file_write(file_name, data):

    """ Writes and replaces data in a file"""

    f = open(file_name, 'wb')
    f.write(data)
    f.close()
    return


def file_time(cipher_time, size):

    """This function determines how many files can be ciphered in 1 second"""

    # starts a count and time sum
    count = 0
    time_total = 0
    # loops with the time sum is less than 1000000000 nanoseconds (1 second)
    while time_total < 1000000000:
        count = count + 1
        time_total = cipher_time + time_total
    # count needs to be subtracted by 1 because we need the number of files under 1 second
    count = count - 1

    print("\t\t\tThe file size in Bytes:\t", size)
    print("\t\t\tThe number of files ciphered in 1 second:\t", count)
    print("\t\t\tBytes per second:\t", (size / cipher_time * 1000000000))
    return


def aes_key_size(key_size, file_name):

    """This runs the AES cipher needed based on key size"""

    # reads in file and sets daa into a variable
    f = open(file_name, 'rb')
    pt_original = f.read()
    f.close()
    size = pt_original.__sizeof__()

    # sets up the encryptor / decryptor
    backend = default_backend()
    key = os.urandom(key_size)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    # the timing and encryption of the pt
    encryptor_size_one = cipher.encryptor()
    cipher_time = time.perf_counter_ns()
    ct = encryptor_size_one.update(pt_original) + encryptor_size_one.finalize()
    cipher_time = time.perf_counter_ns() - cipher_time
    file_write(file_name, ct)
    print("\t\t\tEncryption Time in Seconds:\t", cipher_time / 1000000000)
    file_time(cipher_time, size)
    # opens file and reads the data into a variable
    f = open(file_name, 'rb')
    file = f.read()
    f.close()
    size = file.__sizeof__()
    # the timing and decryption of the file
    decryptor_size_one = cipher.decryptor()
    cipher_time = time.perf_counter_ns()
    pt_new = decryptor_size_one.update(file) + decryptor_size_one.finalize()
    cipher_time = time.perf_counter_ns() - cipher_time
    file_write(file_name, pt_new)
    print("\n\t\t\tDecryption Time in Seconds:\t", cipher_time / 1000000000)
    file_time(cipher_time, size)
    # checks to see if the original message and the decrypted message are the same
    status = pt_new == pt_original
    print("\n\t\t\tMessage Match:\t", status)
    return


def rsa_private_key_size(file_name):

    """This Function Performs RSA"""

    # opens the file for the given file name and puts its data to a variable
    f = open(file_name, 'rb')
    pt_original = f.read()
    f.close()
    size = pt_original.__sizeof__()

    private_key_size = 2048
    # size is 2048 bits because that is the current key size standard
    # private_key is the generated private key
    # used settings suggested by the library's site
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=private_key_size,
        backend=default_backend()
    )
    # public_key is the generated public key based on the private key
    public_key = private_key.public_key()
    # get starting time and then encrypts the file
    cipher_time = time.perf_counter_ns()
    cipher_text = public_key.encrypt(
        pt_original,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    # gets the total time encrypting, overwrites encrypted message to the file, and sends that to the file_time function
    cipher_time = time.perf_counter_ns() - cipher_time
    file_write(file_name, cipher_text)
    print("\t\t\tEncryption Time in Seconds:", cipher_time / 1000000000)
    file_time(cipher_time, size)
    # opens up the overwritten file and sends its data to a variable. Also gets the size of the new data
    f = open(file_name, 'rb')
    file = f.read()
    f.close()
    size = file.__sizeof__()
    # starts the timer and decrypts the message
    cipher_time = time.perf_counter_ns()
    pt_new = private_key.decrypt(
        file,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    # gets the total time, overwrites the file with the decrypted message, and sends the time to the file_time function
    cipher_time = time.perf_counter_ns() - cipher_time
    file_write(file_name, pt_new)
    print("\n\t\t\tDecryption Time in Seconds:", cipher_time / 1000000000)
    file_time(cipher_time, size)
    # checks to see if the original message and the decrypted message are the same
    status = pt_original == pt_new
    print("\n\t\t\tMessage Match:", status)
    return


# file generation
file_one_name = 'fileone.txt'
file_two_name = 'filetwo.txt'
file_one_size = 12800000
file_two_size = 64000000

file_generator(file_one_name, file_one_size)
file_generator(file_two_name, file_two_size)

# AES
print("\nAES:")
print("\tAES 256 Bit Key:")
print("\t\tFile One:")
aes_key_size(32, file_one_name)

print("\n\t\tFile Two:")
aes_key_size(32, file_two_name)

print("\n\tAES 128 Bit Key:")
print("\t\tFile One:")
aes_key_size(16, file_one_name)

print("\n\t\tFile Two:")
aes_key_size(16, file_two_name)

# RSA
file_one_size = 50
file_two_size = 70
file_generator(file_one_name, file_one_size)
file_generator(file_two_name, file_two_size)

print("\nRSA:")
print("\t\tFile One:")
rsa_private_key_size(file_one_name)

print("\n\t\tFile Two:")
rsa_private_key_size(file_two_name)

