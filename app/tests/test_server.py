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


def test_booking(client, data):
    # shouldn't be able to book more than 12 seats & from whats available
    # Shouldn't be able to book if they don't have enough points (1 point = 1 competition)
    # Shouldn't book a competition if it's date has passed
    club = data["clubs"].get_by("name", "Simply Lift", first=True)
    competition = data["competitions"].get_by("name", "Spring Festival", first=True)

    res = client.post(
        "/confirm_booking",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "seats": 999,
        },
        follow_redirects=True,
    )

    assert res.status_code == 200, "didn't return 200"
    assert b"Sorry, we don&#39;t have enough seats available for that competition." in res.data
