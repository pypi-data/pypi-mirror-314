# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description:
# @Time   : 2024-08-16 17:05
# @Author : 毛鹏
import json
from functools import partial

from mango_ui.init import *
from mango_ui.models.models import TableColumnModel, TableMenuItemModel


class MangoTable(QTableWidget):
    click = Signal(object)

    def __init__(self, row_column: list[TableColumnModel], row_ope: list[TableMenuItemModel] = None):
        super().__init__()
        self.row_column = row_column
        self.row_ope = row_ope
        self.column_count = len(row_column)
        self.header_labels = [i.name for i in row_column]
        self.set_stylesheet()
        self.setColumnCount(self.column_count)
        self.setHorizontalHeaderLabels(self.header_labels)
        self.data: list[dict] = None
        self.set_column_widths()
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.verticalHeader().setVisible(False)

        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setMouseTracking(True)

    def set_column_widths(self):
        for index, column in enumerate(self.row_column):
            if column.width:
                self.setColumnWidth(index, column.width)
                self.horizontalHeader().setSectionResizeMode(index, QHeaderView.Fixed)
            else:
                self.horizontalHeader().setSectionResizeMode(index, QHeaderView.Stretch)

    def set_value(self, data):
        self.data = data
        self.setRowCount(0)
        if data is None:
            return

        for row, item in enumerate(data):
            self.insertRow(row)
            for row1, column in enumerate(self.row_column):
                if column.key != 'ope':
                    if isinstance(item[column.key], dict):
                        item1 = item[column.key].get('name', json.dumps(item[column.key], ensure_ascii=False))
                    elif isinstance(item[column.key], list):
                        item1 = json.dumps(item[column.key], ensure_ascii=False)
                    else:
                        item1 = item[column.key]
                    if column.option is not None:
                        item1 = self.get_option_value(column.option, item1)
                    cell_item = QTableWidgetItem(str(item1) if item1 is not None else '')
                    self.setItem(row, row1, cell_item)

            if self.row_ope:
                action_widget = QWidget()
                action_layout = QHBoxLayout()
                action_widget.setLayout(action_layout)
                for ope in self.row_ope:
                    but = QPushButton(ope.name)
                    but.setStyleSheet(
                        'QPushButton { background-color: transparent; border: none; padding: 0; color: blue; font-size: 10px; }')
                    but.setCursor(QCursor(Qt.PointingHandCursor))
                    action_layout.addWidget(but)
                    if not ope.son:
                        but.clicked.connect(partial(self.but_clicked, {'action': ope.action, 'row': item}))
                    else:
                        menu = QMenu()
                        for ope1 in ope.son:
                            action = QAction(ope1.name, self)
                            action.triggered.connect(partial(self.but_clicked, {'action': ope1.action, 'row': item}))
                            menu.addAction(action)
                        but.clicked.connect(lambda _, m=menu: m.exec_(QCursor.pos()))

                self.setCellWidget(row, len(self.row_column) - 1, action_widget)

    def get_option_value(self, option: list[dict], item1) -> str:
        for i in option:
            if i.get('children'):
                for e in i.get('children'):
                    if e.get('children'):
                        for q in e.get('children'):
                            if q.get('value') == item1:
                                return q.get('label')
                    else:
                        if e.get('value') == item1:
                            return e.get('label')
            if str(i.get('value')) == str(item1):
                return i.get('label')

    def but_clicked(self, data):
        self.click.emit(data)

    def mousePressEvent(self, event):
        local_pos = event.position().toPoint()
        item = self.itemAt(local_pos)
        if item:
            row = item.row()
            self.click.emit({'action': 'click_row', 'row': self.data[row]})
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        local_pos = event.position().toPoint()
        item = self.itemAt(local_pos)
        if item:
            text = item.text()
            rect = self.visualItemRect(item)
            if self.fontMetrics().horizontalAdvance(text) + 20 > rect.width():
                QToolTip.showText(QCursor.pos(), text)
            else:
                QToolTip.hideText()
        else:
            QToolTip.hideText()
        super().mouseMoveEvent(event)

    def get_selected_items(self):
        selected_items = []
        for row in range(self.rowCount()):
            if self.item(row, 1).isSelected():
                content_item = self.item(row, 0)
                selected_items.append(content_item.text())
        return selected_items

    def set_stylesheet(self, ):
        style = f'''
        /* 
        QTableWidget */

        QTableWidget {{	
        	background-color: {THEME.background_color};
        	padding: 5px;
        	border-radius: {THEME.border_radius};
        	gridline-color: {THEME.color.color1};
            color: {THEME.font_color};
        }}
        QTableWidget::item{{
        	border-color: none;
        	padding-left: 5px;
        	padding-right: 5px;
        	gridline-color: rgb(44, 49, 60);
            border-bottom: 1px solid {THEME.border};
        }}
        QTableWidget::item:selected{{
        	background-color: {THEME.color.color2};
            color: {THEME.font_color};

        }}
        QHeaderView::section{{
        	background-color: rgb(33, 37, 43);
        	max-width: 30px;
        	border: 1px solid rgb(44, 49, 58);
        	border-style: none;
            border-bottom: 1px solid rgb(44, 49, 60);
            border-right: 1px solid rgb(44, 49, 60);
        }}
        QTableWidget::horizontalHeader {{	
        	background-color: rgb(33, 37, 43);
        }}
        QTableWidget QTableCornerButton::section {{
            border: none;
        	background-color: {THEME.color.color2};
        	padding: 3px;
            border-top-left-radius: {THEME.border_radius};
        }}
        QHeaderView::section:horizontal
        {{
            border: none;
        	background-color: {THEME.color.color5};
        	padding: 3px;
        }}
        QHeaderView::section:vertical
        {{
            border: none;
        	background-color: {THEME.color.color5};
        	padding-left: 5px;
            padding-right: 5px;
            border-bottom: 1px solid {THEME.border};
            margin-bottom: 1px;
        }}


        /* 
        ScrollBars */
        QScrollBar:horizontal {{
            border: none;
            background: {THEME.color.color1};
            height: 8px;
            margin: 0px 21px 0 21px;
        	border-radius: 0px;
        }}
        QScrollBar::handle:horizontal {{
            background: {THEME.color.color5};
            min-width: 25px;
        	border-radius: 4px
        }}
        QScrollBar::add-line:horizontal {{
            border: none;
            background: {THEME.color.color5};
            width: 20px;
        	border-top-right-radius: 4px;
            border-bottom-right-radius: 4px;
            subcontrol-position: right;
            subcontrol-origin: margin;
        }}
        QScrollBar::sub-line:horizontal {{
            border: none;
            background: {THEME.color.color10};
            width: 20px;
        	border-top-left-radius: 4px;
            border-bottom-left-radius: 4px;
            subcontrol-position: left;
            subcontrol-origin: margin;
        }}
        QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal
        {{
             background: none;
        }}
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
        {{
             background: none;
        }}
        QScrollBar:vertical {{
        	border: none;
            background: {THEME.background_color};
            width: 8px;
            margin: 21px 0 21px 0;
        	border-radius: 0px;
        }}
        QScrollBar::handle:vertical {{	
        	background: {THEME.color.color5};
            min-height: 25px;
        	border-radius: 4px
        }}
        QScrollBar::add-line:vertical {{
             border: none;
            background: {THEME.color.color5};
             height: 20px;
        	border-bottom-left-radius: 4px;
            border-bottom-right-radius: 4px;
             subcontrol-position: bottom;
             subcontrol-origin: margin;
        }}
        QScrollBar::sub-line:vertical {{
        	border: none;
            background: {THEME.color.color5};
             height: 20px;
        	border-top-left-radius: 4px;
            border-top-right-radius: 4px;
             subcontrol-position: top;
             subcontrol-origin: margin;
        }}
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
             background: none;
        }}

        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
             background: none;
        }}
        '''
        self.setStyleSheet(style)
