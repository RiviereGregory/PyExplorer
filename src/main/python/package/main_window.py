from PySide2 import QtWidgets, QtCore


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.setWindowTitle("PyExplorer")
        self.setup_ui()
        self.create_file_model()

    def setup_ui(self):
        self.create_widgets()
        self.create_layouts()
        self.modify_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.toolbar = QtWidgets.QToolBar()
        self.tree_view = QtWidgets.QTreeView()
        self.list_view = QtWidgets.QListView()
        self.sld_iconSize = QtWidgets.QSlider()
        self.main_widget = QtWidgets.QWidget()

    def modify_widgets(self):
        css_file = self.ctx.get_resource("style.css")
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())
        # Modification de la vue dans listView pour afficher des icone au lieu de list
        self.list_view.setViewMode(QtWidgets.QListView.IconMode)
        self.list_view.setUniformItemSizes(True)
        self.list_view.setIconSize(QtCore.QSize(48, 48))
        # Ajout du trie
        self.tree_view.setSortingEnabled(True)
        # Ajout de la couleur alterné des ligne
        self.tree_view.setAlternatingRowColors(True)
        # Modication de l'entête pour s'adapter
        self.tree_view.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

    def create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout(self.main_widget)

    def add_widgets_to_layouts(self):
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self.setCentralWidget(self.main_widget)
        self.main_layout.addWidget(self.tree_view)
        self.main_layout.addWidget(self.list_view)
        self.main_layout.addWidget(self.sld_iconSize)

    def setup_connections(self):
        self.tree_view.clicked.connect(self.treeview_clicked)
        self.list_view.clicked.connect(self.listview_clicked)
        self.list_view.doubleClicked.connect(self.listview_double_clicked)

    def create_file_model(self):
        self.model = QtWidgets.QFileSystemModel()
        root_path = QtCore.QDir.rootPath()
        self.model.setRootPath(root_path)
        self.tree_view.setModel(self.model)
        self.list_view.setModel(self.model)
        self.list_view.setRootIndex(self.model.index(root_path))
        self.tree_view.setRootIndex(self.model.index(root_path))

    def treeview_clicked(self, index):
        if self.model.isDir(index):
            self.list_view.setRootIndex(index)
        else:
            self.list_view.setRootIndex(index.parent())

    def listview_clicked(self, index):
        self.tree_view.selectionModel().setCurrentIndex(index, QtCore.QItemSelectionModel.ClearAndSelect)

    def listview_double_clicked(self, index):
        self.list_view.setRootIndex(index)
