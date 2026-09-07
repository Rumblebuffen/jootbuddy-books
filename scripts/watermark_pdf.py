#!/usr/bin/env python3
"""
watermark_pdf.py — stamp a personalised footer onto every page of a PDF
before you email it out.

Usage:
    python3 watermark_pdf.py INPUT.pdf "Buyer Name" ORDER_REF OUTPUT.pdf

Install once:
    pip install pypdf reportlab --break-system-packages
"""

import sys
import io
from datetime import date

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    print("Missing dependency. Run: pip install pypdf reportlab --break-system-packages")
    sys.exit(1)

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import Color
except ImportError:
    print("Missing dependency. Run: pip install pypdf reportlab --break-system-packages")
    sys.exit(1)


def make_stamp_overlay(page_width, page_height, buyer_name, order_ref):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(page_width, page_height))
    text = f"Licensed to {buyer_name} · Order {order_ref} · Please do not redistribute"
    c.setFont("Helvetica", 7)
    c.setFillColor(Color(0, 0, 0, alpha=0.45))
    c.drawCentredString(page_width / 2, 0.35 * 72, text)
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


def watermark(input_path, buyer_name, order_ref, output_path):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        stamp = make_stamp_overlay(width, height, buyer_name, order_ref)
        page.merge_page(stamp)
        writer.add_page(page)

    writer.add_metadata({
        "/LicensedTo": buyer_name,
        "/OrderRef": order_ref,
        "/DeliveredOn": date.today().isoformat(),
    })

    with open(output_path, "wb") as f:
        writer.write(f)

    print(f"Done: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(1)

    input_pdf, buyer, order_ref, output_pdf = sys.argv[1:5]
    watermark(input_pdf, buyer, order_ref, output_pdf)
