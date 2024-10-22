import sys
from PySide2 import QtGui, QtCore, QtWidgets
from pxr import Usd, UsdUtils, Sdf
from pxr.Usdviewq.stageView import StageView
import os


class PreviewUSDWidget(QtWidgets.QWidget):
    def __init__(self, stage=None) -> None:
        super(PreviewUSDWidget, self).__init__()
        self.model = StageView.DefaultDataModel()

        self.view = StageView(dataModel=self.model)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.setContentsMargins(0, 0, 0, 0)

        if stage:
            self.setStage(stage)

    def setStage(self, stage) -> None:
        self.model.stage = stage

    def closeEvent(self, event) -> None:
        # Ensure to close the renderer to avoid GlfPostPendingGLErrors
        self.view.closeRenderer()


class Window(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(Window, self).__init__()

        self.folder_path = ""
        self.usd_window = None

        self.show_ui()
        self.init_ui_functionnals()

    def show_ui(self) -> None:
        self.setWindowTitle("USD Houdini")

        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QtWidgets.QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        left_widget = QtWidgets.QWidget()
        right_widget = QtWidgets.QWidget()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)

        # Left Layout
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(5)

        buttons_widget = QtWidgets.QWidget()
        button_widget_layout = QtWidgets.QVBoxLayout(buttons_widget)
        button_widget_layout.setContentsMargins(0, 0, 0, 0)

        self.folder_path_te = QtWidgets.QTextEdit()
        self.folder_path_te.setReadOnly(True)
        self.folder_path_te.setMaximumHeight(30)
        self.folder_path_te.setAlignment(QtCore.Qt.AlignBottom)
        self.folder_path_te.setContentsMargins(0, 0, 0, 0)
        self.folder_path_te.setPlaceholderText("folder path...")
        button_widget_layout.addWidget(self.folder_path_te)

        self.select_folder_btn = QtWidgets.QPushButton("Select USD Folder")
        button_widget_layout.addWidget(self.select_folder_btn)
        self.preview_usd_btn = QtWidgets.QPushButton("Preview USD")
        button_widget_layout.addWidget(self.preview_usd_btn)
        self.import_btn = QtWidgets.QPushButton("Import To Houdini")
        button_widget_layout.addWidget(self.import_btn)

        left_layout.addWidget(buttons_widget)

        self.file_list = QtWidgets.QListWidget()
        self.file_list.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self.file_list.setStyleSheet("font-size: 10pt;")
        self.file_list.setFocusPolicy(QtCore.Qt.NoFocus)
        left_layout.addWidget(self.file_list, stretch=1)

        # Right Layout
        right_layout = QtWidgets.QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        self.usd_tree = QtWidgets.QTreeWidget()
        # right_layout.addWidget(self.usd_tree)

        self.resize(QtCore.QSize(750, 750))

    def init_ui_functionnals(self) -> None:
        self.select_folder_btn.clicked.connect(self.select_folder)
        self.preview_usd_btn.clicked.connect(self.preview_usd)

    def select_folder(self) -> None:
        self.folder_path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select a USD Folder"
        )
        self.folder_path_te.setText(self.folder_path)
        self.update_file_list()

    def update_file_list(self) -> None:
        if not os.path.exists(self.folder_path):
            return

        self.file_list.clear()
        for file in os.listdir(self.folder_path):
            if not os.path.isfile(os.path.join(self.folder_path, file)):
                continue
            if (
                ".usd" in file[-6:]
            ):  # Check for all files that end with ".usd", ".usda", etc...
                self.file_list.addItem(file)

    def preview_usd(self) -> None:
        if self.file_list.currentItem() is None:
            print("Please select a file")
            return

        selected_file = self.folder_path + "/" + self.file_list.currentItem().text()

        if not os.path.exists(selected_file):
            print("Please select a correct file")
            return

        with Usd.StageCacheContext(UsdUtils.StageCache.Get()):
            stage = Usd.Stage.Open(selected_file)

        self.usd_window = PreviewUSDWidget(stage)
        self.usd_window.setWindowTitle("USD Viewer")
        self.usd_window.resize(QtCore.QSize(750, 750))
        self.usd_window.show()

        self.usd_window.view.updateView(resetCam=True, forceComputeBBox=True)

    def closeEvent(self, event) -> None:
        if self.usd_window is not None:
            # Ensure to close the renderer to avoid GlfPostPendingGLErrors
            self.usd_window.close()


window = Window()
window.show()
