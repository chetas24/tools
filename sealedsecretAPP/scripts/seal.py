import subprocess
from pathlib import Path

def seal_secret(input_value: str, cert_path: Path, sealed_dir: Path, kubeseal_path: Path,
                 secret_name="dummy-secret", secret_namespace="dummy-namespace", key_name="secret", debug=False):

    def log_debug(msg):
        if debug:
            print(f"\033[1;33m[DEBUG] {msg}\033[0m")

    def print_colored(msg, color_code):
        print(f"\033[{color_code}m{msg}\033[0m")

    print_colored("\n                             🔐 Sealed Secrets Generator", "1;35")
    print("-----------------------------------------")
    print_colored("⚠️  This tool only works if you have a specific folder structure with certificate and kubeseal.exe.", "1;33")

    # Check paths
    if not kubeseal_path.exists():
        raise FileNotFoundError("kubeseal.exe not found.")
    if not cert_path.exists():
        raise FileNotFoundError(f"Certificate file not found: {cert_path}")
    if not sealed_dir.exists():
        sealed_dir.mkdir(parents=True)
        log_debug(f"Created sealed directory: {sealed_dir}")

    if input_value.strip() != input_value:
        raise ValueError("Value contains leading or trailing whitespace.")

    if " " in input_value:
        log_debug(f"Warning: Value contains internal whitespace: '{input_value}'")

    # Create temporary YAML
    secret_yaml = f"""
apiVersion: v1
kind: Secret
metadata:
  name: {secret_name}
  namespace: {secret_namespace}
type: Opaque
stringData:
  {key_name}: {input_value}
"""
    log_debug("Temporary secret YAML created.")

    try:
        result = subprocess.run([
            str(kubeseal_path), "--cert", str(cert_path), "--scope", "cluster-wide", "--format", "yaml"
        ], input=secret_yaml.encode(), capture_output=True, check=True)

        sealed_output = result.stdout.decode()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"kubeseal error: {e.stderr.decode().strip()}")

    # Save to file
    sealed_file = sealed_dir / "latest.yaml"
    sealed_file.write_text(sealed_output)
    log_debug(f"Sealed secret saved to: {sealed_file}")

    return sealed_output
