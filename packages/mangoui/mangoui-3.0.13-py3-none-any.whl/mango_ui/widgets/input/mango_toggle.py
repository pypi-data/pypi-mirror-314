# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description:
# @Time   : 2024-08-16 17:05
# @Author : 毛鹏
from mango_ui.enums.enums import StatusEnum
from mango_ui.init import *
from mango_ui.models.models import ComboBoxDataModel


class MangoToggle(QCheckBox):
    click = Signal(object)
    change_requested = Signal(object)

    def __init__(self, value=False, auto_update_status=True, **kwargs):
        super().__init__()
        self.value = value
        self.kwargs = kwargs
        self.auto_update_status = auto_update_status
        self.data = [ComboBoxDataModel(id=str(i.get('id')), name=i.get('name')) for i in [
            {'id': 0, 'name': '关闭&进行中&失败'}, {'id': 1, 'name': '启用&已完成&通过'}]]
        self.setFixedSize(50, 28)
        self.setCursor(Qt.PointingHandCursor)  # type: ignore

        self._position = 3
        self.animation = QPropertyAnimation(self, b"position")
        self.animation.setEasingCurve(QEasingCurve.OutBounce)  # type: ignore
        self.animation.setDuration(500)
        self.clicked.connect(self.on_clicked)
        self.stateChanged.connect(self.set_animation)
        self.set_value(self.value)
        self.change_requested.connect(self.set_animation)

    def get_value(self) -> int:
        return int(self.isChecked())

    def set_value(self, value: bool | StatusEnum):
        if value is None:
            return
        if isinstance(value, StatusEnum):
            self.value = bool(value)
        else:
            self.value = value
        self.setChecked(self.value)

    @Property(float)
    def position(self):
        return self._position

    @position.setter
    def position(self, pos):
        self._position = pos
        self.update()

    def on_clicked(self, value):
        if self.auto_update_status:
            self.set_value(value)
        self.click.emit({'value': int(self.isChecked())})

    def set_animation(self, value):
        self.animation.stop()
        if self.isChecked():
            self.animation.setEndValue(self.width() - 27)
        else:
            self.animation.setEndValue(3)
        self.animation.start()

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)  # type: ignore
        p.setFont(QFont("Segoe UI", 9))
        p.setPen(Qt.NoPen)  # type: ignore
        rect = QRect(0, 0, self.width(), self.height())
        if self.isChecked():
            p.setBrush(QColor(THEME.group.success))
            p.drawRoundedRect(0, 0, rect.width(), 28, 14, 14)
            p.setBrush(QColor(THEME.color.color5))
            p.drawEllipse(self._position, 3, 22, 22)
        else:
            p.setBrush(QColor(THEME.color.color2))
            p.drawRoundedRect(0, 0, rect.width(), 28, 14, 14)
            p.setBrush(QColor(THEME.color.color5))
            p.drawEllipse(self._position, 3, 22, 22)
        p.end()
