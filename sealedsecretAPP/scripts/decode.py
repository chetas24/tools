import base64

def decode_base64_string(encoded_string):
    try:
        # Decode the base64 string
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_string = decoded_bytes.decode('utf-8')
        return decoded_string
    except Exception as e:
        return f"Error decoding base64: {e}"

def decode_secret(encoded_string: str, debug: bool = False):
    def log_debug(msg):
        if debug:
            print(f"\033[1;33m[DEBUG] {msg}\033[0m")

    def print_colored(msg, color_code):
        print(f"\033[{color_code}m{msg}\033[0m")

    print_colored("\n                               🧩 Base64 Decoder", "1;35")
    print("-----------------------------------------")

    log_debug(f"Input string: {encoded_string}")

    try:
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_string = decoded_bytes.decode('utf-8')
    except Exception as e:
        print_colored(f"❌ Error decoding base64: {e}", "1;31")
        return None

    print_colored("✅ Decoded Output:", "1;32")
    print("-----------------------------------------")
    print(decoded_string)
    print("-----------------------------------------")
    return decoded_string
