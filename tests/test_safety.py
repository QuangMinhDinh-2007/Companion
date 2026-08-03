from app.core.safety import check_for_crisis, get_crisis_response, CRISIS_HOTLINES

def test_detects_crisis():
    assert check_for_crisis("I want to kill myself") == True

def test_ignores_normal_sadness():
    assert check_for_crisis("I had a really bad day") == False

def test_case_insensitive():
    assert check_for_crisis("I WANT TO HURT MYSELF") == True

def test_empty_message():
    assert check_for_crisis("") == False

def test_crisis_response_has_hotline():
    response = get_crisis_response()
    assert any(num in response for num in CRISIS_HOTLINES.values())