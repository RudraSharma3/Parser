# SMS Transaction Parser

A Python project for parsing financial and banking SMS messages using regex rules and Gemini AI structured outputs.

## Features

- **Regex-based Parsing (`parser_regex.py`)**: Rule-based extraction for common transaction formats (SBI, HDFC, amount, merchant, transaction type, category).
- **AI-powered Parsing (`parser.py`)**: Uses Google GenAI (`gemini-2.0-flash`) with Pydantic structured outputs to extract and categorize transactions.
- **Data Models (`models.py`)**: Pydantic models for transactions and transaction types.

## Setup & Usage

1. **Install Dependencies**:
   ```bash
   pip install pydantic google-genai
   ```

2. **Environment Variable (for AI parser)**:
   ```bash
   # Windows PowerShell:
   $env:GOOGLE_API_KEY="your-api-key"

   # Linux/macOS:
   export GOOGLE_API_KEY="your-api-key"
   ```

3. **Run the parser**:
   ```bash
   python main.py
   ```
