import os
import qrcode
import json
import uuid
from PIL import Image
from encryption import encrypt_data


class QRGenerator:

    def __init__(self, secure=False, output_dir="qr"):
        self.secure = secure
        self.output_dir = output_dir
        self._ensure_output_directory()

    # Ensure qr directory exists
    def _ensure_output_directory(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def build_payload(self, data: dict) -> str:
        qr_type = data.get("type")

        if qr_type == "text":
            payload = data.get("content")

        elif qr_type == "url":
            payload = data.get("url")

        elif qr_type == "email":
            payload = f"mailto:{data['email']}?subject={data.get('subject','')}&body={data.get('body','')}"

        elif qr_type == "phone":
            payload = f"tel:{data['number']}"

        elif qr_type == "sms":
            payload = f"SMSTO:{data['number']}:{data.get('message','')}"

        elif qr_type == "wifi":
            payload = f"WIFI:T:{data.get('security','WPA')};S:{data['ssid']};P:{data['password']};;"

        elif qr_type == "vcard":
            payload = f"""BEGIN:VCARD
VERSION:3.0
FN:{data['name']}
ORG:{data.get('organization','')}
TITLE:{data.get('title','')}
TEL:{data.get('phone','')}
EMAIL:{data.get('email','')}
URL:{data.get('website','')}
END:VCARD"""

        elif qr_type == "geo":
            payload = f"geo:{data['latitude']},{data['longitude']}"

        elif qr_type == "event":
            payload = f"""BEGIN:VEVENT
SUMMARY:{data['title']}
LOCATION:{data.get('location','')}
DTSTART:{data['start']}
DTEND:{data['end']}
END:VEVENT"""

        elif qr_type == "crypto_wallet":
            payload = f"{data['network']}:{data['address']}"

        elif qr_type == "json":
            payload = json.dumps(data["payload"])

        elif qr_type == "raw":
            payload = data["content"]

        else:
            payload = json.dumps(data)

        if self.secure:
            payload = encrypt_data(payload)

        return payload

    def generate(self,
                 data: dict,
                 filename=None,
                 logo_path=None,
                 fill_color="black",
                 back_color="white"):

        payload = self.build_payload(data)

        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4
        )

        qr.add_data(payload)
        qr.make(fit=True)

        img = qr.make_image(
            fill_color=fill_color,
            back_color=back_color
        ).convert("RGBA")  # Important for transparency

        # --------------------------
        # LOGO INSERTION (SAFE)
        # --------------------------
        if logo_path:

            if not os.path.exists(logo_path):
                print(f"[WARNING] Logo not found: {logo_path}")
            else:
                logo = Image.open(logo_path).convert("RGBA")

                qr_width, qr_height = img.size
                logo_size = qr_width // 4  # 25% of QR width

                logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

                pos = (
                    (qr_width - logo_size) // 2,
                    (qr_height - logo_size) // 2
                )

                img.paste(logo, pos, mask=logo)

        # --------------------------

        if not filename:
            filename = f"{uuid.uuid4().hex}.png"

        if not filename.endswith(".png"):
            filename += ".png"

        full_path = os.path.join(self.output_dir, filename)

        img.save(full_path)

        print(f"[SUCCESS] QR Code saved as {full_path}")




























if __name__ == "__main__":

    generator = QRGenerator()

    generator.generate(
        {
            "type": "url",
            "url": "https://www.linkedin.com/in/chemiosis-daniel-34542826a"
        },
        filename="linkedin",
        logo_path="logo/linkedin.png"
    )

    generator.generate(
        {
            "type": "url",
            "url": "https://www.youtube.com/@eruditewbt"
        },
        filename="youtube",
        logo_path="logo/youtube.png"
    )

    generator.generate(
        {
            "type": "url",
            "url": "https://x.com/gbenga_oje16648"
        },
        filename="x",
        logo_path="logo/x.png"
    )

    generator.generate(
        {
            "type": "url",
            "url": "https://chat.whatsapp.com/KJFAGqSsiNCAln0ZDJT6OO?mode=gi_c"
        },
        filename="whatsappgroup",
        logo_path="logo/whatsappgroup.png"
    )


    # # Example 2: WiFi
    # generator.generate({
    #     "type": "wifi",
    #     "ssid": "DanNetwork",
    #     "password": "SuperSecure123",
    #     "security": "WPA"
    # }, filename="wifi_qr.png")


    # # Example 3: Phone
    # generator.generate({
    #     "type": "phone",
    #     "number": "+2348000000000"
    # }, filename="phone_qr.png")


    # # Example 4: JSON data
    # generator.generate({
    #     "type": "json",
    #     "payload": {
    #         "name": "Dan",
    #         "department": "Software Engineering",
    #         "level": 300
    #     }
    # }, filename="json_qr.png")


    # # Example 5: Secure encrypted QR
    # secure_gen = QRGenerator(secure=True)
    # secure_gen.generate({
    #     "type": "text",
    #     "content": "Confidential Data"
    # }, filename="secure_qr.png")