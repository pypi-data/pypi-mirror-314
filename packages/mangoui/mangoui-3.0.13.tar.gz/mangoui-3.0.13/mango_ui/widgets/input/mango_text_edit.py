# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-09-18 11:11
# @Author : 毛鹏
from mango_ui.init import *


class MangoTextEdit(QTextEdit):
    click = Signal(object)

    def __init__(self, placeholder, value: str | None = None, subordinate: str | None = None):
        super().__init__()
        self.value = value
        self.subordinate = subordinate


        if placeholder:
            self.setPlaceholderText(placeholder)

        if self.value:
            self.set_value(self.value)
        self.set_stylesheet()

    def set_value(self, text: str):
        self.setPlainText(text)

    def get_value(self):
        return self.toPlainText()

    def set_stylesheet(self):
        style = f"""
        QTextEdit {{
        	background-color: {THEME.background_color};
        	border-radius: {THEME.border_radius};
        	border: 1px solid {THEME.border};
        	padding-left: 10px;
            padding-right: 10px;
        	selection-color: {THEME.background_color};
        	selection-background-color: {THEME.color.color4};
            color: {THEME.font_color};
        }}

        QTextEdit:focus {{
            border: 1px solid {THEME.border};
            background-color: {THEME.color.color2};
        }}
        """
        self.setStyleSheet(style)
