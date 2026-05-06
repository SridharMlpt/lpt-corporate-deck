# ==================================================
# PROFESSIONAL QR LEAD CAPTURE SYSTEM
# FOR VISITING CARD / CORPORATE DECK
# ==================================================

from flask import Flask, render_template, request, redirect, send_file
import pandas as pd
import qrcode
import os
import socket
from datetime import datetime

app = Flask(__name__)

# ==================================================
# AUTO GET LOCAL IP
# ==================================================

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

PORT = 5000

BASE_URL = "https://lpt-corporate-deck.onrender.com"

# ==================================================
# FILE PATHS
# ==================================================

PROJECT_FOLDER = r"C:\Users\LPTTDIV004\PycharmProjects\pythonProject1"

PDF_FILE = os.path.join(
    PROJECT_FOLDER,
    "corporate_deck.pdf"
)

QR_FILE = os.path.join(
    PROJECT_FOLDER,
    "visiting_card_qr.png"
)

CSV_FILE = os.path.join(
    PROJECT_FOLDER,
    "visitor_leads.csv"
)

# ==================================================
# GENERATE QR CODE
# ==================================================

def generate_qr():

    qr = qrcode.QRCode(
        version=1,
        box_size=12,
        border=5
    )

    qr.add_data(BASE_URL)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    img.save(QR_FILE)

    print("\n===================================")
    print("QR CODE GENERATED SUCCESSFULLY")
    print("Saved At:")
    print(QR_FILE)
    print("===================================\n")

generate_qr()

# ==================================================
# HOME PAGE
# ==================================================

@app.route("/")
def home():

    return render_template("form_1.html")

# ==================================================
# SAVE LEAD DETAILS
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

    print("\n=========== NEW VISITOR ===========")
    print("Name    :", name)
    print("Email   :", email)
    print("Phone   :", phone)
    print("Company :", company)
    print("Time    :", time_now)
    print("===================================\n")

    # SAVE DATA
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

    print("===================================")
    print("APPLICATION RUNNING")
    print("Open Browser:")
    print(BASE_URL)
    print("===================================\n")

    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=True
    )