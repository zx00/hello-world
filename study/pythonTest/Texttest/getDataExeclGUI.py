import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel, QDateEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.font_manager as fm

class DataAnalyzerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Data Analyzer')
        self.setGeometry(100, 100, 800, 600)

        self.file_label = QLabel('选择xlsx文件:')
        self.file_name_label = QLabel('')  # 用于显示选择的文件名
        self.file_button = QPushButton('选择文件', self)
        self.file_button.clicked.connect(self.select_file)

        self.start_label = QLabel('开始时间:')
        self.start_date_edit = QDateEdit(self)
        self.start_date_edit.setCalendarPopup(True)

        self.end_label = QLabel('结束时间:')
        self.end_date_edit = QDateEdit(self)
        self.end_date_edit.setCalendarPopup(True)

        self.analyze_button = QPushButton('执行分析', self)
        self.analyze_button.clicked.connect(self.analyze_data)

        self.weekly_button = QPushButton('查看周总数', self)
        self.weekly_button.clicked.connect(self.plot_weekly_totals)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.file_label)
        self.layout.addWidget(self.file_name_label)
        self.layout.addWidget(self.file_button)
        self.layout.addWidget(self.start_label)
        self.layout.addWidget(self.start_date_edit)
        self.layout.addWidget(self.end_label)
        self.layout.addWidget(self.end_date_edit)
        self.layout.addWidget(self.analyze_button)
        self.layout.addWidget(self.weekly_button)
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, '选择xlsx文件', '', 'Excel Files (*.xlsx)')
        if file_path:
            self.file_path = file_path
            self.file_name_label.setText(f'选择的文件: {file_path}')

    def analyze_data(self):
        if hasattr(self, 'file_path'):
            start_date = self.start_date_edit.date().toPyDate()
            end_date = self.end_date_edit.date().toPyDate()

            # 读取Excel文件
            df = pd.read_excel(self.file_path)

            # 过滤符合时间段的数据
            mask = (df['创建时间'] >= start_date) & (df['创建时间'] <= end_date)
            filtered_data = df[mask]

            # 统计每个时间段的总数和行数据
            grouped_data = filtered_data.groupby(pd.Grouper(key='创建时间', freq='D')).size().reset_index(name='Count')
            grouped_rows = {}
            for date, group_df in filtered_data.groupby(pd.Grouper(key='创建时间', freq='D')):
                grouped_rows[date] = group_df

            # 输出统计结果和行数据
            print("Grouped Data:")
            print(grouped_data)

            print("\nGrouped Rows:")
            for date, rows in grouped_rows.items():
                print(f"Date: {date}")
                print(rows)
                print("\n")

            # 更新图形
            self.plot_grouped_data(grouped_data)

    def plot_weekly_totals(self):
        if hasattr(self, 'file_path'):
            # 读取Excel文件
            df = pd.read_excel(self.file_path)

            # 过滤符合时间段的数据
            start_date = self.start_date_edit.date().toPyDate()
            end_date = self.end_date_edit.date().toPyDate()

            mask = (df['创建时间'] >= start_date) & (df['创建时间'] <= end_date)
            filtered_data = df[mask]

            # 按周统计总数
            weekly_totals = filtered_data.groupby(pd.Grouper(key='创建时间', freq='W')).size().reset_index(name='Count')

            # 绘制折线图
            self.ax.clear()
            self.ax.plot(weekly_totals['创建时间'], weekly_totals['Count'])
            self.ax.set_xlabel('时间')
            self.ax.set_ylabel('总数')
            self.ax.set_title('周总数情况')

            # 设置中文显示
            font_path = "SimHei.ttf"  # 请将SimHei.ttf替换为你本地的中文字体路径
            prop = fm.FontProperties(fname=font_path)
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams['axes.unicode_minus'] = False

            self.canvas.draw()

    def plot_grouped_data(self, grouped_data):
        # 绘制折线图
        self.ax.clear()
        self.ax.plot(grouped_data['创建时间'], grouped_data['Count'])
        self.ax.set_xlabel('时间')
        self.ax.set_ylabel('总数')
        self.ax.set_title('每日总数情况')

        # 设置中文显示
        font_path = "SimHei.ttf"  # 请将SimHei.ttf替换为你本地的中文字体路径
        prop = fm.FontProperties(fname=font_path)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DataAnalyzerApp()
    ex.show()
    sys.exit(app.exec_())
