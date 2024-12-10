# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description:
# @Time   : 2024-08-16 17:05
# @Author : 毛鹏
import time

from mango_ui.init import *


class MangoPushButton(QPushButton):
    def __init__(
            self,
            text,
            parent=None,
            **kwargs
    ):
        super().__init__()
        self.setText(text)
        self.kwargs = kwargs

        if parent:
            self.setParent(parent)

        self.set_stylesheet()
        self.setCursor(Qt.PointingHandCursor)

    def set_stylesheet(self, height=35, width=60):
        style = f'''
        QPushButton {{
            border: 1px solid {THEME.border};
            color: {THEME.font_color};
            border-radius: {THEME.border_radius};	
            background-color: {self.kwargs.get('color') if self.kwargs.get('color') else THEME.color.color4};
        }}
        QPushButton:hover {{
            background-color: {THEME.hover.background_color};
        }}
        QPushButton:pressed {{	
            background-color: {THEME.pressed.background_color};
        }}
        '''
        self.setStyleSheet(style)
        self.setMinimumHeight(height)
        self.setMinimumWidth(width)
