# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-08-30 14:51
# @Author : 毛鹏
from mango_ui.init import *


class MangoDialog(QDialog):
    def __init__(self, tips: str, size: tuple = (400, 300)):
        super().__init__()
        self.setWindowTitle(tips)
        self.setFixedSize(*size)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowIcon(QIcon(':/icons/app_icon.png'))
        # 设置样式表
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {THEME.background_color}; /* 主体背景颜色 */
            }}
            QDialog::title {{
                background-color: {THEME.background_color}; /* 标题栏背景颜色 */
                color: {THEME.font_color}; /* 标题栏文字颜色 */
            }}
        """)
