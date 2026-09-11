# PhishLens

PhishLens is a small cybersecurity project that analyzes emails and checks for simple phishing indicators.

I built this project to practice Python, backend development, APIs, and basic cybersecurity concepts in one practical project.

## What PhishLens does

The user sends an email to the API with:

* sender
* subject
* body

PhishLens analyzes the email and looks for some suspicious patterns, such as:

* urgent language
* password requests
* suspicious keywords in URLs
* IP addresses used as URLs
* sender domain and URL domain mismatch

The analyzer then calculates a risk score and classifies the email as:

* `LOW`
* `MEDIUM`
* `HIGH`

The project also saves analysis results in a SQLite database.

## How it works

```text
Client / Swagger
       |
       | POST /analyze
       v
   FastAPI API
       |
       v
 Email Analyzer
       |
       v
 Score + Risk
       |
       v
 SQLite Database
```

There is also a history endpoint:

```text
GET /analyses
       |
       v
 SQLite Database
       |
       v
 Previous analyses
```

## Technologies used

* Python
* FastAPI
* Pydantic
* SQLite
* Uvicorn
* Pytest
* Regular Expressions (`re`)
* `urllib.parse`

## Project structure

```text
PhishLens/
│
├── analyzer.py
├── database.py
├── main.py
├── test_analyzer.py
├── requirements.txt
├── phishlens.db
└── README.md
```

### `analyzer.py`

Contains the phishing analysis logic.

It extracts URLs and domains, checks several suspicious indicators, calculates the score, and determines the risk level.

### `database.py`

Handles the SQLite database.

It contains functions for saving analysis results and retrieving previous analyses.

### `main.py`

Contains the FastAPI application and API endpoints.

### `test_analyzer.py`

Contains automated tests for the analyzer using Pytest.

### `requirements.txt`

Contains the Python packages needed to run the project.

## Risk scoring

The current scoring rules are simple rules created for this project.

| Indicator               |          Score |
| ----------------------- | -------------: |
| Urgent language         |            +15 |
| Password request        |            +25 |
| IP address used in URL  |            +30 |
| Suspicious URL keywords |            +30 |
| Sender/domain mismatch  | Indicator only |

The final score is limited to 100.

```text
0 - 39   → LOW
40 - 69  → MEDIUM
70 - 100 → HIGH
```

These scores are part of the current prototype and are not an official phishing detection standard.

## API endpoints

### `GET /`

Checks whether the API is running.

Example response:

```json
{
  "message": "PhishLens API is running"
}
```

### `POST /analyze`

Analyzes an email.

Example request:

```json
{
  "sender": "security@company.com",
  "subject": "URGENT: Your account will be suspended",
  "body": "You must verify your password immediately. Click here: https://fake-login.com/verify"
}
```

Example response:

```json
{
  "urls": [
    "https://fake-login.com/verify"
  ],
  "domains": [
    "fake-login.com"
  ],
  "sender_domain": "company.com",
  "indicators": [
    "Urgent language",
    "Password request",
    "Sender/domain mismatch",
    "Suspicious URL keywords"
  ],
  "score": 70,
  "risk": "HIGH"
}
```

### `GET /analyses`

Returns the previous email analyses saved in the SQLite database.

Example:

```json
[
  {
    "id": 1,
    "sender": "support@example.com",
    "subject": "URGENT: Verify your account",
    "score": 70,
    "risk": "HIGH",
    "created_at": "2026-09-11 14:11:38"
  }
]
```

## Running the project

Clone the repository:

```bash
git clone https://github.com/aaminazerguine/PhishLens.git
cd PhishLens
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI also provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

## Running the tests

Run:

```bash
pytest
```

The current tests cover examples such as:

* a normal email
* a phishing email with several suspicious indicators
* an email containing an IP address in the URL

## Current limitations

PhishLens is a learning project and a prototype.

It does not currently use machine learning, external threat-intelligence services, SPF/DKIM/DMARC verification, or advanced URL reputation checks.

The current score is based on simple rules, so the result should not be considered a final security decision.

## Why I built it

I wanted to move from small Python exercises to a project that connects several concepts together.

While building PhishLens, I practiced:

* Python functions and modules
* regular expressions
* URL parsing
* basic cybersecurity analysis
* REST API concepts
* FastAPI
* JSON requests and responses
* Pydantic validation
* SQLite
* SQL `INSERT` and `SELECT`
* automated testing with Pytest

This project is still evolving as I learn more about backend development and cybersecurity.
