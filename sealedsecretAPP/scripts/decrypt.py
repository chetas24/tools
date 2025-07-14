import subprocess
from pathlib import Path

def decrypt_secret(sealed_file: Path, key_path: Path, output_dir: Path, kubeseal_path: Path, debug=False):

    def log_debug(msg):
        if debug:
            print(f"\033[1;33m[DEBUG] {msg}\033[0m")

    def print_colored(msg, color_code):
        print(f"\033[{color_code}m{msg}\033[0m")

    print_colored("\n                               🔓 Sealed Secrets Decrypter", "1;35")
    print("-----------------------------------------")
    print_colored("⚠️  This tool only works if the private key matches the certificate used to seal.", "1;33")
    print()

    # Check paths
    if not kubeseal_path.exists():
        raise FileNotFoundError("kubeseal.exe not found in script directory.")
    log_debug(f"Using kubeseal binary at: {kubeseal_path}")

    if not sealed_file.exists():
        raise FileNotFoundError(f"Sealed secret file '{sealed_file}' not found.")
    log_debug(f"Selected sealed secret file: {sealed_file}")

    if not key_path.exists():
        raise FileNotFoundError(f"Private key file '{key_path}' not found.")
    log_debug(f"Selected key: {key_path}")

    if not output_dir.exists():
        output_dir.mkdir(parents=True)
        log_debug(f"Created output directory: {output_dir}")

    # Run kubeseal
    print()
    print_colored(f"🔍 Decrypting sealed secret using '{key_path.name}'...", "1;33")
    log_debug(f"Command: {kubeseal_path} --recovery-unseal --recovery-private-key \"{key_path}\" < \"{sealed_file}\"")

    try:
        result = subprocess.run(
            [str(kubeseal_path), "--recovery-unseal", "--recovery-private-key", str(key_path)],
            input=sealed_file.read_bytes(),
            capture_output=True,
            check=True
        )
        decrypted_output = result.stdout.decode()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"kubeseal error: {e.stderr.decode().strip()}")

    # Save to file
    output_path = output_dir / "latest.yaml"
    output_path.write_text(decrypted_output)
    log_debug(f"Decrypted YAML saved to {output_path}")

    print_colored("✅ Decrypted Secret:", "1;32")
    print("-----------------------------------------")
    print(decrypted_output)
    print("-----------------------------------------")

    print_colored("\n--------------Make sure to copy the decrypted value---------------", "1;36")
    print_colored(f"\n💾 Decrypted secret saved to: {output_path}", "1;32")

    return decrypted_output
