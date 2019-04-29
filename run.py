import GetMac
import MacOpen

ip = ''
mac = ''
isp = ''


def get_info_mac():
    all_mac_ip = GetMac.get_all_if_info()       # 得到全部的mac和ip
    for k, v in all_mac_ip.items():
        print(k, v)


if __name__ == '__main__':
    get_info_mac()
    print("联通 1\t电信 2\t移动 3")
    print("请根据获取得到的数据输入信息")
    # mac = input('MAC:')
    # ip = input('IP:')
    # isp = input('运营商')
    ip = '10.21.109.19'
    mac = 'C8-5B-76-61-1F-C4'
    isp = '1'
    status = MacOpen.macopen(ip, mac, isp)
    print("找到的state:", status)