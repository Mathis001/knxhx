USE potholes;

INSERT INTO status(`name`) VALUES
('Under Review'),
('In Queue'), 
('In Progress'),
('Done');

INSERT INTO priority(`name`) VALUES ('Default');

CREATE USER 'knoxpotholes'@'localhost' IDENTIFIED BY 'knoxpotholes';
GRANT ALL PRIVILEGES ON potholes.* TO 'knoxpotholes'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
