# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-09-01 下午9:53
# @Author : 毛鹏
from mango_ui.init import *


class MangoNotification(QFrame):
    def __init__(self, parent, message, style):
        super().__init__(parent)
        self.style = style
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setFixedSize(240, 80)
        self.setObjectName("MangoNotification")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 0, 0)
        self.layout.addWidget(QLabel(message))
        self.setFrameShape(QFrame.NoFrame)

        # 设置微红色背景色
        self.set_style()
        # 设置渐隐效果
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(1500)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(self.close)
        self.animation.start()
        self.hovered = False

    def enterEvent(self, event):
        """鼠标进入事件，暂停渐隐动画"""
        if self.hovered is False:
            self.hovered = True
            self.animation.stop()  # 停止动画

    def leaveEvent(self, event):
        """鼠标离开事件，重新开始渐隐动画"""
        if self.hovered is True:
            self.hovered = False
            self.animation.start()  # 重新开始动画

    def set_style(self):
        self.setStyleSheet(f"""
            QFrame#MangoNotification {{
                background-color: {self.style};
                border-radius: 10px;
                border: 1px solid black;
            }}
        """)
