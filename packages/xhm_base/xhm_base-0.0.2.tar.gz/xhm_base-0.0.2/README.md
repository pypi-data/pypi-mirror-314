# XHM SDK 使用说明

# 封装sdk时请多考虑去解决一类问题、而不是一个问题

## 使用教程

安装单个模块：

    pip install xhm_all[xhm_log]

安装所有：

    pip install xhm_all

### 二、poetry

安装：

    poetry add xhm_all@0.1.7 --verbose

### 在代码中使用BOCHU SDK

    from xhm_log import log
    
    def test_case():
        log.error('cc')

## 开发包上传

    # pip install setuptools==58.0.4
     python setup.py sdist upload -r nexus

### poetry 开发包

    poetry config repositories.nexus http://nexus.fscut.com/repository/fs-pypi/
    poetry config http-basic.nexus 用户名 密码
 
    poetry build
    poetry publish --repository nexus

    # 官方
    poetry config pypi-token.pypi pypi-AgEIcHlwaS5vcmcCJGYyM2E5ZjkxLWZhYTYtNGE2Mi1iOGZlLTczOGU2YjVhNzNkNAACKlszLCIwNzE3NWUwYy05YTA5LTQ3ZmMtOTYxNS0xZjExZjQyMmVhMDEiXQAABiCb__bveg49S186PbTgid0-FqFAz5GOxr0sB5dY23NuKg

### 更新并安装

    poetry add xhm_all==0.5.6

### 升级记录

| 版本    | 日期         | 更新记录          | 开发人员 |
|-------|------------|---------------|------|
| 0.0.1 | 2024-12-08 | 拆分基础SDK和业务SDK | 邹慧刚  |

