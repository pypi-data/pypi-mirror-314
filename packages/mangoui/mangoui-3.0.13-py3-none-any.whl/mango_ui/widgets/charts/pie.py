# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-10-23 17:49
# @Author : 毛鹏
import matplotlib
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

# 设置字体为支持中文的字体
matplotlib.rcParams['font.family'] = 'SimHei'  # 或者 'Microsoft YaHei'
matplotlib.rcParams['axes.unicode_minus'] = False  # 显示负号


class MangoPiePlot(QWidget):
    def __init__(self):
        super().__init__()
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasQTAgg(self.fig)

        # 布局设置
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def draw(self, data: list[dict]):
        self.ax.clear()  # 清除之前的图
        sizes = [item['value'] for item in data]
        labels = [item['name'] for item in data]
        colors = ['#FF9999', '#66B3FF']
        if all(size == 0 for size in sizes):
            # 绘制默认饼状图
            default_sizes = [1, 1]  # 两个部分，表示无数据
            default_labels = ['无数据', '']
            self.ax.pie(default_sizes, labels=default_labels, colors=['#CCCCCC', '#FFFFFF'], startangle=90)
        else:
            # 绘制饼状图
            self.ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        self.ax.axis('equal')  # 确保饼状图是圆形
        self.canvas.draw()
