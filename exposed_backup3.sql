-- MySQL dump 10.13  Distrib 9.3.0, for Win64 (x86_64)
--
-- Host: localhost    Database: osphyncodes
-- ------------------------------------------------------
-- Server version	9.3.0

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add child',7,'add_child'),(26,'Can change child',7,'change_child'),(27,'Can delete child',7,'delete_child'),(28,'Can view child',7,'view_child'),(29,'Can add child visit',8,'add_childvisit'),(30,'Can change child visit',8,'change_childvisit'),(31,'Can delete child visit',8,'delete_childvisit'),(32,'Can view child visit',8,'view_childvisit'),(33,'Can add hts sample',9,'add_htssample'),(34,'Can change hts sample',9,'change_htssample'),(35,'Can delete hts sample',9,'delete_htssample'),(36,'Can view hts sample',9,'view_htssample'),(37,'Can add system log',10,'add_systemlog'),(38,'Can change system log',10,'change_systemlog'),(39,'Can delete system log',10,'delete_systemlog'),(40,'Can view system log',10,'view_systemlog');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$k0WyJeYJxRfjprPU6Y3alQ$t2x/cB/NyyrlILrERLKX6Bu69xWFlxxNcGNFPf3lnP0=','2025-07-13 16:51:43.515573',1,'osphyncodes','josephy','ng\'omba','ngombajosephy@gmail.com',1,1,'2025-07-05 07:13:27.000000'),(5,'pbkdf2_sha256$1000000$WoiTPSF2V3IWzAYHWdR6eB$Nrl67blk3iYgg7xNxPPaqEGF0cUODYaCUOu6U62bXRM=','2025-07-13 16:52:09.767854',1,'Prince','Prince','Ng\'omba','prinom@gmail.com',1,1,'2025-07-13 16:50:11.654635');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `children_child`
--

DROP TABLE IF EXISTS `children_child`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `children_child` (
  `hcc_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `child_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `child_dob` date NOT NULL,
  `child_birth_weight` decimal(5,2) NOT NULL,
  `guardian_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `guardian_phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `physical_address` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `agrees_to_fup` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `mother_status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `mother_art_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `mother_art_start_date` date DEFAULT NULL,
  `child_gender` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `relationship` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`hcc_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `children_child`
--

LOCK TABLES `children_child` WRITE;
/*!40000 ALTER TABLE `children_child` DISABLE KEYS */;
INSERT INTO `children_child` VALUES ('1106','John Waya','2024-11-06',1.70,'Hawa Davie','None','Kubuli near borehole','Yes','Alive OnART','1257',NULL,'Male','Mother'),('1451','Icra Ibrahim','2023-07-03',2.90,'Fazira Makwinja','None','Issa Village','Yes','Alive OnART','290',NULL,'Male','Mother'),('1454','Jazilu Ali Idrissa','2023-07-15',2.80,'Dija Ali','None','Mlani Masyasya at namalomba residence near borehole','Yes','Alive OnART','1072',NULL,'Male','Mother'),('1460','Aneesha Mkandawire','2023-07-28',2.30,'Laina Adam','None','Ng\'ombe at Kaloyesi\'s household','Yes','Alive OnART','2787',NULL,'Female','Mother'),('1481','Ayatu Wasili','2023-09-12',3.20,'Laisi Wasili','None','Kapinjiri at nduwele near lawrence','Yes','Alive OnART','2817','2021-07-05','Male','Mother'),('1489','Alima Ngunga','2023-10-13',2.70,'Aisha Ahamadu','None','Chapola near graveyard at Mnomba','Yes','Alive OnART','2837','2021-08-30','Female','Mother'),('1524','Lukia John','2024-01-15',3.10,'Saujati Deusi','None','Mlanimasyasya at che Mkoka','Yes','Alive OnART','1873','2017-11-22','Female','Mother'),('1562','Mphatso Lapukeni','2024-03-31',3.30,'Hawa Adam','None','Ng\'ombe near borehole at Kasimbo family','Yes','Alive OnART','2338','2019-03-29','Male','Mother'),('1566','Idrissa Frank','2024-04-11',2.30,'Patricia Usuman','None','Moto at Bali\'s residence near Lake','Yes','Alive OnART','1847',NULL,'Male','Mother'),('1570','Mariam Isapi','2024-04-11',2.50,'Michisyeje Twalibu','None','Tumbwe near primary school kwitanda clan make enock','Yes','Alive OnART','1118','2015-12-09','Female','Mother'),('1573','Zione Geofrey','2024-04-07',2.10,'Ulaya Seleman','None','Ng\'ombe near Mpungukwa tree at matin\'s residence as ulaya seleman','Yes','Alive OnART','136','2012-02-10','Female','Mother'),('1594','Uma Isack','2024-06-18',2.90,'Saujatu Lali','None','Biti Kalanje near mosque','Yes','Alive OnART','2821','2021-07-19','Male','Mother'),('1597','Jazaka Lenjere','2024-06-26',3.20,'Teuka Ajida','None','Ng\'ombe near Sikizi Tree','Yes','Alive OnART','2889','2021-12-21','Male','Mother'),('1601','Modester Chiwaya','2024-07-11',2.40,'Patricia Magwetsera','None','Tumbwe at Mr Chiwaya Residence near new apostolic church','Yes','Alive OnART','2098','2018-07-10','Female','Mother'),('1610','Bashil Bwanali','2024-07-29',3.20,'Saujati Saizi','None','Ng\'ombe near borehole at kasimbo residence','Yes','Alive OnART','398','2013-04-17','Male','Mother'),('1635','Hamida Saidi','2024-09-07',2.90,'Alima Saidi','None','Matukuta near Mingole residence','Yes','Alive OnART','2636','2016-02-24','Female','Mother'),('1637','Indi Mbwana','2024-09-26',3.50,'Sarah Chintengo','0991315835','Mbanda near Kampepuza market at abdul residence','Yes','Alive OnART','1327','2016-06-22','Female','Mother'),('1640','Sainab Majidu','2024-10-01',2.50,'Sakina Amidu','None','Mbuzi @ Bakali residence near borehole','Yes','Alive OnART','1605','2017-03-20','Female','Mother'),('1641','Shanifu Julius','2024-10-01',2.70,'Pakombwere Alabi','None','Fowo village at Biti white residence near miwawe river','Yes','Alive OnART','279','2012-09-05','Male','Mother'),('1644','Bright Phiri','2024-10-06',2.90,'Lexa Chizimba','0886200692','Taliya Village taliya turn off left side ask for chimbalanga','Yes','Alive OnART','3271','2024-04-22','Male','Mother'),('1646','Jazaka Sefu','2024-10-08',2.50,'Machemba Sefu','None','Mlanichapola at titukulane sign post','Yes','Alive OnART','232','2012-07-04','Male','Mother'),('1648','Yusuf Ishmael Msusa','2024-08-14',3.00,'Zione Msusa','None','Fowo at che waya near borehole','Yes','Alive OnART','3290','2024-05-20','Male','Mother'),('1651','Samson Abdul','2024-10-17',3.00,'Patuma Awali','None','Moto near ntengeza kenaka kufusa khomo la amadu','Yes','Alive OnART',NULL,NULL,'Male','Mother'),('1654','Patuma Shukurani','2024-11-05',2.70,'Patuma Assani','0993474705','Mwanjati at Sawanja near borehole','Yes','Alive OnART','3326','2024-08-19','Female','Mother'),('1655','Amina Hussein','2024-10-04',2.50,'Laita Lajab','None','Mlanimasyasya near taliya F.P. School, Chikole residence','Yes','Alive OnART','867','2024-10-04','Female','Mother'),('1656','Davie Walusa','2024-11-12',2.70,'Lucy Walusa','None','Mwanjati 1 @ Wasayo near Mwanjati School','Yes','Alive OnART','541','2013-10-02','Male','Mother'),('1658','Shukulani Mmadi','2024-11-13',2.80,'Luckia Mmadi','None','Ng\'ombe at lajabu\'s Residence near Msikizi','Yes','Alive OnART','2395','2019-06-07','Female','Mother'),('1659','Shumesidine Muhammad','2024-11-14',2.10,'Utule Allie','None','Magongwe at Chisanje\'s Residence near mosque','Yes','Alive OnART','3333','2024-09-09','Female','Mother'),('1660','Rame Selemani','2024-11-15',2.30,'Fatima Allie','None','Kwilasya Razinga residence near mosque','Yes','Alive OnART','577','2013-10-23','Female','Mother'),('1661','Juma Goliati','2024-11-15',3.10,'Sinjiri Goliati','None','Tumbwe Mdulu Village at Makwelera residence near Dimba','Yes','Alive OnART','2856','2021-10-18','Male','Mother'),('1662','Fauziya Makwinja','2024-11-19',2.90,'Asiyatu Makwinja','None','Ng\'ombe near School at Abiti Ali residence','Yes','Alive OnART','3317',NULL,'Female','Mother'),('1663','Agness Peter','2024-11-20',3.40,'Aisha Silaji','None','Machakwani at Omar residence near borehole','Yes','Alive OnART','3318',NULL,'Female','Mother'),('1664','Lajab Bwanali','2024-11-20',3.60,'Zione Ajati','None','Mnekasya at Labiano\'s residence near Kundi river','Yes','Alive OnART','2133',NULL,'Male','Mothe'),('1666','Juma Yasini','2024-10-11',2.80,'Sigele Yasin','0991694033','Chapola Namabvi near chigayo chakambulire, Dyton residence','Yes','Alive OnART','2522',NULL,'Male','Mother'),('1668','Razack James','2024-12-06',3.30,'Tabia kassim','None','Ng\'ombe near kachete lake at Manjawira residence','Yes','Alive OnART','2608',NULL,'Male','Mother'),('1669','Sumaiya Hussein','2024-12-08',3.10,'Cecelia Rasheed','None','Taliya Near School at Issa Residence','Yes','Alive OnART','3083',NULL,'Female','Mother'),('1672','Dija Mdala','2025-01-01',2.80,'Hajira Mdala','0988902887','Chapola near mosque at Mpende residence','Yes','Alive OnART','876',NULL,'Female','Mother'),('1674','Nazeer Abrahaman','2025-01-17',2.20,'Hawa Rajab','0995123289','Fow behind the market at Adam\'s residence','Yes','Alive OnART','752',NULL,'Male','Mother'),('1675','Aisha Allie','2025-01-17',2.90,'Asiyatu Fosiko','None','Chapola near mosque at sefu residence','Yes','Alive OnART','2020',NULL,'Female','Mother'),('1676','Estery Usi','2025-01-19',2.60,'Rose Usi','None','Ng\'ombe near the lake at mhango residence','Yes','Alive OnART','3214',NULL,'Female','Mother'),('1677','Sime Muhammad','2024-12-26',2.60,'Mariam Ibra','None','Fowo','Yes','Alive OnART','2836','2021-08-23','Female','Mother'),('1678','Lukushena Alick','2025-01-21',2.80,'Asiyatu Billy','None','Issa near graveyard at Issa residence ask mai ake a zakiya','Yes','Alive OnART','3008',NULL,'Female','Mother'),('1679','Sara Adam','2025-01-31',3.40,'Mariam Adam','None','Naluma near Lajab maize meal at Kalino clan','Yes','Alive OnART','2616',NULL,'Female','Mother'),('1680','Edward Kasimu','2025-02-03',3.00,'Rose Katengu','None','Chilonga near Dam at Windo residence','Yes','Alive OnART','1834',NULL,'Male','Mother'),('1681','Shalifa Issa','2025-02-03',2.30,'Zainab John','None','Ng\'ombe @ Kazembe','Yes','Alive OnART','1743',NULL,'Female','Mother'),('1682','Junaidi Anisa','2025-02-02',3.20,'Sakina Iron','0886743688','M\'doka chowe at Biti Shaibu near Mlambe tree','Yes','Alive OnART','2684',NULL,'Male','Mother'),('1683','Jazaka Liya','2025-01-22',3.20,'Lima Liya','None','Talia near mosque at muli last mosque','Yes','Alive OnART','1180',NULL,'Male','Mother'),('1684','Atupele Asima','2025-01-22',3.00,'Amina Shaibu','None','Machakwani at Lilongwe along the lake','Yes','Alive OnART','848',NULL,'Female','Mother'),('1685','Mariam Mussa','2025-02-10',1.90,'Patuma Saidi','None','Ng\'ombe near borehole','Yes','Alive OnART','4744',NULL,'Female','Mother'),('1686','Chikondi Mussa','2025-02-10',1.70,'Patuma Saidi','None','Ng\'ombe near borehole','Yes','Alive OnART','4744',NULL,'Male','Mother'),('1687','Hanisha Yusufu','2025-02-12',1.90,'Rose Islam','None','Magongwe near Mdalamakumba school','Yes','Alive OnART','13',NULL,'Female','Mother'),('1688','Amina Namwera','2025-02-12',3.30,'Aisha Wayala','None','Kapinjiri near Mosque','Yes','Alive OnART',NULL,NULL,'Female','Mother'),('1689','Laisa Missi','2024-12-24',3.00,'Saituna Missi','None','Malunda at Lemani residence near borehole','Yes','Alive OnART','2644',NULL,'Female','Mother'),('1691','Issa Ajusu','2025-12-17',3.00,'Marriam Jafali','None','Mlani masyasya Ukanda residence near borehole','Yes','Alive OnART','2443',NULL,'Male','Mother'),('1692','Mirriam Mustafa','2025-01-10',3.00,'Mirriam Mustafa','None','Chilonga at che Window','Yes','Alive OnART','639','2020-04-09','Female','Mother'),('1693','Fahim Yahaya','2025-02-24',3.10,'Mariam Yahaya','None','Chapola at biti majawa residence near market','Yes','Alive OnART','2766',NULL,'Male','Mother'),('1694','Hanilu Jawadu','2025-02-27',3.30,'Stella Lucius','None','Rashid at Mwase\'s Residence','Yes','Alive OnART','3186',NULL,'Male','Mother'),('1695','Veronica Mwamadi','2024-12-29',3.00,'Edina Kachepa','None','Tumbwe @ Masuku near CCAP Church','Yes','Alive OnART','757',NULL,'Female','Mother'),('1696','Hanifu Janes','2025-03-07',2.30,'Kuseka William','None','Mlanimasyasya at chesomba\'s residence near river','Yes','Alive OnART',NULL,NULL,'Male','Mother'),('1699','Gloria Wilson','2025-03-19',3.00,'Veronica Moses','None','matukuta at Raphael Residence','Yes','Alive OnART','2184',NULL,'Female','Mother'),('1702','Issa Msusa','2025-03-22',3.30,'Marriam Saiti','None','Ng\'ombe near borehole at safari residence','Yes','Alive OnART','1996',NULL,'Male','Mother'),('1703','Blisseings Dyason','2025-04-08',1.90,'Grace Banda','None','Fowo at Ndileya\'s residence near borehole','Yes','Alive OnART','1277',NULL,'Male','Mother'),('1704','Paulos Dyson','2025-04-08',1.60,'Grace Panda','None','Fowo at Ndileya\'s residence near borehole','Yes','Alive OnART','1277',NULL,'Male','Mother'),('1705','Zainab Jonasi','2025-04-08',2.90,'Maria Namate','None','Issa near the village headman at holande residence','Yes','Alive OnART','238',NULL,'Female','Mother'),('1707','Lilian Chikumbutso','2025-04-10',2.70,'Halima Frank','None','Rashid near borehole at frank trace residence','Yes','Alive OnART','3370','2024-12-16','Female','Mother'),('1708','Felix Kaluwa','2025-04-14',3.20,'Sumaya William','None','Ng\'ombe at Kalowo residence near lake','Yes','Alive OnART','3351',NULL,'Male','Mother'),('1709','Bibi Mbaya','2025-02-04',2.40,'Mbuseje Msusa','None','Biti kalanje at Piyasi','Yes','Alive OnART','150','2012-02-29','Female','Mother'),('1710','Atupele Rashid','2025-04-08',2.50,'Asiyatu Imedi','None','Mtaka 2 near nursery school sign post at sabiti','Yes','Alive OnART','3051',NULL,'Female','Mother'),('1711','Ishmael Mbwana','2025-04-19',2.80,'Jackreen Leonard','None','Mbuzi near mosque at Mapudi','Yes','Alive OnART','1520',NULL,'Male','Mother'),('1714','Shaniya Ajison','2025-04-28',3.30,'Asiyatu Jali','None','Mpundi at Pausanda\'s residence near graveyard','Yes','Alive OnART',NULL,NULL,'Female','Mother'),('1715','Lashima Akidu','2025-04-29',3.30,'Lima Majidu','None','Ng\'ombe at Mandiwaza\'s residence near shops','Yes','Alive OnART','2323',NULL,'Female','Mother'),('1716','Razack Twaibu','2025-05-02',3.60,'Edina Twaibu','None','Chapola near the Lake at Mr usuman\'s Residence','Yes','Alive OnART','596','2013-11-26','Male','Mother'),('1717','Charity Jannatu','2025-05-12',2.90,'Dija Kazembe','None','Mpundi','Yes','Alive OnART','1449',NULL,'Female','Mother'),('1718','Abdulrazack Kalisa','2025-04-22',3.00,'Fatima Anafi','0885481060','Mdala at abiti Mussa at Baobab tree after lugola primary','Yes','Alive OnART','2834',NULL,'Male','Mother'),('1719','Sallina John','2025-05-28',3.00,'Hawa Abudu','None','Biti kalanje at Biti Yasin\'s residence near football groung','Yes','Alive OnART','2417',NULL,'Female','Mother'),('1720','Jamila Yusuf','2025-03-16',3.00,'Zalia Belo','None','Chapola at Chitambo near lake','Yes','Alive OnART','464',NULL,'Female','Mother'),('1722','Abdul Saiti','2025-05-31',2.70,'Pakombwere Alli','None','Mpundi near Mosque at Mtola','Yes','Alive OnART','000','1900-01-01','Male','Mother'),('1723','Zainab Abdul','2025-06-01',3.50,'Maimuna Usseni','None','Chapola near borehole at Windimedi residence','Yes','Alive OnART','2716','2020-12-22','Female','Mother'),('1724','Grace Asedi','2025-06-06',3.00,'Asiyatu Geofrey','None','Mwanjati near Mwanjati Primary','Yes','Alive OnART','1834','1900-01-01','Female','Mother'),('1725','Lucia Geofrey','2025-06-10',3.20,'Grace Alli','None','Mpundi near Manyumba ten at Samuel Kanjoka\'s Residence','Yes','Alive OnART','2334','2019-03-21','Female','Mother'),('1726','Haji Asick','2025-06-14',3.20,'Hawa Kasimu','None','Ng\'ombe at Twaibu\'s residence near borehole','Yes','Alive OnART','3050','2020-02-28','Male','Mother'),('1727','Falida Nufu','2025-06-16',2.00,'Labia Anafi','None','Chapola At Mbobo\'s Residence near Borehole','Yes','Alive OnART','809','2014-09-01','Female','Mother'),('1730','Bonomali Jella','2025-06-22',2.70,'Patuma Jella','None','Liwale at Makawa near ground and borehole','Yes','Alive OnART','2464','2018-04-25','Male','Mother'),('1731','Saudi Issa','2025-06-15',3.00,'Maimuna Time','None','Mwanjati near Chikwangwani cha Mwanjati Primary Schook ask for a telala a time','Yes','Alive OnART','3392','2025-02-24','Male','Mother'),('1732','Shabilu Kassimu','2025-05-15',2.60,'Bibi Oliva','None','Matukuta at Bonomali near Miwawe','Yes','Alive OnART','2085','2018-06-28','Male','Mother'),('1734','Rajifu Seleman','2025-07-01',2.80,'Emele Rabson','None','Ng\'ombe near football ground at chikoko residence','Yes','Alive OnART','2314','2019-02-21','Male','Mother'),('1735','Asibu Jonathan','2025-07-08',3.20,'Longwele Amini','None','Tumbwe at Makwelera','Yes','Alive OnART','1656',NULL,'Male','Mother'),('1736','Faiza Jafali','2025-04-10',3.30,'Zaione Amadu','None','Matanda near borehole','Yes','Alive OnART','2265',NULL,'Female','Mother');
/*!40000 ALTER TABLE `children_child` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `children_childvisit`
--

DROP TABLE IF EXISTS `children_childvisit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `children_childvisit` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `visit_date` date DEFAULT NULL,
  `height` decimal(5,2) DEFAULT NULL,
  `weight` decimal(5,2) DEFAULT NULL,
  `muac` decimal(4,1) DEFAULT NULL,
  `wasting` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `breastfeeding` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `mother_art_status` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `clinical_monitoring` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `hiv_testing` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `infection_status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `cpt_given` int unsigned DEFAULT NULL,
  `follow_up_outcome` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `next_appointment_or_outcome_date` date DEFAULT NULL,
  `child_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `drug_given` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `children_childvisit_child_id_15ab8f13_fk_children_` (`child_id`),
  CONSTRAINT `children_childvisit_child_id_15ab8f13_fk_children_` FOREIGN KEY (`child_id`) REFERENCES `children_child` (`hcc_number`),
  CONSTRAINT `children_childvisit_chk_1` CHECK ((`cpt_given` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `children_childvisit`
--

LOCK TABLES `children_childvisit` WRITE;
/*!40000 ALTER TABLE `children_childvisit` DISABLE KEYS */;
INSERT INTO `children_childvisit` VALUES (4,'2025-07-08',71.00,8.50,13.0,'No','M','On ART','NAD','No','D',180,'Con','2025-10-03','1566','CPT'),(5,'2025-07-08',52.00,NULL,NULL,'No','Exc','On ART','NAD','Dbs','D',90,'Con','2025-10-10','1723','CPT'),(6,'2025-07-08',80.00,9.70,13.9,'No','<6','On ART','NAD','No','D',180,'Con','2025-10-03','1489','CPT'),(8,'2025-07-09',52.00,NULL,NULL,'No','Exc','On ART','NAD','Dbs','D',30,'Con','2025-08-08','1719','CPT'),(9,'2025-07-09',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Rt','C',NULL,'Dis','2025-07-09','1454','CPT'),(10,'2025-07-09',70.00,8.80,14.5,'No','M','On ART','NAD','No','D',180,'Con','2025-10-04','1640','CPT'),(11,'2025-07-08',NULL,2.80,NULL,'No','Exc','On ART','NAD','No','C',105,'Con','2025-08-08','1734','NVP'),(12,'2025-06-22',NULL,2.70,NULL,'No','Exc','On ART','NAD','No','C',200,'Con','2025-08-04','1730','NVP'),(13,'2025-06-15',NULL,3.00,NULL,'No','Exc','On ART','NAD','No','C',60,'Con','2025-07-31','1731','2P'),(14,'2025-06-14',NULL,3.20,NULL,'No','Exc','On ART','NAD','No','C',NULL,'Con','2025-07-25','1726','NVP'),(15,'2025-06-10',NULL,3.20,NULL,'No','Exc','On ART','NAD','No','C',NULL,'Con','2025-07-23','1725','NVP'),(16,'2025-06-16',NULL,2.00,NULL,'No','Exc','On ART','NAD','No','C',NULL,'Con','2025-07-25','1727','NVP'),(17,'2025-06-06',NULL,2.70,NULL,'No','Exc','On ART','NAD','No','C',NULL,'Con','2025-07-14','1722','NVP'),(18,'2025-05-02',NULL,3.60,NULL,'No','Exc','On ART','NAD','No','C',200,'Con','2025-06-13','1716','NVP'),(19,'2025-06-13',58.00,6.10,NULL,'No','Exc','On ART','NAD','Dbs','A',180,'Con','2025-08-06','1716','CPT'),(20,'2025-05-15',NULL,2.60,NULL,'No','Exc','On ART','NAD','No','C',200,'Con','2025-06-30','1732','NVP'),(21,'2025-06-30',54.00,4.80,NULL,'No','Exc','On ART','NAD','Dbs','C',90,'Con','2025-10-03','1732','CPT'),(22,'2025-05-12',NULL,2.90,NULL,'No','Exc','On ART','NAD','No','C',200,'Con','2025-06-23','1717','NVP'),(23,'2025-06-26',54.00,5.00,NULL,'No','Exc','On ART','NAD','Dbs','C',90,'Con','2025-10-03','1717','CPT'),(24,'2025-04-15',NULL,3.20,NULL,'No','Exc','On ART','NAD','No','C',200,'Con','2025-05-30','1708','NVP'),(25,'2025-05-30',NULL,5.20,NULL,'No','Exc','On ART','NAD','Dbs','A',30,'Con','2025-06-27','1708','CPT'),(26,'2025-06-30',59.00,6.00,NULL,'No','Exc','On ART','NAD','No','C',180,'Con','2025-09-19','1708','CPT'),(27,'2025-04-28',NULL,3.30,NULL,'No','Exc','On ART','NAD','No','C',200,'Con','2025-06-13','1714','NVP'),(28,'2025-04-29',NULL,3.30,NULL,'No','Exc','On ART','NAD','No','C',200,'Con','2025-06-13','1715','NVP'),(29,'2025-06-13',58.00,5.50,NULL,'No','Exc','On ART','NAD','Dbs','A',90,'Con','2025-09-05','1715','CPT'),(30,'2025-04-16',NULL,2.80,NULL,'No','Exc','No ART','NAD','No','C',200,'Con','2025-05-20','1710','NVP'),(31,'2025-05-20',56.00,4.50,NULL,'No','Exc','On ART','NAD','No','C',60,'Con','2025-07-11','1710','CPT'),(32,'2025-04-08',NULL,1.90,NULL,'No','Exc','On ART','NAD','No','C',200,'Con','2025-05-23','1703','NVP'),(33,'2025-06-06',47.00,2.90,NULL,'No','Exc','On ART','NAD','Dbs','A',120,'Con','2025-10-02','1703','CPT'),(34,'2025-04-08',NULL,1.60,NULL,'No','Exc','On ART','NAD','Dbs','A',200,'Con','2025-05-23','1704','NVP'),(35,'2025-06-06',47.00,3.20,NULL,'No','Exc','On ART','NAD','Dbs','A',120,'Con','2025-10-02','1704','CPT'),(36,'2025-05-28',51.00,5.50,NULL,'No','Exc','On ART','NAD','No','C',200,'Con','2025-06-05','1718','NVP'),(37,'2025-06-06',51.00,5.50,NULL,'No','Exc','On ART','NAD','Dbs','A',90,'Con','2025-09-03','1718','CPT'),(38,'2025-04-09',NULL,2.90,NULL,'No','Exc','On ART','NAD','No','C',100,'Con','2025-05-23','1705','NVP'),(39,'2025-06-06',52.00,5.00,NULL,'No','Exc','On ART','NAD','Dbs','C',90,'Con','2025-09-05','1705','CPT'),(40,'2025-04-10',NULL,2.70,NULL,'No','Exc','On ART','NAD','No','C',100,'Con','2025-05-23','1707','NVP'),(41,'2025-07-01',NULL,58.00,NULL,'No','Exc','On ART','NAD','Dbs','C',90,'Con','2025-09-19','1707','CPT'),(42,'2025-04-19',NULL,2.80,NULL,'No','Exc','On ART','NAD','No','C',200,'Con','2025-05-30','1711','NVP'),(43,'2025-05-30',53.00,5.00,NULL,'No','Exc','On ART','NAD','Dbs','A',90,'Con','2025-08-08','1711','CPT'),(44,'2025-03-23',NULL,3.30,NULL,'No','Exc','On ART','NAD','No','C',100,'Con','2025-05-09','1702','NVP'),(45,'2025-05-30',59.00,5.90,NULL,'No','Exc','On ART','NAD','Dbs','C',90,'Con','2025-08-22','1720','CPT'),(46,'2025-06-26',NULL,NULL,NULL,'No','Exc','On ART','NAD','No','C',NULL,'To','2025-06-26','1699',NULL),(47,'2025-04-18',NULL,3.40,NULL,'No','Exc','On ART','NAD','No','C',90,'Con','2025-07-16','1696','CPT'),(48,'2025-03-28',49.00,3.80,NULL,'No','Exc','On ART','NAD','Dbs','A',91,'Con','2025-06-20','1685','CPT'),(49,'2025-03-28',50.10,4.00,NULL,'No','Exc','On ART','NAD','Dbs','A',90,'Con','2025-06-20','1686','CPT'),(50,'2025-04-15',NULL,NULL,NULL,'No','Exc','On ART','NAD','Dbs','A',90,'Con','2025-07-04','1709','CPT'),(51,'2025-07-01',62.00,6.00,NULL,'No','M','On ART','NAD','No','C',180,'Con','2025-09-26','1688','CPT'),(52,'2025-07-01',61.00,5.50,NULL,'No','M','On ART','NAD','No','C',90,'Con','2025-09-26','1687','CPT'),(53,'2025-05-02',62.00,7.30,NULL,'No','Exc','On ART','NAD','No','C',180,'Con','2025-07-25','1682','CPT'),(54,'2025-04-04',57.00,5.50,NULL,'No','Exc','On ART','NAD','Dbs','A',120,'Con','2025-07-10','1693','CPT'),(55,'2025-06-27',63.00,6.60,NULL,'No','Exc','On ART','NAD','No','C',120,'Con','2025-10-31','1681','CPT'),(56,'2025-06-27',73.00,9.60,NULL,'No','Exc','On ART','NAD','No','C',180,'Con','2025-09-19','1680','CPT'),(57,'2025-04-11',57.00,6.40,NULL,'No','Exc','On ART','NAD','Dbs','A',120,'Con','2025-07-18','1694','CPT'),(58,'2025-05-30',NULL,NULL,NULL,'No','Exc','On ART','NAD','No','C',360,'Con','2025-11-21','1674','CPT'),(59,'2025-05-30',62.00,NULL,NULL,'No','Exc','On ART','NAD','No','C',90,'Con','2025-08-22','1684','CPT'),(60,'2025-04-25',63.00,NULL,NULL,'No','Exc','On ART','NAD','No','C',180,'Con','2025-07-25','1672','CPT'),(61,'2025-05-16',64.00,NULL,NULL,'No','Exc','On ART','NAD','No','C',180,'Con','2025-08-15','1675','CPT'),(62,'2025-04-07',NULL,NULL,NULL,'No','Exc','On ART','NAD','Dbs','A',180,'Con','2025-07-18','1676','CPT'),(63,'2025-02-21',54.00,NULL,NULL,'No','Exc','On ART','NAD','No','C',90,'Con','2025-05-16','1692','CPT'),(64,'2025-06-06',58.00,6.00,NULL,'No','Exc','On ART','NAD','No','C',180,'Con','2025-09-05','1678','CPT'),(65,'2025-06-06',640.00,8.50,NULL,'No','M','On ART','Sick','No','C',180,'Con','2025-09-05','1683','CPT'),(66,NULL,NULL,NULL,NULL,'No','Exc','On ART','NAD','No','C',NULL,'To','2025-07-18','1724','CPT'),(67,'2025-05-19',57.00,5.90,NULL,'No','Exc','On ART','NAD','Dbs','A',90,'Con','2025-08-15','1736','CPT'),(68,'2025-07-08',NULL,3.20,NULL,'No','Exc','On ART','NAD','No','C',200,'Con','2025-08-19','1735','NVP'),(69,'2025-07-10',82.00,13.00,17.5,'No','Exc','On ART','NAD','Rt','A',NULL,'Dis','2025-07-10','1460','None'),(70,'2025-07-10',66.00,7.60,12.5,'No','M','On ART','Sick','No','C',180,'Con','2025-09-26','1637','CPT'),(71,'2025-07-11',NULL,NULL,NULL,NULL,'M','On ART',NULL,'No','C',180,'Con','2025-10-10','1481','CPT'),(72,'2025-07-11',73.00,8.00,13.5,'No','Exc','On ART','NAD','No','C',180,'Con','2025-10-17','1594','CPT'),(73,'2025-07-11',70.00,8.00,12.8,'No','Exc','On ART','NAD','No','C',180,'Con','2025-10-10','1573','CPT'),(74,'2025-07-11',68.00,8.00,13.0,'No','Exc','On ART','NAD','No','C',180,'Con','2025-10-03','1648','CPT'),(75,'2025-07-11',80.00,11.30,14.0,'No','Exc','On ART','NAD','Rt','A',NULL,'Dis','2025-07-11','1451','None'),(76,'2025-07-11',64.00,8.50,14.0,'No','M','On ART','NAD','No','C',180,'Con','2025-10-24','1663','CPT'),(77,'2025-07-11',71.00,8.00,12.0,'No','M','On ART','NAD','No','C',180,'Con','2025-10-03','1570','CPT'),(78,'2025-07-11',76.00,10.50,13.5,'No','M','On ART','NAD','No','C',180,'Con','2025-10-10','1524','CPT'),(79,'2025-07-11',67.50,9.50,16.5,'No','M','On ART','NAD','No','A',180,'Con','2025-10-03','1601','CPT'),(80,'2025-07-11',74.00,10.00,14.0,'No','M','On ART','NAD','Rt','A',180,'Con','2025-10-03','1610','CPT'),(81,'2025-07-11',79.00,11.30,15.0,'No','M','On ART','NAD','Rt','A',180,'Con','2025-10-10','1597','CPT'),(82,'2025-07-11',67.00,8.00,NULL,'No','M','On ART','NAD','No','C',180,'Con','2025-10-10','1693','CPT'),(83,'2025-07-11',82.00,11.50,14.4,'No','M','On ART','NAD','No','C',180,'Con','2025-10-10','1562','CPT'),(84,'2025-07-11',78.00,8.50,13.9,'No','M','On ART','NAD','No','C',120,'Con','2025-09-05','1635','CPT'),(85,'2025-05-22',60.00,7.10,NULL,'No','Exc','On ART','NAD','Dbs','A',180,'Con','2025-08-15','1669','CPT'),(86,'2025-06-03',69.00,9.50,15.0,'No','M','On ART','NAD','No','C',180,'Con','2025-09-05','1668','CPT'),(87,'2025-06-02',64.00,7.40,13.0,'No','M','On ART','NAD','No','C',180,'Con','2025-08-22','1695','CPT'),(88,'2025-05-07',66.00,7.00,NULL,'No','Exc','On ART','NAD','Dbs','A',180,'Con','2025-08-01','1677','CPT'),(89,'2025-05-19',64.00,6.40,NULL,'No','Exc','On ART','NAD','Dbs','A',180,'Con','2025-08-15','1691','None'),(90,'2025-04-29',64.00,7.60,NULL,'No','Exc','On ART','NAD','No','C',180,'Con','2025-07-21','1689','CPT'),(91,NULL,NULL,NULL,NULL,'No','Exc','On ART','NAD','No','C',NULL,'To','2025-02-20','1656','CPT'),(92,'2025-02-28',NULL,5.50,NULL,'No','Exc','On ART','NAD','Dbs','A',90,'Con','2025-05-30','1654','CPT'),(93,'2025-04-18',NULL,7.00,NULL,'No','Exc','On ART','NAD','No','C',NULL,'Con','2025-07-11','1662','CPT'),(94,'2025-05-16',65.00,7.40,13.0,'No','M','On ART','NAD','No','C',180,'Con','2025-08-08','1664','CPT'),(95,'2025-05-09',74.00,8.50,15.0,'No','M','On ART','NAD','No','C',180,'Con','2025-08-01','1658','CPT'),(96,'2025-04-01',59.00,6.10,NULL,'No','Exc','On ART','NAD','No','C',240,'Con','2025-07-18','1659','CPT'),(97,'2025-06-06',66.00,7.00,12.5,'No','M','On ART','NAD','No','C',180,'Con','2025-09-05','1660','CPT'),(98,'2025-06-20',60.00,6.60,12.5,'No','M','On ART','NAD','No','C',180,'Con','2025-09-12','1106','CPT'),(99,'2025-06-06',70.00,8.60,NULL,'No','M','On ART','NAD','No','C',180,'Con','2025-08-29','1661','CPT'),(100,'2025-06-19',68.00,7.70,13.5,'No','M','On ART','NAD','No','C',240,'Con','2025-10-17','1651','CPT'),(101,'2025-06-13',NULL,8.30,NULL,'No','M','On ART','NAD','No','C',240,'Con','2025-10-10','1644','CPT'),(102,'2025-05-30',72.00,7.90,NULL,'No','M','On ART','NAD','No','C',180,'Con','2025-08-22','1666','CPT'),(103,'2025-06-27',69.00,8.90,14.7,'No','M','On ART','NAD','No','C',180,'Con','2025-09-19','1641','CPT'),(104,'2025-06-27',66.00,7.90,14.0,'No','M','On ART','NAD','No','C',180,'Con','2025-09-19','1655','CPT'),(105,'2025-04-22',67.00,8.00,NULL,'No','Exc','On ART','NAD','No','C',180,'Con','2025-07-13','1646','CPT');
/*!40000 ALTER TABLE `children_childvisit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `children_htssample`
--

DROP TABLE IF EXISTS `children_htssample`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `children_htssample` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sample_date` date NOT NULL,
  `test_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `sample_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `result` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `date_received` date DEFAULT NULL,
  `child_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `children_htssample_child_id_00066d79_fk_children_` (`child_id`),
  CONSTRAINT `children_htssample_child_id_00066d79_fk_children_` FOREIGN KEY (`child_id`) REFERENCES `children_child` (`hcc_number`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `children_htssample`
--

LOCK TABLES `children_htssample` WRITE;
/*!40000 ALTER TABLE `children_htssample` DISABLE KEYS */;
INSERT INTO `children_htssample` VALUES (1,'2025-07-08','DBS','679',NULL,NULL,'1723'),(2,'2024-11-15','DBS','618','Negative','2024-11-21','1640'),(3,'2025-06-13','DBS','676','Negative','2025-06-27','1715'),(4,'2025-07-09','DBS','666','Negative','2025-06-03','1710'),(5,'2025-06-06','DBS','672','Negative','2025-06-23','1703'),(6,'2025-06-06','DBS','673','Negative','2025-06-23','1704'),(7,'2025-06-06','DBS','671','Negative','2025-06-23','1718'),(8,'2025-06-06','DBS','674','Negative','2025-06-23','1705'),(9,'2025-07-01','DBS','678',NULL,NULL,'1707'),(10,'2025-05-30','DBS','338','Negative','2025-06-10','1711'),(11,'2025-05-30','DBS','669','Negative','2025-06-10','1720'),(12,'2025-04-23','DBS','660','Negative','2025-05-09','1696'),(13,'2025-04-15','DBS','659','Negative','2025-05-09','1709'),(14,'2025-03-28','DBS','651','Negative','2025-04-10','1688'),(15,'2025-03-28','DBS','652','Negative','2025-04-09','1687'),(16,'2025-03-21','DBS','650','Negative','2025-03-27','1682'),(17,'2025-04-04','DBS','655','Negative','2025-04-14','1693'),(18,'2025-04-04','DBS','656','Negative','2025-04-14','1680'),(19,'2025-04-11','DBS','658','Negative','2025-04-17','1694'),(20,'2025-02-28','DBS','639','Negative','2025-03-11','1674'),(21,'2025-03-14','DBS','647','Negative','2025-03-27','1684'),(22,'2025-04-25','DBS','661','Negative','2025-05-15','1672'),(23,'2025-03-24','DBS','642','Negative','2025-03-27','1675'),(24,'2025-04-07','DBS','657','Negative','2025-04-14','1676'),(25,'2025-03-07','DBS','643','Negative','2025-03-27','1678'),(26,'2025-03-07','DBS','644','Negative','2025-03-27','1683'),(27,'2025-03-14','DBS','646','Negative','2025-03-27','1679'),(28,'2025-05-15','DBS','665','Negative','2025-06-03','1736'),(29,'2025-07-10','Rapid','15550-36-4-H','Negative','2025-07-10','1460'),(30,'2024-11-08','DBS','614','Negative','2024-11-28','1637'),(31,'2024-10-16','Rapid','12070-72-8-B','Negative','2024-10-16','1481'),(32,'2025-06-16','Rapid','15550-24-17-X','Negative','2025-06-16','1594'),(33,'2025-04-04','Rapid','13771-78-17-B','Negative','2025-04-04','1573'),(34,'2024-10-25','DBS','609','Negative','2024-11-25','1648'),(35,'2025-07-11','Rapid','7368-34-2-X','Negative','2025-07-11','1451'),(36,'2025-01-09','DBS','634','Negative','2025-02-13','1663'),(37,'2025-04-11','Rapid','13771-86-4-Z','Negative','2025-04-11','1570'),(38,'2025-01-20','Rapid','13817-44-9-G','Negative','2025-01-20','1524'),(39,'2025-07-11','Rapid','15550-36-8-F','Negative','2025-07-11','1601'),(40,'2025-07-11','Rapid','15550-36-9-W','Negative','2025-07-11','1610'),(41,'2025-07-11','Rapid','15550-36-8-F','Negative','2025-07-11','1597'),(42,'2025-04-07','Rapid','13947-98-4-P','Negative','2025-04-07','1562'),(43,'2024-10-18','DBS','604','Negative','2024-11-25','1635'),(44,'2025-05-22','DBS','666','Negative','2025-06-03','1669'),(45,'2025-01-20','DBS','638','Negative','2025-03-04','1668'),(46,'2025-03-07','DBS','645','Negative','2021-03-27','1695'),(47,'2025-05-07','DBS','663','Negative','2025-05-22','1677'),(48,'2025-02-28','DBS','640','Negative','2025-03-11','1654'),(49,'2024-12-27','DBS','632','Negative','2025-01-09','1662'),(50,'2025-01-10','DBS','636','Negative','2025-02-13','1664'),(51,'2024-12-27','DBS','630','Negative','2025-01-09','1658'),(52,'2024-12-27','DBS','630','Negative','2025-01-09','1658'),(53,'2024-12-27','DBS','633','Negative','2025-01-09','1659'),(54,'2024-12-27','DBS','631','Negative','2025-01-09','1660'),(55,'2024-12-27','DBS','631','Negative','2025-01-09','1660'),(56,'2024-12-20','DBS','629','Negative','2025-01-09','1106'),(57,'2024-12-20','DBS','629','Negative','2025-01-09','1106'),(58,'2024-12-23','DBS','634','Negative','2025-01-09','1661'),(59,'2024-12-23','DBS','634','Negative','2025-01-09','1661'),(60,'2024-11-28','DBS','623','Negative','2024-12-10','1651'),(61,'2024-11-15','DBS','617','Negative','2024-12-04','1644'),(62,'2024-11-22','DBS','621','Negative','2024-12-11','1666'),(63,'2024-11-15','DBS','615','Negative','2024-12-07','1641'),(64,'2024-11-15','DBS','616','Negative','2024-12-07','1655'),(65,'2024-12-06','DBS','625','Negative','2024-12-19','1646');
/*!40000 ALTER TABLE `children_htssample` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `children_systemlog`
--

DROP TABLE IF EXISTS `children_systemlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `children_systemlog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `action` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `children_systemlog_user_id_e469c4c9_fk_auth_user_id` (`user_id`),
  CONSTRAINT `children_systemlog_user_id_e469c4c9_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `children_systemlog`
--

LOCK TABLES `children_systemlog` WRITE;
/*!40000 ALTER TABLE `children_systemlog` DISABLE KEYS */;
/*!40000 ALTER TABLE `children_systemlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-07-07 06:12:50.656000','2560','Mariam Allie (2560)',3,'',7,1),(2,'2025-07-07 06:12:50.656000','1683','Josephine Phinius (1683)',3,'',7,1),(3,'2025-07-07 06:12:50.656000','122','Alexander Amos (122)',3,'',7,1),(4,'2025-07-07 06:12:50.656000','12','Mariam Allie (12)',3,'',7,1),(5,'2025-07-07 06:16:20.620000','1865','Josephy Martha (1865)',1,'[{\"added\": {}}]',7,1),(6,'2025-07-07 06:18:06.564000','1865','Josephy Chimwemwe (1865)',2,'[{\"changed\": {\"fields\": [\"Child name\"]}}]',7,1),(7,'2025-07-07 06:25:53.142000','6','Josephy Chimwemwe - 2025-07-07 - 32 months',1,'[{\"added\": {}}]',8,1),(8,'2025-07-07 06:35:24.197000','1866','Maria Kadzanjankhoma (1866)',1,'[{\"added\": {}}]',7,1),(9,'2025-07-07 08:21:11.197000','1866','Maria Kadzanjankhoma (1866)',3,'',7,1),(10,'2025-07-07 08:21:11.197000','1865','Josephy Chimwemwe (1865)',3,'',7,1),(11,'2025-07-07 08:23:34.106000','1730','Bonomali Jella (1730)',1,'[{\"added\": {}}]',7,1),(12,'2025-07-07 08:25:34.397000','1731','Saudi Issa (1731)',1,'[{\"added\": {}}]',7,1),(13,'2025-07-07 08:27:20.035000','1724','Grace Asedi (1724)',1,'[{\"added\": {}}]',7,1),(14,'2025-07-07 08:28:54.419000','1726','Haji Asick (1726)',1,'[{\"added\": {}}]',7,1),(15,'2025-07-07 08:30:27.158000','1727','Falida Nufu (1727)',1,'[{\"added\": {}}]',7,1),(16,'2025-07-07 08:31:58.821000','1725','Lucia Geofrey (1725)',1,'[{\"added\": {}}]',7,1),(17,'2025-07-07 08:33:56.895000','1723','Zainab Abdul (1723)',1,'[{\"added\": {}}]',7,1),(18,'2025-07-07 08:35:36.120000','1722','Abdul Saiti (1722)',1,'[{\"added\": {}}]',7,1),(19,'2025-07-07 08:36:49.297000','1716','Razack Twaibu (1716)',1,'[{\"added\": {}}]',7,1),(20,'2025-07-07 08:38:39.577000','1732','Shabilu Kassimu (1732)',1,'[{\"added\": {}}]',7,1),(21,'2025-07-07 08:42:22.466000','1','Osphyncodes',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]',4,1),(22,'2025-07-07 21:34:19.183000','1000','Test Child (1000)',1,'[{\"added\": {}}]',7,1),(23,'2025-07-07 21:36:03.298000','2','Test Child - 2025-05-01 - -2 months',1,'[{\"added\": {}}]',8,1),(24,'2025-07-07 21:37:06.431000','2','Test Child - 2025-05-01 - -2 months',2,'[{\"changed\": {\"fields\": [\"Follow up outcome\"]}}]',8,1),(25,'2025-07-07 21:37:33.271000','2','Test Child - 2025-05-01 - -2 months',2,'[{\"changed\": {\"fields\": [\"Follow up outcome\"]}}]',8,1),(26,'2025-07-07 21:38:25.740000','2','Test Child - 2025-05-01 - -2 months',2,'[{\"changed\": {\"fields\": [\"Next appointment or outcome date\"]}}]',8,1),(27,'2025-07-07 21:38:42.827000','2','Test Child - 2025-05-01 - -2 months',2,'[{\"changed\": {\"fields\": [\"Follow up outcome\"]}}]',8,1),(28,'2025-07-07 21:39:08.440000','2','Test Child - 2025-05-01 - -2 months',2,'[{\"changed\": {\"fields\": [\"Next appointment or outcome date\"]}}]',8,1),(29,'2025-07-07 21:39:29.896000','2','Test Child - 2025-05-01 - -2 months',2,'[{\"changed\": {\"fields\": [\"Next appointment or outcome date\"]}}]',8,1),(30,'2025-07-07 21:43:19.521000','2','Test Child - 2025-05-01 - -2 months',2,'[{\"changed\": {\"fields\": [\"Next appointment or outcome date\"]}}]',8,1),(31,'2025-07-07 21:58:56.867000','1003','Josephy Ng\'omba (1003)',3,'',7,1),(32,'2025-07-07 21:58:56.867000','1002','Josephy Ng\'omba (1002)',3,'',7,1),(33,'2025-07-07 21:58:56.867000','1000','Josephy Ng\'omba (1000)',3,'',7,1),(34,'2025-07-08 11:19:15.391000','1','osphyncodes',2,'[{\"changed\": {\"fields\": [\"Username\"]}}]',4,1),(35,'2025-07-08 12:50:23.192000','1566','Idrissa Frank (1566)',1,'[{\"added\": {}}]',7,1),(36,'2025-07-08 12:57:23.752000','1489','Alima Ngunga (1489)',1,'[{\"added\": {}}]',7,1),(37,'2025-07-09 14:46:38.358000','3','Bonomali Jella - None - ? months',3,'',8,1),(38,'2025-07-09 14:46:38.358000','1','Bonomali Jella - None - ? months',3,'',8,1),(39,'2025-07-09 14:55:29.083000','15','Lucia Geofrey - 2025-06-10 - 0 months',2,'[{\"changed\": {\"fields\": [\"Visit date\"]}}]',8,1),(40,'2025-07-09 15:56:54.145000','34','Paulos Dyson - 2025-04-08 - 0 months',2,'[{\"changed\": {\"fields\": [\"Next appointment or outcome date\"]}}]',8,1),(41,'2025-07-09 15:58:33.166000','34','Paulos Dyson - 2025-04-08 - 0 months',2,'[{\"changed\": {\"fields\": [\"Height\", \"Weight\", \"Drug given\", \"Cpt given\"]}}]',8,1),(42,'2025-07-09 16:37:38.597000','51','Amina Namwera - 2025-07-01 - 5 months',2,'[{\"changed\": {\"fields\": [\"Breastfeeding\"]}}]',8,1),(43,'2025-07-09 17:13:28.770000','65','Jazaka Liya - 2025-06-06 - 5 months',2,'[{\"changed\": {\"fields\": [\"Clinical monitoring\"]}}]',8,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(7,'children','child'),(8,'children','childvisit'),(9,'children','htssample'),(10,'children','systemlog'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-07-09 22:43:15.547841'),(2,'auth','0001_initial','2025-07-09 22:43:17.178992'),(3,'admin','0001_initial','2025-07-09 22:43:17.610919'),(4,'admin','0002_logentry_remove_auto_add','2025-07-09 22:43:17.641972'),(5,'admin','0003_logentry_add_action_flag_choices','2025-07-09 22:43:17.662215'),(6,'contenttypes','0002_remove_content_type_name','2025-07-09 22:43:17.931292'),(7,'auth','0002_alter_permission_name_max_length','2025-07-09 22:43:18.093647'),(8,'auth','0003_alter_user_email_max_length','2025-07-09 22:43:18.148189'),(9,'auth','0004_alter_user_username_opts','2025-07-09 22:43:18.171149'),(10,'auth','0005_alter_user_last_login_null','2025-07-09 22:43:18.339382'),(11,'auth','0006_require_contenttypes_0002','2025-07-09 22:43:18.352413'),(12,'auth','0007_alter_validators_add_error_messages','2025-07-09 22:43:18.376115'),(13,'auth','0008_alter_user_username_max_length','2025-07-09 22:43:18.568574'),(14,'auth','0009_alter_user_last_name_max_length','2025-07-09 22:43:18.736615'),(15,'auth','0010_alter_group_name_max_length','2025-07-09 22:43:18.788166'),(16,'auth','0011_update_proxy_permissions','2025-07-09 22:43:18.811107'),(17,'auth','0012_alter_user_first_name_max_length','2025-07-09 22:43:19.009148'),(18,'children','0001_initial','2025-07-09 22:43:19.090735'),(19,'children','0002_alter_child_child_name_alter_child_guardian_name','2025-07-09 22:43:19.157647'),(20,'children','0003_child_child_gender','2025-07-09 22:43:19.311834'),(21,'children','0004_childvisit','2025-07-09 22:43:19.568752'),(22,'children','0005_child_relationship','2025-07-09 22:43:19.733621'),(23,'children','0006_htssample','2025-07-09 22:43:19.968894'),(24,'children','0007_systemlog','2025-07-09 22:43:20.164362'),(25,'children','0007_alter_childvisit_breastfeeding_and_more','2025-07-09 22:43:21.187606'),(26,'children','0008_merge_20250708_0014','2025-07-09 22:43:21.201266'),(27,'children','0009_alter_htssample_date_received_alter_htssample_result','2025-07-09 22:43:21.533923'),(28,'children','0010_childvisit_drug_given_alter_childvisit_breastfeeding_and_more','2025-07-09 22:43:21.706399'),(29,'children','0011_alter_childvisit_breastfeeding_and_more','2025-07-09 22:43:21.755820'),(30,'sessions','0001_initial','2025-07-09 22:43:21.857418');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('1be6mfrpe5rguz6st2mq05qx39tlrr7y','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZks3:-0kDyI5eavTB6fabbeyCjYlpBqnL90tnd3agG8mjvgI','2025-07-10 06:50:03.607706'),('1rfvcurjpudsz6oo122xdytuogeqy1iu','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uYuw3:gAzKFfU-3xnJqj_iSSNSlRzT-zhTNfpnA2GQHzZHoEk','2025-07-07 23:22:43.255000'),('3tv2plnuelrbxoowub25v9poixpq0lxo','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZdcx:EnOPyoSmKZQuKOBUkgOgKFqmTkot0Cmh4UqnKPLhMG4','2025-07-09 23:05:59.608304'),('4oguh0k2iqgo5g6k2903juvq473bshnk','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uaCwW:FxpaaY_IaemT1oJ6mbBMdin3FgfSNXWRa8UvBD2rAJg','2025-07-11 12:48:32.819045'),('5bkkdsraxpwq6najlb8t1fns76d6xhxr','e30:1uZkMh:zZxI8kPITUNH5gE7gjW3U8Hu-0JHe_tJLi0nBM9WhPg','2025-07-10 06:17:39.155622'),('5j7l3xd8t1qweevp2e8xy1u8hqe7ni25','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZTmN:mXwzbYJ0yhmwAITtxF7kh2x97U42HU8HQ6VvtnRS9tQ','2025-07-09 12:35:03.427000'),('607e96lrve5rnisbh3dold0gwcf5g9nt','e30:1uZU2c:jk-RQ1lOSyALfQH0LpU-wwAN6xjA458JHXjmHXsNL7w','2025-07-09 12:51:50.424000'),('6oohpppicrz5hzizqa6a5zcsl46pxk06','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZn5k:_mPfbpifhC4g0ljHRdKEzeBCEpaHfOpSqvN47fNkwUQ','2025-07-10 09:12:20.188284'),('7m7t241d6ojnq6ufgd1g55zbl4q036vk','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZALU:rEOako8Lexn9K6tVNgjC8lBr9-AMULR4vzL3u5JVjYY','2025-07-08 15:50:00.785000'),('8wt1dplwt6eowod0rq7i7rr72tplebhj','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZ5AJ:hfWcVGpHQ1c7S2IBeJ39kWwu520elEPi5UMd0luRkNI','2025-07-08 10:18:07.300000'),('95t0f6b09fjq2inr5hjzox5dr86gk6uk','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZeZr:8LF9IaT2_HcY3oUdFfoFHKSoAeKbiGpLblix8IseMsg','2025-07-10 00:06:51.116521'),('9deqixd7dkc2fcpsmdrk7ih29i8b4wcw','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZtXO:e-p_m12XvjiaUtTUbf-f7hMo-c41ms2QDCxf8-LsMF0','2025-07-10 16:05:18.401695'),('9kjnzii6dxklr7pc3yy31040ndoqfsk3','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZAS2:Mx1ZSEu85QtY5JXW6YTMxTQO6ZAVHMJJQKsOKraTD8Y','2025-07-08 15:56:46.298000'),('9zyq2ddw90vwvytoos63hz4iv3qbk3f3','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZpe5:VHIeRwM89qFYqE_PpqFA_F-qE7zCpsJ_wPK7Pk__hbY','2025-07-10 11:55:57.644948'),('a4nep7h5v1caiviyc8ica7zknok55mpd','e30:1uZcJk:x2mHziYXeGO0db4TOAeLkm58Rnv9e-XbDhbVKO4HrtU','2025-07-09 21:42:04.451000'),('bdvmy3j5z85zrvui8s5dezz9pn3s61g6','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZaX3:CSzfc22SFAWJghbR_3QUdYCfZTkztfveXRsO7cTtS1U','2025-07-09 19:47:41.621000'),('bsg0b4pnjdx626qpn2l5kxixmg26dztf','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZdIV:x2hKLZQPqWfnnLI6TZ9IXE-n1a8wvJBXzSjxyvzWpn0','2025-07-09 22:44:51.764000'),('bvx0galwgikkxfxhejzyzl2ddcc6luvc','.eJxVjLEOwyAQQ_-FuULJHRDo2D3fgLiDlLQVkUIyVf33EilDa3nys_0WPuxb9ntNq5-juAotLr8ZBX6mcoD4COW-SF7Kts4kj4o8aZXjEtPrdnb_DnKoua0hkgOaLDcDWw2kOquMIgKDCXhwAR2iHrjJdBhtj8QTR-i1UobF5wvugjgA:1ub0I2:n5R6vdse_YsylDKPMR7nihM0UxE7sXLjiLp5fxSsSoM','2025-07-13 17:30:02.935100'),('c1owo6s7owgrxxphkzi2lkroyrdoja5g','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZe1a:le-O5SSBPw2b7_pcERUzTloxg8LJ4wm9imD5AoIt0vM','2025-07-09 23:31:26.670812'),('cwivh3jwrhycl5mnaxgsn0zpvvdagz2h','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZZ4V:XNRkU_1XFmisWT4kfn64l6wqkfbFJ8VMsJeDmaOjytY','2025-07-09 18:14:07.062000'),('d4jo63mddnokj1gsq0w7ud8i3jxp6dg3','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZNPO:3n2rkel51SLwvi8MS512cTXUUE9-AihBegpjMqj3030','2025-07-09 05:46:54.934000'),('dgeyp8hl64xv1k4bfvp0i1j13fgmg4zd','e30:1uZ8GI:nW0v7Co9RjbAaV0BYQJhQau1AUnAtH2L4nQcNmsyGkY','2025-07-08 13:36:30.985000'),('diwq5sq278d1eyk3g125pr0sla3srp1y','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZc1Y:EmpPn3Xw7SPNFyZsNOYFqjo8Erz2QCK53LbfzLEc0Fg','2025-07-09 21:23:16.345000'),('ein6emhtg7u52s9fct17gyts09jb4i4m','e30:1uaxlj:J3VcsjhBjMXCuropC4RASKJ5EQUMR5us0x_ooSLrvtU','2025-07-13 14:48:31.735051'),('gd7h8d6rusidx1nt17c3zh74wi6xibzr','e30:1uZleZ:tHT15lyIgdZqTooZb6O1l0kRFeSZ-LBpF-wc_GeaW4w','2025-07-10 07:40:11.189397'),('ijevxjexql3d68sysxcy725a0fy8m3c0','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZGGS:S_QZFHIJ5k1xsnO5Or4OzppSN9p-2PID_OCfedWUOfk','2025-07-08 22:09:12.377000'),('itju4zpl2qazyz75isf4xcsuoky68csf','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZ7RO:GeO5wsREO15QVuyLDICNcUnoeDYRbw9H8-U1YzxgTHY','2025-07-08 12:43:54.494000'),('jt6dxv8wd2c14o9djqrvp1jaz48hgq94','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uaEWw:p25ZsXoz-NpBz3_M_5BaZGZBiFQmva_kYRaZ4kCYlYM','2025-07-11 14:30:14.898190'),('kcplguq6j754zpjekjdbrjvserxkxdgx','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZq7k:XUEQD-n0HOuKZiXHeILDSY2etmms0JRlkU53evyPC-k','2025-07-10 12:26:36.464735'),('leuoio91bhtkkrfx2ztuzp2dafuwk65e','e30:1uZoe5:NdWzOvSEtAzrH4u3j0HUxye9KHhWS8v8wULsCQ9bNeY','2025-07-10 10:51:53.477793'),('lsj71642vvdd43evqqgkzeb24ruuw8qc','e30:1uZnKQ:KgxEqzIsbfoopoYiLhYJIxx8hqrAuGEHzFdoYpEgSIY','2025-07-10 09:27:30.173283'),('lyal3ak9ekjwhjibnacbnqk6sfgk2x2g','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uabEQ:5NJ44eVfh9l80WCdeXcS0ZdiUW17vZUQc7TyZ37_juQ','2025-07-12 14:44:38.914230'),('mchjod859wcx2fuw21b6o3t71qm99m4c','e30:1uZkaD:_w5nA5_t6d952zQPLAXgkDfnLETC6ZUDdlZDMADkO6o','2025-07-10 06:31:37.836731'),('mlrlf4bg9fns6xtb9b7k2z791mnp16ql','e30:1uZ2q2:sHX_SMoooZHx_wHIhYws_4qfnYf6c4oPwStIIvJlSFw','2025-07-08 07:49:02.020000'),('mnxacd2whye3j9ff97x2ib5v2hq664d1','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZ6Lz:CVfDVprPl0wLbPqIPQI61IACvw5oUolNp4l4NIDKGuY','2025-07-08 11:34:15.595000'),('mvijaf93sfce4cwachwpcpk2uo127g2x','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uaxPB:1QfQr5pQpX1HnVgsy_u-uPbIAe8HaUKgUaU9YqHzfvc','2025-07-13 14:25:13.921008'),('n3fwneyuskzv32o16f41l5u6sgicu5jf','e30:1uZNef:vMnp2AXQzVatH0hn6sZg6-r6sZX_IxIOML4JUJ6Dvl0','2025-07-09 06:02:41.436000'),('n52wiapjk1rm8tfdiisfknqgw2rb5njl','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZVSI:lwNa5XOI8LloegQKfJuhr8TtSCtHNlCrZQhXFoL_W0Y','2025-07-09 14:22:26.525000'),('negp2xsfc4ygbittdzhs7f3zkd06vbru','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uYv2M:T5Lc_kMoRzSNdTi3YkurFnUDJ4S5euwE18hXlza7Mtc','2025-07-07 23:29:14.786000'),('nhl00sqpugqpdn9j6ozseftke4oklx3e','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZAQD:dcYfTBRli3NBvoo55qet55iyJSJVu5cbLZx3PtUSu54','2025-07-08 15:54:53.972000'),('otjutujcq656g5y8rt89ab7dl9y622yy','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZ80L:kjyiARMUWEH-8mdob8Bh9UfNH1oa7LMYmYrEyryHjic','2025-07-08 13:20:01.933000'),('pg8klw4oc0z3palpagb4ht81uhq39zne','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uYvHi:P_1ouIIo_K_OTgv1nrCY-XwQf8Esw_1c2c-RZ9Tbutg','2025-07-07 23:45:06.318000'),('rdrcrp0ne1q2bvciu3w0iu9t4cam58zk','.eJxVjMsOwiAQRf-FtSHQzhRw6d5vIDM8pGogKe3K-O_apAvd3nPOfQlP21r81tPi5yjOYhSn340pPFLdQbxTvTUZWl2XmeWuyIN2eW0xPS-H-3dQqJdvzQbBjDFAZlCWjSFgl3HKIwyQCG0AHjhMhpXT0VmVUKPVORtNGFUS7w_j3Tfb:1uZ2ay:atezPK5IbNzeiPzOgQhbzVbELNpT4qN5bPgaBOtC1Gw','2025-07-08 07:33:28.209000'),('rkayfdr49124lxp1urnnmvcvj1p8doir','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZk7M:YRIkkGNd4dN798Ft_ABwuX7N4ALM2FK04Sh-wKBnAUY','2025-07-10 06:01:48.524723'),('thtko94w10xugdfh7gz4i4sjopv7fn0f','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZnbF:Gm9jXPZkFQNWMGH2JK7swQR-n5LqAPjFjgf2H0dUGmQ','2025-07-10 09:44:53.443821'),('u76atb1v1or5l67wq9u5kji9zs81205x','e30:1uZqZv:Tto8Gz_qQl4YlxYCaivhkEwmNp1OEehGfPzHGvNFjNY','2025-07-10 12:55:43.147504'),('uagbk8ddbcibeojg6wxqaxdgurvnyjkh','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZYcs:wVhSfGS5u-9HNaovz1tVBvWAENAYpMFpLfiPcETYcck','2025-07-09 17:45:34.663000'),('wygqpqr17qv71n5m3h7kch9wr5wz48co','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZbQO:1xTprHZt1euGa8UBENw65EZ1ExHSGnFwMqK_A0jcLo8','2025-07-09 20:44:52.671000'),('wzmrbmxxiqnq182uljudzsd3byho0eam','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZkqQ:jhm75z0Of2gEP5X98wLoKHmecOPLthRpl5mL_UfA5qw','2025-07-10 06:48:22.684872'),('x06t1lx4oazxwfulbtvwhxudxnj4xxzk','e30:1uaDBD:MvJYj0BnNCWNuGgu592KtwF4xEMcJMDZSHn20xRT1D4','2025-07-11 13:03:43.054913'),('xbgrezdctxa8zldjsbp5z4pau36ia53v','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZlMp:JBdjhnCgYSqkOz9rQG6BvFSQP6HkET3X0aBK8X0iKlo','2025-07-10 07:21:51.659319'),('xwjqxtdejpml3b9sgx7rtri5i3a972w8','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZk4g:3Z79H8aq8zas-XkL2FnII-9RDYq8G-IjD_Rzh3LrDIo','2025-07-10 05:59:02.605026'),('y8nc1sxq9qu21o6lp1m3l7u7qj5bnox6','.eJxVjEEOwiAQRe_C2pAyDAVcuvcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnEWSpx-t0jpkdsO-E7tNss0t3WZotwVedAurzPn5-Vw_w4q9fqtMyP6Ygpp6wm1IwXGOZ3AoB1NKaAoa7CDUqNVHiFGZhtdQRyKBZ_F-wPJ6jcg:1uZoHt:rIMJLDc3_CrFd6x6RcnMSmX9ntb67K5I6DmtZzLlyWA','2025-07-10 10:28:57.490553'),('z0i8apcnlz542x0r0z4hprrjg8wtgajo','e30:1uZAxP:t6bg_Zm0kIccTm19_hC5DPgpZB34htevIOPWqd6wK84','2025-07-08 16:29:11.570000');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-13 22:25:58
