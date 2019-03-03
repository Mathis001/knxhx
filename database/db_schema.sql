/*CREATE DATABASE*/

CREATE DATABASE IF NOT EXISTS `potholes`;

/*Set Database*/

USE potholes;

/*CREATE TABLE zone*/

CREATE TABLE IF NOT EXISTS `zone`(
	`id` INT NOT NULL AUTO_INCREMENT,
	`zone_number` INT DEFAULT 0,
	`zone_notes` VARCHAR(255) DEFAULT '',
	PRIMARY KEY (`id`)
	);

/*CREATE TABLE status*/

CREATE TABLE IF NOT EXISTS `status`(
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(255) NOT NULL,
	PRIMARY KEY (`id`)
	);

/*CREATE TABLE location*/

CREATE TABLE IF NOT EXISTS `location`(
	`id` INT NOT NULL AUTO_INCREMENT,
    `input_address` VARCHAR(255) NOT NULL,
    `full_address` VARCHAR(255) NOT NULL,
	`city` VARCHAR(255) NOT NULL,
	`latitude` VARCHAR(255) DEFAULT '',
	`longitude` VARCHAR(255) DEFAULT '',
	PRIMARY KEY (`id`)
	);


/*CREATE TABLE reporter*/

CREATE TABLE IF NOT EXISTS `reporter`(
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(255) NOT NULL,
	`phone_number` VARCHAR(255) NOT NULL,
	PRIMARY KEY (`id`)
	);

/*CREATE TABLE priority*/

CREATE TABLE IF NOT EXISTS `priority`(
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(255) NOT NULL,
	PRIMARY KEY (`id`)
	);

/*CREATE TABLE reported*/

CREATE TABLE IF NOT EXISTS `reported` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`status_id` INT NOT NULL,
	`location_id` INT NOT NULL,
	`zone_id` INT NOT NULL,
	`reporter_id` INT NOT NULL,
	`priority_id` INT NOT NULL,
	PRIMARY KEY (`id`),
	FOREIGN KEY (`status_id`) REFERENCES status(`id`),
	FOREIGN KEY (`zone_id`) REFERENCES zone(`id`),
	FOREIGN KEY (`reporter_id`) REFERENCES reporter(`id`),
	FOREIGN KEY (`priority_id`) REFERENCES priority(`id`)
	);

/*CREATE TABLE trucks*/
CREATE TABLE IF NOT EXISTS `trucks` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`)
    );

/*CREATE TABLE work orders*/
CREATE TABLE IF NOT EXISTS `workorders` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`request_id` INT NOT NULL,
	`w_o` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`)
	);

/*CREATE TABLE jobs*/
CREATE TABLE IF NOT EXISTS `jobs` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `workorder_id` INT NOT NULL,
    `truck_id` INT NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`workorder_id`) REFERENCES workorders(`id`),
    FOREIGN KEY (`truck_id`) REFERENCES trucks(`id`)
    );

/*CREATE TABLE authlvl*/
CREATE TABLE IF NOT EXISTS `authlvl` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`auth_name` VARCHAR(255) NOT NULL,
	PRIMARY KEY (`id`)
	);

/*CREATE TABLE user*/
CREATE TABLE IF NOT EXISTS `user` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(255) NOT NULL,
	`password` VARCHAR(255) NOT NULL,
	`api_token` VARCHAR(255) NOT NULL,
	`auth` INT NOT NULL,
	PRIMARY KEY (`id`),
	FOREIGN KEY (`auth`) REFERENCES authlvl(`id`)
	);
