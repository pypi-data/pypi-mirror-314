import os

import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path


def generate(invoices_path, pdfs_path, company_name, image_path, product_id, product_name, amount_purchased,
             price_per_unit, total_price):
    """
    This function converts invoice Excel files into pdf invoices.
    :param invoices_path:
    :param pdfs_path:
    :param company_name:
    :param image_path:
    :param product_id:
    :param product_name:
    :param amount_purchased:
    :param price_per_unit:
    :param total_price:
    :return:
    """
    filepaths = glob.glob(f"{invoices_path}/*.xlsx")
    for filepath in filepaths:

        filename = Path(filepath).stem
        invoice_nr, date  = filename.split("-")


        pdf = FPDF(orientation="p", unit="mm", format="A4")

        pdf.add_page()

        pdf.set_font(family="Times", size=16, style="IB")
        pdf.cell(w=50, h=8, txt=f"Invoice nr. {invoice_nr}", ln=1)
        pdf.set_font(family="Times", size=16, style="IB")
        pdf.cell(w=50, h=8, txt=f"Date: {date}", ln=1)
        pdf.cell(w=50, h=8, ln=1)
        pdf.line(10,30,210,30)

        df = pd.read_excel(filepath, sheet_name="Sheet 1")
        headers = list(df.columns)
        headers = [x.replace("_"," ").title() for x in headers]

        # add a header
        pdf.set_font(family="Times", size=10, style="B")
        pdf.set_text_color(0, 10, 10)
        pdf.cell(w=30, h=8, txt=headers[0], border=1)
        pdf.cell(w=75, h=8, txt=headers[1], border=1)
        pdf.cell(w=35, h=8, txt=headers[2], border=1)
        pdf.cell(w=30, h=8, txt=headers[3], border=1)
        pdf.cell(w=20, h=8, txt=headers[4], border=1, ln=1)

        #rows for items
        for index, row in df.iterrows():
            pdf.set_font(family="Times", size = 10)
            pdf.set_text_color(80,80,80)
            pdf.cell(w=30, h=8, txt=str(row[product_id]),border=1)
            pdf.cell(w=75, h=8, txt=str(row[product_name]),border=1)
            pdf.cell(w=35, h=8, txt=str(row[amount_purchased]),border=1)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]),border=1)
            pdf.cell(w=20, h=8, txt=str(row[total_price]),border=1,ln=1)

        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt="", border=0)
        pdf.cell(w=75, h=8, txt="", border=0)
        pdf.cell(w=35, h=8, txt="", border=0)
        pdf.cell(w=30, h=8, txt="Total  ",align="R", border=0)
        pdf.cell(w=20, h=8, txt=str(df["total_price"].sum()), border=1, ln=1)

        # Add total line
        pdf.set_font(family="Times", size=14, style="B")
        pdf.cell(w=30, h=8, txt=f"The total price is {df['total_price'].sum()}", ln=1)
        # add name and logo
        pdf.set_font(family="Times", size=14, style="B")
        pdf.set_text_color(0, 0, 0)
        pdf.cell(w=25, h=8, txt=f"{company_name}")
        pdf.image(image_path, w=10)

        if not os.path.exists(pdfs_path):
            os.mkdir(pdfs_path)
        pdf.output(f"{pdfs_path}/{filename}.pdf")



