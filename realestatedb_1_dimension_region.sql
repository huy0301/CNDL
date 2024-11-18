-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: realestatedb_1
-- ------------------------------------------------------
-- Server version	8.0.39

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
-- Table structure for table `dimension_region`
--

DROP TABLE IF EXISTS `dimension_region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dimension_region` (
  `region_id` int NOT NULL AUTO_INCREMENT,
  `region_name` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  PRIMARY KEY (`region_id`),
  KEY `idx_dimension_region_name_city` (`region_name`,`city`),
  KEY `idx_dimension_region_name` (`region_name`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dimension_region`
--

LOCK TABLES `dimension_region` WRITE;
/*!40000 ALTER TABLE `dimension_region` DISABLE KEYS */;
INSERT INTO `dimension_region` VALUES (21,'Huyện Bình Chánh ','Hồ Chí Minh'),(35,'Huyện Củ Chi ','Hồ Chí Minh'),(30,'Huyện Đông Anh ','Hà Nội'),(4,'Huyện Gia Lâm ','Hà Nội'),(36,'Huyện Hóc Môn ','Hồ Chí Minh'),(27,'Huyện Nhà Bè ','Hồ Chí Minh'),(33,'Huyện Thanh Oai ','Hà Nội'),(31,'Huyện Thanh Trì ','Hà Nội'),(32,'Huyện Thường Tín ','Hà Nội'),(16,'Quận 1 ','Hồ Chí Minh'),(13,'Quận 10 ','Hồ Chí Minh'),(34,'Quận 12 ','Hồ Chí Minh'),(18,'Quận 3 ','Hồ Chí Minh'),(26,'Quận 4 ','Hồ Chí Minh'),(19,'Quận 5 ','Hồ Chí Minh'),(22,'Quận 6 ','Hồ Chí Minh'),(14,'Quận 7 ','Hồ Chí Minh'),(12,'Quận 8 ','Hồ Chí Minh'),(3,'Quận Ba Đình ','Hà Nội'),(10,'Quận Bắc Từ Liêm ','Hà Nội'),(23,'Quận Bình Tân ','Hồ Chí Minh'),(11,'Quận Bình Thạnh ','Hồ Chí Minh'),(5,'Quận Cầu Giấy ','Hà Nội'),(8,'Quận Đống Đa ','Hà Nội'),(25,'Quận Gò Vấp ','Hồ Chí Minh'),(6,'Quận Hà Đông ','Hà Nội'),(7,'Quận Hai Bà Trưng ','Hà Nội'),(9,'Quận Hoàng Mai ','Hà Nội'),(28,'Quận Long Biên ','Hà Nội'),(2,'Quận Nam Từ Liêm ','Hà Nội'),(15,'Quận Phú Nhuận ','Hồ Chí Minh'),(24,'Quận Tân Bình ','Hồ Chí Minh'),(17,'Quận Tân Phú ','Hồ Chí Minh'),(29,'Quận Tây Hồ ','Hà Nội'),(1,'Quận Thanh Xuân ','Hà Nội'),(20,'Thành phố Thủ Đức ','Hồ Chí Minh');
/*!40000 ALTER TABLE `dimension_region` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-19  0:26:19
