from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import fitz  # PyMuPDF
import pdfplumber
import pytesseract
from PIL import Image
import io

app = FastAPI()

@app.post("/api/pdfparse/")
async def parse_pdf(upload: UploadFile = File(...)):
    contents = await upload.read()
    pdf_bytes_io = io.BytesIO(contents)

    # PyMuPDF
    doc = fitz.open(stream=pdf_bytes_io, filetype="pdf")
    pymupdf_text = [{"page": i+1, "text": p.get_text()} for i, p in enumerate(doc)]

    # pdfplumber
    pdf_bytes_io.seek(0)
    plumber_text = []
    with pdfplumber.open(pdf_bytes_io) as pdf:
        for i, p in enumerate(pdf.pages):
            plumber_text.append({"page": i+1, "text": p.extract_text()})

    # OCR with Tesseract
    ocr_text = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        text = pytesseract.image_to_string(img)
        ocr_text.append({"page": i+1, "text": text})

    return JSONResponse({
        "pymupdf": pymupdf_text,
        "pdfplumber": plumber_text,
        "ocr": ocr_text,
    })
