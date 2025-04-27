#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据库设置脚本
"""

import os
import pymysql
from dotenv import load_dotenv


def create_database() -> bool:
    """
    创建数据库
    
    Returns:
        是否成功创建
    """
    try:
        # 加载环境变量
        load_dotenv()
        
        # 获取数据库配置
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = int(os.getenv('DB_PORT', '3306'))
        db_user = os.getenv('DB_USER', 'root')
        db_password = os.getenv('DB_PASSWORD', '')
        db_name = os.getenv('DB_NAME', 'excel_data_manager')
        
        # 连接到MySQL服务器（不指定数据库）
        conn = pymysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password
        )
        
        with conn.cursor() as cursor:
            # 检查数据库是否存在
            cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
            if cursor.fetchone():
                print(f"数据库 '{db_name}' 已存在")
                return True
                
            # 创建数据库
            cursor.execute(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"成功创建数据库: {db_name}")
            
            return True
            
    except Exception as e:
        print(f"创建数据库失败: {e}")
        return False
    
    finally:
        if 'conn' in locals() and conn:
            conn.close()


def setup_tables() -> bool:
    """
    设置数据库表结构
    
    Returns:
        是否成功设置
    """
    try:
        # 加载环境变量
        load_dotenv()
        
        # 获取数据库配置
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = int(os.getenv('DB_PORT', '3306'))
        db_user = os.getenv('DB_USER', 'root')
        db_password = os.getenv('DB_PASSWORD', '')
        db_name = os.getenv('DB_NAME', 'excel_data_manager')
        
        # 连接到指定数据库
        conn = pymysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name
        )
        
        with conn.cursor() as cursor:
            # 创建员工信息表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    department VARCHAR(100),
                    position VARCHAR(100),
                    hire_date DATE,
                    salary DECIMAL(10,2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 创建Excel数据表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS excel_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    file_name VARCHAR(255) NOT NULL,
                    sheet_name VARCHAR(100) NOT NULL,
                    row_data JSON,
                    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            print("成功创建数据库表结构")
            return True
            
    except Exception as e:
        print(f"设置数据库表结构失败: {e}")
        return False
    
    finally:
        if 'conn' in locals() and conn:
            conn.close()


if __name__ == '__main__':
    print("开始设置数据库...")
    
    if create_database():
        if setup_tables():
            print("数据库设置完成")
        else:
            print("数据库表结构设置失败")
    else:
        print("数据库创建失败")