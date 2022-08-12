from tests.unit.conftest import client


def test_should_status_code_ok(client):
    response = client.get("/")
    assert response.status_code == 200

def test_should_return_index_template(client):
    response = client.get("/")
    data = response.data.decode('utf-8')
    print(data)
    assert data == """<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GUDLFT Registration</title>
</head>
<body>
    <h1>Welcome to the GUDLFT Registration Portal!</h1>
    
            
    Please enter your secretary email to continue:
    <form action="showSummary" method="post">
        <label for="email">Email:</label>
        <input type="email" name="email" id=""/>
        <button type="submit">Enter</button>
    </form>
  
</body>
</html>"""