import json


def test_authors(test_app, add_authors):
    # Arrange
    client = test_app.test_client()

    # Act
    resp = client.get("/authors")
    data = json.loads(resp.data)

    # Assert
    assert resp.status_code == 200
    assert data == [
        {
            'birthday': '1998-04-22',
            'id': 1,
            'name': 'Or Moshe'
        },
        {
            'birthday': '1987-06-24',
            'id': 2,
            'name': 'Leo Messi'
        },
    ]
