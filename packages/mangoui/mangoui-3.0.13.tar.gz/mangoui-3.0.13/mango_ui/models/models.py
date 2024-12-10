# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-10-08 16:15
# @Author : 毛鹏
from typing import Any

from pydantic import BaseModel

from mango_ui.enums.enums import InputEnum


class Font(BaseModel):
    family: str
    title_size: int
    text_size: int


class GroupColors(BaseModel):
    info: str
    warning: str
    success: str
    error: str


class HoverState(BaseModel):
    background_color: str
    color: str


class PressedState(BaseModel):
    background_color: str
    color: str


class DisabledState(BaseModel):
    background_color: str
    color: str


class ThemeColors(BaseModel):
    color1: str
    color2: str
    color3: str
    color4: str
    color5: str
    color6: str
    color7: str
    color8: str
    color9: str
    color10: str


class Theme(BaseModel):
    theme_name: str
    font_color: str
    font_family: str
    font_size: str
    font_weight: str
    icon_color: str
    icon_hover: str
    icon_pressed: str
    icon_active: str
    card_color: str
    color: ThemeColors
    background_color: str
    border: str
    border_radius: str
    padding: str
    margin: str
    width: str
    height: str
    text_align: str
    line_height: str
    group: GroupColors
    hover: HoverState
    pressed: PressedState
    disabled: DisabledState
    font: Font


class LeftMenuSize(BaseModel):
    minimum: int
    maximum: int


class ColumnSize(BaseModel):
    minimum: int
    maximum: int


class AppConfig(BaseModel):
    app_name: str
    version: str
    copyright: str
    year: int
    theme_name: str
    custom_title_bar: bool

    lef_menu_size: LeftMenuSize
    left_menu_content_margins: int
    left_column_size: ColumnSize
    right_column_size: ColumnSize


class ThemeConfig(BaseModel):
    theme_name: str
    dark_one: str
    dark_two: str
    dark_three: str
    dark_four: str
    bg_one: str
    bg_two: str
    bg_three: str
    icon_color: str
    icon_hover: str
    icon_pressed: str
    icon_active: str
    context_color: str
    context_hover: str
    context_pressed: str
    text_title: str
    text_foreground: str
    text_description: str
    text_active: str
    white: str
    pink: str
    green: str
    red: str
    yellow: str
    blue: str
    orange: str
    radius: str
    border_size: str
    font: Font


class LeftMenuModel(BaseModel):
    btn_icon: str | None = None
    btn_id: str
    btn_text: str
    btn_tooltip: str
    show_top: bool
    is_active: bool
    is_active: bool
    submenus: list['LeftMenuModel'] = []
    url: str | None = None
    but_obj: Any | None = None
    frame_object: Any | None = None


class TitleBarMenusModel(BaseModel):
    btn_icon: str
    btn_id: str
    btn_tooltip: str
    is_active: bool


class MenusModel(BaseModel):
    left_menus: list[LeftMenuModel]
    title_bar_menus: list[TitleBarMenusModel]


class SearchDataModel(BaseModel):
    title: str
    placeholder: str
    key: str
    type: InputEnum = InputEnum.INPUT
    select: dict | list[dict] | Any = None
    input_object: None = None
    value: str | None = None
    subordinate: str | None = None  # 是否联动下级选择条件


class RightDataModel(BaseModel):
    name: str
    theme: str
    action: str
    obj: Any | None = None


class FormDataModel(BaseModel):
    title: str
    placeholder: str
    key: str
    input_object: None = None
    value: str | None = None
    type: InputEnum = InputEnum.INPUT
    select: dict | list[dict] | Any = None  # 选项数据
    subordinate: str | None = None  # 是否联动下级选择条件
    required: bool = True  # 是否必填


class TableColumnModel(BaseModel):
    key: str
    name: str
    width: int | None = None
    option: dict | list[dict] | None = None


class TableMenuItemModel(BaseModel):
    name: str
    action: str
    son: list['TableMenuItemModel'] = []


class FieldListModel(BaseModel):
    key: str
    name: str


class CascaderModel(BaseModel):
    value: str
    label: str
    parameter: dict | None = None
    children: list['CascaderModel'] = []

    @classmethod
    def get_model(cls, data):
        if isinstance(data, dict):
            data = [data]
        return [
            cls(
                value=str(i['value']),
                label=i['label'],
                parameter=i.get('parameter'),
                children=cls.get_model(i.get('children', []))
            ) for i in data
        ]


class TreeModel(BaseModel):
    key: str
    status: int
    title: str
    children: list['TreeModel'] = []
    data: Any | None = None

    @classmethod
    def get_model(cls, data):
        return [cls(
            key=str(i['key']),
            status=i['status'],
            title=i.get('title'),
            data=i,
            children=[cls.get_model(child) for child in i.get('children', [])]) for i in data]


class DialogCallbackModel(BaseModel):
    key: str | None = None
    value: int | str | None
    input_object: Any | None = None
    subordinate: str
    subordinate_input_object: Any | None = None


class ComboBoxDataModel(BaseModel):
    id: str | None
    name: str | None

    @classmethod
    def get_model(cls, data):
        return [cls(id=str(i['id']), name=i['name']) for i in data]


if __name__ == '__main__':
    print(CascaderModel.get_model({'value': 13, 'label': '新智投', 'parameter': None,
                                   'children': [{'value': 107, 'label': '登录', 'parameter': None, 'children': []},
                                                {'value': 106, 'label': '项目', 'parameter': None, 'children': []},
                                                {'value': 105, 'label': '小红书实时看版', 'parameter': None,
                                                 'children': []},
                                                {'value': 104, 'label': '报数助手', 'parameter': None, 'children': []},
                                                {'value': 103, 'label': '用户中心', 'parameter': None, 'children': []},
                                                {'value': 102, 'label': '首页', 'parameter': None, 'children': []}]}))
