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
    # She lift has 16 points, spring festival has only 2 seats available
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
    # She lift has 16 points, spring festival has 16 seats available
    club = data["clubs"].get_by("name", "She Lifts", first=True)
    competition = data["competitions"].get_by("name", "IBM 5100 Competition", first=True)

    res = client.post(
        "/confirm_booking",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "seats": 16,
        },
        follow_redirects=True,
    )

    assert res.status_code == 200, "didn't return 200"
    assert b"Sorry, we can only book up to 12 seats at a time." in res.data
