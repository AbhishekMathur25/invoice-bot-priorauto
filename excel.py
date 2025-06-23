import pandas as pd
import os
from datetime import datetime

def save_invoice_to_excel(invoice_data: dict, output_dir="invoices"):
    os.makedirs(output_dir, exist_ok=True)

    
    purchase_date_str = invoice_data.get("Purchase Date")
    if not purchase_date_str:
        print("'Purchase Date' not found in invoice data.")
        return

    try:
        purchase_date = datetime.strptime(purchase_date_str, "%d-%b-%y")
    except ValueError:
        print("Invalid 'Purchase Date' format. Expected 'DD-MMM-YY'.")
        return

    filename = f"purchases_{purchase_date.strftime('%d-%b-%y')}.xlsx"
    filepath = os.path.join(output_dir, filename)

    
    item_names = invoice_data.get("Items List", [])
    hsn_codes = invoice_data.get("HSN/SAC", [])
    quantities = invoice_data.get("items Quantity", [])
    rates = invoice_data.get("Items Rate", [])
    prices = invoice_data.get("Items Price", [])

    
    max_len = max(len(item_names), len(hsn_codes), len(quantities), len(rates), len(prices), 1)

    def normalize(lst):
        return lst + [None] * (max_len - len(lst))  # Use None = null in Excel

    items_df = pd.DataFrame({
        "Invoice Number": [invoice_data.get("Invoice Number")] * max_len,
        "Purchase Date": [purchase_date_str] * max_len,
        "Motor Vehicle Number": [invoice_data.get("Motor Vehicle Number")] * max_len,
        "Seller Name": [invoice_data.get("Seller Name")] * max_len,
        "HSN/SAC": normalize(hsn_codes),
        "Item Name": normalize(item_names),
        "Quantity": normalize(quantities),
        "Rate": normalize(rates),
        "Price": normalize(prices)
    })

    # Add empty row between invoices
    empty_row = pd.DataFrame([ [None] * len(items_df.columns) ], columns=items_df.columns)

    if os.path.exists(filepath):
        existing_df = pd.read_excel(filepath)
        combined_df = pd.concat([existing_df, empty_row, items_df], ignore_index=True)
    else:
        combined_df = items_df

    combined_df.to_excel(filepath, index=False)
    print(f"✅ Invoice saved to: {filepath}")
