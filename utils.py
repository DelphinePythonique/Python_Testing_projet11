def clubs_file(app):
    db_path = app.config["DB_PATH"]
    return f"{db_path}clubs.json"


def competitions_file(app):
    db_path = app.config["DB_PATH"]
    return f"{db_path}competitions.json"


def bookings_file(app):
    db_path = app.config["DB_PATH"]
    return f"{db_path}bookings.json"
