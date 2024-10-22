import sys
from PySide2 import QtGui, QtCore, QtWidgets
from pxr import Usd, UsdUtils, Sdf
from pxr.Usdviewq.stageView import StageView

class Widget(QtWidgets.QWidget):
    def __init__(self, stage=None):
        super(Widget, self).__init__()
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
        
        layout = QtWidgets.QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        buttons_widget = QtWidgets.QWidget()
        button_widget_layout = QtWidgets.QVBoxLayout(buttons_widget)
        button_widget_layout.setContentsMargins(50, 10, 50, 0)

        self.select_folder_btn = QtWidgets.QPushButton("Select USD Folder")
        button_widget_layout.addWidget(self.select_folder_btn)
        self.preview_usd_btn = QtWidgets.QPushButton("Preview USD")
        button_widget_layout.addWidget(self.preview_usd_btn)
        self.import_btn = QtWidgets.QPushButton("Import To Houdini")
        button_widget_layout.addWidget(self.import_btn)

        layout.addWidget(buttons_widget)

        file_list_widget = QtWidgets.QWidget()
        file_list_layout = QtWidgets.QVBoxLayout(file_list_widget)
        file_list_layout.setContentsMargins(50, 10, 50, 10)

        self.file_list = QtWidgets.QListWidget()
        file_list_layout.addWidget(self.file_list)
        layout.addWidget(file_list_widget)
        
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