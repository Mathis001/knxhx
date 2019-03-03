USE potholes;

INSERT INTO status(`name`) VALUES
('Under Review'),
('In Queue'), 
('In Progress'),
('Done');

INSERT INTO priority(`name`) VALUES ('Default');
INSERT INTO truck(`name`) VALUES ('Truck 1');

CREATE USER 'knoxpotholes'@'localhost' IDENTIFIED BY 'knoxpotholes';
GRANT ALL PRIVILEGES ON potholes.* TO 'knoxpotholes'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
