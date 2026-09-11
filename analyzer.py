import re
from urllib.parse import urlparse


def analyze_email(sender, subject, body):
    score = 0
    indicators = []

    text = (subject + " " + body).lower()

    # 1. Extract URLs
    urls = re.findall(r"https?://[^\s]+", text)

    # 2. Extract URL domains
    domains = []

    for url in urls:
        parsed_url = urlparse(url)
        domains.append(parsed_url.netloc)

    # 3. Extract sender domain
    sender_domain = sender.split("@")[-1]

    # 4. Check urgent language
    urgent_words = [
        "urgent",
        "immediately",
        "as soon as possible"
    ]

    for word in urgent_words:
        if word in text:
            score += 15
            indicators.append("Urgent language")
            break

    # 5. Check password request
    password_words = [
        "password",
        "verify your password",
        "enter your password"
    ]

    for word in password_words:
        if word in text:
            score += 25
            indicators.append("Password request")
            break

    # 6. Compare sender domain with URL domain
    if urls:
        url_domain = urlparse(urls[0]).netloc

        if sender_domain != url_domain:
            indicators.append("Sender/domain mismatch")

    # 7. Analyze URL
    for url in urls:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        # URL uses an IP address
        if re.match(r"^\d+\.\d+\.\d+\.\d+", domain):
            score += 30
            indicators.append("IP address used in URL")

        # Suspicious words inside URL
        suspicious_url_words = [
            "login",
            "verify",
            "secure",
            "account",
            "password"
        ]

        for word in suspicious_url_words:
            if word in url:
                score += 30
                indicators.append("Suspicious URL keywords")
                break

    # 8. Keep score between 0 and 100
    score = min(score, 100)

    # 9. Determine risk level
    if score >= 70:
        risk = "HIGH"
    elif score >= 40:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    # 10. Return analysis result
    return {
        "urls": urls,
        "domains": domains,
        "sender_domain": sender_domain,
        "indicators": indicators,
        "score": score,
        "risk": risk
    }

