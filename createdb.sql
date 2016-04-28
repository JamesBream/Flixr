##############
# FLIXR v0.1 #
##############
#  Build DB  #
##############

CREATE DATABASE IF NOT EXISTS Flixr;

DROP TABLE IF EXISTS `Flixr`.`tbl_user`;
CREATE TABLE `Flixr`.`tbl_user` (
    `user_id` BIGINT NOT NULL AUTO_INCREMENT,
    `user_email` VARCHAR(254) NOT NULL,
    `user_firstname` VARCHAR(35) NOT NULL,
    `user_lastname` VARCHAR(35) NOT NULL,
    `user_password` VARCHAR(70) NOT NULL,
    PRIMARY KEY (`user_id`)
);

DROP TABLE IF EXISTS `Flixr`.`tbl_bookmark`;
CREATE TABLE `Flixr`.`tbl_bookmark` (
    `bookmark_id` BIGINT NOT NULL AUTO_INCREMENT,
    `bookmark_date` DATETIME NOT NULL,
    `user_id` BIGINT NOT NULL,
    `movie_id` BIGINT NOT NULL,
    PRIMARY KEY (`bookmark_id`)
);


# Procedures
#######################################


# Procedure for creating a user from passed in data
DROP PROCEDURE IF EXISTS `Flixr`.`sp_createUser`;
USE `Flixr`;
DELIMITER $$
CREATE PROCEDURE `sp_createUser`(
    IN p_email VARCHAR(254),
	IN p_firstname VARCHAR(35),
    IN p_lastname VARCHAR(35),
	IN p_password VARCHAR(66)
)
BEGIN
    # Check whether the user already exists
	IF (SELECT EXISTS (SELECT 1 FROM tbl_user WHERE user_email = p_email) ) THEN
	
		SELECT 'Email Address Already Registered!';
	
	ELSE
	
		INSERT INTO tbl_user
		(
            user_email,
			user_firstname,
			user_lastname,
			user_password
		)
		VALUES
		(
			p_email,
			p_firstname,
			p_lastname,
            p_password
		);
		
	END IF;
END$$
DELIMITER ;


# Procedure for validating user login
DROP PROCEDURE IF EXISTS `Flixr`.`sp_validateLogin`;
USE `Flixr`;
DELIMITER $$
CREATE PROCEDURE `sp_validateLogin` (IN p_email VARCHAR(254)
)
BEGIN
    SELECT * FROM tbl_user WHERE user_email = p_email;
END$$
DELIMITER ;


# Create/Delete(toggle) bookmark
DROP PROCEDURE IF EXISTS `Flixr`.`sp_toggleBookmark`;
USE `Flixr`;
DELIMITER $$
CREATE PROCEDURE `sp_toggleBookmark` (
    IN p_user_id BIGINT,
    IN p_movie_id BIGINT
)
BEGIN
    # Check for existing value 
    IF (SELECT EXISTS (SELECT 1 FROM tbl_bookmark WHERE user_id = p_user_id AND movie_id = p_movie_id)) THEN
    
        # Delete existing value
        DELETE FROM tbl_bookmark WHERE user_id = p_user_id AND movie_id = p_movie_id;
    
    ELSE
        
        INSERT INTO tbl_bookmark (
            bookmark_date,
            user_id,
            movie_id
        )
        VALUES (
            NOW(),
            p_user_id,
            p_movie_id
        );
        
    END IF;
END$$
DELIMITER ;