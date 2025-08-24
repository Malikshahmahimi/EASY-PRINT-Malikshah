# print_all_service.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
from PyPDF2 import PdfReader
# from pptx import Presentation  # if needed
# import win32print, win32com.client  # when you actually print

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # <— allow frontend to call Flask

@app.route("/api/ping", methods=["GET"])
def ping():
    return jsonify(status="ok")

def count_pdf_pages(path: Path) -> int:
    return len(PdfReader(open(path, "rb")).pages)

@app.route("/api/print-all", methods=["POST"])
def print_all():
    """
    Body example:
    {
      "files": [
        {"path": "C:/jobs/abc.pdf", "type":"pdf"},
        {"path": "C:/jobs/notes.pdf", "type":"pdf"}
      ],
      "printerSpeedPPM": 20
    }
    """
    data = request.get_json(force=True) or {}
    files = data.get("files", [])
    ppm = max(1, int(data.get("printerSpeedPPM", 20)))

    total_pages = 0
    for f in files:
        p = Path(f.get("path", ""))
        t = (f.get("type") or "").lower()
        if t == "pdf" and p.exists():
            total_pages += count_pdf_pages(p)
        elif t == "image":
            total_pages += 1
        # TODO: add docx/pptx if you need

    est_time_min = round(total_pages / ppm, 2)

    # TODO: trigger real printing here if you want
    # print_to_windows_printer(files)

    return jsonify(totalPages=total_pages, estTimeMin=est_time_min, started=False)
    
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)