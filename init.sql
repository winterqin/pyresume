-- 设置字符集
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- 创建数据库
CREATE DATABASE IF NOT EXISTS pyresume_db 
  CHARACTER SET utf8mb4 
  COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE pyresume_db;

-- 设置时区
SET time_zone = '+00:00';

-- pyresume项目初始化脚本
-- 这里可以添加初始化数据或表结构