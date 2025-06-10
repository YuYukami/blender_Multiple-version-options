import sys
from PyQt5 import QtWidgets, QtGui
import configparser
import re

class BlenderConfigTool(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.submissionSections = []  # 用來儲存 BlenderSubmission.py 版本的 QLineEdit
        self.initUI()

    def initUI(self):
        # Layouts
        mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(mainLayout)
        
        xaninfobox = QtWidgets.QGroupBox("使用說明")
        xaninfolayout = QtWidgets.QVBoxLayout()
        xaninfobox.setLayout(xaninfolayout)
        
        xanwarinfo = QtWidgets.QLabel("版本號碼一定要三位數,並且.param以及.py的版本號碼需要一致，否則會抓不到")
        xanwarinfo2 = QtWidgets.QLabel("特殊版本可以修改成自己知道的號碼")
        
        xaninfolayout.addWidget(xanwarinfo)
        xaninfolayout.addWidget(xanwarinfo2)
        mainLayout.addWidget(xaninfobox)

        # File Selection Section
        fileSelectionGroupBox = QtWidgets.QGroupBox("選擇檔案")
        fileSelectionLayout = QtWidgets.QVBoxLayout()
        fileSelectionGroupBox.setLayout(fileSelectionLayout)

        defaultLocationButton = QtWidgets.QPushButton("加載預設位置")
        defaultLocationButton.clicked.connect(self.loadDefaultLocations)
        fileSelectionLayout.addWidget(defaultLocationButton)

        self.paramFilePathEdit = QtWidgets.QLineEdit()
        self.paramFilePathEdit.setPlaceholderText("選擇 Blender.param 檔案")
        paramFileButton = QtWidgets.QPushButton("瀏覽")
        paramFileButton.clicked.connect(self.selectParamFile)
        fileSelectionLayout.addWidget(self.paramFilePathEdit)
        fileSelectionLayout.addWidget(paramFileButton)

        self.submissionFilePathEdit = QtWidgets.QLineEdit()
        self.submissionFilePathEdit.setPlaceholderText("選擇 BlenderSubmission.py 檔案")
        submissionFileButton = QtWidgets.QPushButton("瀏覽")
        submissionFileButton.clicked.connect(self.selectSubmissionFile)
        fileSelectionLayout.addWidget(self.submissionFilePathEdit)
        fileSelectionLayout.addWidget(submissionFileButton)

        mainLayout.addWidget(fileSelectionGroupBox)

        # Blender.param Section
        paramGroupBox = QtWidgets.QGroupBox("Blender.param 配置")
        paramLayout = QtWidgets.QVBoxLayout()
        paramGroupBox.setLayout(paramLayout)

        self.paramSections = []  # 儲存每個版本區塊中的 (版本, 路徑) QLineEdit 參考

        addParamButton = QtWidgets.QPushButton("新增 Blender 版本區塊")
        addParamButton.clicked.connect(lambda: self.addParamSection())
        paramLayout.addWidget(addParamButton)

        loadParamButton = QtWidgets.QPushButton("讀取 Blender.param 版本")
        loadParamButton.clicked.connect(self.loadParamFile)
        paramLayout.addWidget(loadParamButton)

        updateParamButton = QtWidgets.QPushButton("更新 Blender.param 檔案")
        updateParamButton.clicked.connect(self.updateParamFile)
        paramLayout.addWidget(updateParamButton)

        # 用來放置所有 Blender.param 版本區塊，加入滾動區域
        self.paramSectionsContainer = QtWidgets.QWidget()
        self.paramSectionsContainerLayout = QtWidgets.QVBoxLayout()
        self.paramSectionsContainer.setLayout(self.paramSectionsContainerLayout)
        self.paramSectionsScrollArea = QtWidgets.QScrollArea()
        self.paramSectionsScrollArea.setWidgetResizable(True)
        self.paramSectionsScrollArea.setWidget(self.paramSectionsContainer)
        paramLayout.addWidget(self.paramSectionsScrollArea)

        mainLayout.addWidget(paramGroupBox)

        # BlenderSubmission.py Section
        submissionGroupBox = QtWidgets.QGroupBox("BlenderSubmission.py 版本設定")
        submissionLayout = QtWidgets.QVBoxLayout()
        submissionGroupBox.setLayout(submissionLayout)

        # 新增版本按鈕
        addSubmissionVersionButton = QtWidgets.QPushButton("新增版本")
        addSubmissionVersionButton.clicked.connect(lambda: self.addSubmissionVersionSection())
        submissionLayout.addWidget(addSubmissionVersionButton)

        loadSubmissionButton = QtWidgets.QPushButton("讀取 BlenderSubmission.py 版本")
        loadSubmissionButton.clicked.connect(self.loadSubmissionFile)
        submissionLayout.addWidget(loadSubmissionButton)

        updateSubmissionButton = QtWidgets.QPushButton("更新 BlenderSubmission.py 版本設定")
        updateSubmissionButton.clicked.connect(self.updateSubmissionFile)
        submissionLayout.addWidget(updateSubmissionButton)

        # 用來放置所有 BlenderSubmission.py 版本區塊，加入滾動區域
        self.submissionSectionsContainer = QtWidgets.QWidget()
        self.submissionSectionsContainerLayout = QtWidgets.QVBoxLayout()
        self.submissionSectionsContainer.setLayout(self.submissionSectionsContainerLayout)
        self.submissionSectionsScrollArea = QtWidgets.QScrollArea()
        self.submissionSectionsScrollArea.setWidgetResizable(True)
        self.submissionSectionsScrollArea.setWidget(self.submissionSectionsContainer)
        submissionLayout.addWidget(self.submissionSectionsScrollArea)

        mainLayout.addWidget(submissionGroupBox)

        # User Information Display Section
        userInfoGroupBox = QtWidgets.QGroupBox("程式資訊")
        userInfoLayout = QtWidgets.QVBoxLayout()
        userInfoGroupBox.setLayout(userInfoLayout)

        nameLabel = QtWidgets.QLabel("Jed © | Xanthus Co., Inc.")
        userInfoLayout.addWidget(nameLabel)

        mainLayout.addWidget(userInfoGroupBox)

        # Window Settings
        self.setWindowTitle('Deadline_新增版本工具')
        self.setGeometry(1000, 550, 700, 600)
        self.show()

    def loadDefaultLocations(self):
        self.paramFilePathEdit.setText(r"\\192.168.2.237\DeadlineRepository10\plugins\Blender\Blender.param")
        self.submissionFilePathEdit.setText(r"\\192.168.2.237\DeadlineRepository10\scripts\Submission\BlenderSubmission.py")

    def selectParamFile(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "選擇 Blender.param 檔案", "", "Config Files (*.param);;All Files (*)")
        if filePath:
            self.paramFilePathEdit.setText(filePath)

    def selectSubmissionFile(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "選擇 BlenderSubmission.py 檔案", "", "Python Files (*.py);;All Files (*)")
        if filePath:
            self.submissionFilePathEdit.setText(filePath)

    # -------------------------------
    # Blender.param 部分
    # -------------------------------
    def addParamSection(self, version="", path=""):
        sectionWidget = QtWidgets.QWidget()
        sectionLayout = QtWidgets.QHBoxLayout()
        sectionWidget.setLayout(sectionLayout)

        versionInput = QtWidgets.QLineEdit()
        versionInput.setPlaceholderText("Blender 版本（例如：4.0.0）")
        versionInput.setText(version)

        pathInput = QtWidgets.QLineEdit()
        pathInput.setPlaceholderText("Blender 執行檔路徑")
        pathInput.setText(path)

        removeButton = QtWidgets.QPushButton("移除")
        removeButton.clicked.connect(lambda: self.removeParamSection(sectionWidget))

        sectionLayout.addWidget(versionInput)
        sectionLayout.addWidget(pathInput)
        sectionLayout.addWidget(removeButton)

        self.paramSectionsContainerLayout.addWidget(sectionWidget)
        self.paramSections.append((versionInput, pathInput))

    def removeParamSection(self, sectionWidget):
        version = sectionWidget.layout().itemAt(0).widget().text()
        self.paramSectionsContainerLayout.removeWidget(sectionWidget)
        sectionWidget.deleteLater()
        self.paramSections = [s for s in self.paramSections if s[0] != sectionWidget.layout().itemAt(0).widget()]

        # 同時從 Blender.param 檔案中移除對應區塊
        paramFilePath = self.paramFilePathEdit.text()
        if paramFilePath:
            config = configparser.ConfigParser()
            config.read(paramFilePath)
            section_name = f"Blender_{version}_RenderExecutable"
            if section_name in config.sections():
                config.remove_section(section_name)
                with open(paramFilePath, 'w') as configfile:
                    config.write(configfile)

    def loadParamFile(self):
        paramFilePath = self.paramFilePathEdit.text()
        if not paramFilePath:
            QtWidgets.QMessageBox.warning(self, "檔案錯誤", "請選擇一個有效的 Blender.param 檔案。")
            return

        config = configparser.ConfigParser()
        config.read(paramFilePath)

        # 清空目前的版本區塊
        while self.paramSectionsContainerLayout.count():
            child = self.paramSectionsContainerLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.paramSections = []

        # 讀取符合格式的區塊，並以新增區塊的方式加入 UI
        for section in config.sections():
            if section.startswith("Blender_") and section.endswith("_RenderExecutable"):
                parts = section.split("_")
                if len(parts) >= 3:
                    version = parts[1]
                    path = config[section].get("Default", "")
                    self.addParamSection(version, path)

    def updateParamFile(self):
        config = configparser.ConfigParser()
        config.optionxform = lambda option: option  # 避免 key 自動轉小寫

        paramFilePath = self.paramFilePathEdit.text()
        if not paramFilePath:
            QtWidgets.QMessageBox.warning(self, "檔案錯誤", "請選擇一個有效的 Blender.param 檔案。")
            return

        config.read(paramFilePath)

        for versionInput, pathInput in self.paramSections:
            version = versionInput.text()
            path = pathInput.text()
            if version and path:
                section_name = f"Blender_{version}_RenderExecutable"
                config[section_name] = {
                    'Type': 'multilinemultifilename',
                    'Label': f'Blender {version} Executable',
                    'Category': 'Render Executables',
                    'CategoryOrder': '0',
                    'Default': path,
                    'Description': 'The path to the Blender executable file used for rendering. Enter alternative paths on separate lines.'
                }

        with open(paramFilePath, 'w') as configfile:
            config.write(configfile)

    # -------------------------------
    # BlenderSubmission.py 部分
    # -------------------------------
    def addSubmissionVersionSection(self, version=""):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        widget.setLayout(layout)

        versionInput = QtWidgets.QLineEdit()
        versionInput.setPlaceholderText("Blender 版本")
        versionInput.setText(version)

        removeButton = QtWidgets.QPushButton("移除")
        removeButton.clicked.connect(lambda: self.removeSubmissionVersionSection(widget))

        layout.addWidget(versionInput)
        layout.addWidget(removeButton)

        self.submissionSectionsContainerLayout.addWidget(widget)
        self.submissionSections.append(versionInput)

    def removeSubmissionVersionSection(self, widget):
        self.submissionSectionsContainerLayout.removeWidget(widget)
        widget.deleteLater()
        # 移除對應的 QLineEdit
        version_input = widget.layout().itemAt(0).widget()
        self.submissionSections = [v for v in self.submissionSections if v != version_input]

    def loadSubmissionFile(self):
        submissionFilePath = self.submissionFilePathEdit.text()
        if not submissionFilePath:
            QtWidgets.QMessageBox.warning(self, "檔案錯誤", "請選擇一個有效的 BlenderSubmission.py 檔案。")
            return

        try:
            with open(submissionFilePath, 'r') as file:
                content = file.read()

            match = re.search(r'scriptDialog.AddComboControlToGrid\("BlenderVersion", "ComboControl",\s*"[^"]+",\s*\((.*?)\)\s*,', content, re.DOTALL)
            if match:
                versions_str = match.group(1)
                versions = [v.strip().strip('"') for v in versions_str.split(',') if v.strip().strip('"')]

                # 清空目前的版本區塊
                while self.submissionSectionsContainerLayout.count():
                    child = self.submissionSectionsContainerLayout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
                self.submissionSections = []

                # 加入讀取到的版本
                for version in versions:
                    self.addSubmissionVersionSection(version)
            else:
                QtWidgets.QMessageBox.warning(self, "資訊", "找不到版本資訊。")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "錯誤", str(e))

    def updateSubmissionFile(self):
        submissionFilePath = self.submissionFilePathEdit.text()
        if not submissionFilePath:
            QtWidgets.QMessageBox.warning(self, "檔案錯誤", "請選擇一個有效的 BlenderSubmission.py 檔案。")
            return

        # 從各版本區塊中取得版本字串
        versions = [v.text().strip() for v in self.submissionSections if v.text().strip()]
        if not versions:
            QtWidgets.QMessageBox.warning(self, "輸入錯誤", "請輸入至少一個版本。")
            return

        try:
            with open(submissionFilePath, 'r') as file:
                content = file.read()

            # 更新 ComboControl 中的 Blender 版本字串
            new_versions_str = ', '.join(f'"{v}"' for v in versions)
            updated_content = re.sub(
                r'(scriptDialog.AddComboControlToGrid\("BlenderVersion", "ComboControl",\s*"[^"]+",\s*\()(.*?)(\)\s*,)',
                lambda match: f'{match.group(1)}{new_versions_str}{match.group(3)}',
                content, flags=re.DOTALL
            )

            with open(submissionFilePath, 'w') as file:
                file.write(updated_content)

            QtWidgets.QMessageBox.information(self, "成功", "BlenderSubmission.py 更新成功。")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "錯誤", str(e))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = BlenderConfigTool()
    sys.exit(app.exec_())
