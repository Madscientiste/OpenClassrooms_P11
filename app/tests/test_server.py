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
