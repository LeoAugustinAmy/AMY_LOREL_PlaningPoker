from PyQt5.QtWidgets import QApplication
from views.View import View

app = QApplication([])
w = View()
w.show()
app.exec()