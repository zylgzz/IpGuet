from psutil import net_if_addrs
import re


def get_all_if_info():
    try:
        if_infos = net_if_addrs()
        if_name = if_infos.keys()
        d1 = {}
        for i in if_name:
            if_detail = if_infos.get(i)
            d2 = {'ip_addr': None, 'mac_addr': None}
            for j in if_detail:
                info = j[1]
                flag = re.match('^([0-9]{1,3}\.){3}[0-9]{1,3}$', info)
                if flag:
                    d2['ip_addr'] = info
                else:
                    flag = re.match('^(([a-f0-9]{2}:)|([a-f0-9]{2}-)){5}[a-f0-9]{2}$', info, re.IGNORECASE)
                    if flag:
                        d2['mac_addr'] = info
            d1.update({i: d2})
        return d1
    except Exception as e:
        return None


if __name__ == '__main__':
    result = get_all_if_info()
    for k, v in result.items():
        print(k, v)