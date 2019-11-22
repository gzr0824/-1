/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 50638
 Source Host           : localhost:3306
 Source Schema         : dfms

 Target Server Type    : MySQL
 Target Server Version : 50638
 File Encoding         : 65001

 Date: 26/10/2019 17:24:43
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for device_information
-- ----------------------------
DROP TABLE IF EXISTS `device_information`;
CREATE TABLE `device_information` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `ip` varchar(50) DEFAULT NULL COMMENT '设备ip',
  `info` varchar(1024) DEFAULT NULL COMMENT '库位信息',
  `network_status` int(5) DEFAULT '0' COMMENT '网络状态 1正常 2失败',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

-- ----------------------------
-- Records of device_information
-- ----------------------------
BEGIN;
INSERT INTO `device_information` VALUES (1, '192.168.0.10', NULL, 1, '2019-10-17 19:17:57');
INSERT INTO `device_information` VALUES (2, '192.168.0.50', NULL, 0, NULL);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
