import os
import sys
import subprocess
from pathlib import Path

# Constants
SECRET_NAME = "dummy-secret"
SECRET_NAMESPACE = "dummy-namespace"
KEY_NAME = "secret"

# Detect if running as .exe
IS_FROZEN = getattr(sys, 'frozen', False)
BASE_DIR = Path(sys.executable).parent if IS_FROZEN else Path(__file__).parent

CERT_DIR = BASE_DIR / "certs"
SEALED_DIR = BASE_DIR / "sealed"
KUBESEAL_CMD = BASE_DIR / "kubeseal.exe"

# Debug Mode
DEBUG = False
if len(sys.argv) > 1 and sys.argv[1] == "debug=true":
    DEBUG = True

def log_debug(msg):
    if DEBUG:
        print(f"\033[1;33m[DEBUG] {msg}\033[0m")

def print_colored(msg, color_code):
    print(f"\033[{color_code}m{msg}\033[0m")

print_colored("\n                             🔐 Sealed Secrets Generator", "1;35")
print("-----------------------------------------")
print_colored("⚠️  This tool only works if you have a specific folder structure with certificate and kubeseal.exe.", "1;33")

# Check kubeseal binary
log_debug(f"Looking for kubeseal: {KUBESEAL_CMD}")
if not KUBESEAL_CMD.exists():
    print_colored("❌ kubeseal.exe not found next to script. Please place it in the same directory.", "1;31")
    sys.exit(1)

# Check cert directory
if not CERT_DIR.exists():
    print_colored(f"❌ Directory '{CERT_DIR}' not found. Please create it and add your .crt files.", "1;31")
    sys.exit(1)

cert_files = sorted(CERT_DIR.glob("*.crt"))
if not cert_files:
    print_colored(f"❌ No certificates (.crt) found in {CERT_DIR}", "1;31")
    sys.exit(1)

# Select certificate
print_colored(f"\n📄 Available certificates:", "1;34")
for i, cert in enumerate(cert_files, 1):
    print(f"  [{i}] {cert.name}")

try:
    cert_choice = int(input("\nEnter the number of the certificate to use: "))
    if cert_choice < 1 or cert_choice > len(cert_files):
        raise ValueError
except ValueError:
    print_colored("❌ Invalid certificate selection.", "1;31")
    sys.exit(1)

cert_path = cert_files[cert_choice - 1]
log_debug(f"Selected certificate: {cert_path}")

# Input secret value
input_value = input("\nEnter the value to seal: ")

if input_value.strip() != input_value:
    print_colored("❌ Error: Value contains leading or trailing whitespace. Please remove it and try again.", "1;31")
    sys.exit(1)

if " " in input_value:
    print("\n⚠️  Warning: Your value contains whitespace inside:")
    print(f"    ➤ '{input_value}'")
    confirm = input("Are you sure you want to continue? (y/n): ").lower()
    if confirm != 'y':
        print_colored("❌ Aborted by user.", "1;31")
        sys.exit(1)

# Check sealed directory
if not SEALED_DIR.exists():
    print_colored(f"❌ Directory '{SEALED_DIR}' not found. Please create it.", "1;31")
    sys.exit(1)

# Construct temporary YAML
secret_yaml = f"""
apiVersion: v1
kind: Secret
metadata:
  name: {SECRET_NAME}
  namespace: {SECRET_NAMESPACE}
type: Opaque
stringData:
  {KEY_NAME}: {input_value}
"""
log_debug("Temporary secret YAML created.")

# Run kubeseal
log_debug("Running kubeseal...")
try:
    result = subprocess.run([
        str(KUBESEAL_CMD), "--cert", str(cert_path), "--scope", "cluster-wide", "--format", "yaml"
    ], input=secret_yaml.encode(), capture_output=True, check=True)
    sealed_output = result.stdout.decode()
except subprocess.CalledProcessError as e:
    print_colored("❌ Failed to seal secret. kubeseal returned an error.", "1;31")
    print_colored(e.stderr.decode(), "1;31")
    sys.exit(1)

# Output result
print_colored(f"\n🔍 sealing secret using '{cert_path.name}'...", "1;33")
print_colored("✅ SealedSecret:", "1;32")
print("-------------------------------------------")
print(sealed_output)
print("-------------------------------------------")

# Save to file
sealed_file = SEALED_DIR / "latest.yaml"
with open(sealed_file, "w") as f:
    f.write(sealed_output)

log_debug(f"Sealed secret saved to: {sealed_file}")
print_colored(f"\n💾 YAML saved to: {sealed_file}", "1;32")  # Green
print()