from flask import Flask, render_template, request, redirect, send_file
import pandas as pd
import qrcode
import os
from datetime import datetime

app = Flask(__name__)

# ==================================================
# YOUR LIVE RENDER URL
# ==================================================

BASE_URL = "https://lpt-corporate-deck.onrender.com"

# ==================================================
# BASE DIRECTORY
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==================================================
# FILE PATHS
# ==================================================

PDF_FILE = os.path.join(
    BASE_DIR,
    "corporate_deck.pdf"
)

CSV_FILE = os.path.join(
    BASE_DIR,
    "visitor_leads.csv"
)

QR_FILE = os.path.join(
    BASE_DIR,
    "visiting_card_qr.png"
)

# ==================================================
# GENERATE QR CODE
# ==================================================

def generate_qr():

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )

    qr.add_data(BASE_URL)

    qr.make(fit=True)

    img = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    # SAVE QR CODE
    img.save(QR_FILE)

    print("QR CODE GENERATED SUCCESSFULLY")

generate_qr()

# ==================================================
# HOME PAGE
# ==================================================

@app.route("/")
def home():

    return render_template("form_1.html")

# ==================================================
# SAVE VISITOR DETAILS
# ==================================================

@app.route("/submit", methods=["POST"])
def submit():

    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    company = request.form.get("company")

    time_now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    data = {
        "DateTime": [time_now],
        "Name": [name],
        "Email": [email],
        "Phone": [phone],
        "Company": [company]
    }

    df = pd.DataFrame(data)

    # SAVE TO CSV
    if os.path.exists(CSV_FILE):

        df.to_csv(
            CSV_FILE,
            mode='a',
            header=False,
            index=False
        )

    else:

        df.to_csv(
            CSV_FILE,
            index=False
        )

    return redirect("/deck")

# ==================================================
# OPEN PDF
# ==================================================

@app.route("/deck")
def deck():

    return send_file(
        PDF_FILE,
        mimetype="application/pdf",
        as_attachment=False
    )

# ==================================================
# RUN APPLICATION
# ==================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )