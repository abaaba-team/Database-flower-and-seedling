/*
 Navicat Premium Data Transfer

 Source Server         : fct_mysql
 Source Server Type    : MySQL
 Source Server Version : 80025
 Source Host           : jp-tyo-ilj-1.natfrp.cloud:49930
 Source Schema         : fas

 Target Server Type    : MySQL
 Target Server Version : 80025
 File Encoding         : 65001

 Date: 26/12/2021 21:45:19
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for client
-- ----------------------------
DROP TABLE IF EXISTS `client`;
CREATE TABLE `client`  (
  `C_name` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `C_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `C_birthday` date NULL DEFAULT NULL,
  `C_phonenumber` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `C_mail` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `C_age` int(0) NULL DEFAULT NULL,
  `C_photo` blob NULL,
  `C_discount` int(0) NULL DEFAULT NULL,
  PRIMARY KEY (`C_ID`) USING BTREE,
  INDEX `C_name`(`C_name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for client_purchase
-- ----------------------------
DROP TABLE IF EXISTS `client_purchase`;
CREATE TABLE `client_purchase`  (
  `FAS_name` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `P_ID` int(0) NOT NULL AUTO_INCREMENT,
  `NotFreezingClient` tinyint(1) NOT NULL,
  `C_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `FC_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `FASID` int(10) UNSIGNED ZEROFILL NOT NULL,
  `S_name` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `TotalPurchase` float NULL DEFAULT NULL,
  `Price` float NULL DEFAULT NULL,
  `TotalCount` int(0) NULL DEFAULT NULL,
  `TotalDiscount` float NULL DEFAULT NULL,
  `OrderDate` date NULL DEFAULT NULL,
  `EstimatedDeliveryDate` date NULL DEFAULT NULL,
  `ActualDeliveryDate` date NULL DEFAULT NULL,
  PRIMARY KEY (`P_ID`) USING BTREE,
  INDEX `FASID`(`FASID`) USING BTREE,
  INDEX `FAS_name`(`FAS_name`) USING BTREE,
  INDEX `client_purchase_ibfk_4`(`C_ID`) USING BTREE,
  INDEX `client_purchase_ibfk_7`(`FC_ID`) USING BTREE,
  CONSTRAINT `client_purchase_ibfk_3` FOREIGN KEY (`FASID`) REFERENCES `supplier_relationship_with_flower` (`FASID`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `client_purchase_ibfk_4` FOREIGN KEY (`C_ID`) REFERENCES `client` (`C_ID`) ON DELETE SET NULL ON UPDATE RESTRICT,
  CONSTRAINT `client_purchase_ibfk_7` FOREIGN KEY (`FC_ID`) REFERENCES `freezing_client` (`C_ID`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 183 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for flower_and_seedling
-- ----------------------------
DROP TABLE IF EXISTS `flower_and_seedling`;
CREATE TABLE `flower_and_seedling`  (
  `F_ID` int(0) NOT NULL AUTO_INCREMENT,
  `FAS_name` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`F_ID`, `FAS_name`) USING BTREE,
  INDEX `R_ID`(`F_ID`) USING BTREE,
  INDEX `S_ID`(`FAS_name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 31 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for freezing_client
-- ----------------------------
DROP TABLE IF EXISTS `freezing_client`;
CREATE TABLE `freezing_client`  (
  `C_name` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `C_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `C_birthday` date NULL DEFAULT NULL,
  `C_phonenumber` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `C_mail` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `C_age` int(0) NULL DEFAULT NULL,
  `C_photo` blob NULL,
  `C_discount` int(0) NULL DEFAULT NULL,
  PRIMARY KEY (`C_ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for supplier
-- ----------------------------
DROP TABLE IF EXISTS `supplier`;
CREATE TABLE `supplier`  (
  `S_name` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '',
  `S_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `S_phonenumber` bigint(0) NULL DEFAULT NULL,
  `S_mail` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `S_principle` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`S_ID`) USING BTREE,
  INDEX `S_name`(`S_name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for supplier_relationship_with_flower
-- ----------------------------
DROP TABLE IF EXISTS `supplier_relationship_with_flower`;
CREATE TABLE `supplier_relationship_with_flower`  (
  `FASID` int(10) UNSIGNED ZEROFILL NOT NULL AUTO_INCREMENT,
  `FAS_name` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `S_name` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '',
  `TotalCount` int(0) NULL DEFAULT NULL,
  `Unit` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Price` float(10, 2) NULL DEFAULT NULL,
  `Subtotal` int(0) NULL DEFAULT NULL,
  `StoragePlace` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `PurchaseDate` date NULL DEFAULT NULL,
  `F_ID` int(0) NULL DEFAULT NULL,
  PRIMARY KEY (`FASID`, `FAS_name`) USING BTREE,
  INDEX `FASID`(`FASID`) USING BTREE,
  INDEX `F_ID`(`F_ID`) USING BTREE,
  INDEX `S_name`(`S_name`) USING BTREE,
  CONSTRAINT `F_ID` FOREIGN KEY (`F_ID`) REFERENCES `flower_and_seedling` (`F_ID`) ON DELETE SET NULL ON UPDATE RESTRICT,
  CONSTRAINT `S_name` FOREIGN KEY (`S_name`) REFERENCES `supplier` (`S_name`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 183 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
