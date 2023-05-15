#!/usr/bin/env python

import os

def print_message(message):
    if message is None:
        message = ""
    len_message = len(message) + 4
    print('=' * len_message)
    print('= {} ='.format(message))
    print('=' * len_message)


def print_install(message):
    if message is None:
        message = ""
    p_message = f"Installing {message}."
    print_message(p_message)


print_install("Python 3.7")

apt_install_python37 = """apt-get update && \
apt-get upgrade -y && \
apt-get dist-upgrade -y && \
apt-get install -y build-essential checkinstall && \
apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev zlib1g-dev libffi-dev wget && \
cd /usr/src && \
wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz && \
tar xzf Python-3.7.3.tgz && \
rm Python-3.7.3.tgz && \
cd Python-3.7.3 && \
./configure --enable-optimizations && \
make altinstall && \
cd .. && \
rm -rf Python-3.7.3 && \
apt-get remove --purge -y checkinstall libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev zlib1g-dev libffi-dev && \
apt-get remove --purge -y wget && \
apt-get autoremove -y && \
apt-get clean
"""
os.system(apt_install_python37)

os.system("apt-get update")
os.system("apt-get upgrade -y")
