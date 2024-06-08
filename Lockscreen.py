from PyQt5 import QtWidgets, QtGui, QtCore
import pygame
import pygame.freetype
import sys
import keyboard

class BlackScreen(QtWidgets.QWidget):
    def __init__(self, screen):
        super().__init__()
        self.setWindowTitle('Secondary Locker')
        self.setGeometry(screen.geometry())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("background-color:black;")
        self.showFullScreen()

def create_window():
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    
    icon = pygame.image.load(r'C:\Lockscreen\images\title.png')
    pygame.display.set_icon(icon)

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

    screen.fill((0, 0, 0))

    image = pygame.image.load(r'C:\Lockscreen\images\lock.png')
    image_rect = image.get_rect()
    image_rect.topleft = (50, 50)
    screen.blit(image, image_rect)
    
    pygame.display.set_caption('Primary Locker')

    font = pygame.freetype.Font(None, 24)
    text_surface, rect = font.render("This PC is currently locked.", (255, 0, 0))
    
    text_x = image_rect.right + 10
    text_y = image_rect.centery - (rect.height // 2)
    screen.blit(text_surface, (text_x, text_y))
    
    trademark_text = "Polar Locker © Pourta Services. All Rights Reserved."
    trademark_surface, trademark_rect = font.render(trademark_text, (255, 255, 255))
    
    trademark_x = screen_width - trademark_surface.get_width() - 10 
    trademark_y = screen_height - trademark_surface.get_height() - 10
    screen.blit(trademark_surface, (trademark_x, trademark_y))

    pygame.display.flip()

def main():
    pygame.init()

    keyboard.block_key('windows')
    keyboard.add_hotkey('alt+tab', lambda: None, suppress=True)

    app = QtWidgets.QApplication(sys.argv)
    msgBox = QtWidgets.QMessageBox()
    msgBox.setIcon(QtWidgets.QMessageBox.Information)
    msgBox.setText(r"Do you want to run this program? This program disables alt+tab and is a fullscreen exclusive app. You can also use Win+L to lock your PC. If you want to cancel and terminate the process, click Cancel. If you want to continue, click Ok.")
    msgBox.setWindowTitle("Lockscreen")
    msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
    
    returnValue = msgBox.exec()
    if returnValue == QtWidgets.QMessageBox.Ok:
        create_window()
        screens = app.screens()
        for screen in screens[1:]:
            window = BlackScreen(screen)
            window.show()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    create_window()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_INSERT:
                        keyboard.unblock_key('windows')
                        keyboard.remove_hotkey('alt+tab')
                        pygame.quit()
                        sys.exit()
    else:
        sys.exit()

if __name__ == "__main__":
    main()