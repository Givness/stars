from PyQt6.QtWidgets import QMainWindow, QTabWidget
from gui.knowledge_editor import KnowledgeEditorWidget
from gui.knowledge_viewer import KnowledgeViewerWidget
from gui.data_input import DataInputWidget
from logic.knowledge_base import KnowledgeBase

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Классификация звёзд")
        self.resize(800, 600)

        self.kb = KnowledgeBase("data/knowledge_base.json")

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.knowledge_editor_tab = KnowledgeEditorWidget(self.kb)
        self.knowledge_viewer_tab = KnowledgeViewerWidget(self.kb)
        self.data_input_tab = DataInputWidget(self.kb)

        self.tabs.addTab(self.knowledge_editor_tab, "Редактор знаний")
        self.tabs.addTab(self.knowledge_viewer_tab, "Просмотр базы знаний")
        self.tabs.addTab(self.data_input_tab, "Ввод данных")

        self.tabs.currentChanged.connect(self.refresh_current_tab)

    def refresh_current_tab(self, index):
        widget = self.tabs.widget(index)
        if hasattr(widget, "refresh"):
            widget.refresh()