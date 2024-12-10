# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-09-01 下午10:01
# @Author : 毛鹏
from mango_ui.init import *


class MangoMessage(QWidget):
    def __init__(self, parent, message, style):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)  # 保持在最上面
        self.setFixedHeight(30)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # 设置背景颜色和边框
        self.setStyleSheet(f"background-color: {style}; border-radius: 10px;")

        # 根据文字长度调整宽度
        self.label = QLabel(message)
        self.layout.addStretch(1)
        self.layout.addWidget(self.label, 8)
        self.layout.addStretch(1)
        font_metrics = QFontMetrics(self.label.font())
        text_width = font_metrics.boundingRect(message).width() + 25
        self.setFixedWidth(text_width)

        # 设置渐隐效果
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(1500)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(self.close)
        self.animation.start()

        self.hovered = False

    # @staticmethod
    # def create_colored_icon(color) -> QIcon:
    #     # 创建一个透明的 QPixmap
    #     pixmap = QPixmap(32, 32)  # 设置图标的大小
    #     pixmap.fill(Qt.transparent)
    #
    #     # 使用 QPainter 绘制图标
    #     painter = QPainter(pixmap)
    #     painter.setRenderHint(QPainter.Antialiasing)
    #
    #     # 这里可以加载原始图标
    #     original_icon = QPixmap(":/icons/app_icon.png")  # 替换为你的图标路径
    #     painter.drawPixmap(0, 0, original_icon)
    #
    #     # 设置颜色
    #     painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    #     painter.fillRect(pixmap.rect(), QColor(color))
    #     painter.end()
    #
    #     return QIcon(pixmap)

    def enterEvent(self, event):
        """鼠标进入事件，暂停渐隐动画"""
        if self.hovered is False:
            self.hovered = True
            self.animation.stop()

    def leaveEvent(self, event):
        """鼠标离开事件，重新开始渐隐动画"""
        if self.hovered is True:
            self.hovered = False
            self.animation.start()
