import time, os, sys, pdb
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QCheckBox, QHBoxLayout, QVBoxLayout, QAction
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox
from PyQt5.Qt import Qt

class Gui(QMainWindow):

    class todo_item(QWidget):

        def __init__(self):
            super().__init__()
            # Create Checkbox
            self.checkbox = QCheckBox()

            # Create Label
            self.label = QLabel()

            # Create Layout
            layout = QHBoxLayout()

            # Add checkbox and label to layout
            layout.addWidget(self.checkbox)
            layout.addWidget(self.label)

            layout.setAlignment(Qt.AlignLeft)

            # Set layout
            self.setLayout(layout)

        def set_text(self, text):
            self.label.setText(text)

        def is_checked(self):
            return self.checkbox.isChecked()

        def text(self):
            return self.label.text()

    def __init__(self):
        super().__init__()
        self.todos = []
        self.init_gui()
        self.show()

    def init_gui(self):
        # Create Main Layout
        self.main_layout = QVBoxLayout()

        # Add menu bar items
        bar = self.menuBar()
        todos = bar.addMenu("Todos")

        add_action = QAction("&Add", self)
        add_action.setShortcut("Ctrl+A")

        delete_action = QAction("&Delete", self)
        delete_action.setShortcut("Ctrl+D")

        edit_action = QAction("&Edit")
        edit_action.setShortcut("Ctrl+E")

        todos.addAction(add_action)
        todos.addAction(delete_action)
        todos.addAction(edit_action)

        add_action.triggered.connect(self.add_todo)
        edit_action.triggered.connect(self.edit_todo)
        delete_action.triggered.connect(self.delete_todos)

        # Create placeholder central widget
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)

        # Set layout to main layout
        self.main_layout.setAlignment(Qt.AlignTop)
        self.setCentralWidget(central_widget)

    def add_todo(self):
        # Create new todo item
        new_todo = self.todo_item()
        # Open Todo Dialog
        todo_text, ok = QInputDialog.getText(self, "Get text", "Todo:", QLineEdit.Normal, "")

        if not ok:
            return
        new_todo.set_text(todo_text)
        self.todos.append(new_todo)
        self.main_layout.addWidget(new_todo)

    def edit_todo(self):
        pass

    def delete_todos(self):
        todos_to_delete = []
        if self.main_layout.count() < 1:
            QMessageBox.information(self, "Todo Delete", "No Todos Selected")
            return

        for i in range(len(self.todos)):
            if self.todos[i].is_checked():
                todos_to_delete.append(i)

        if len(todos_to_delete) < 1:
            return

        message = "\n\t-" + "\n\t-".join([self.todos[i].text() for i in todos_to_delete])
        ok = QMessageBox.question(self, "Todo Delete", "Delete Selected Items?" + message)

        if ok == QMessageBox.Yes:
            for i in todos_to_delete:
                self.todos.pop(i)
                item = self.main_layout.takeAt(i)
                item.widget().deleteLater()




if __name__ == '__main__':
    app = QApplication([])
    window = Gui()
    sys.exit(app.exec())
