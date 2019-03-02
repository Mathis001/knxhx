-- ---------------------------
-- Table 'Table1'
-- ---------------------------

CREATE TABLE 'reported'(
	'id' INT NOT NULL AUTO_INCREMENT,
	'w_o_date' DATE NOT NULL,
	'status_id' VARCHAR NOT NULL,
	'w_o_number' VARCHAR NOT NULL,
	'req_number' VARCHAR NOT NULL,
	'zone_id' VARCHAR NOT NULL,
	'reporter_id' VARCHAR NOT NULL
	PRIMARY KEY (`id`)
	FOREIGN KEY (`status_id`) REFERENCES status(`id`),
	FOREIGN KEY (`zone_id`) REFERENCES zone(`id`),
	FOREIGN KEY (`reporter_id`) REFERENCES reporter`id`)
	);

CREATE TABLE 'zone'(
	'id' INT NOT NULL AUTO_INCREMENT,
	'zone_number' VARCHAR NOT NULL,
	'zone_notes' VARCHAR NOT NULL,
	PRIMARY KEY (`id`)
	);
CREATE TABLE 'status'(
	'id' INT NOT NULL AUTO_INCREMENT,
	'name' VARCHAR NOT NULL,
	PRIMARY KEY (`id`)
	);
CREATE TABLE 'reporter'(
	'id' INT NOT NULL AUTO_INCREMENT,
	'name' VARCHAR NOT NULL,
	'phone_number' VARCHAR NOT NULL,
	PRIMARY KEY (`id`)
	);