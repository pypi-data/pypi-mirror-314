# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-10-31 9:51
# @Author : 毛鹏
import os

from mango_ui.pages import *
from mango_ui.settings.settings import STYLE, MENUS


os.environ["QT_FONT_DPI"] = "96"

def main():
    page_dict = {
        'home': HomePage,
        'component': ComponentPage,
        'feedback': FeedbackPage,
        'container': ContainerPage,
        'charts': ChartsPage,
        'display': DisplayPage,
        'graphics': GraphicsPage,
        'input': InputPage,
        'layout': LayoutPage,
        'layout_page_1': Layout1Page,
        'layout_page_2': Layout2Page,
        'component_page_3': Layout3Page,
        'component_page_4': Layout4Page,
        'menu': MenuPage,
        'miscellaneous': MiscellaneousPage,
        'window': WindowPage,
    }

    app = QApplication([])
    login_window = MangoMain1Window(STYLE, MENUS, page_dict)
    login_window.show()
    app.exec()


main()
