-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: snm
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `filesdata`
--

DROP TABLE IF EXISTS `filesdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `filesdata` (
  `filesid` int unsigned NOT NULL AUTO_INCREMENT,
  `filedata` longblob,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `userid` int unsigned DEFAULT NULL,
  `filename` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`filesid`),
  KEY `userid` (`userid`),
  CONSTRAINT `filesdata_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `userdata` (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filesdata`
--

LOCK TABLES `filesdata` WRITE;
/*!40000 ALTER TABLE `filesdata` DISABLE KEYS */;
INSERT INTO `filesdata` VALUES (3,_binary 'import random\r\nimport math\r\nimport smtplib  #simple mail transfer protocol\r\ndigits=\"0123456789\"\r\nOTP=\"\"\r\nfor i in range(6):\r\n    OTP+=digits[math.floor(random.random()*10)]\r\notp=OTP+\" is your otp\"\r\nmsg=otp\r\ns=smtplib.SMTP(\"smtp.gmail.com\",587)\r\ns.starttls()\r\ns.login(\"annaladasubindubabu@gmail.com\",\"jzry hoce opza tavu\")\r\nuser=\"annaladasubindubabu@gmail.com\"\r\nmail=input(\"enter your mail which you want to send\")\r\ns.sendmail(user,mail,msg)\r\nwhile 1:\r\n    a=input(\"enter your otp:\")\r\n    if a==OTP:\r\n        print(\"Valid\")\r\n    else:\r\n        print(\"Invalid\")\r\n        \r\n','2026-05-13 16:32:06',1,'opt-generation.py');
/*!40000 ALTER TABLE `filesdata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notesdata`
--

DROP TABLE IF EXISTS `notesdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notesdata` (
  `notesid` int unsigned NOT NULL AUTO_INCREMENT,
  `notes_title` varchar(50) NOT NULL,
  `notes_description` longtext,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `userid` int unsigned DEFAULT NULL,
  PRIMARY KEY (`notesid`),
  KEY `userid` (`userid`),
  CONSTRAINT `notesdata_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `userdata` (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notesdata`
--

LOCK TABLES `notesdata` WRITE;
/*!40000 ALTER TABLE `notesdata` DISABLE KEYS */;
INSERT INTO `notesdata` VALUES (3,'Python','Easy to learn\r\n','2026-05-08 15:25:23',1),(4,'HTML1\r\n','To develop structure of webpages','2026-05-08 15:27:24',1);
/*!40000 ALTER TABLE `notesdata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userdata`
--

DROP TABLE IF EXISTS `userdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userdata` (
  `userid` int unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `useremail` varchar(50) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `userpassword` varchar(50) NOT NULL,
  PRIMARY KEY (`userid`),
  UNIQUE KEY `useremail` (`useremail`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userdata`
--

LOCK TABLES `userdata` WRITE;
/*!40000 ALTER TABLE `userdata` DISABLE KEYS */;
INSERT INTO `userdata` VALUES (1,'BINDUBABU','annaladasubindubabu@gmail.com','2026-05-06 14:37:15','Bindu@123'),(7,'VAMSI','vamsivarunkamanchi@gmail.com','2026-05-06 14:56:01','Vamsi@420');
/*!40000 ALTER TABLE `userdata` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-16 14:18:05
