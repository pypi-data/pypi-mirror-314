import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PySide6 多选表格示例")
        self.setGeometry(100, 100, 400, 300)

        # 创建中心小部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建布局
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # 创建表格
        self.table_widget = QTableWidget(5, 2)  # 5 行 2 列
        self.table_widget.setHorizontalHeaderLabels(["选择", "内容"])

        # 填充表格
        for row in range(5):
            # 添加内容
            content_item = QTableWidgetItem(f"内容 {row + 1}")
            content_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table_widget.setItem(row, 1, content_item)

        self.layout.addWidget(self.table_widget)

        # 创建按钮
        self.button = QPushButton("获取选中的项")
        self.button.clicked.connect(self.get_selected_items)
        self.layout.addWidget(self.button)

    def get_selected_items(self):
        selected_items = []
        # 获取所有被选中的行
        for row in range(self.table_widget.rowCount()):
            if self.table_widget.item(row, 1).isSelected():
                content_item = self.table_widget.item(row, 1)
                selected_items.append(content_item.text())
        print("选中的项:", selected_items)

    def mousePressEvent(self, event):
        # 清除之前的选择
        self.table_widget.clearSelection()
        # 获取鼠标点击的位置
        item = self.table_widget.itemAt(event.pos())
        if item:
            # 选择当前行
            self.table_widget.setCurrentItem(item)
        super().mousePressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
