'''
下面是一个使用PyQt和Python，结合Pandas和OpenPyXL库来实现读取本地xlsx文件、进行时间段选择、处理数据、导出处理后的数据的简单示例。

确保你已经安装了PyQt5、pandas和openpyxl，可以使用以下命令进行安装：

bash
Copy code
pip install PyQt5 pandas openpyxl

'''


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QDateTimeEdit
import pandas as pd

class ExcelProcessor(QWidget):
    def __init__(self):
        super(ExcelProcessor, self).__init__()

        self.data = pd.DataFrame()  # 存储读取的数据
        self.filtered_data = pd.DataFrame()  # 存储处理后的数据

        self.file_path_label = QLabel('File Path: No file selected')
        self.load_button = QPushButton('Load Excel File')
        self.start_date_edit = QDateTimeEdit(self)
        self.start_date_edit.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
        self.end_date_edit = QDateTimeEdit(self)
        self.end_date_edit.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
        self.filter_button = QPushButton('Filter Data')
        self.export_button = QPushButton('Export Data')

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(self.file_path_label)
        layout.addWidget(self.load_button)
        layout.addWidget(QLabel('Start Date:'))
        layout.addWidget(self.start_date_edit)
        layout.addWidget(QLabel('End Date:'))
        layout.addWidget(self.end_date_edit)
        layout.addWidget(self.filter_button)
        layout.addWidget(self.export_button)

        self.setLayout(layout)

        self.load_button.clicked.connect(self.load_excel_file)
        self.filter_button.clicked.connect(self.filter_data)
        self.export_button.clicked.connect(self.export_data)

    def load_excel_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open Excel File', '', 'Excel Files (*.xlsx *.xls)')

        if file_path:
            self.file_path_label.setText(f'File Path: {file_path}')
            self.data = pd.read_excel(file_path)

    def filter_data(self):
        start_date = self.start_date_edit.dateTime().toPyDateTime()
        end_date = self.end_date_edit.dateTime().toPyDateTime()

        mask = (self.data['Timestamp'] >= start_date) & (self.data['Timestamp'] <= end_date)
        self.filtered_data = self.data.loc[mask]

        # 在这里添加你对数据的处理步骤，例如筛选某些列，进行统计等

        print("Data filtered.")

    def export_data(self):
        if not self.filtered_data.empty:
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(self, 'Save Excel File', '', 'Excel Files (*.xlsx)')

            if file_path:
                self.filtered_data.to_excel(file_path, index=False)
                print(f'Data exported to {file_path}')
        else:
            print("No data to export.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    excel_processor = ExcelProcessor()
    excel_processor.show()
    sys.exit(app.exec_())
