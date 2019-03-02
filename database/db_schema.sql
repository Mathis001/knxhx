/*Set Database*/


USE potholes;

/*CREATE TABLE zone Database*/


CREATE TABLE IF NOT EXISTS `zone`(
	`id` INT NOT NULL AUTO_INCREMENT,
	`zone_number` VARCHAR(255) NOT NULL,
	`zone_notes` VARCHAR(255) NOT NULL,
	PRIMARY KEY (`id`)
	);

/*CREATE TABLE status Database*/

CREATE TABLE IF NOT EXISTS `status`(
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(255) NOT NULL,
	PRIMARY KEY (`id`)
	);

/*CREATE TABLE reporter Database*/

CREATE TABLE IF NOT EXISTS `reporter`(
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(255) NOT NULL,
	`phone_number` VARCHAR(255) NOT NULL,
	PRIMARY KEY (`id`)
	);

/*CREATE TABLE reported Database*/


CREATE TABLE IF NOT EXISTS `reported` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`status_id` INT NOT NULL,
	`wo_number` VARCHAR(255) NOT NULL,
	`req_number` VARCHAR(255) NOT NULL,
	`zone_id` VARCHAR(255) NOT NULL,
	`reporter_id` VARCHAR(255) NOT NULL,
	PRIMARY KEY (`id`),
	FOREIGN KEY (`status_id`) REFERENCES status(`id`),
	FOREIGN KEY (`zone_id`) REFERENCES zone(`id`),
	FOREIGN KEY (`reporter_id`) REFERENCES reporter(`id`)
	);

