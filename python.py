from PIL import Image

# Convert message to binary
def message_to_bin(message):
    return ''.join(format(ord(c), '08b') for c in message)

# Encode message in image
def encode_image(image_path, message, password):
    img = Image.open(image_path).convert('RGB')
    data = message_to_bin(password) + message_to_bin(message)
    if len(data) > img.width * img.height * 3:
        raise ValueError("Message too large")
    
    data_index = 0
    for row in range(img.height):
        for col in range(img.width):
            pixel = list(img.getpixel((col, row)))
            for color in range(3):
                if data_index < len(data):
                    pixel[color] = pixel[color] & 0b11111110 | int(data[data_index])
                    data_index += 1
            img.putpixel((col, row), tuple(pixel))
    
    img.save("encoded_image.png")
    print("Data hidden successfully!")

# Decode message from image
def decode_image(image_path, password):
    img = Image.open(image_path).convert('RGB')
    data, data_index, password_found = '', 0, False
    binary_password = message_to_bin(password)

    for row in range(img.height):
        for col in range(img.width):
            pixel = list(img.getpixel((col, row)))
            for color in range(3):
                data += str(pixel[color] & 1)
                if len(data) == len(binary_password) and not password_found:
                    if data == binary_password:
                        password_found = True
                        data = ''
                        break
            if password_found: break
        if password_found: break

    hidden_message = ''.join(chr(int(data[i:i+8], 2)) for i in range(0, len(data), 8))
    print("Decoded Message:", hidden_message)

# Main
if __name__ == '__main__':
    # Get image file name and password from user
    image_name = input("Subanesh.png")
    message = input("Enter the message to hide: ")
    password = input("Enter a password for secure hiding: ")

    try:
        encode_image(image_name, message, password)
        print("\nDecoding the message from the encoded image...\n")
        decode_image("encoded_image.png", password)
    except Exception as e:
        print(f"Error: {e}")
