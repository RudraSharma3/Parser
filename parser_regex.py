import re


def extract_amount(text):
    patterns = [
        r'Rs\.?\s?(\d+\.?\d*)',
        r'INR\s?(\d+\.?\d*)',
        r'₹\s?(\d+\.?\d*)',
        r'debited by\s?(\d+\.?\d*)',
        r'credited by\s?(\d+\.?\d*)',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return float(match.group(1))

    return None


def extract_type(text):
    text = text.lower()
    if any(word in text for word in ["debited", "spent", "paid", "debit"]):
        return "DEBIT"
    elif any(word in text for word in ["credited", "received", "credit"]):
        return "CREDIT"
    return "UNKNOWN"


def extract_bank(text):
    text = text.lower()
    if "sbi" in text:
        return "SBI"
    elif "hdfc" in text:
        return "HDFC"
    return "UNKNOWN"


def clean_merchant(name):
    name = re.split(r'debit|credited|ref|rs|on|date', name, flags=re.IGNORECASE)[0]
    name = re.sub(r'Refno.*', '', name, flags=re.IGNORECASE)
    name = name.replace('-', ' ')
    return name.strip().title()


def extract_merchant(text):
    patterns = [
        r'trf to\s([A-Za-z0-9\s\-]+?)(?:\sRef|$)',
        r'at\s([A-Za-z0-9\s\-]+?)(?:\sRef|$)',
        r'from\s([A-Za-z0-9\s\-]+?)(?:\sRef|$)',
        r'for\s([A-Za-z0-9\s\-]+?)\s(debit|credited|on)',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return clean_merchant(match.group(1))

    return "UNKNOWN"


def is_person_name(name):
    words = name.split()
    return len(words) >= 2 and all(w.isalpha() for w in words)

def detect_category(merchant):
    merchant_lower = merchant.lower()

    if any(word in merchant_lower for word in ["cafe", "zomato", "swiggy", "restaurant"]):
        return "Food"
    elif any(word in merchant_lower for word in ["amazon", "flipkart"]):
        return "Shopping"
    elif any(word in merchant_lower for word in ["utilities", "electric", "bill"]):
        return "Bills"
    elif any(word in merchant_lower for word in ["mmtc", "gold", "pamp"]):
        return "Investment"
    elif is_person_name(merchant):
        return "P2P"

    return "Other"


def generate_summary(data):
    if data["amount"] and data["merchant"] != "UNKNOWN":
        return f"You {'spent' if data['type']=='DEBIT' else 'received'} ₹{data['amount']} {'at' if data['type']=='DEBIT' else 'from'} {data['merchant']}"
    return "Transaction detected"


def parse_sms_regex(text):
    amount = extract_amount(text)
    merchant = extract_merchant(text)
    txn_type = extract_type(text)
    bank = extract_bank(text)
    category = detect_category(merchant)

    result = {
        "amount": amount,
        "merchant": merchant,
        "bank_name": bank,
        "type": txn_type,
        "category": category,
        "plain_language_summary": ""
    }

    result["plain_language_summary"] = generate_summary(result)

    return result