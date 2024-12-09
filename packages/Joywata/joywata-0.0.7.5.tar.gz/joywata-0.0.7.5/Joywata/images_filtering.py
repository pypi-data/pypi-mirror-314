import sys
import os
try:
    from PyQt5.QtWidgets import (
        QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog,
        QListWidget, QHBoxLayout, QSplitter, QSizePolicy, QScrollArea, QMessageBox
    )
    from PyQt5.QtGui import QPixmap
    from PyQt5.QtCore import Qt, QTimer
except:
    PYQT5 = None

class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.image_list = []
        self.current_index = 0
        self.timer = None  # 定时器用于连续切换图片
        self.save_path = None  # 用于保存文件名的路径

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        splitter = QSplitter(Qt.Horizontal)

        # 左侧区域
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # 打开文件夹按钮
        self.open_folder_button = QPushButton("打开文件夹", self)
        self.open_folder_button.setFixedWidth(120)  # 设置固定宽度
        self.open_folder_button.clicked.connect(self.open_folder)
        left_layout.addWidget(self.open_folder_button, alignment=Qt.AlignLeft)  # 使按钮左对齐

        # 图片显示区域
        self.image_layout = QVBoxLayout()
        self.label = QLabel("请点击下面的按钮选择文件夹", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.image_layout.addWidget(self.label)

        self.image_address_label = QLabel("", self)
        self.image_address_label.setAlignment(Qt.AlignCenter)
        self.image_address_label.setFixedHeight(20)
        self.image_layout.addWidget(self.image_address_label)

        # 当前图片位置的显示标签
        self.position_label = QLabel("", self)
        self.position_label.setAlignment(Qt.AlignCenter)
        self.position_label.setFixedHeight(20)
        self.image_layout.addWidget(self.position_label)

        # 按钮布局
        self.button_layout = QHBoxLayout()
        self.prev_button = QPushButton("上一张", self)
        self.prev_button.clicked.connect(self.show_previous_image)
        self.prev_button.setEnabled(False)
        self.prev_button.setAutoRepeat(True)  # 按住时连续触发
        self.button_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("下一张", self)
        self.next_button.clicked.connect(self.show_next_image)
        self.next_button.setEnabled(False)
        self.next_button.setAutoRepeat(True)  # 按住时连续触发
        self.button_layout.addWidget(self.next_button)

        self.select_button = QPushButton("选择", self)
        self.select_button.clicked.connect(self.select_image)
        self.select_button.setEnabled(False)
        self.button_layout.addWidget(self.select_button)

        self.image_layout.addLayout(self.button_layout)
        left_layout.addLayout(self.image_layout)

        splitter.addWidget(left_widget)

        # 右侧显示文件名的滚动区域
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.list_widget = QListWidget(self.scroll_area)
        self.scroll_area.setWidget(self.list_widget)
        self.scroll_area.setWidgetResizable(True)

        splitter.addWidget(self.scroll_area)

        # 设置初始宽度，右侧栏占整个界面的1/5
        splitter.setSizes([self.size().width() * 4 / 5, self.size().width() * 1 / 5])

        # 将 splitter 添加到主布局
        main_layout.addWidget(splitter)

        self.setLayout(main_layout)

        self.setWindowTitle("图片查看器")
        self.resize(800, 600)

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder:
            # 获取文件夹中的所有图片文件，并按文件名排序
            self.image_list = [os.path.join(folder, f) for f in os.listdir(folder)
                               if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
            self.image_list.sort()  # 按文件名排序

            if self.image_list:
                self.current_index = 0
                self.show_image()
                self.prev_button.setEnabled(True)
                self.next_button.setEnabled(True)
                self.select_button.setEnabled(True)

    def show_image(self):
        if self.image_list:
            pixmap = QPixmap(self.image_list[self.current_index])
            pixmap = self.resize_image(pixmap)  # 调整图片大小

            self.label.setPixmap(pixmap)
            self.label.setText("")  # 清空提示文本
            # 显示当前图片的地址
            self.image_address_label.setText(self.image_list[self.current_index])

            # 显示当前图片的序号和总图片数
            total_images = len(self.image_list)
            current_position = self.current_index + 1  # 索引从 0 开始，所以加 1
            self.position_label.setText(f"当前图片: {current_position} / {total_images}")

    def resize_image(self, pixmap):
        """根据窗口大小调整图片大小"""
        label_width = self.label.width()
        label_height = self.label.height()

        # 按比例缩放，保持宽高比
        return pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def show_previous_image(self):
        if self.image_list:
            if self.current_index == 0:
                QMessageBox.information(self, "提示", "已到达第一张图片")
            else:
                self.current_index -= 1
                self.show_image()

    def show_next_image(self):
        if self.image_list:
            if self.current_index == len(self.image_list) - 1:
                QMessageBox.information(self, "提示", "已到达最后一张图片")
            else:
                self.current_index += 1
                self.show_image()

    def select_image(self):
        # 如果没有选择保存路径，提示用户选择路径
        if self.save_path is None:
            QMessageBox.warning(self, "提示", "点击OK，选择txt保存路径。")

            folder = QFileDialog.getSaveFileName(self, "选择保存文件", "", "Text Files (*.txt)")
            if not folder[0]:  # 用户没有选择路径
                QMessageBox.warning(self, "提示", "请选择保存文件路径")
                return
            self.save_path = folder[0]  # 保存文件路径

        # 获取当前图片的文件名
        filename = os.path.basename(self.image_list[self.current_index])

        # 检查文件名是否已经存在于右侧栏中
        existing_items = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]

        # 检查文件名是否已经存在于txt文件中
        if os.path.exists(self.save_path):
            with open(self.save_path, "r") as file:
                existing_files = file.read().splitlines()
        else:
            existing_files = []

        # 如果文件名已经存在，则弹出提示框
        if filename in existing_items or filename in existing_files:
            QMessageBox.warning(self, "提示", "该图片已被选择，不会重复添加。")
            return

        # 将当前文件名添加到右侧列表中
        self.list_widget.addItem(filename)

        # 将当前文件名写入用户选择的txt文件
        with open(self.save_path, "a") as file:
            file.write(filename + "\n")

        # 如果是最后一张图片，弹出提示框
        if self.current_index == len(self.image_list) - 1:
            QMessageBox.information(self, "提示", "已选择最后一张图片")
        else:
            # 跳转到下一张图
            self.current_index += 1
            self.show_image()

    def start_timer(self, direction):
        """启动定时器进行图片切换"""
        if not self.timer:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.auto_change_image)
        self.timer.start(200)  # 每200毫秒切换一次图片

        self.direction = direction  # 记录当前方向

    def stop_timer(self):
        """停止定时器"""
        if self.timer:
            self.timer.stop()
            self.timer = None

    def auto_change_image(self):
        """自动切换图片"""
        if self.direction == 'next':
            self.show_next_image()
        elif self.direction == 'prev':
            self.show_previous_image()

    def mousePressEvent(self, event):
        """长按时启动定时器"""
        if event.button() == Qt.LeftButton:
            if self.prev_button.underMouse():
                self.start_timer('prev')
            elif self.next_button.underMouse():
                self.start_timer('next')

    def mouseReleaseEvent(self, event):
        """松开鼠标时停止定时器"""
        if event.button() == Qt.LeftButton:
            self.stop_timer()

    def resizeEvent(self, event):
        """当窗口大小改变时，重新缩放图片"""
        self.show_image()


def manual_image_filtering_interface():
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())
