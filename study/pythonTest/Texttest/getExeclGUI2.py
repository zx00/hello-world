'''

对存在严重程度、模块、创建时间、BUG状态、标签列的execl，写一个可以从本机选择xlxs文件，有先对自定义标签数据进行筛选然后进行严重程度统计、模块BUG状态分布、
自定义周或者日BUG关闭和总数据情况折线图展示的功能，
功能使用通过按钮触发，界面通过pyqt实现，功能通过pandas和matplops实现，处理后的数据有按钮可以对处理后的数据进行导出，严重程度和总BUG关闭情况通过饼图呈现
'''

import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel, QComboBox,QCheckBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.font_manager as fm


class BugAnalyzerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Bug Analyzer')
        self.setGeometry(100, 100, 800, 600)

        self.file_label = QLabel('选择xlsx文件:')
        self.file_name_label = QLabel('')  # 用于显示选择的文件名
        self.file_button = QPushButton('选择文件', self)
        self.file_button.clicked.connect(self.select_file)

        # self.label_filter_label = QLabel('选择标签:')
        # self.label_filter_combo = QComboBox(self)
        # # 添加标签选项，你可以根据实际情况修改
        # self.label_filter_combo.addItems(['稳健测试', '标签2', '标签3'])
        self.label_group = QLabel('选择标签:')
        self.label_checkboxes = {}
        self.create_label_checkboxes()

        self.analyze_button = QPushButton('执行分析', self)
        self.analyze_button.clicked.connect(self.analyze_data)

        self.export_button = QPushButton('导出数据', self)
        self.export_button.clicked.connect(self.export_data)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.file_label)
        self.layout.addWidget(self.file_name_label)
        self.layout.addWidget(self.file_button)
        # self.layout.addWidget(self.label_filter_label)
        # self.layout.addWidget(self.label_filter_combo)
        for checkbox in self.label_checkboxes.values():
            self.layout.addWidget(checkbox)
        self.layout.addWidget(self.analyze_button)
        self.layout.addWidget(self.export_button)
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)
    def set_chinese_font(self):
        font_path = "SimHei.ttf"  # 请将SimHei.ttf替换为你本地的中文字体路径
        prop = fm.FontProperties(fname=font_path)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

    def create_label_checkboxes(self):
        # 根据实际标签列的数据，创建对应的复选框
        labels = ['稳健测试', '万翼测试', '']  # 请替换为实际的标签数据
        for label in labels:
            checkbox = QCheckBox(label, self)
            self.label_checkboxes[label] = checkbox
    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, '选择xlsx文件', '', 'Excel Files (*.xlsx)')
        if file_path:
            # 读取xlsx文件
            self.data = pd.read_excel(file_path)
            self.file_name_label.setText(f'选择的文件: {file_path}')

    def analyze_data(self):
        if hasattr(self, 'data'):

             # 设置中文显示
            font_path = "SimHei.ttf"  # 请将SimHei.ttf替换为你本地的中文字体路径
            prop = fm.FontProperties(fname=font_path)
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams['axes.unicode_minus'] = False

            # 根据选择的标签进行筛选
            # selected_label = self.label_filter_combo.currentText()
            # filtered_data = self.data[self.data['标签'] == selected_label]

            selected_labels = [label for label, checkbox in self.label_checkboxes.items() if checkbox.isChecked()]

            if not selected_labels:
                print("请选择至少一个标签.")
                return
            # 根据选择的标签筛选数据
            mask = self.data['标签'].isin(selected_labels)
            filtered_data = self.data[mask]



            # 严重程度统计
            severity_counts = filtered_data['严重程度'].value_counts()

            # 模块BUG状态分布
            module_bug_status_counts = filtered_data.groupby(['模块', '状态']).size().unstack().fillna(0)

            # 自定义周或者日BUG关闭
            # 这里假设有一个日期列 '创建时间列'
            filtered_data['创建时间'] = pd.to_datetime(filtered_data['创建时间'])
            filtered_data.set_index('创建时间', inplace=True)
            weekly_closed_bugs = filtered_data.resample('W').sum()

            # 总数据情况折线图展示
            total_data_counts = self.data['标签'].value_counts()

            # 绘制折线图
            self.ax.clear()
            self.ax.plot(total_data_counts.index, total_data_counts.values)
            self.ax.set_xlabel('标签')
            self.ax.set_ylabel('数据数量')
            self.ax.set_title('总数据情况')
            self.canvas.draw()

            # 绘制饼图
            self.figure_pie, ax_pie = plt.subplots()
            # ax_pie.pie(severity_counts, labels=severity_counts.index, autopct='%1.1f%%', startangle=90)
            ax_pie.pie(severity_counts, labels=severity_counts.index, autopct='%1.1f%%', startangle=90)
            ax_pie.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            ax_pie.set_title('严重程度分布')
            self.canvas_pie = FigureCanvas(self.figure_pie)
            self.layout.addWidget(self.canvas_pie)

    def export_data(self):
        if hasattr(self, 'data'):
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(self, '导出数据', '', 'Excel Files (*.xlsx)')
            if file_path:
                # 将处理后的数据导出到Excel文件
                with pd.ExcelWriter(file_path) as writer:
                    self.data.to_excel(writer, sheet_name='Original Data')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BugAnalyzerApp()
    ex.show()
    sys.exit(app.exec_())
