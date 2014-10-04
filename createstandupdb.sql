-- create database standup;
use standup;
CREATE USER 'django'@'*' IDENTIFIED BY 'django';
GRANT ALL ON *.* TO 'django'@'localhost';
use standup;



-- ---
-- Globals
-- ---

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- SET FOREIGN_KEY_CHECKS=0;

-- ---
-- Table 'user'
-- 
-- ---

DROP TABLE IF EXISTS `user`;
		
CREATE TABLE `user` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `name` VARCHAR(20) NULL DEFAULT NULL,
  `stand_height` INTEGER NULL DEFAULT NULL,
  `sit_height` INTEGER NULL DEFAULT NULL,
  `presensce_status` INTEGER(20) NULL DEFAULT NULL,
  `sit_status` INTEGER(10) NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'deskheight_history'
-- 
-- ---

DROP TABLE IF EXISTS `deskheight_history`;
		
CREATE TABLE `deskheight_history` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `user_id` INTEGER NULL DEFAULT NULL,
  `height` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'motion_history'
-- 
-- ---

DROP TABLE IF EXISTS `motion_history`;
		
CREATE TABLE `motion_history` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `user_id` INTEGER NULL DEFAULT NULL,
  `inmotion_status` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'daily_winner'
-- 
-- ---

DROP TABLE IF EXISTS `daily_winner`;
		
CREATE TABLE `daily_winner` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `date` DATE NULL DEFAULT NULL,
  `user_id` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'datamart'
-- 
-- ---

DROP TABLE IF EXISTS `datamart`;
		
CREATE TABLE `datamart` (
  `user_id` INTEGER NULL DEFAULT NULL,
  `longest_stand` INTEGER NULL DEFAULT NULL,
  `longest_sit` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`)
);

-- ---
-- Foreign Keys 
-- ---

ALTER TABLE `deskheight_history` ADD FOREIGN KEY (user_id) REFERENCES `user` (`id`);
ALTER TABLE `motion_history` ADD FOREIGN KEY (user_id) REFERENCES `user` (`id`);
ALTER TABLE `daily_winner` ADD FOREIGN KEY (user_id) REFERENCES `user` (`id`);
ALTER TABLE `datamart` ADD FOREIGN KEY (user_id) REFERENCES `user` (`id`);

-- ---
-- Table Properties
-- ---

-- ALTER TABLE `user` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `deskheight_history` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `motion_history` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `daily_winner` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `datamart` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ---
-- Test Data
-- ---

INSERT INTO `user` (`name`,`stand_height`,`sit_height`,`presensce_status`,`sit_status`) VALUES
('Matt','34','26','0','1');
INSERT INTO `user` (`name`,`stand_height`,`sit_height`,`presensce_status`,`sit_status`) VALUES
('Courtney','28','20','0','1');
-- INSERT INTO `deskheight_history` (`id`,`user_id`,`height`) VALUES
-- ('','','');
-- INSERT INTO `motion_history` (`id`,`user_id`,`inmotion_status`) VALUES
-- ('','','');
-- INSERT INTO `daily_winner` (`id`,`date`,`user_id`) VALUES
-- ('','','');
-- INSERT INTO `datamart` (`user_id`,`longest_stand`,`longest_sit`) VALUES
-- ('','','');

