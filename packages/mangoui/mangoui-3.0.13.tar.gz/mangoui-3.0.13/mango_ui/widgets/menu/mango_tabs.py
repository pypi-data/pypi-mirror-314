# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-10-14 17:30
# @Author : 毛鹏
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QTabWidget, QWidget

from mango_ui.settings.settings import THEME


class MangoTabs(QTabWidget):
    clicked = Signal(str)

    def __init__(self):
        super().__init__()
        self.previous_index = 0
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(f"""
            QTabWidget {{
                background-color: {THEME.background_color}; /* 设置整个选项卡的底色 */
            }}
            QTabBar::tab {{
                border: none;  /* 去掉选项卡的边框 */
                padding: 6px; /* 内边距 */
            }}
            QTabBar::tab:selected {{
                background: {THEME.color.color4}; /* 选中时的背景颜色 */
            }}
            QTabBar::tab:hover {{
                background: {THEME.hover.background_color}; /* 鼠标悬停时的背景颜色 */
            }}
            QTabBar::tab {{                                
                border-right: 1px solid {THEME.border}; /* 保留按钮之间的边框 */
            }}
            QTabBar::tab:last {{
                border-right: none; /* 最后一个选项卡不显示右边框 */
            }}
            QTabWidget::pane {{
                border: 1px solid {THEME.border}; /* 底部横条 */
                border-left: none; /* 取消顶部边框 */
                border-right: none; /* 取消顶部边框 */
                border-bottom: none; /* 取消顶部边框 */
            }}
        """)

    def add_tab(self, layout, tab_name):
        new_tab = QWidget()
        new_tab.setContentsMargins(0, 0, 0, 0)
        layout.setContentsMargins(0, 5, 0, 0)
        new_tab.setLayout(layout)
        self.addTab(new_tab, tab_name)
