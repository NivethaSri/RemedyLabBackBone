# app/services/extractor_service.py

import pdfplumber
import docx
import pytesseract
from PIL import Image
import cv2
import json
import csv
import re
import os

def extract_text_from_pdf(file_path):
    full_text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
    return full_text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_image(file_path):
    image = cv2.imread(file_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return pytesseract.image_to_string(gray, config='--psm 6')

def extract_text_from_csv(file_path):
    rows = []
    with open(file_path, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            rows.append(" ".join(row))
    return "\n".join(rows)

def extract_text_from_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return json.dumps(data, indent=2)

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
       return extract_metrics(extract_text_from_pdf(file_path))
    elif ext in [".jpg", ".jpeg", ".png"]:
        return extract_metrics(extract_text_from_image(file_path))
    elif ext == ".docx":
        return extract_metrics(extract_text_from_docx(file_path))
    elif ext == ".csv":
        return extract_metrics(extract_text_from_csv(file_path))
    elif ext == ".json":
        return extract_metrics(extract_text_from_json(file_path))
    else:
        raise ValueError("Unsupported file format")

def contains_numeric(s):
    return bool(re.search(r"\d", s))


def is_clean_test_name(name):
    return bool(re.fullmatch(r"[a-zA-Z0-9()\- %.]+", name.strip()))


def extract_metrics(raw_text):
    lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
    results = []

    tech_keywords = r"(C\.L\.I\.A|C\.M\.I\.A|ELISA|ECLIA|FIA|RCHCM|CMIA|SANDWICH|PHOTOMETRY)"
    value_unit_pattern = r"[<>]?\d+(?:\.\d+)?"
    units_pattern = r"ng/?mL|mg/?dL|µIU/mL|pg/mL|IU/mL|IU/L|gm/dl|lakhs|cells/cumm|mmol/L|microgm/dl|%"
    normal_range_pattern = r"[a-zA-Z0-9<>=:/\.\- \(\)%]+"

    patterns = [
        re.compile(
            rf"(?P<test_name>.+?)\s+(?P<technology>{tech_keywords})\s+(?P<value>{value_unit_pattern})\s*(?P<unit>{units_pattern})",
            re.IGNORECASE,
        ),
        re.compile(
            rf"(?P<test_name>.+?)\s+(?P<value>{value_unit_pattern})\s+(?P<unit>{units_pattern})\s+(?P<normal_range>{normal_range_pattern})?",
            re.IGNORECASE,
        ),
        re.compile(
            rf"(?P<test_name>.+?)\s+(?P<normal_range>{normal_range_pattern})\s+(?P<value>{value_unit_pattern})\s+(?P<unit>{units_pattern})",
            re.IGNORECASE,
        ),
        re.compile(
            rf"(?P<test_name>.+?)\s+(?P<value>{value_unit_pattern})\s*(?P<unit>{units_pattern})",
            re.IGNORECASE,
        ),
    ]

    for line in lines:
        for pattern in patterns:
            match = pattern.match(line)
            if match:
                group_dict = match.groupdict()
                results.append(
                    {
                        "test_name": group_dict.get("test_name", "").strip(),
                        "value": group_dict.get("value", "nil").strip(),
                        "unit": group_dict.get("unit", "").strip(),
                        "technology": group_dict.get("technology", "").strip()
                        if "technology" in group_dict
                        else "",
                        "normal_range": group_dict.get("normal_range", "").strip()
                        if "normal_range" in group_dict
                        else "",
                    }
                )
                break


    cleaned_results = [
        result
        for result in results
        if result["value"].replace(".", "", 1).isdigit()
        and (result.get("normal_range", "") == "" or contains_numeric(result.get("normal_range", "")))
        and is_clean_test_name(result.get("test_name", ""))
    ]
    return cleaned_results

