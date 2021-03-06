#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-09-25 21:11:15
@LastEditTime : 2020-06-01 15:40:17
'''

import socket

from .baseclass import BruteBaseClass


class BruteForce(BruteBaseClass):
    """BruteForce"""

    def check_unauth(self,host,port):
        if self.flag:
            try:
                socket.setdefaulttimeout(self.timeout)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host, port))
                s.send("INFO\r\n".encode())
                result = s.recv(1024)
            except Exception as e:
                hook_msg((False,host,port,"Anonymous",""))
            else:
                if "redis_version".encode() in result:
                    hook_msg((True,host,port,"Anonymous",""))
                    self.unauth_result.append(host)
            finally:
                s.close()

    def worker(self, payload):
        if self.flag:
            host, port, user, pwd = payload
            data = "AUTH {}\r\n".format(pwd)
            try:
                socket.setdefaulttimeout(self.timeout)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host, port))
                s.send(data.encode())
                result = s.recv(1024)
            except Exception as e:
                hook_msg((False, host, port, user, pwd))
                logger.error("{} {}".format(host, e))
            else:
                if "+OK".encode() in result:
                    hook_msg((True, host, port, "", pwd))
                elif b"invalid password" in result:
                    hook_msg((False, host, port, "", pwd))
            finally:
                s.close()
