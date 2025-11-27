from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget

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

    # Adding events
    self.newGameButton.clicked.connect(lambda: self.switch_page(1))
    self.backButton.clicked.connect(lambda: self.switch_page(0))
    self.quitButton.clicked.connect(self.quit_game)
    self.switch_page(0)
  
  def quit_game(self):
      """
      @def quit_game
      @brief Quit the application
      """
      print("Quit !")
      self.close()

  def switch_page(self, num_page=0):
      """
      @def switch_page
      @brief Switch to the specified page
      @param num_page : page number to switch to
      """

      self.stackedWidget.setCurrentIndex(num_page)
      print(f"Switched to page {num_page}")


