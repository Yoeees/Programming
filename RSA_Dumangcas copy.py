# Johnwences Fabe P. Dumangcas

# this was already covered in our CSC-102 class when we were using C, sir.
# Using C made programming quite challenging because we needed to create structs 
# using string data types to handle large integer values, which i struggled with and failed haha.
# now I am using Python since it can handle integers of arbitrary size.
# i also included file handling like we did in CSC-102,



import random

class RSA:
    def __init__(self):
        self.n = self.e = self.d = None

    def checkPrime(self, x):  # method for checking if a number is prime
        if x <= 1:
            return False
        for i in range(2, int(x**0.5) + 1):
            if x % i == 0:
                return False
        return True

    def gcd(self, a, b):  # method for checking co-primes (relative prime numbers)
        while b != 0:
            a, b = b, a % b
        return a

    def extended_gcd(self, a, b):  # method to compute the modular inverse of e
        if a == 0:
            return (b, 0, 1)
        else:
            g, x1, y1 = self.extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return (g, x, y)

    def mod_inverse(self, e, phi_n):  # method to compute the private key d
        g, x, _ = self.extended_gcd(e, phi_n)
        if g != 1:
            raise ValueError(f"The numbers {e} and {phi_n} are not coprime, so the modular inverse does not exist.")
        else:
            return x % phi_n

    def generate_random_prime(self, min_value, max_value):

        while True:
            # Generate a random number within the given range
            num = random.randint(min_value, max_value)
            # Ensure the number is odd (even numbers can't be prime)
            if num % 2 == 0:
                num += 1
            # Check if it's a prime number
            if self.checkPrime(num):
                return num

    def modular_exponentiation(self, base, exp, mod):  # used for encrypting and decrypting
        result = 1
        base = base % mod
        while exp > 0:
            if (exp % 2) == 1:  # If exp is odd
                result = (result * base) % mod
            exp = exp >> 1  # exp = exp // 2
            base = (base * base) % mod
        return result



    def string_to_number(self, s):  # convert a string message into a list of ascii values
        return [ord(char) for char in s]

    def number_to_string(self, nums):  # vice versa
        return ''.join(chr(num) for num in nums)

    def generateKeys(self):

        while True:
            p = self.generate_random_prime(2, 100)
            q = self.generate_random_prime(2, 100)

            if p != q:
                break  # Exit loop when p and q are distinct

        self.n = p * q
        phi_n = (p - 1) * (q - 1)

        while True:
            self.e = self.generate_random_prime(3, phi_n)
            if self.gcd(self.e, phi_n) == 1:
                break  # Exit loop when a valid e is found

        self.d = self.mod_inverse(self.e, phi_n)

        print(f"Generated keys:\n p = {p}\n q = {q}\n n = {self.n}\n phi_n = {phi_n}\n e = {self.e}\n d = {self.d}")
        print(f"Public key: ({self.n},{self.e})\nPrivate key: ({self.n},{self.d}) ")

  
    def padding(self, num, length):
        num_str = str(num)
        return '0' * (length - len(num_str)) + num_str
    
    def encryption(self):
        if self.n is None or self.e is None:
            print("Keys not generated. Please generate keys first.")
            return

        msg = input("Enter a message: ")

        # Convert the message to ASCII values
        letters = self.string_to_number(msg)

        # Determine the length required for each encrypted number
        length = len(str(self.n))

        # Pad each ASCII value
        padded_letters = [self.padding(num, length) for num in letters]
        
        encryption_key = int(input("Enter encryption key: "));

        # Encrypt the numeric representation of the message
        encrypted_numbers = [self.modular_exponentiation(int(num), encryption_key, self.n) for num in padded_letters]

        # Concatenate the encrypted numbers into a single string without spaces
        encrypted_message = ''.join(self.padding(num, length) for num in encrypted_numbers)

        print(f"Encrypting message '{msg}' with public key ({self.n}, {self.e})")
        print(f"Encrypted message: {encrypted_message}")


    def decryption(self):
        if self.n is None or self.d is None:
            print("Keys not generated or private key not available. Please generate keys first.")
            return

        encrypted_message = input("Enter the encrypted message: ")

        # Determine the length of each encrypted number
        length = len(str(self.n))
        decryption_key = int(input("Enter decryption key: "));
        # Split the encrypted message into chunks of fixed length
        try:
            encrypted_numbers = [int(encrypted_message[i:i+length]) for i in range(0, len(encrypted_message), length)]
        except ValueError:
            print("Invalid input. Please ensure the encrypted message is a valid concatenation of numbers.")
            return

        # Decrypt the numeric representation of the message
        decrypted_numbers = [self.modular_exponentiation(num, decryption_key, self.n) for num in encrypted_numbers]

        # Convert decrypted numbers back to characters using ASCII
        decrypted_message = self.number_to_string(decrypted_numbers)

        print(f"Decrypted message with private key ({self.n}, {self.d}): {decrypted_message}")


    def txtFileEncryption(self):
        if self.n is None or self.e is None:
            print("Keys not generated. Please generate keys first.")
            return

        msg = input("Enter a message: ")

        # Convert the message to ASCII values
        letters = self.string_to_number(msg)

        # Determine the length required for each encrypted number
        length = len(str(self.n))

        # Pad each ASCII value
        padded_letters = [self.padding(num, length) for num in letters]
        
        encryption_key = int(input("Enter encryption key: "))

        # Encrypt the numeric representation of the message
        encrypted_numbers = [self.modular_exponentiation(int(num), encryption_key, self.n) for num in padded_letters]

        # Concatenate the encrypted numbers into a single string without spaces
        encrypted_message = ''.join(self.padding(num, length) for num in encrypted_numbers)

        # Write the encrypted message to a file
        with open('cipher.txt', 'w') as txtFile:
            txtFile.write(encrypted_message)

        print(f"Encrypted message written to 'cipher.txt'.")


    def txtFileDecryption(self):
        if self.n is None or self.d is None:
            print("Keys not generated or private key not available. Please generate keys first.")
            return

        try:
            # Read the encrypted message from the file
            with open('cipher.txt', 'r') as txtFile:
                encrypted_message = txtFile.read()

            print("File 'cipher.txt' found and read successfully.")

            length = len(str(self.n))
            decryption_key = int(input("Enter decryption key: "))

            # Split the encrypted message into chunks of fixed length
            try:
                encrypted_numbers = [int(encrypted_message[i:i+length]) for i in range(0, len(encrypted_message), length)]
            except ValueError:
                print("Invalid input. Please ensure the encrypted message is a valid concatenation of numbers.")
                return

            # Decrypt the numeric representation of the message
            decrypted_numbers = [self.modular_exponentiation(num, decryption_key, self.n) for num in encrypted_numbers]

            # Convert decrypted numbers back to characters using ASCII
            decrypted_message = self.number_to_string(decrypted_numbers)

            print(f"Decrypted message with private key ({self.n}, {self.d}): {decrypted_message}")

        except FileNotFoundError:
            print("File 'cipher.txt' not found. Please ensure the file exists.")



    def display_menu(self):
        print("\n--- Menu ---")
        print("1. Generate keys")
        print("2. Encrypt a message")
        print("3. Decrypt a message")
        print("4. Encrypt a message to a file")
        print("5. Decrypt a message from a file")
        print("q. Quit")

    def menu(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                self.generateKeys()
                print("\n")
            elif choice == '2':
                self.encryption()
                print("\n")
            elif choice == '3':
                self.decryption()
                print("\n")
            elif choice == '4':
                self.txtFileEncryption()
            elif choice == '5':
                self.txtFileDecryption()
            elif choice.lower() == 'q':
                print("Exiting the menu.")
                break
            else:
                print("Invalid choice. Please try again.")

# Created an instance of RSA and run the menu
rsa = RSA()
rsa.menu()