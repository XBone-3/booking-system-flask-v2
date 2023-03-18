-- MySQL Script generated by MySQL Workbench
-- Sat Mar 18 19:55:10 2023
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema crittle
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `crittle` ;

-- -----------------------------------------------------
-- Schema crittle
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `crittle` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `crittle` ;

-- -----------------------------------------------------
-- Table `crittle`.`admins`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `crittle`.`admins` ;

CREATE TABLE IF NOT EXISTS `crittle`.`admins` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `mobile` VARCHAR(45) NOT NULL,
  `online` INT NOT NULL DEFAULT '0',
  `registered_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `admin_password` VARCHAR(225) NOT NULL,
  `admin` TINYINT NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `idadmins_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `crittle`.`bookings`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `crittle`.`bookings` ;

CREATE TABLE IF NOT EXISTS `crittle`.`bookings` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `sport` VARCHAR(12) NOT NULL,
  `courtname` VARCHAR(9) NOT NULL,
  `year` INT NOT NULL,
  `month` VARCHAR(12) NOT NULL,
  `day` INT NOT NULL,
  `timeslot` VARCHAR(12) NOT NULL,
  `comment` VARCHAR(255) NOT NULL DEFAULT 'You did not comment on this booking.. But, we think you enjoyed a lot.',
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 14
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `crittle`.`slotsavailable`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `crittle`.`slotsavailable` ;

CREATE TABLE IF NOT EXISTS `crittle`.`slotsavailable` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `sport` VARCHAR(45) NOT NULL,
  `courtname` VARCHAR(45) NOT NULL,
  `timeslot` VARCHAR(45) NOT NULL,
  `availability` TINYINT NOT NULL DEFAULT '1',
  `date` DATE NULL DEFAULT curdate(),
  PRIMARY KEY (`id`),
  INDEX `id_idx` (`id` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 34
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `crittle`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `crittle`.`users` ;

CREATE TABLE IF NOT EXISTS `crittle`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `mobile` VARCHAR(45) NOT NULL,
  `online` TINYINT NOT NULL DEFAULT '0',
  `register_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_password` VARCHAR(225) NOT NULL,
  `admin` TINYINT NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
