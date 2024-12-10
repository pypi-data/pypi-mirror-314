# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description:
# @Time   : 2024-08-16 17:05
# @Author : 毛鹏
from mango_ui.init import *

style = """
/* HORIZONTAL */
QSlider {{ margin: {_margin}px; }}
QSlider::groove:horizontal {{
    border-radius: {_bg_radius}px;
    height: {_bg_size}px;
	margin: 0px;
	background-color: {_bg_color};
}}
QSlider::groove:horizontal:hover {{ background-color: {_bg_color_hover}; }}
QSlider::handle:horizontal {{
    border: none;
    height: {_handle_size}px;
    width: {_handle_size}px;
    margin: {_handle_margin}px;
	border-radius: {_handle_radius}px;
    background-color: {_handle_color};
}}
QSlider::handle:horizontal:hover {{ background-color: {_handle_color_hover}; }}
QSlider::handle:horizontal:pressed {{ background-color: {_handle_color_pressed}; }}

/* VERTICAL */
QSlider::groove:vertical {{
    border-radius: {_bg_radius}px;
    width: {_bg_size}px;
    margin: 0px;
	background-color: {_bg_color};
}}
QSlider::groove:vertical:hover {{ background-color: {_bg_color_hover}; }}
QSlider::handle:vertical {{
	border: none;
    height: {_handle_size}px;
    width: {_handle_size}px;
    margin: {_handle_margin}px;
	border-radius: {_handle_radius}px;
    background-color: {_handle_color};
}}
QSlider::handle:vertical:hover {{ background-color: {_handle_color_hover}; }}
QSlider::handle:vertical:pressed {{ background-color: {_handle_color_pressed}; }}
"""


class MangoSlider(QSlider):
    def __init__(self,
                 margin=0,
                 bg_size=20,
                 bg_radius=10,
                 bg_color=THEME.color.color1,
                 bg_color_hover=THEME.color.color3,
                 handle_margin=2,
                 handle_size=16,
                 handle_radius=8,
                 handle_color=THEME.color.color4,
                 handle_color_hover=THEME.color.color8,
                 handle_color_pressed=THEME.color.color4):
        super().__init__()
        adjust_style = style.format(
            _margin=margin,
            _bg_size=bg_size,
            _bg_radius=bg_radius,
            _bg_color=bg_color,
            _bg_color_hover=bg_color_hover,
            _handle_margin=handle_margin,
            _handle_size=handle_size,
            _handle_radius=handle_radius,
            _handle_color=handle_color,
            _handle_color_hover=handle_color_hover,
            _handle_color_pressed=handle_color_pressed
        )

        self.setStyleSheet(adjust_style)
