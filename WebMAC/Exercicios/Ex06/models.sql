CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username TEXT NOT NULL UNIQUE,
    username_display TEXT NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE usersession (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    token TEXT NOT NULL UNIQUE,
    expires_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE trip (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    destination TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    budget REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
