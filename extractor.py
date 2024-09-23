import pdfplumber
import re

def extract_resume_data(pdf_path):
    extracted_data = {
        "name": None,
        "phone": None,
        "email": None,
        "education": [],
        "work_experience": [],
        "technologies": []
    }

    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    extracted_data['name'] = extract_name(text)
    extracted_data['phone'] = extract_phone(text)
    extracted_data['email'] = extract_email(text)
    extracted_data['education'] = extract_education(text)
    extracted_data['work_experience'] = extract_work_experience(text)
    extracted_data['technologies'] = extract_technologies(text)

    return extracted_data

def extract_name(text): 
    name_pattern =r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)"
    names = re.findall(name_pattern, text)
    return names[0] if names else None

def extract_phone(text):
    phone_pattern = r'\(?[0-9]{3}\)?[-.\s]?[0-9]+[-.\s]?[0-9]+[-.\s]?[0-9]+'
    phone = re.findall(phone_pattern, text)
    return phone[0] if phone else None

def extract_email(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else None

def extract_education(text):
    education_pattern = r'(?:B.E\.?A\.?|B.tech\.?S\.?|M\.?A\.?|M\.?S\.?|Ph\.?D\.?)\s[^\n]+'
    return re.findall(education_pattern, text)

def extract_work_experience(text):
    work_exp_pattern = r'(?:Experience|Work|Employment)[^\n]*\n(.+?)(?=\n[A-Z])'
    return re.findall(work_exp_pattern, text, re.DOTALL)

def extract_technologies(text):
    tech_pattern = r'\b(?:Python|Java|C\+\+|JavaScript|SQL|HTML|CSS|Ruby)\b'
    return list(set(re.findall(tech_pattern, text)))
