from analyzer import analyze_email


def test_normal_email():
    result = analyze_email(
        "teacher@university.edu",
        "Tomorrow's class",
        "Hello, tomorrow's class will start at 9 AM."
    )

    assert result["score"] == 0
    assert result["risk"] == "LOW"



def test_phishing_email():
    result = analyze_email(
        "security@company.com",
        "URGENT: Your account will be suspended",
        "You must verify your password immediately. "
        "Click here: https://fake-login.com/verify"
    )

    assert result["score"] == 70
    assert result["risk"] == "HIGH"    



def test_ip_url():
    result = analyze_email(
        "admin@company.com",
        "Account verification",
        "Please verify your account here: "
        "http://192.168.1.50/login"
    )

    assert result["score"] == 60
    assert result["risk"] == "MEDIUM"    