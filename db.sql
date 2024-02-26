CREATE DATABASE  IF NOT EXISTS `fitness` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `fitness`;
-- MySQL dump 10.13  Distrib 8.0.27, for macos11 (x86_64)
--
-- Host: localhost    Database: fitness
-- ------------------------------------------------------
-- Server version	8.0.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `class`
--

DROP TABLE IF EXISTS `class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class` (
  `id` int NOT NULL,
  `trainerid` int DEFAULT NULL,
  `classname` varchar(20) DEFAULT NULL,
  `availability` varchar(10) DEFAULT NULL,
  `classdate` date DEFAULT NULL,
  `classday` varchar(10) DEFAULT NULL,
  `classtime` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fktrainerid_idx` (`trainerid`),
  CONSTRAINT `fktrainerid` FOREIGN KEY (`trainerid`) REFERENCES `trainer` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class`
--

LOCK TABLES `class` WRITE;
/*!40000 ALTER TABLE `class` DISABLE KEYS */;
INSERT INTO `class` VALUES (1,3,'Pilates','Yes','2022-08-15','Monday','15:00'),(2,2,'HIIT','Yes','2022-08-16','Tuesday','09:00'),(3,1,'Yoga','Full','2022-08-19','Friday','16:00'),(4,2,'HIIT',NULL,'2022-08-15','Monday','09:00'),(5,4,'Aquarobics',NULL,'2022-08-22','Monday','11:00'),(6,3,'Pilates',NULL,'2022-08-24','Wednesday','17:00'),(7,4,'Aquarobics',NULL,'2022-08-23','Tuesday','11:00'),(8,5,'Boxfit',NULL,'2022-08-18','Thursday','14:00'),(9,5,'Boxfit',NULL,'2022-08-19','Friday','14:00'),(10,6,'Balance',NULL,'2022-08-25','Thursday','08:00'),(11,6,'Balance',NULL,'2022-08-24','Wednesday','10:00'),(12,7,'Tai Chi',NULL,'2022-08-26','Friday','13:00'),(13,7,'Tai Chi',NULL,'2022-09-03','Saturday','12:00'),(14,8,'Pilates',NULL,'2022-09-04','Sunday','11:30'),(15,8,'Pilates',NULL,'2022-09-05','Monday','11:30'),(16,9,'Balance',NULL,'2022-08-31','Wednesday','11:00'),(17,9,'Balance',NULL,'2022-08-24','Wednesday','12:00'),(18,10,'Yoga',NULL,'2022-08-21','Sunday','08:00'),(19,10,'Yoga',NULL,'2022-08-28','Sunday','09:00');
/*!40000 ALTER TABLE `class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classbooking`
--

DROP TABLE IF EXISTS `classbooking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `classbooking` (
  `bookingid` int NOT NULL AUTO_INCREMENT,
  `memberid` int DEFAULT NULL,
  `classid` int DEFAULT NULL,
  `attendancestatus` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`bookingid`),
  KEY `fkmemberid_idx` (`memberid`),
  KEY `class_id_idx` (`classid`),
  CONSTRAINT `class_id` FOREIGN KEY (`classid`) REFERENCES `class` (`id`),
  CONSTRAINT `fkmemberid` FOREIGN KEY (`memberid`) REFERENCES `member` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classbooking`
--

LOCK TABLES `classbooking` WRITE;
/*!40000 ALTER TABLE `classbooking` DISABLE KEYS */;
INSERT INTO `classbooking` VALUES (1,1,1,'attend'),(2,3,3,'absent'),(3,2,3,'absent'),(14,1,16,'absent'),(15,2,8,'attend'),(16,2,15,'attend'),(17,2,11,'attend'),(18,3,1,'attend'),(19,3,15,'attend'),(20,3,10,'attend'),(21,13,14,'attend'),(22,13,19,'attend'),(23,13,16,'attend'),(24,13,12,'attend'),(25,15,1,'attend'),(26,15,2,'absent'),(27,15,11,'attend'),(28,16,1,'attend'),(29,16,11,'absent'),(30,1,14,NULL);
/*!40000 ALTER TABLE `classbooking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gymattendance`
--

DROP TABLE IF EXISTS `gymattendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gymattendance` (
  `attendanceid` int NOT NULL,
  `lastvisitdate` date DEFAULT NULL,
  `attendancenotes` varchar(45) DEFAULT NULL,
  `memberid` int DEFAULT NULL,
  PRIMARY KEY (`attendanceid`),
  KEY `fkmember_idx` (`memberid`),
  CONSTRAINT `fkmember` FOREIGN KEY (`memberid`) REFERENCES `member` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gymattendance`
--

LOCK TABLES `gymattendance` WRITE;
/*!40000 ALTER TABLE `gymattendance` DISABLE KEYS */;
INSERT INTO `gymattendance` VALUES (1,'2022-08-07','notes',1),(2,'2022-07-08','notes',2),(3,'2022-06-09','regular attending',3),(4,'2022-08-08',NULL,13),(5,'2022-08-20',NULL,15),(6,'2022-08-22',NULL,16),(7,'2022-08-19',NULL,17),(8,'2022-08-10',NULL,18),(9,'2022-08-13',NULL,19),(10,'2022-08-22',NULL,35);
/*!40000 ALTER TABLE `gymattendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member` (
  `id` int NOT NULL AUTO_INCREMENT,
  `firstName` varchar(20) NOT NULL,
  `lastName` varchar(20) NOT NULL,
  `address` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `healthIssues` varchar(20) DEFAULT NULL,
  `joindate` date DEFAULT NULL,
  `leftdate` date DEFAULT NULL,
  `membershipstatus` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member`
--

LOCK TABLES `member` WRITE;
/*!40000 ALTER TABLE `member` DISABLE KEYS */;
INSERT INTO `member` VALUES (1,'shirly','Duncan','33 Beach Street','shirly@example.com','02100920124','1989-03-02','Female','no','2020-09-09',NULL,'1'),(2,'Emily','Young','12B Eban Ave, Christchurch','emily@example.com','210990992','1988-09-08','Female','no','2021-09-08',NULL,'1'),(3,'Adam','Walker','20 Compton Street, Napier','Adam@example.com','220119822','1997-09-06','Male','no','2022-01-09','2022-03-01','1'),(13,'Maria','Parker','11 Anzac Ave, Auckland Central','maria@example.com','220115611','1994-02-10','Male','no','2021-03-09',NULL,'1'),(15,'Nita','Daniel','23 Lynden Ave, Kumea','daniel@icloud.com','213891890','1988-06-16','Female','no','2021-12-02',NULL,'1'),(16,'Noah','Bush','77 Short street, Wellington','bush@icloud.ca','210364870','1995-05-18','Male','no','2022-06-09',NULL,'1'),(17,'Mia','Foster','18 Welland Place, Huntly','foster@google.net','211045920','1987-10-16','Female','no','2022-02-03',NULL,'1'),(18,'Keane','Delaney','111 Linley Street, Hamilton','delaney@gmail.com','02100029384','1983-09-20','Male','no','3020-09-08',NULL,'1'),(19,'Raymond','Lim','33 mountain view road','raymond@example.com','02100988097','1990-02-15','Male','No',NULL,NULL,'0'),(35,'Kristy','Lasiar','123 Linsy Ave','kristy@example.com','02100998236','1989-03-01','Female','no',NULL,NULL,NULL);
/*!40000 ALTER TABLE `member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `paymentid` int NOT NULL AUTO_INCREMENT,
  `memberid` int NOT NULL,
  `paymentdate` date NOT NULL,
  `paymentamount` int NOT NULL,
  `type` varchar(20) NOT NULL,
  PRIMARY KEY (`paymentid`),
  KEY `fk_memberId_id_idx` (`memberid`),
  CONSTRAINT `fk_memberId_id` FOREIGN KEY (`memberid`) REFERENCES `member` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES (1,2,'2022-06-03',60,'membership'),(4,3,'2022-08-16',180,'membership'),(5,13,'2020-05-07',180,'membership'),(6,15,'2022-06-03',180,'membership'),(7,16,'2021-08-13',120,'membership'),(8,17,'2022-08-16',180,'membership'),(9,18,'2022-08-16',60,'membership');
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PTbooking`
--

DROP TABLE IF EXISTS `PTbooking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PTbooking` (
  `id` int NOT NULL AUTO_INCREMENT,
  `trainerid` int DEFAULT NULL,
  `memberid` int NOT NULL,
  `trainingname` varchar(35) DEFAULT NULL,
  `paymentdate` varchar(10) DEFAULT NULL,
  `trainingcost` int DEFAULT NULL,
  `classdate` varchar(10) DEFAULT NULL,
  `classtime` varchar(20) NOT NULL,
  `location` varchar(20) DEFAULT NULL,
  `attendancestatus` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `trainerID_idx` (`trainerid`),
  KEY `memberid_idx` (`memberid`),
  CONSTRAINT `memberid` FOREIGN KEY (`memberid`) REFERENCES `member` (`id`),
  CONSTRAINT `trainerID` FOREIGN KEY (`trainerid`) REFERENCES `trainer` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PTbooking`
--

LOCK TABLES `PTbooking` WRITE;
/*!40000 ALTER TABLE `PTbooking` DISABLE KEYS */;
INSERT INTO `PTbooking` VALUES (1,1,2,'yoga','2022-08-05',50,'2022-08-08','16:00-18.00','Training room 2','attend'),(2,2,1,'HIIT','2022-08-08',75,'2022-08-09','09:00-11.00','Training room 2','absent'),(3,1,1,'Yoga','2022-08-20',50,'2022-08-23','15:00-17.00','Training room 2','attend');
/*!40000 ALTER TABLE `PTbooking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trainer`
--

DROP TABLE IF EXISTS `trainer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trainer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `firstName` varchar(20) NOT NULL,
  `lastName` varchar(20) NOT NULL,
  `email` varchar(45) DEFAULT NULL,
  `address` varchar(45) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `speciality` varchar(45) DEFAULT NULL,
  `freetime` varchar(20) NOT NULL,
  `cost` int(05) DEFAULT NULL,
  `status` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trainer`
--

LOCK TABLES `trainer` WRITE;
/*!40000 ALTER TABLE `trainer` DISABLE KEYS */;
INSERT INTO `trainer` VALUES (1,'Jack','Ma','jack@example.com','111 Bens Road, Dunedin','2002-09-09','M','Yoga','15:00 - 17:00','50','1'),(2,'Henry','Ali','henry@example.com','22 Nathan Street, Hastings','1991-09-08','M','HIIT','09:00 - 10:00','75','1'),(3,'Fritz','Bradshaw','metus.in@yahoo.couk','55 Grey Street, Upper North','1983-08-06','F','Spinning ','15:00 - 18:00','50','1'),(4,'Indigo','Kaufman','manga.a.tortor@hotmail.net','22 Somerset Road, Whaganui','1989-10-19','F','Aquarobics','10:00 - 12:00','50','1'),(5,'Damian','York','amet.consecteuer@outlook.net','33 London Street, Auckland','1994-05-04','M','Boxfit','13:00 - 15:00','60','1'),(6,'Yetta','Hunt','hunt@outlook.edu','29 Hereford Street, Auckland','1992-04-14','M','Balance','08:00 - 12:30','60','1'),(7,'Sierra','Knox','blandit@icloud.couk','90 Devon Road, Wellington','1979-12-19','M','Tai Chi','12:00 - 14:00','45','1'),(8,'Jael','York','fermentum@yahoo.edu','12/33 Mosston Road, Timaru','1990-07-20','F','Pilates','11:30 - 13:00','65','1'),(9,'Walter','Sims','Sims@icloud.edu','33 East Street, Queenstown','1981-08-01','M','Balance','11:00 - 13:00','70','1'),(10,'Buckminster','Lopez','viverra@google.com','259 Lincoln Road, Lincoln','1993-03-16','F','Yoga','08:00 - 10:00','45','1');
/*!40000 ALTER TABLE `trainer` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-08-24  0:05:18
