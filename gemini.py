from google import genai
from google.genai import types
import pathlib
from keymanager import GeminiKeyManager
from dotenv import load_dotenv
import os
from excel import save_invoice_to_excel

# Load .env file for API keys
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
API_KEYS = os.getenv("GEMINI_API_KEYS", "").split(",")

# Create the manager
key_manager = GeminiKeyManager(API_KEYS)

def get_gemini_client():
    return genai.Client(api_key=key_manager.get_key())

def get_invoice_schema():
    return genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "Invoice Number": genai.types.Schema(type=genai.types.Type.STRING),
            "Seller Name": genai.types.Schema(type=genai.types.Type.STRING),
            "Seller Address": genai.types.Schema(type=genai.types.Type.STRING),
            "Seller GSTIN": genai.types.Schema(type=genai.types.Type.STRING),
            "Purchase Date": genai.types.Schema(type=genai.types.Type.STRING),
            "Motor Vehicle Number": genai.types.Schema(type=genai.types.Type.STRING),
            "Items List": genai.types.Schema(
                type=genai.types.Type.ARRAY,
                items=genai.types.Schema(type=genai.types.Type.STRING),
            ),
            "Items Price": genai.types.Schema(
                type=genai.types.Type.ARRAY,
                items=genai.types.Schema(type=genai.types.Type.STRING),
            ),
            "items Quantity": genai.types.Schema(
                type=genai.types.Type.ARRAY,
                items=genai.types.Schema(type=genai.types.Type.STRING),
            ),
            "HSN/SAC": genai.types.Schema(
                type=genai.types.Type.ARRAY,
                items=genai.types.Schema(type=genai.types.Type.NUMBER),
            ),
            "Items Rate": genai.types.Schema(
                type=genai.types.Type.ARRAY,
                items=genai.types.Schema(type=genai.types.Type.STRING),
            ),
            "GST Amount": genai.types.Schema(type=genai.types.Type.NUMBER),
            "Total Amount": genai.types.Schema(type=genai.types.Type.NUMBER),
        }
    )

def processed_marker_path(pdf_path):
    return pdf_path + ".processed"

async def run_gemini_invoice_extraction(pdf_path: str):
    if os.path.exists(processed_marker_path(pdf_path)):
        print(f"[INFO] Skipping already processed: {pdf_path}")
        return None
    client = get_gemini_client()
    filepath = pathlib.Path(pdf_path)
    pdf_data = filepath.read_bytes()
    response_schema = get_invoice_schema()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(data=pdf_data, mime_type="application/pdf"),
            types.Part(text="Extract all invoice details from this PDF.")
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=response_schema,
        )
    )
    key_manager.rotate_key()  # Rotate to next key after each request
    result = response.parsed
    if result:
        save_invoice_to_excel(result)
        # Mark as processed
        with open(processed_marker_path(pdf_path), 'w') as f:
            f.write('processed')
    return result


# import asyncio
# if __name__ == "__main__":
#     result = asyncio.run(run_gemini_invoice_extraction(r"D:\Prior\downloads\2025-06-24\PRIOR AUTO ACCESSORIES BILL NO 09 (PRIMETECH).pdf"))
#     print(json.dumps(result, indent=2))
