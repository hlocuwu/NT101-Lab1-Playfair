import numpy as np
import random
import math

def get_key_matrix(key, n):
    """Chuyển chuỗi key thành ma trận khóa n x n"""
    key = key.upper()
    key_numbers = [ord(char) - ord('A') + 1 if char != 'Z' else 0 for char in key]  # A=1, B=2, ..., Z=00

    # Nếu key chưa đủ, bổ sung bằng 'X' (X = 24)
    while len(key_numbers) < n * n:
        key_numbers.append(ord('X') - ord('A') + 1)

    key_matrix = np.array(key_numbers).reshape(n, n)
    return key_matrix

def generate_random_key(n):
    """Tạo key ngẫu nhiên với kích thước n x n, đảm bảo định thức nguyên tố cùng nhau với 26"""
    while True:
        # Tạo key ngẫu nhiên
        key = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(n * n))
        key_matrix = get_key_matrix(key, n)

        # Tính định thức
        det = int(round(np.linalg.det(key_matrix)))
        det = det % 26  # Lấy định thức modulo 26

        # Kiểm tra xem định thức có nguyên tố cùng nhau với 26 không
        if math.gcd(det, 26) == 1:
            return key

def mod_inverse_matrix(matrix, mod):
    """Tính ma trận nghịch đảo theo modulo"""
    det = int(round(np.linalg.det(matrix)))  # Tính định thức
    det_inv = pow(det, -1, mod)  # Tính nghịch đảo của định thức modulo mod

    adjugate = np.linalg.inv(matrix) * det
    adjugate = np.round(adjugate).astype(int)  # Làm tròn và chuyển thành số nguyên
    inverse_matrix = (det_inv * adjugate) % mod  # Ma trận nghịch đảo

    return inverse_matrix

def text_to_numbers(text):
    """Chuyển đổi văn bản thành số (A=1, ..., Y=25, Z=00)"""
    return [ord(char) - ord('A') + 1 if char != 'Z' else 0 for char in text]

def numbers_to_text(numbers):
    """Chuyển đổi số thành văn bản (1=A, ..., 25=Y, 00=Z)"""
    return ''.join(chr(num + ord('A') - 1) if num != 0 else 'Z' for num in numbers)

def prepare_text(text, size):
    """Chuẩn bị văn bản: viết hoa, loại bỏ khoảng trắng, thêm ký tự nếu thiếu"""
    text = text.upper().replace(" ", "")
    while len(text) % size != 0:
        text += 'X'  # Thêm 'X' nếu thiếu (X = 24)
    return text

def hill_encrypt(plaintext, key_matrix):
    """Mã hóa văn bản bằng Hill Cipher"""
    n = len(key_matrix)
    plaintext = prepare_text(plaintext, n)
    numbers = text_to_numbers(plaintext)

    ciphertext_numbers = []
    for i in range(0, len(numbers), n):
        block = np.array(numbers[i:i+n])
        encrypted_block = np.dot(key_matrix, block) % 26  # Mã hóa từng block
        ciphertext_numbers.extend(encrypted_block)

    return numbers_to_text(ciphertext_numbers)

def hill_decrypt(ciphertext, key_matrix):
    """Giải mã văn bản bằng Hill Cipher"""
    n = len(key_matrix)
    key_inverse = mod_inverse_matrix(key_matrix, 26)
    numbers = text_to_numbers(ciphertext)

    plaintext_numbers = []
    for i in range(0, len(numbers), n):
        block = np.array(numbers[i:i+n])
        decrypted_block = np.dot(key_inverse, block) % 26  # Giải mã từng block
        plaintext_numbers.extend(decrypted_block)

    return numbers_to_text(plaintext_numbers)

if __name__ == "__main__":
    n = int(input("Nhập kích thước ma trận khóa (n x n): "))
    
    # Tạo key ngẫu nhiên nếu người dùng không nhập key
    key = input("Nhập khóa (chuỗi ký tự, để trống để tạo ngẫu nhiên): ").strip()
    if not key:
        key = generate_random_key(n)
        print(f"Key ngẫu nhiên được tạo: {key}")

    key_matrix = get_key_matrix(key, n)
    print(f"Ma trận khóa {n}x{n}:")
    print(key_matrix)

    # Kiểm tra định thức của ma trận khóa
    det = int(round(np.linalg.det(key_matrix)))
    det = det % 26
    print(f"Định thức của ma trận khóa (mod 26): {det}")
    if math.gcd(det, 26) != 1:
        print("Lỗi: Ma trận khóa không có nghịch đảo modulo 26. Vui lòng thử lại.")
        exit()

    print("\nChọn thao tác:")
    print("1. Mã hóa")
    print("2. Giải mã")
    choice = input("Nhập lựa chọn (1 hoặc 2): ").strip()

    if choice == "1":
        plaintext = input("Nhập văn bản cần mã hóa: ").strip()
        ciphertext = hill_encrypt(plaintext, key_matrix)
        print(f"Văn bản đã mã hóa: {ciphertext}")

    elif choice == "2":
        ciphertext = input("Nhập văn bản cần giải mã: ").strip()
        plaintext = hill_decrypt(ciphertext, key_matrix)
        print(f"Văn bản đã giải mã: {plaintext}")
    else:
        print("Lựa chọn không hợp lệ. Vui lòng nhập 1 hoặc 2.")