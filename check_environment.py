#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
环境检查工具
"""

import sys
import platform
import subprocess
from typing import Tuple, List


def check_python_version() -> Tuple[str, str]:
    """
    检查Python版本
    
    Returns:
        当前Python版本和推荐版本
    """
    current_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    recommended_version = "3.8.0"
    return current_version, recommended_version


def check_os() -> str:
    """
    检查操作系统
    
    Returns:
        操作系统名称
    """
    return platform.system()


def check_pip_packages() -> List[Tuple[str, str]]:
    """
    检查已安装的pip包
    
    Returns:
        包含(包名, 版本)的列表
    """
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'list', '--format=freeze'],
            capture_output=True,
            text=True
        )
        
        packages = []
        for line in result.stdout.splitlines():
            if '==' in line:
                name, version = line.split('==', 1)
                packages.append((name.strip(), version.strip()))
                
        return packages
        
    except Exception as e:
        print(f"检查pip包时出错: {e}")
        return []


def check_required_packages() -> List[Tuple[str, str, bool]]:
    """
    检查必需包是否已安装
    
    Returns:
        包含(包名, 推荐版本, 是否安装)的列表
    """
    required_packages = [
        ("openpyxl", "3.0.7"),
        ("pymysql", "1.0.2"),
        ("python-dotenv", "0.19.0")
    ]
    
    installed_packages = {name.lower(): version for name, version in check_pip_packages()}
    
    results = []
    for name, recommended_version in required_packages:
        installed = name.lower() in installed_packages
        results.append((name, recommended_version, installed))
        
    return results


def print_environment_report():
    """
    打印环境检查报告
    """
    print("="*50)
    print("环境检查报告")
    print("="*50)
    
    # 检查Python版本
    current_version, recommended_version = check_python_version()
    print(f"\nPython版本:\n当前: {current_version}\n推荐: {recommended_version}")
    
    # 检查操作系统
    print(f"\n操作系统: {check_os()}")
    
    # 检查必需包
    print("\n必需包检查:")
    for name, recommended_version, installed in check_required_packages():
        status = "已安装" if installed else "未安装"
        print(f"- {name} (推荐: {recommended_version}): {status}")
    
    print("\n" + "="*50)


if __name__ == '__main__':
    print_environment_report()