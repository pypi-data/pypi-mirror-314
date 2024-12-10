# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-10-23 17:42
# @Author : 毛鹏
import numpy
import pyqtgraph
from PySide6.QtWidgets import QVBoxLayout, QWidget


class MangoLinePlot(QWidget):
    def __init__(self, title, left, bottom):
        super().__init__()
        # 创建绘图窗口
        self.plot_widget = pyqtgraph.PlotWidget()
        self.plot_widget.setBackground('w')  # 设置背景颜色为白色
        self.plot_widget.setTitle(title, color='b', size='20pt')
        self.plot_widget.setLabel('left', left, color='g', size='12pt')
        self.plot_widget.setLabel('bottom', bottom, color='g', size='12pt')
        self.plot_widget.addLegend()

        # 布局
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

    def draw(self, data: list[dict]):
        self.plot_widget.clear()

        days = numpy.arange(len(data[0]['value'])) + 1
        colors = ['b', 'r', 'g', 'c', 'm', 'y']

        for index, item in enumerate(data):
            color = colors[index % len(colors)]
            self.plot_widget.plot(
                days,
                item['value'],
                pen=color,
                name=item['name'],
                width=2,
                symbol='o',
                symbolBrush=color
            )
