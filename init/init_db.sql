CREATE TABLE IF NOT EXISTS products (
    model VARCHAR(50) PRIMARY KEY,
    maker VARCHAR(10),
    type VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS printers (
    code SERIAL PRIMARY KEY,
    model VARCHAR(50) REFERENCES products(model),
    color CHAR(1),
    type VARCHAR(10),
    price NUMERIC
);

CREATE TABLE IF NOT EXISTS personal_computers (
    code SERIAL PRIMARY KEY,
    model VARCHAR(50) REFERENCES products(model),
    speed INT,
    ram INT,
    hd INT,
    cd VARCHAR(10),
    price NUMERIC
);

CREATE TABLE IF NOT EXISTS laptops (
    code SERIAL PRIMARY KEY,
    model VARCHAR(50) REFERENCES products(model),
    speed INT,
    ram INT,
    hd INT,
    price NUMERIC,
    screen INT
);

INSERT INTO products (model, maker, type) VALUES
('Printer1', 'MakerA', 'Printer'),
('Printer2', 'MakerA', 'Printer'),
('PC1', 'MakerB', 'PC'),
('PC2', 'MakerB', 'PC'),
('Laptop1', 'MakerC', 'Laptop'),
('Laptop2', 'MakerC', 'Laptop');

INSERT INTO printers (model, color, type, price) VALUES
('Printer1', 'Y', 'Laser', 150.00),
('Printer2', 'N', 'Inkjet', 120.00);

INSERT INTO personal_computers (model, speed, ram, hd, cd, price) VALUES
('PC1', 3200, 8, 500, 'DVD', 450.00),
('PC2', 3400, 16, 1000, 'Blu-ray', 550.00);

INSERT INTO laptops (model, speed, ram, hd, price, screen) VALUES
('Laptop1', 2500, 16, 1000, 800.00, 15),
('Laptop2', 2600, 8, 750, 700.00, 13);