from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

"""
@class View
@brief Main Window class
"""
class View(QMainWindow) :
  """
  Main Window class
  """
  def __init__(self):
    """
    @def __init__
    @brief Constructor
    """
    super().__init__()

    uic.loadUi("ui/test.ui", self)

    self.quitButton.clicked.connect(self.quit_game)
  
  def quit_game(self):
      """
      @def quit_game
      @brief Quit the application
      """
      print("Quit !")
      self.close()

