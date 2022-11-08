import sys
from tkinter.simpledialog import *
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import QUESTION
import cv2
from PySide6.QtGui import QAction, QImage, QPixmap
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QMainWindow, 
QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog
)
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Photoshop")

        #메뉴바 만들기
        self.menu = self.menuBar()
        self.menu_file = self.menu.addMenu("파일")
        file_open = QAction("이미지 열기", self, triggered = self.show_File_Dialog)
        second_file_open = QAction("합칠 이미지 열기", self, triggered = self.import_second_image)
        exit = QAction("나가기", self, triggered= quit)
        self.menu_file.addAction(file_open)
        self.menu_file.addAction(second_file_open)
        self.menu_file.addAction(exit)
        self.menu_file = self.menu.addMenu("편집")
        refresh = QAction("새로고침", self, triggered = self.clear_label)
        inverted = QAction("색 반전", self, triggered = self.inverted)
        blured = QAction("흐림 효과", self, triggered = self.blured)
        mask = QAction("마스크", self, triggered = self.mask)
        merge = QAction("이미지 합치기", self, triggered = self.imagemerge)
        self.menu_file.addAction(refresh)
        self.menu_file.addAction(inverted)
        self.menu_file.addAction(blured)
        self.menu_file.addAction(mask)
        self.menu_file.addAction(merge)
        self.menu_file = self.menu.addMenu("회전")
        rotate90 = QAction("시계방향 회전", self, triggered = self.rotate90)
        reverse90 = QAction("반시계 회전", self, triggered = self.reverse_rotate90)
        flip_img = QAction("좌우 반전", self, triggered = self.flip_image)
        self.menu_file.addAction(rotate90)
        self.menu_file.addAction(reverse90)
        self.menu_file.addAction(flip_img)



        #메인화면 레이아웃
        main_layout = QHBoxLayout()

        #사이드바 메뉴버튼
        #sidebar = QVBoxLayout()
        #button1 = QPushButton("회전")
        #button2 = QPushButton("역회전")
        #button3 = QPushButton("듀오 톤")
        #button4 = QPushButton("합체")
        #button1.clicked.connect(self.rotate90)
        #button2.clicked.connect(self.reverse_rotate90)
        #button3.clicked.connect(self.blured)
        #button4.clicked.connect(self.imagemerge)
        #sidebar.addWidget(button1)
        #sidebar.addWidget(button2)
        #sidebar.addWidget(button3)
        #sidebar.addWidget(button4)

        #main_layout.addLayout(sidebar)
        
        height = 640
        width = 480

        self.label1 = QLabel(self)
        self.label1.setFixedSize(height, width)
        main_layout.addWidget(self.label1)

        self.label2 = QLabel(self)
        self.label2.setFixedSize(height, width)
        main_layout.addWidget(self.label2)

        self.label3 = QLabel(self)
        self.label3.setFixedSize(height, width)
        main_layout.addWidget(self.label3)

        widget = QWidget(self)
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def show_File_Dialog(self):     #이미지 열기
        file_name = QFileDialog.getOpenFileName(self, "이미지 열기", "./")
        self.image = cv2.imread(file_name[0])
        main_h, main_w, _ = self.image.shape
        bytes_per_line = 3 * main_w
        image = QImage(self.image.data, main_w, main_h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        image = image.scaledToHeight(640)
        image = image.scaledToWidth(480)
        pixmap = QPixmap(image)    
        self.label1.setPixmap(pixmap)
        

    def import_second_image(self):     #두번째 이미지 열기
        file_name2 = QFileDialog.getOpenFileName(self, "이미지 열기", "./")
        self.image2 = cv2.imread(file_name2[0])
        h, w, _ = self.image2.shape
        bytes_per_line = 3 * w
        image2 = QImage(self.image2.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        image2 = image2.scaledToHeight(640)
        image2 = image2.scaledToWidth(480)
        pixmap = QPixmap(image2)    
        self.label3.setPixmap(pixmap)
    

    def save_File(self):
        file_save = cv2.imwrite("new_Image", self.image, params=None)

    def flip_image(self):   #이미지 좌우 반전
        image = cv2.flip(self.image, 1)
        h, w, _ = image.shape
        bytes_per_line = 3 * w
        image = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        image = image.scaledToHeight(640)
        image = image.scaledToWidth(480)
        pixmap = QPixmap(image)
        self.label2.setPixmap(pixmap)

    def clear_label(self):  #지우기(초기화)
        self.label1.clear()
        self.label2.clear()
        self.label3.clear()

    def rotate90(self):     #시계 방향으로 90도
        image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
        h, w, _ = image.shape
        bytes_per_line = 3 * w
        image = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        image = image.scaledToHeight(640)
        image = image.scaledToWidth(480)
        pixmap = QPixmap(image)
        self.label2.setPixmap(pixmap)

    def reverse_rotate90(self):     #반시계 방향으로 90도
        image = cv2.rotate(self.image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        h, w, _ = image.shape
        bytes_per_line = 3 * w
        image = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        image = image.scaledToHeight(640)
        image = image.scaledToWidth(480)
        pixmap = QPixmap(image)
        self.label2.setPixmap(pixmap)
        
    def inverted(self):     #색반전
        h, w, _ = self.image.shape
        bytes_per_line = 3 * w
        image = QImage(self.image.data, w, h, bytes_per_line, QImage.Format_BGR888
        ).rgbSwapped()
        image = image.scaledToHeight(640)
        image = image.scaledToWidth(480)
        pixmap = QPixmap(image)
        self.label2.setPixmap(pixmap)

    def blured(self):       #이미지 흐릿하게
        h, w, _ = self.image.shape
        bytes_per_line = 3 * w
        kernel = np.full((5, 5), 0.04)
        blured = cv2.filter2D(self.image, -1, kernel)
        image = QImage(blured.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        image = image.scaledToHeight(640)
        image = image.scaledToWidth(480)
        pixmap = QPixmap(image)
        self.label2.setPixmap(pixmap)

    def mask(self):     #이미지에 마스크 입히기
        h, w, _ = self.image.shape
        bytes_per_line = 3 * w
        mask = np.zeros_like(self.image)
        cv2.circle(self.image, (w//2, h//2), w//2, (0,0,0), 175)
        masked_image = cv2.bitwise_and(self.image, mask)
        masked_image = QImage(self.image.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        masked_image = masked_image.scaledToHeight(640)
        masked_image = masked_image.scaledToWidth(480)
        pixmap = QPixmap(masked_image)
        self.label2.setPixmap(pixmap)


    def imagemerge(self):       #이미지 합치기
        alpha = 0.5
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        image2 = cv2.cvtColor(self.image2, cv2.COLOR_BGR2RGB)
        h, w = image.shape[:2]
        bytes_per_line = 3 * w
        image2 = cv2.resize(image2, (image.shape[1],image.shape[0]))
        mergeimage = image * alpha + image2 * (1-alpha)
        mergeimage = mergeimage.astype(np.uint8)
        mergeimage = QImage(mergeimage.data, w, h, bytes_per_line, QImage.Format_BGR888).rgbSwapped()
        pixmap = QPixmap(mergeimage)
        self.label3.setPixmap(pixmap)

        





if __name__ == "__main__":
    app=QApplication()
    window=MainWindow()
    window.show()
    sys.exit(app.exec())