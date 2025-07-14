from flask import Flask, render_template, request, redirect, url_for, flash
from pathlib import Path
import os
from scripts.seal import seal_secret
from scripts.decrypt import decrypt_secret
from scripts.decode import decode_secret


app = Flask(__name__)
app.secret_key = "supersecretkey"

# --- Configure paths ---
BASE_DIR = Path(__file__).resolve().parent
CERT_DIR = BASE_DIR / "certs"
SEALED_DIR = BASE_DIR / "sealed"
KEY_DIR = BASE_DIR / "keys"
OUTPUT_DIR = BASE_DIR / "decrypted"
KUBESEAL_BIN = BASE_DIR / "kubeseal.exe"

@app.route("/")
def index():
    certs = [f.name for f in CERT_DIR.glob("*.crt")]
    sealed_files = [f.name for f in SEALED_DIR.glob("*.yaml")]
    key_files = [f.name for f in KEY_DIR.glob("*") if f.is_file()]

    return render_template("index.html", certs=certs, sealed_files=sealed_files, key_files=key_files)

@app.route("/seal", methods=["POST"])
def seal():
    value = request.form.get("secret_value")
    cert_name = request.form.get("cert_name")
    cert_path = CERT_DIR / cert_name

    try:
        sealed_output = seal_secret(
            input_value=value,
            cert_path=cert_path,
            sealed_dir=SEALED_DIR,
            kubeseal_path=KUBESEAL_BIN
        )
        return render_template("result.html", title="Sealed Output", result=sealed_output)
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("index"))

@app.route("/decrypt", methods=["POST"])
def decrypt():
    sealed_name = request.form.get("sealed_file")
    key_name = request.form.get("key_file")

    try:
        decrypted_output = decrypt_secret(
            sealed_file=SEALED_DIR / sealed_name,
            key_path=KEY_DIR / key_name,
            output_dir=OUTPUT_DIR,
            kubeseal_path=KUBESEAL_BIN
        )
        return render_template("result.html", title="Decrypted Output", result=decrypted_output)
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("index"))

@app.route("/decode", methods=["POST"])
def decode():
    b64_string = request.form.get("encoded_string")
    decoded_output = decode_secret(b64_string, debug=True)
    return render_template("result.html", title="Decoded Output", result=decoded_output)

if __name__ == "__main__":
    app.run(debug=True)
