CREATE TABLE `doctors` (
  `d_id` int(3) NOT NULL AUTO_INCREMENT,
  `d_name` varchar(50) NOT NULL,
  `specialization` varchar(40) DEFAULT NULL,
  `fee` int(11) NOT NULL,
  `contact` varchar(20) NOT NULL,
  PRIMARY KEY (`d_id`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `patients` (
  `p_id` int(3) NOT NULL AUTO_INCREMENT,
  `p_name` varchar(50) NOT NULL,
  `sex` enum('M','F') NOT NULL,
  `age` int(3) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`p_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `clinics` (
  `c_id` int(3) NOT NULL AUTO_INCREMENT,
  `c_name` varchar(250) NOT NULL,
  `c_address` varchar(250) NOT NULL,
  `c_phone` varchar(20) NOT NULL,
  PRIMARY KEY (`c_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `pharmacies` (
  `pharma_id` int(10) NOT NULL AUTO_INCREMENT,
  `pharma_Name` varchar(50) NOT NULL,
  `phone` varchar(20) NOT NULL,
  PRIMARY KEY (`pharma_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `appointments` (
  `a_id` int(3) NOT NULL AUTO_INCREMENT,
  `p_id` int(3) NOT NULL,
  `d_id` int(3) NOT NULL,
  `c_id` int(3) NOT NULL,
  `schedule` datetime NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`a_id`),
  KEY `p_id` (`p_id`),
  KEY `d_id` (`d_id`),
  KEY `c_id` (`c_id`),
  CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`p_id`) REFERENCES `patients` (`p_id`),
  CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`d_id`) REFERENCES `doctors` (`d_id`),
  CONSTRAINT `appointments_ibfk_3` FOREIGN KEY (`c_id`) REFERENCES `clinics` (`c_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `schedules` (
  `schedule_id` int(3) NOT NULL AUTO_INCREMENT,
  `d_id` int(3) NOT NULL,
  `c_id` int(3) NOT NULL,
  `day` varchar(10) NOT NULL,
  `start` time NOT NULL,
  `end` time NOT NULL,
  PRIMARY KEY (`schedule_id`),
  KEY `c_id` (`c_id`),
  KEY `fk_d_id` (`d_id`),
  CONSTRAINT `fk_d_id` FOREIGN KEY (`d_id`) REFERENCES `doctors` (`d_id`),
  CONSTRAINT `schedules_ibfk_1` FOREIGN KEY (`c_id`) REFERENCES `clinics` (`c_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `clinic_doctors` (
  `d_id` int(3) NOT NULL,
  `c_id` int(3) NOT NULL,
  `salary` int(10) DEFAULT NULL,
  `joining_date` date DEFAULT NULL,
  PRIMARY KEY (`d_id`,`c_id`),
  CONSTRAINT `clinic_doctors_ibfk_1` FOREIGN KEY (`d_id`) REFERENCES `doctors` (`d_id`),
  CONSTRAINT `clinic_doctors_ibfk_2` FOREIGN KEY (`c_id`) REFERENCES `clinics` (`c_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `clinics_timings` (
  `c_id` int(3) NOT NULL,
  `day` varchar(10) NOT NULL,
  `start` time NOT NULL,
  `end` time NOT NULL,
  PRIMARY KEY (`c_id`,`day`,`start`,`end`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `login_clinics` (
  `_id` int(3) NOT NULL AUTO_INCREMENT,
  `c_id` int(3) NOT NULL,
  `username` varchar(10) NOT NULL UNIQUE,
  `password` varchar(20) NOT NULL UNIQUE,
  PRIMARY KEY (`_id`,`username`),
  KEY `c_id` (`c_id`),
  CONSTRAINT `login_clinics_ibfk_1` FOREIGN KEY (`c_id`) REFERENCES `clinics` (`c_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `login_doctors` (
  `_id` int(3) NOT NULL AUTO_INCREMENT,
  `d_id` int(3) NOT NULL,
  `username` varchar(10) NOT NULL UNIQUE,
  `password` varchar(20) NOT NULL UNIQUE,
  PRIMARY KEY (`_id`,`username`),
  KEY `d_id` (`d_id`),
  CONSTRAINT `login_doctors_ibfk_1` FOREIGN KEY (`d_id`) REFERENCES `doctors` (`d_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `login_patients` (
  `_id` int(3) NOT NULL AUTO_INCREMENT,
  `p_id` int(3) NOT NULL,
  `username` varchar(10) NOT NULL UNIQUE,
  `password` varchar(20) NOT NULL UNIQUE,
  PRIMARY KEY (`_id`,`username`),
  KEY `p_id` (`p_id`),
  CONSTRAINT `login_patients_ibfk_1` FOREIGN KEY (`p_id`) REFERENCES `patients` (`p_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `login_pharmacies` (
  `_id` int(3) NOT NULL AUTO_INCREMENT,
  `pharma_id` int(3) NOT NULL,
  `username` varchar(10) NOT NULL UNIQUE,
  `password` varchar(20) NOT NULL UNIQUE,
  PRIMARY KEY (`_id`,`username`),
  KEY `pharma_id` (`pharma_id`),
  CONSTRAINT `login_pharmacies_ibfk_1` FOREIGN KEY (`pharma_id`) REFERENCES `pharmacies` (`pharma_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `medical_histories` (
  `mh_id` int(3) NOT NULL AUTO_INCREMENT,
  `p_id` int(3) NOT NULL,
  `allergies` varchar(100) DEFAULT NULL,
  `diabetes` varchar(100) DEFAULT NULL,
  `bp` varchar(100) DEFAULT NULL,
  `infectious_diseases` varchar(100) DEFAULT NULL,
  `family_history` varchar(100) DEFAULT NULL,
  `surgical_history` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`mh_id`),
  KEY `p_id` (`p_id`),
  CONSTRAINT `medical_histories_ibfk_1` FOREIGN KEY (`p_id`) REFERENCES `patients` (`p_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `prescriptions` (
  `prescription_id` int(3) NOT NULL AUTO_INCREMENT,
  `p_id` int(3) NOT NULL,
  `d_id` int(3) NOT NULL,
  `meds` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`prescription_id`),
  KEY `prescriptions_ibfk_1` (`p_id`),
  KEY `prescriptions_ibfk_2` (`d_id`),
  CONSTRAINT `prescriptions_ibfk_1` FOREIGN KEY (`p_id`) REFERENCES `patients` (`p_id`),
  CONSTRAINT `prescriptions_ibfk_2` FOREIGN KEY (`d_id`) REFERENCES `doctors` (`d_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `reports` (
  `report_id` int(3) NOT NULL AUTO_INCREMENT,
  `p_id` int(3) NOT NULL,
  `d_id` int(3) NOT NULL,
  `symptoms` varchar(100) DEFAULT NULL,
  `illness` varchar(100) DEFAULT NULL,
  `tests_required` varchar(100) DEFAULT NULL,
  `test_reports` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`report_id`),
  KEY `p_id` (`p_id`),
  KEY `d_id` (`d_id`),
  CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`p_id`) REFERENCES `patients` (`p_id`),
  CONSTRAINT `reports_ibfk_2` FOREIGN KEY (`d_id`) REFERENCES `doctors` (`d_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
