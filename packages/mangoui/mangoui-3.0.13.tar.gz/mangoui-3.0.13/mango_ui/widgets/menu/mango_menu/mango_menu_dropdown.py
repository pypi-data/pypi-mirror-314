# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-11-17 12:42
# @Author : 毛鹏

from PySide6.QtCore import QRect, Qt, QPoint
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QComboBox, QGraphicsDropShadowEffect, QLabel

from mango_ui.settings.settings import THEME


class MangoDropdownMenu(QComboBox):
    def __init__(self, app_parent, options, tooltip_text='', btn_id=None):
        super().__init__(app_parent)
        self.setObjectName(btn_id)
        self.setCursor(Qt.PointingHandCursor)

        self.options = options
        self.tooltip_text = tooltip_text
        self.tooltip = _ToolTip(
            app_parent,
            tooltip_text,
            THEME.color.color4,
            THEME.color.color5,
            THEME.font_color
        )
        self.tooltip.hide()

        self.setStyleSheet("QComboBox {"
                           "border: 2px solid " + THEME.color.color4 + ";"
                                                                       "border-radius: 8px;"
                                                                       "padding: 5px;"
                                                                       "background-color: " + THEME.background_color + ";"
                                                                                                                       "color: " + THEME.font_color + ";"
                                                                                                                                                      "}"
                                                                                                                                                      "QComboBox::drop-down {"
                                                                                                                                                      "subcontrol-origin: padding;"
                                                                                                                                                      "subcontrol-position: top right;"
                                                                                                                                                      "width: 20px;"
                                                                                                                                                      "border-left-width: 0px;"
                                                                                                                                                      "border-left-color: transparent;"
                                                                                                                                                      "border-left-style: solid;"
                                                                                                                                                      "border-radius: 0px;"
                                                                                                                                                      "}"
                           )

        self.addItems(options)

    def enterEvent(self, event):
        self.tooltip.move_tooltip()
        self.tooltip.show()

    def leaveEvent(self, event):
        self.tooltip.hide()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.tooltip.hide()
            super().mousePressEvent(event)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)

        # 绘制背景
        rect = QRect(0, 0, self.width(), self.height())
        p.setBrush(QColor(THEME.color.color4))
        p.drawRoundedRect(rect, 8, 8)

        # 绘制文本
        p.setPen(QColor(THEME.font_color))
        p.drawText(rect, Qt.AlignVCenter | Qt.AlignLeft, self.currentText())

        p.end()


class _ToolTip(QLabel):
    style_tooltip = """ 
    QLabel {{		
        background-color: {_dark_one};	
        color: {_text_foreground};
        padding-left: 10px;
        padding-right: 10px;
        border-radius: 17px;
        border: 0px solid transparent;
        border-left: 3px solid {_context_color};
        font: 800 9pt "Segoe UI";
    }}
    """

    def __init__(self, parent, tooltip, dark_one, context_color, text_foreground):
        QLabel.__init__(self)

        style = self.style_tooltip.format(
            _dark_one=dark_one,
            _context_color=context_color,
            _text_foreground=text_foreground
        )
        self.setObjectName(u"label_tooltip")
        self.setStyleSheet(style)
        self.setMinimumHeight(34)
        self.setParent(parent)
        self.setText(tooltip)
        self.adjustSize()

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.shadow)

    def move_tooltip(self):
        gp = self.parent().mapToGlobal(QPoint(0, 0))
        pos = self.parent().mapFromGlobal(gp)
        pos_x = pos.x() + self.parent().width() + 5
        pos_y = pos.y() + (self.parent().height() - self.height()) // 2
        self.move(pos_x, pos_y)
