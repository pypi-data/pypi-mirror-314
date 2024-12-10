# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-10-15 14:28
# @Author : 毛鹏
from PySide6.QtWidgets import QTimeEdit

from mango_ui.settings.settings import THEME


class MangoTimeEdit(QTimeEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_style()

    def set_style(self, height=30):
        self.setStyleSheet(f"""
            QTimeEdit {{
                background-color: {THEME.background_color};
                border-radius: {THEME.border_radius};
                border: 1px solid {THEME.border};
                padding-left: 10px;
                padding-right: 10px;
                selection-color: {THEME.background_color};
                selection-background-color: {THEME.color.color5};
                color: {THEME.font_color};
        }}
        
        QTimeEdit:focus {{
            border: 1px solid {THEME.border};
            background-color: {THEME.color.color1};
        }}
        QTimeEdit::up-button, QTimeEdit::down-button {{
            border: none; /* 去掉边框 */
            background: transparent; /* 背景透明 */
            width: 0; /* 设置宽度为0 */
            height: 0; /* 设置高度为0 */
            margin: 0; /* 去掉外边距 */
            padding: 0; /* 去掉内边距 */
        }}
        """)
        self.setMinimumHeight(height)
