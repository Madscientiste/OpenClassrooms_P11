import html


def test_index(client, data):
    res = client.get("/")
    assert res.status_code == 200


def test_login(client, data):
    clubs = data["clubs"]
    valid_email = clubs.get_random("email")

    res = client.post("/summary", data={"email": valid_email}, follow_redirects=True)
    assert res.status_code == 200

    res = client.post("/summary", data={"email": "ayaya@gmail.com"}, follow_redirects=True)
    assert res.status_code == 401


def test_booking_case1(client, data):
    """Test if we can book more seats than are available"""

    club = data["clubs"].get_by("name", "She Lifts", first=True)
    competition = data["competitions"].get_by("name", "Spring Festival", first=True)

    res = client.post(
        "/confirm_booking",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "seats": 14,
        },
        follow_redirects=True,
    )

    assert res.status_code == 200, "didn't return 200"
    assert b"Sorry, we don&#39;t have enough seats available for that competition." in res.data


def test_booking_case2(client, data):
    """Test if we can book more than 12 seats at once"""

    club = data["clubs"].get_by("name", "She Lifts", first=True)
    competition = data["competitions"].get_by("name", "AYAYA Festival", first=True)

    res = client.post(
        "/confirm_booking",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "seats": 14,
        },
        follow_redirects=True,
    )

    assert res.status_code == 200, "didn't return 200"
    assert b"Sorry, we can only book up to 12 seats at a time." in res.data


def test_booking_case3(client, data):
    """Test if we can book a competition that has already passed"""

    club = data["clubs"].get_by("name", "She Lifts", first=True)
    competition = data["competitions"].get_by("name", "IBM 5100 Competition", first=True)

    res = client.post(
        "/confirm_booking",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "seats": 8,
        },
        follow_redirects=True,
    )

    assert res.status_code == 200, "didn't return 200"
    assert b"Sorry, that competition has already passed." in res.data


def test_booking_case4(client, data):
    """Test if the points are correctly deducted after a booking"""

    club = data["clubs"].get_by("name", "She Lifts", first=True)
    competition = data["competitions"].get_by("name", "Futuristic Friday", first=True)

    res = client.post(
        "/confirm_booking",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "seats": 4,
        },
        follow_redirects=True,
    )

    assert res.status_code == 200, "didn't return 200"
    assert b"Great-booking complete!" in res.data
    assert b"Points available: 15" in res.data


def test_booking_case5(client, data):
    """Test if we can book if we don't have enough club points"""

    club = data["clubs"].get_by("name", "UPNP port", first=True)
    competition = data["competitions"].get_by("name", "Futuristic Friday", first=True)

    res = client.post(
        "/confirm_booking",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "seats": 4,
        },
        follow_redirects=True,
    )

    assert res.status_code == 200, "didn't return 200"
    assert b"Sorry, you don&#39;t have enough points to book seats." in res.data
