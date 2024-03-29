CREATE TABLE `department` (
  `department_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`department_id`)
);

CREATE TABLE `course` (
  `course_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `department_id` INT NOT NULL,
  `call_number` VARCHAR(45) NULL,
  `status` ENUM('pending', 'approved', 'rejected') NULL,
  FULLTEXT KEY course_search_index (name, call_number),
  PRIMARY KEY (`course_id`),
  CONSTRAINT `fk_course__department` FOREIGN KEY (`department_id`)
    REFERENCES `department` (`department_id`)
) ENGINE=InnoDB;

-- TODO: make uni not null
CREATE TABLE `professor` (
  `professor_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `uni` VARCHAR(15) NULL UNIQUE,
  `status` ENUM('pending', 'approved', 'rejected') NULL,
  FULLTEXT KEY professor_search_index (first_name, last_name, uni),
  PRIMARY KEY (`professor_id`)
) ENGINE=InnoDB;

CREATE TABLE `department_professor`(
  `professor_id` INT NOT NULL,
  `department_id` INT NOT NULL,
  CONSTRAINT `fk_department_professor__professor` FOREIGN KEY (`professor_id`)
    REFERENCES `professor` (`professor_id`),
  CONSTRAINT `fk_department_professor__department` FOREIGN KEY (`department_id`)
    REFERENCES `department` (`department_id`)
);

CREATE TABLE `course_professor` (
  `course_professor_id` INT NOT NULL AUTO_INCREMENT,
  `professor_id` INT NULL,
  `course_id` INT NULL,
  `status` ENUM('pending', 'approved', 'rejected') NULL,
  PRIMARY KEY (`course_professor_id`),
  CONSTRAINT unique_professor_id__course_id UNIQUE (professor_id, course_id),
  CONSTRAINT `fk_course_professor__professor` FOREIGN KEY(`professor_id`)
    REFERENCES `professor` (`professor_id`),
  CONSTRAINT `fk_course_professor__course` FOREIGN KEY (`course_id`)
    REFERENCES `course` (`course_id`)
);

CREATE TABLE `review` (
  `review_id` INT NOT NULL AUTO_INCREMENT,
  `course_professor_id` INT NOT NULL,
  `content` TEXT NULL,
  `ip` VARCHAR(15) DEFAULT NULL,
  `workload` TEXT NULL,
  `rating` INT NULL,
  `submission_date` DATETIME DEFAULT NULL,
  PRIMARY KEY (`review_id`),
  CONSTRAINT `fk_review__course_professor` FOREIGN KEY (`course_professor_id`)
    REFERENCES `course_professor` (`course_professor_id`)
);

CREATE TABLE `vote` (
  `review_id` INT NOT NULL,
  `ip` VARCHAR(15) DEFAULT NULL,
  `created_at` DATETIME DEFAULT NULL,
  `type` ENUM('agree', 'disagree', 'funny') NOT NULL,
  CONSTRAINT `fk_vote__review` FOREIGN KEY (`review_id`)
    REFERENCES `review`(`review_id`)
);

CREATE TABLE `user` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(255) NOT NULL,
  `username` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `privileges` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`user_id`)
);

CREATE TABLE `flag` (
  `flag_id` INT NOT NULL AUTO_INCREMENT,
  `review_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `type` ENUM(
    'approved',
    'pending',
    'libel',
    'insufficient'
  ) NOT NULL,
  `created_at` DATETIME NOT NULL,
  PRIMARY KEY(`flag_id`),
  CONSTRAINT `fk_flag__review` FOREIGN KEY (`review_id`)
    REFERENCES `review` (`review_id`),
  CONSTRAINT `fk_flag__user` FOREIGN KEY (`user_id`)
    REFERENCES `user` (`user_id`)
);

CREATE TABLE `badge` (
  `badge_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(60) NOT NULL,
  `description` VARCHAR(255) NOT NULL,
  PRIMARY KEY(`badge_id`)
);

CREATE TABLE `badge_professor` (
  `professor_id` INT NOT NULL,
  `badge_id` INT NOT NULL,
  CONSTRAINT `fk_badge_professor__professor` FOREIGN KEY (`professor_id`)
    REFERENCES `professor` (`professor_id`),
  CONSTRAINT `fk_badge_professor__badge` FOREIGN KEY (`badge_id`)
    REFERENCES `badge` (`badge_id`)
);
