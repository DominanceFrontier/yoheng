DROP DATABASE IF EXISTS yoheng$default;

CREATE DATABASE yoheng$default;

USE yoheng$default;

CREATE TABLE User (
id INT NOT NULL AUTO_INCREMENT,
fullname VARCHAR(256),
username VARCHAR(25) UNIQUE NOT NULL,
password VARCHAR(25) NOT NULL,
PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE TABLE Friend (
id INT NOT NULL AUTO_INCREMENT,
User1_id INT NOT NULL,
User2_id INT NOT NULL,
PRIMARY KEY (id),
FOREIGN KEY (User1_id) REFERENCES User(id),
FOREIGN KEY (User2_id) REFERENCES User(id)
) ENGINE=InnoDB;

CREATE TABLE Article (
id INT NOT NULL AUTO_INCREMENT,
User_id INT NOT NULL,
title VARCHAR(256) NOT NULL,
body TEXT,
PRIMARY KEY (id),
FOREIGN KEY (User_id) REFERENCES User(id)
) ENGINE=InnoDB;

CREATE TABLE Tag (
id INT NOT NULL AUTO_INCREMENT,
line VARCHAR(256) UNIQUE NOT NULL,
PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE TABLE Perm (
id INT NOT NULL AUTO_INCREMENT,
category VARCHAR(256) UNIQUE NOT NULL,
PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE TABLE TravelDest (
id INT NOT NULL AUTO_INCREMENT,
title VARCHAR(256) NOT NULL,
PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE TABLE Article_Tag (
id INT NOT NULL AUTO_INCREMENT,
Article_id INT NOT NULL,
Tag_id INT NOT NULL,
PRIMARY KEY (id),
FOREIGN KEY (Article_id) REFERENCES Article(id),
FOREIGN KEY (Tag_id) REFERENCES Tag(id)
) ENGINE=InnoDB;

CREATE TABLE Article_Perm (
id INT NOT NULL AUTO_INCREMENT,
Article_id INT NOT NULL,
Perm_id INT NOT NULL,
PRIMARY KEY (id),
FOREIGN KEY (Article_id) REFERENCES Article(id),
FOREIGN KEY (Perm_id) REFERENCES Perm(id)
) ENGINE=InnoDB;

CREATE TABLE Article_TravelDest (
id INT NOT NULL AUTO_INCREMENT,
Article_id INT NOT NULL,
TravelDest_id INT NOT NULL,
PRIMARY KEY (id),
FOREIGN KEY (Article_id) REFERENCES Article(id),
FOREIGN KEY (TravelDest_id) REFERENCES TravelDest(id)
) ENGINE=InnoDB;

