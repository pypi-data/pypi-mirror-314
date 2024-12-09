# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework  
@File    :   RuntimeUtil.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/11 13:50   shenpeng   1.0         None
"""

import subprocess
import platform
import psutil
from loguru import logger


class RuntimeUtil:
    @staticmethod
    def run_cmd(cmd, encoding='utf-8'):
        """
        Executes the given system command and returns its output as a string.
        """
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        return result.stdout.encode(encoding)

    @staticmethod
    def get_system_info():
        """
        Returns a string containing information about the current system.
        """
        return platform.uname()._asdict()

    @staticmethod
    def get_os_name():
        """
        Returns the name of the operating system.
        """
        return platform.system()

    @staticmethod
    def get_cpu_info():
        """
        Returns information about the system's CPU.
        """
        return psutil.cpu_times_percent()._asdict()

    @staticmethod
    def get_memory_info():
        """
        Returns information about the system's memory.
        """
        return psutil.virtual_memory()._asdict()

    @staticmethod
    def get_disk_info():
        """
        Returns information about the system's disk.
        """
        return psutil.disk_usage('/')._asdict()

    @staticmethod
    def get_system_info_dict():
        """
        Returns all system information as a dictionary.
        """
        system_info = {
            'OS Name': RuntimeUtil.get_os_name(),
            'System Info': RuntimeUtil.get_system_info(),
            'CPU Info': RuntimeUtil.get_cpu_info(),
            'Memory Info': RuntimeUtil.get_memory_info(),
            'Disk Info': RuntimeUtil.get_disk_info(),
        }
        return system_info


if __name__ == '__main__':
    logger.info(RuntimeUtil.get_system_info_dict())
    result = RuntimeUtil.run_cmd("ls")

