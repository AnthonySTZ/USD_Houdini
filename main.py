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
        

path = "A:\\Programming\\USD_Houdini\\open_usd.usda"
with Usd.StageCacheContext(UsdUtils.StageCache.Get()):
    stage = Usd.Stage.Open(path)

window = Widget(stage)
window.setWindowTitle("USD Viewer")
window.resize(QtCore.QSize(750, 750))
window.show()

window.view.updateView(resetCam=True, forceComputeBBox=True)