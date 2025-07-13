import os
import sys
import subprocess
from pathlib import Path



# --- Setup base directories (relative to script location) ---
IS_FROZEN = getattr(sys, 'frozen', False)
BASE_DIR = Path(sys.executable).parent if IS_FROZEN else Path(__file__).parent

SEALED_DIR = BASE_DIR / "sealed"
KEY_DIR = BASE_DIR / "keys"
OUTPUT_DIR = BASE_DIR / "decrypted"
KUBESEAL_BIN = BASE_DIR / "kubeseal.exe"  # Bundled binary

# --- Debug Logging ---
DEBUG = False
if len(sys.argv) > 1 and sys.argv[1] == "debug=true":
    DEBUG = True

def log_debug(msg):
    if DEBUG:
        print(f"[DEBUG] {msg}")

def print_colored(msg, color_code):
    print(f"\033[{color_code}m{msg}\033[0m")

print_colored("🔓 Sealed Secrets Recovery Tool", "1;33")
print("-----------------------------------------")
print_colored("⚠️  This tool only works if the private key matches the certificate used to seal.", "1;33")
print()

# Check for kubeseal binary
if not KUBESEAL_BIN.exists():
    print_colored("❌ kubeseal.exe not found in script directory.", "1;31")
    sys.exit(1)
log_debug(f"Using kubeseal binary at: {KUBESEAL_BIN}")

# --- Validate Sealed Directory ---
if not SEALED_DIR.exists():
    print_colored(f"❌ Directory '{SEALED_DIR}' not found.", "1;31")
    sys.exit(1)

sealed_files = sorted(SEALED_DIR.glob("*.yaml"))
log_debug(f"Found {len(sealed_files)} sealed YAMLs")

if not sealed_files:
    print_colored(f"❌ No SealedSecret YAMLs found in {SEALED_DIR}", "1;31")
    sys.exit(1)

print_colored("📄 Available sealed secrets:", "1;33")
for i, file in enumerate(sealed_files, 1):
    print(f"  [{i}] {file.name}")

try:
    sealed_choice = int(input("Select sealed secret file to decrypt: "))
    if sealed_choice < 1 or sealed_choice > len(sealed_files):
        raise ValueError
except ValueError:
    print_colored("❌ Invalid selection.", "1;31")
    sys.exit(1)

sealed_file = sealed_files[sealed_choice - 1]
log_debug(f"Selected sealed secret file: {sealed_file}")

# --- Validate Key Directory ---
if not KEY_DIR.exists():
    print_colored(f"❌ Directory '{KEY_DIR}' not found.", "1;31")
    sys.exit(1)

key_files = sorted(KEY_DIR.glob("*.key"))
log_debug(f"Found {len(key_files)} key files")

if not key_files:
    print_colored(f"❌ No .key files found in {KEY_DIR}", "1;31")
    sys.exit(1)

print_colored("🔐 Available private keys:", "1;33")
for i, key in enumerate(key_files, 1):
    print(f"  [{i}] {key.name}")

try:
    key_choice = int(input("Select private key to use: "))
    if key_choice < 1 or key_choice > len(key_files):
        raise ValueError
except ValueError:
    print_colored("❌ Invalid key selection.", "1;31")
    sys.exit(1)

key_path = key_files[key_choice - 1]
log_debug(f"Selected key: {key_path}")

# --- Validate Output Directory ---
if not OUTPUT_DIR.exists():
    print_colored(f"❌ Directory '{OUTPUT_DIR}' not found.", "1;31")
    sys.exit(1)

# --- Run Decryption ---
print()
print_colored(f"🔍 Decrypting sealed secret using '{key_path.name}'...", "1;33")
log_debug(f"Command: {KUBESEAL_BIN} --recovery-unseal --recovery-private-key \"{key_path}\" < \"{sealed_file}\"")

try:
    result = subprocess.run(
        [str(KUBESEAL_BIN), "--recovery-unseal", "--recovery-private-key", str(key_path)],
        input=sealed_file.read_bytes(),
        capture_output=True,
        check=True
    )
    decrypted_output = result.stdout.decode()
except subprocess.CalledProcessError as e:
    print_colored("❌ Decryption failed.", "1;31")
    print_colored("🧾 kubeseal error output:", "1;31")
    print(e.stderr.decode())
    sys.exit(1)

# --- Output Decrypted YAML ---
print_colored("✅ Decrypted Secret:", "1;32")
print("-----------------------------------------")
print(decrypted_output)
print("-----------------------------------------")

output_path = OUTPUT_DIR / "latest.yaml"
output_path.write_text(decrypted_output)
log_debug(f"Decrypted YAML saved to {output_path}")

print_colored(f"\n💾 Decrypted secret saved to: {output_path}", "1;32")
