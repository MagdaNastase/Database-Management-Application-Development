-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: bazadedate
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `sculptors`
--

DROP TABLE IF EXISTS `sculptors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sculptors` (
  `SculptorID` int NOT NULL AUTO_INCREMENT,
  `Nume` varchar(100) NOT NULL,
  `Prenume` varchar(100) NOT NULL,
  `AnNastere` int DEFAULT NULL,
  `AnDeces` int DEFAULT NULL,
  `Nationalitate` varchar(50) DEFAULT NULL,
  `StilArtistic` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`SculptorID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sculptors`
--

LOCK TABLES `sculptors` WRITE;
/*!40000 ALTER TABLE `sculptors` DISABLE KEYS */;
INSERT INTO `sculptors` VALUES (1,'Michelangelo','Buonarroti',1475,1564,'Italian','Renaștere'),(2,'Auguste','Rodin',1840,1917,'Francez','Modern'),(3,'Constantin','Brâncuși',1876,1957,'Român','Avangardist'),(4,'Antonio','Canova',1757,1822,'Italian','Neoclasic');
/*!40000 ALTER TABLE `sculptors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sculpture_sculptor`
--

DROP TABLE IF EXISTS `sculpture_sculptor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sculpture_sculptor` (
  `SculptureID` int NOT NULL,
  `SculptorID` int NOT NULL,
  PRIMARY KEY (`SculptureID`,`SculptorID`),
  KEY `SculptorID` (`SculptorID`),
  CONSTRAINT `sculpture_sculptor_ibfk_1` FOREIGN KEY (`SculptureID`) REFERENCES `sculptures` (`SculptureID`) ON DELETE CASCADE,
  CONSTRAINT `sculpture_sculptor_ibfk_2` FOREIGN KEY (`SculptorID`) REFERENCES `sculptors` (`SculptorID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sculpture_sculptor`
--

LOCK TABLES `sculpture_sculptor` WRITE;
/*!40000 ALTER TABLE `sculpture_sculptor` DISABLE KEYS */;
INSERT INTO `sculpture_sculptor` VALUES (1,1),(2,1),(3,1),(2,2);
/*!40000 ALTER TABLE `sculpture_sculptor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sculptures`
--

DROP TABLE IF EXISTS `sculptures`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sculptures` (
  `SculptureID` int NOT NULL AUTO_INCREMENT,
  `Titlu` varchar(150) NOT NULL,
  `Material` varchar(100) DEFAULT NULL,
  `Inaltime` decimal(5,2) DEFAULT NULL,
  `Greutate` decimal(6,2) DEFAULT NULL,
  `AnCreatie` int DEFAULT NULL,
  `LocatieMuzeu` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`SculptureID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sculptures`
--

LOCK TABLES `sculptures` WRITE;
/*!40000 ALTER TABLE `sculptures` DISABLE KEYS */;
INSERT INTO `sculptures` VALUES (1,'David','Marmură',5.17,6000.00,1504,'Galleria dell\'Accademia, Florența'),(2,'Gânditorul','Bronz',1.89,700.50,1904,'Musée Rodin, Paris'),(3,'Pietà','Marmură',1.74,2500.00,1499,'Bazilica Sfântul Petru, Vatican'),(4,'Coloana Infinitului','Oțel',29.33,9000.00,1938,'Târgu Jiu, România');
/*!40000 ALTER TABLE `sculptures` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-30 18:31:56
