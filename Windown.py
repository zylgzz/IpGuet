import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
import GetMac
import MacOpen


class MyWindown(QWidget):
    def __init__(self, parent=None):
        """
        界面的初始化
        :param parent:
        """
        super(MyWindown, self).__init__(parent)
        self.setFont(QtGui.QFont('Arial', 10))
        self.top_layout = QHBoxLayout()
        self.isp = "2"                          # 服务商默认电信,其中联通1,移动3
        self.button_layout = QHBoxLayout()
        self.main_layout = QVBoxLayout()
        # 窗体上半部分的布局
        self.ip_label = QLabel("ip:")
        self.ip_input = QLineEdit()
        self.ip_input.setFixedSize(200, 30)
        self.mac_label = QLabel("mac:")
        self.mac_input = QLineEdit()
        self.mac_input.setFixedSize(200, 30)
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.ip_label)
        self.top_layout.addWidget(self.ip_input)
        self.top_layout.addSpacing(70)
        self.top_layout.addWidget(self.mac_label)
        self.top_layout.addWidget(self.mac_input)
        self.top_layout.addStretch()
        # 中间的布局
        self.list_info = QListWidget()
        self.list_info.setFont(QtGui.QFont('Arial', 10))
        # 下部分的布局
        self.lt_button = QPushButton("联通")
        self.dx_button = QPushButton("电信")
        self.yd_button = QPushButton("移动")
        self.status_label = QLabel()
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.lt_button)
        self.button_layout.addWidget(self.dx_button)
        self.button_layout.addWidget(self.yd_button)
        self.button_layout.addSpacing(70)
        self.button_layout.addWidget(self.status_label)
        self.button_layout.addStretch()
        # 总的布局和窗口的设置
        self.setWindowTitle("专用出校器")
        icon = QIcon()
        icon.addPixmap(QPixmap("icon.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addWidget(self.list_info)
        self.main_layout.addLayout(self.button_layout)
        self.setFixedSize(700, 400)
        self.setLayout(self.main_layout)
        self.show()
        self.signal_slot()
        self.get_infos()

    def signal_slot(self):
        """
        qt信号和槽的连接
        :return:
        """
        self.lt_button.clicked.connect(self.choose_lt_server)
        self.dx_button.clicked.connect(self.choose_dx_server)
        self.yd_button.clicked.connect(self.choose_yd_server)
        self.list_info.itemClicked.connect(self.choose_item)

    def open_mac(self):
        """
        开放mac地址
        :return:
        """
        try:
            status = MacOpen.macopen(self.ip_input.text(), self.mac_input.text(), self.isp)
            print(status)
            if status:
                self.status_label.setText("mac地址已经开放")
                print("状态%s \tmac地址已经开放,可以进行DSL拨号" % (str(status),))
            else:
                self.status_label.setText("预拨号失败")
        except Exception as e:
            self.status_label.setText("超时")
            print(e)

    def get_infos(self):
        """
        获得网卡的信息,将信息填入窗体,任取除了127.0.0.1那个地址
        :return:
        """
        all_mac_ip = GetMac.get_all_if_info()  # 得到全部的mac和ip
        for k, v in all_mac_ip.items():
            print(k, v)
            ip_info = v['ip_addr']
            mac_info = v['mac_addr']
            if not mac_info:
               continue
            if not ip_info:
                continue
            self.list_info.addItem(QListWidgetItem("{:27}\t{:27}\t{:27}".format(mac_info, ip_info, k)))
            if k == '以太网':
                self.ip_input.setText(v['ip_addr'])
                self.mac_input.setText(v['mac_addr'])

    def choose_item(self, item):
        """
        槽函数,随着listwidgetd的选择做出改变
        :param item:
        :return:
        """
        item = item.text()
        item = item.split("\t")
        self.ip_input.setText(item[1].strip())
        self.mac_input.setText(item[0].strip())

    def choose_lt_server(self):
        self.isp = "1"
        self.open_mac()

    def choose_dx_server(self):
        self.isp = "2"
        self.open_mac()

    def choose_yd_server(self):
        self.isp = "3"
        self.open_mac()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    windown = MyWindown()
    sys.exit(app.exec_())
