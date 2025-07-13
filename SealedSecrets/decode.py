import base64

def decode_base64_string(encoded_string):
    try:
        # Decode the base64 string
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_string = decoded_bytes.decode('utf-8')
        return decoded_string
    except Exception as e:
        return f"Error decoding base64: {e}"

if __name__ == "__main__":
    encoded = input("Enter Base64 string to decode: ").strip()
    result = decode_base64_string(encoded)
    print(f"\nDecoded Output:\n{result}")
