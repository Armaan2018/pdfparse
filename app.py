from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import pdfplumber
import pytesseract
from PIL import Image
import io

app = Flask(__name__)

@app.route('/extract-text', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        pdf_filename = file.filename
        file.save(pdf_filename)

        # PyMuPDF Extraction
        doc = fitz.open(pdf_filename)
        pymupdf_text = ""
        for page in doc:
            pymupdf_text += page.get_text()

        # pdfplumber Extraction
        with pdfplumber.open(pdf_filename) as pdf:
            pdfplumber_text = ""
            for page in pdf.pages:
                pdfplumber_text += page.extract_text()

        # OCR Extraction
        ocr_text = ""
        for page in doc:
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            ocr_text += pytesseract.image_to_string(img)

        return jsonify({
            "pymupdf_text": pymupdf_text,
            "pdfplumber_text": pdfplumber_text,
            "ocr_text": ocr_text
        })

if __name__ == '__main__':
    app.run(debug=True)
