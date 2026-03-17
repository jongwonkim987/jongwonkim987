-- CREATE DATABASE Pet_hotel_reservation_system;
USE pet_hotel_reservation_system;

CREATE TABLE petowners(
	owner_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    contact VARCHAR(255)
);
CREATE TABLE pets(
	pet_id INT PRIMARY KEY AUTO_INCREMENT,
    owner_id INT,
    name VARCHAR(100),
    species VARCHAR(100),
    breed VARCHAR(100),
    CONSTRAINT fk_owner FOREIGN KEY (owner_id) REFERENCES petowners(owner_id)
    ON DELETE cascade
    ON UPDATE cascade
);
CREATE TABLE rooms(
	room_id INT PRIMARY KEY AUTO_INCREMENT,
    room_number VARCHAR(100),
    room_type VARCHAR(100),
    price_per_night DECIMAL(10,2)
);
CREATE TABLE reservations(
	reservation_id INT PRIMARY KEY AUTO_INCREMENT,
    pet_id INT,
    room_id INT,
    start_date DATE,
    end_date DATE,
    CONSTRAINT fk_pet_id FOREIGN KEY (pet_id) REFERENCES pets(pet_id)
    ON DELETE cascade
    ON UPDATE cascade,
    CONSTRAINT fk_room_id FOREIGN KEY (room_id) REFERENCES rooms(room_id)
    ON DELETE cascade
    ON UPDATE cascade
);
CREATE TABLE services(
	service_id INT PRIMARY KEY AUTO_INCREMENT,
    reservation_id INT,
    service_name VARCHAR(100),
    service_price DECIMAL(10,2),
    CONSTRAINT fk_reservation_id FOREIGN KEY (reservation_id) REFERENCES reservations(reservation_id)
    ON DELETE cascade
    ON UPDATE cascade
);