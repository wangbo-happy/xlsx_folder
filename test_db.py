#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据库连接测试
"""

import os
import sys
import pymysql
from dotenv import load_dotenv

# 将输出重定向到文件
log_file = open('db_test_log.txt', 'w', encoding='utf-8')
original_stdout = sys.stdout
sys.stdout = log_file

try:
    # 加载环境变量
    load_dotenv()
    
    # 获取数据库配置
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = int(os.getenv('DB_PORT', '3306'))
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_name = os.getenv('DB_NAME', 'excel_data_manager')
    
    print("数据库配置:")
    print(f"主机: {db_host}")
    print(f"端口: {db_port}")
    print(f"用户名: {db_user}")
    print(f"密码: {'*' * len(db_password) if db_password else '空'}")
    print(f"数据库名: {db_name}")
    
    try:
        # 不指定数据库，尝试连接MySQL服务器
        print("\n尝试连接MySQL服务器（不指定数据库）...")
        conn = pymysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password
        )
        print("成功连接到MySQL服务器！")
        conn.close()
        
        # 尝试连接到指定数据库
        print("\n尝试连接到指定数据库...")
        conn = pymysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name
        )
        print(f"成功连接到数据库 {db_name}！")
        
        # 测试查询
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            if tables:
                print("\n数据库中的表:")
                for table in tables:
                    print(f"  - {table[0]}")
            else:
                print("\n数据库中没有表")
        
        conn.close()
        
    except Exception as e:
        print(f"\n数据库连接失败: {e}")
        
        # 给出建议
        if "Access denied" in str(e):
            print("\n可能的解决方案:")
            print("1. 检查数据库用户名和密码是否正确")
            print("2. 确保用户有足够的权限访问数据库")
        elif "Unknown database" in str(e):
            print("\n可能的解决方案:")
            print(f"1. 需要先创建数据库 '{db_name}'")
            print("2. 运行 setup_database.py 来创建数据库")
        elif "Can't connect" in str(e):
            print("\n可能的解决方案:")
            print("1. 确保MySQL服务正在运行")
            print("2. 检查主机名和端口是否正确")
            
except Exception as e:
    print(f"发生错误: {e}")

finally:
    # 恢复标准输出并关闭文件
    sys.stdout = original_stdout
    log_file.close()
    print(f"检查已完成，详细日志已写入 db_test_log.txt 文件")