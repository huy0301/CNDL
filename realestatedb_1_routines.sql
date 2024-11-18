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
-- Temporary view structure for view `unsold_unrented_realestate`
--

DROP TABLE IF EXISTS `unsold_unrented_realestate`;
/*!50001 DROP VIEW IF EXISTS `unsold_unrented_realestate`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `unsold_unrented_realestate` AS SELECT 
 1 AS `region_id`,
 1 AS `Region`,
 1 AS `City`,
 1 AS `Segment`,
 1 AS `TotalUnsold`,
 1 AS `TotalUnrented`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `realestate_segment`
--

DROP TABLE IF EXISTS `realestate_segment`;
/*!50001 DROP VIEW IF EXISTS `realestate_segment`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `realestate_segment` AS SELECT 
 1 AS `region_id`,
 1 AS `Region`,
 1 AS `City`,
 1 AS `Segment`,
 1 AS `TotalProperties`,
 1 AS `AverageRentalPrice`,
 1 AS `AverageSellingPrice`,
 1 AS `TotalArea`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `transaction_count_by_month`
--

DROP TABLE IF EXISTS `transaction_count_by_month`;
/*!50001 DROP VIEW IF EXISTS `transaction_count_by_month`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `transaction_count_by_month` AS SELECT 
 1 AS `region_id`,
 1 AS `RegionName`,
 1 AS `TransactionMonth`,
 1 AS `transaction_type`,
 1 AS `Segment`,
 1 AS `TotalTransactions`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `unsold_unrented_realestate`
--

/*!50001 DROP VIEW IF EXISTS `unsold_unrented_realestate`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `unsold_unrented_realestate` AS select `dimension_region`.`region_id` AS `region_id`,`dimension_region`.`region_name` AS `Region`,`dimension_region`.`city` AS `City`,`dimension_real_estate_type`.`type_name` AS `Segment`,sum((case when (`dimension_real_estate_status`.`status_name` = 'Chưa bán') then 1 else 0 end)) AS `TotalUnsold`,sum((case when (`dimension_real_estate_status`.`status_name` = 'Chưa thuê') then 1 else 0 end)) AS `TotalUnrented` from (((`fact_real_estate_transaction` join `dimension_region` on((`fact_real_estate_transaction`.`region_id` = `dimension_region`.`region_id`))) join `dimension_real_estate_type` on((`fact_real_estate_transaction`.`type_id` = `dimension_real_estate_type`.`type_id`))) join `dimension_real_estate_status` on((`fact_real_estate_transaction`.`status_id` = `dimension_real_estate_status`.`status_id`))) where (`dimension_real_estate_status`.`status_name` in ('Chưa bán','Chưa thuê')) group by `dimension_region`.`region_id`,`dimension_region`.`region_name`,`dimension_region`.`city`,`dimension_real_estate_type`.`type_name` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `realestate_segment`
--

/*!50001 DROP VIEW IF EXISTS `realestate_segment`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `realestate_segment` AS select `dimension_region`.`region_id` AS `region_id`,`dimension_region`.`region_name` AS `Region`,`dimension_region`.`city` AS `City`,`dimension_real_estate_type`.`type_name` AS `Segment`,count(`fact_real_estate_transaction`.`transaction_id`) AS `TotalProperties`,avg(`fact_real_estate_transaction`.`rental_price`) AS `AverageRentalPrice`,avg(`fact_real_estate_transaction`.`price`) AS `AverageSellingPrice`,sum(`fact_real_estate_transaction`.`total_area`) AS `TotalArea` from ((`fact_real_estate_transaction` join `dimension_real_estate_type` on((`fact_real_estate_transaction`.`type_id` = `dimension_real_estate_type`.`type_id`))) join `dimension_region` on((`fact_real_estate_transaction`.`region_id` = `dimension_region`.`region_id`))) group by `dimension_region`.`region_id`,`dimension_region`.`city`,`dimension_real_estate_type`.`type_name` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `transaction_count_by_month`
--

/*!50001 DROP VIEW IF EXISTS `transaction_count_by_month`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `transaction_count_by_month` AS select `fact_real_estate_transaction`.`region_id` AS `region_id`,`dimension_region`.`region_name` AS `RegionName`,date_format(`fact_real_estate_transaction`.`transaction_date`,'%Y-%m') AS `TransactionMonth`,(ifnull(`fact_real_estate_transaction`.`price`,0) > 0) AS `transaction_type`,`dimension_real_estate_type`.`type_name` AS `Segment`,count(`fact_real_estate_transaction`.`transaction_id`) AS `TotalTransactions` from ((`fact_real_estate_transaction` join `dimension_real_estate_type` on((`fact_real_estate_transaction`.`type_id` = `dimension_real_estate_type`.`type_id`))) join `dimension_region` on((`fact_real_estate_transaction`.`region_id` = `dimension_region`.`region_id`))) group by `fact_real_estate_transaction`.`region_id`,`RegionName`,`TransactionMonth`,`transaction_type`,`Segment` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-19  0:26:19
