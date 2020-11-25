CREATE TABLE IF NOT EXISTS City (
city_name varchar(250) NOT NULL,
state varchar(250) NOT NULL,
population int(16) unsigned NOT NULL,
PRIMARY KEY (city_name, state)
);


CREATE TABLE IF NOT EXISTS Store (
store_number int(16) unsigned NOT NULL,
phone_number varchar(20) NOT NULL,
street_address varchar(250) NOT NULL,
city_name varchar(250) NOT NULL,
state varchar(250) NOT NULL,
PRIMARY KEY (store_number),
FOREIGN KEY (city_name, state) REFERENCES City(city_name, state)
);


CREATE TABLE IF NOT EXISTS Date(
dateID varchar(250) NOT NULL,
date_time date NOT NULL UNIQUE,
PRIMARY KEY (dateID)
);


CREATE TABLE IF NOT EXISTS Holiday(
dateID varchar(250) NOT NULL,
holiday_name varchar(250) NOT NULL,
PRIMARY KEY (dateID),
FOREIGN KEY (dateID) REFERENCES Date(dateID)
);


CREATE TABLE IF NOT EXISTS NonHoliday(
dateID varchar(250) NOT NULL,
PRIMARY KEY (dateID),
FOREIGN KEY (dateID) REFERENCES Date(dateID)
);


CREATE TABLE IF NOT EXISTS Membership (
memberID varchar(250) NOT NULL,
signup_date varchar(250) NOT NULL,
store_number int(16) unsigned NOT NULL,
PRIMARY KEY (memberID),
FOREIGN KEY (signup_date) REFERENCES Date(dateID),
FOREIGN KEY (store_number) REFERENCES Store(store_number)
);


CREATE TABLE IF NOT EXISTS YellowJacket (
memberID varchar(250) NOT NULL,
PRIMARY KEY (memberID),
FOREIGN KEY (memberID) REFERENCES Membership(memberID)
);


CREATE TABLE IF NOT EXISTS GiantHornet (
memberID varchar(250) NOT NULL,
PRIMARY KEY (memberID),
FOREIGN KEY (memberID) REFERENCES Membership(memberID)
);


CREATE TABLE IF NOT EXISTS Manufacturer(
manufacturer_name varchar(250) NOT NULL,
max_discount float DEFAULT NULL,
PRIMARY KEY (manufacturer_name),
CHECK (max_discount<0.9)
);


CREATE TABLE IF NOT EXISTS Product(
PID int(16) NOT NULL,
product_name varchar(250) NOT NULL,
retail_price float  NOT NULL,
manufacturer_name varchar(250) NOT NULL,
PRIMARY KEY (PID),
FOREIGN KEY (manufacturer_name) REFERENCES Manufacturer(manufacturer_name)
);


CREATE TABLE IF NOT EXISTS Sold (
store_number int(16) unsigned NOT NULL,
dateID varchar(250) NOT NULL,
PID int(16) NOT NULL,
quantity int(16) unsigned NOT NULL,
PRIMARY KEY (store_number, dateID, PID),
FOREIGN KEY (store_number) REFERENCES Store(store_number),
FOREIGN KEY (dateID) REFERENCES Date(dateID),
FOREIGN KEY (PID) REFERENCES Product(PID)
);


CREATE TABLE IF NOT EXISTS OnSale (
PID int(16) NOT NULL,
dateID varchar(250) NOT NULL,
discount_percentage float NOT NULL DEFAULT 0,
PRIMARY KEY (PID, dateID),
FOREIGN KEY (PID) REFERENCES Product(PID),
FOREIGN KEY (dateID) REFERENCES Date(dateID)
);


CREATE TABLE IF NOT EXISTS Category(
category_name varchar(250) NOT NULL,
PRIMARY KEY (category_name)
);


CREATE TABLE IF NOT EXISTS CategorizedBy(
PID int(16) NOT NULL,
category_name varchar(250) NOT NULL,
PRIMARY KEY (PID, category_name),
FOREIGN KEY (PID) REFERENCES Product(PID),
FOREIGN KEY (category_name) REFERENCES Category(category_name)
);