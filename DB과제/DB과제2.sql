-- 데이터베이스 생성
USE fishbread_db;

-- users 테이블 생성:
CREATE TABLE users(
	user_id INT PRIMARY KEY AUTO_INCREMENT,
    NAME VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    email VARCHAR(100) UNIQUE,
    is_business BOOLEAN DEFAULT FALSE
);

-- orders 테이블 생성:
CREATE TABLE orders(
	order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    order_date DATE,
    amount DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
-- inventory 테이블 생성:
CREATE TABLE inventory(
	item_id INT PRIMARY KEY AUTO_INCREMENT,
    item_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL
    );

-- sales 테이블 생성:
CREATE TABLE sales(
	sale_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    item_id INT,
    quantity_sold INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (item_id) REFERENCES inventory(item_id)
);

-- daily_sales 테이블 생성:
CREATE TABLE daily_sales(
	date DATE PRIMARY KEY,
    total_sales DECIMAL(10,2) NOT NULL
);
