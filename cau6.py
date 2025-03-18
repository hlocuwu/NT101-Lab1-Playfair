def create_playfair_square(key):
    key = key.upper().replace("J", "I")
    key = "".join(dict.fromkeys(key))
    
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    square = []
    for char in key + alphabet:
        if char not in square:
            square.append(char)
    
    return [square[i:i+5] for i in range(0, 25, 5)]

def prepare_text(text):
    text = text.upper().replace(" ", "")
    text = text.replace("J", "I")
    digraphs = []
    for i in range(0, len(text), 2):
        digraph = text[i:i+2]
        if len(digraph) == 1:
            digraph += "X"
        elif digraph[0] == digraph[1]:
            digraph = digraph[0] + "X" + digraph[1]
        digraphs.append(digraph)
    return digraphs

def find_position(square, char):
    for row in range(5):
        for col in range(5):
            if square[row][col] == char:
                return row, col
    return None

def encrypt_digraph(square, digraph):
    a, b = digraph[0], digraph[1]
    row_a, col_a = find_position(square, a)
    row_b, col_b = find_position(square, b)
    
    if row_a == row_b:
        return square[row_a][(col_a + 1) % 5] + square[row_b][(col_b + 1) % 5]
    elif col_a == col_b:
        return square[(row_a + 1) % 5][col_a] + square[(row_b + 1) % 5][col_b]
    else:
        return square[row_a][col_b] + square[row_b][col_a]

def decrypt_digraph(square, digraph):
    a, b = digraph[0], digraph[1]
    row_a, col_a = find_position(square, a)
    row_b, col_b = find_position(square, b)
    
    if row_a == row_b:
        return square[row_a][(col_a - 1) % 5] + square[row_b][(col_b - 1) % 5]
    elif col_a == col_b:
        return square[(row_a - 1) % 5][col_a] + square[(row_b - 1) % 5][col_b]
    else:
        return square[row_a][col_b] + square[row_b][col_a]

def playfair_encrypt(plaintext, key):
    square = create_playfair_square(key)
    digraphs = prepare_text(plaintext)
    ciphertext = ""
    for digraph in digraphs:
        ciphertext += encrypt_digraph(square, digraph)
    return ciphertext

def playfair_decrypt(ciphertext, key):
    square = create_playfair_square(key)
    digraphs = prepare_text(ciphertext)
    plaintext = ""
    for digraph in digraphs:
        plaintext += decrypt_digraph(square, digraph)
    return plaintext

if __name__ == "__main__":
    key = input("Enter the key: ").strip()
    
    print("Choose an option:")
    print("1. Encrypt")
    print("2. Decrypt")
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        plaintext = input("Enter the plaintext: ").strip()
        ciphertext = playfair_encrypt(plaintext, key)
        print(f"Ciphertext: {ciphertext}")
        
    elif choice == "2":
        ciphertext = input("Enter the ciphertext: ").strip()
        plaintext = playfair_decrypt(ciphertext, key)
        print(f"Decrypted Text: {plaintext}")
    else:
        print("Invalid choice. Please choose 1 or 2.")