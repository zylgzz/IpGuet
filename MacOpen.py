# -*- coding: utf-8 -*-

import make_package
import send_package
import re


def macopen(ip, mac, isp):
    # 合法性校验
    try:
        # ip
        index = re.match('^([0-9]{1,3}\\.){3}[0-9]{1,3}$', str(ip))
        if index:
            ip = ip[index.start():index.end()]
        else:
            return None

        # mac
        index = re.search('^(([a-f0-9]{2}:)|([a-f0-9]{2}-)){5}[a-f0-9]{2}$', str(mac), re.IGNORECASE)
        if index:
            mac = mac[index.start():index.end()]
        else:
            return None

        # isp
        index = re.search('^[1-3]$', str(isp))
        if index:
            isp = isp[index.start():index.end()]
        else:
            return None

        print(ip, mac, isp)
        package = make_package.MakePackage().do(ip=ip, mac=mac, isp=isp)
        result = send_package.SendPackage().send_udp(host='172.16.1.1', port=20015, package=package)
        if result:
            return result
        else:
            return None
    except Exception as e:
        print(e)
        return None
