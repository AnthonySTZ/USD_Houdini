import sys
from PySide2 import QtGui, QtCore, QtWidgets
from pxr import Usd, UsdUtils, Sdf
from pxr.Usdviewq.stageView import StageView

class PreviewUSDWidget(QtWidgets.QWidget):
    def __init__(self, stage=None):
        super(PreviewUSDWidget, self).__init__()
        self.model = StageView.DefaultDataModel()
        
        self.view = StageView(dataModel=self.model)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.setContentsMargins(0, 0, 0, 0)
        
        if stage:
            self.setStage(stage)
        
    def setStage(self, stage):
        self.model.stage = stage
                              
    def closeEvent(self, event):        
        # Ensure to close the renderer to avoid GlfPostPendingGLErrors
        self.view.closeRenderer()
        
class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        
        self.show_ui()


    def show_ui(self):
        self.setWindowTitle("USD Houdini")

        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        
        main_layout = QtWidgets.QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        left_widget = QtWidgets.QWidget()
        right_widget = QtWidgets.QWidget()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)
        
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
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

        file_list_widget = QtWidgets.QWidget()
        file_list_layout = QtWidgets.QVBoxLayout(file_list_widget)
        file_list_layout.setContentsMargins(0, 0, 0, 0)

        self.file_list = QtWidgets.QListWidget()
        file_list_layout.addWidget(self.file_list)
        left_layout.addWidget(file_list_widget)


        right_layout = QtWidgets.QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        self.usd_tree = QtWidgets.QTreeWidget()
        right_layout.addWidget(self.usd_tree)
        
        self.resize(QtCore.QSize(750, 750))


path = "A:\\Programming\\USD_Houdini\\open_usd.usda"
with Usd.StageCacheContext(UsdUtils.StageCache.Get()):
    stage = Usd.Stage.Open(path)

# window = Widget(stage)
# window.setWindowTitle("USD Viewer")
# window.resize(QtCore.QSize(750, 750))
# window.show()

# window.view.updateView(resetCam=True, forceComputeBBox=True)

window = Window()
window.show()