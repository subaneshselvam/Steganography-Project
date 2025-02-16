from PIL import Image

# Convert binary data to a message
def bin_to_message(binary_data):
    message = ''
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        message += chr(int(byte, 2))
    return message

# Decode message from image using the password
def decode_image(image_path, password):
    img = Image.open(image_path).convert('RGB')
    data = ''
    password_found = False
    binary_password = ''.join(format(ord(c), '08b') for c in password)  # Convert password to binary

    for row in range(img.height):
        for col in range(img.width):
            pixel = list(img.getpixel((col, row)))
            for color in range(3):
                data += str(pixel[color] & 1)  # Get the least significant bit (LSB)
                
                # If password is found, start extracting the hidden message
                if len(data) == len(binary_password) and not password_found:
                    if data == binary_password:
                        password_found = True
                        data = ''  # Reset data for message extraction
                        break
            if password_found: break
        if password_found: break

    if password_found:
        hidden_message = bin_to_message(data)
        print("Decoded Message:", hidden_message)
    else:
        print("Password not found. Unable to decode message.")

# Main function for decoding
if __name__ == '__main__':
    # Image name is fixed as 'Subanesh.png'
    image_name = "Subanesh.png"  # Image name fixed
    password = input("Enter the password used for hiding the message: ")

    try:
        decode_image(image_name, password)
    except Exception as e:
        print(f"Error: {e}")
