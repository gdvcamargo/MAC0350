CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
    username_display TEXT NOT NULL,
    name TEXT NOT NULL,
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

CREATE TABLE roadmap (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    trip_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    FOREIGN KEY (trip_id) REFERENCES trip(id)
);

CREATE TABLE roadmap_item (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    roadmap_id INTEGER NOT NULL,
    FOREIGN KEY (roadmap_id) REFERENCES roadmap(id)
);

CREATE TABLE place (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    expected_price REAL NOT NULL
);

CREATE TABLE roadmap_item_place (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    roadmap_item_id INTEGER NOT NULL,
    place_id INTEGER NOT NULL,
    
    FOREIGN KEY (roadmap_item_id) REFERENCES roadmap_item(id),
    FOREIGN KEY (place_id) REFERENCES place(id)
);
