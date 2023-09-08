# -*- encoding: utf-8 -*-
import time
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QPushButton, QPlainTextEdit, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap


class HeightFitImage(QLabel):
    
    def setPixmap(self, qPixmap):
        qPixmap = qPixmap.scaled(1, self.height(), Qt.KeepAspectRatioByExpanding)
        super().setPixmap(qPixmap)
    
    def setImage(self, qImage):
        self.setPixmap(QPixmap(qImage))

    def setMatrix(self, numpyArray, imageFormat = QImage.Format_RGB888):
        qImage = QImage(
            numpyArray.data,
            numpyArray.shape[1], numpyArray.shape[0],
            imageFormat
        )
        self.setImage(qImage)

    def load(self, imagePath):
        self.setImage(QImage(imagePath))


class ConsoleWidget(QPlainTextEdit):

    def __init__(self, parent=None):
        """A log console similar to javascript. Inherits from QPlainTextEdit"""
        super().__init__(parent)
        self.setObjectName('console')
        self.setReadOnly(True)
    
    def label_log(self, label_text='', label_color='', message='', escape_html=True):
        """Show a log with label enclosed by '[]' and the time"""
        times = time.localtime()
        if escape_html:
            label_text = self.escape_html(label_text)
            message = self.escape_html(message)
            
        self.appendHtml( \
            '<span style="color:#909090;">[<span style="color:%s;">%s</span>]'\
            ' %d-%02d-%02d %02d:%02d:%02d</span>' \
            '&nbsp; %s' % ( \
                label_color, label_text, \
                times.tm_year, times.tm_mon, times.tm_mday, times.tm_hour, times.tm_min, times.tm_sec, \
                message \
            ) \
        )

    def log(self, message):
        """Print plain text on console. If message is not a string, it will be convert to string"""
        self.appendPlainText(message.__str__())

    def error(self, message, escape_html=True):
        self.label_log('ERROR!', '#FF0080', message, escape_html)
    
    def warn(self, message, escape_html=True):
        self.label_log(' WARN ', '#FF8200', message, escape_html)
    
    def info(self, message, escape_html=True):
        self.label_log(' INFO ', '#3789FF', message, escape_html)
    
    def ok(self, message, escape_html=True):
        self.label_log('  OK  ', '#72DC15', message, escape_html)

    # error: #FF00A7, warn: #FF8200, info: #3789FF, ok: #72DC15
    # error: #FF4060, warn: #FF8200, info: #3789FF, ok: #21D49A

    def escape_html(self, html_str):
        html_str = html_str.replace('<', '&lt;')
        html_str = html_str.replace('>', '&gt;')
        html_str.replace('&', '&amp;')
        html_str = html_str.replace('  ', '&nbsp;&nbsp;')
        return html_str.replace('\n', '<br/>')



app = QApplication([])
window = QWidget()

main_area = QWidget()
video = HeightFitImage()
console = ConsoleWidget()

side_bar = QWidget()
logo = HeightFitImage()
message_icon = QLabel()
message_text = QLabel()
student_name = QLabel()
student_id = QLabel()
stored_photo = HeightFitImage()
captured_photo = HeightFitImage()
similarity = QLabel()
capture_button = QPushButton("Capture")

# Get the size of em length unit (equal to font size) in pixel
em = window.fontInfo().pixelSize()


def init():
    set_layout()
    set_size()
    set_theme()
    window.show()



def set_layout():
    # Window Layout
    window_layout = QHBoxLayout(window)

    # Main area layout
    main_area_layout = QVBoxLayout(main_area)
    video.setObjectName('photo')
    main_area_layout.addWidget(video)
    main_area_layout.addWidget(console)

    # Side_bar Layout
    #Logo Group
    side_bar_layout = QVBoxLayout(side_bar)
    side_bar_layout.addWidget(logo)
    side_bar_layout.addSpacing(2 * em)
    #main_area_layout.addSpacerItem(group_spacing)
    # Student info group
    stored_photo.setObjectName('photo')
    side_bar_layout.addWidget(stored_photo)
    student_name.setObjectName('mainItem')
    side_bar_layout.addWidget(student_name)
    side_bar_layout.addWidget(student_id)
    side_bar_layout.addSpacing(2 * em)
    # Photo group
    side_bar_layout.addWidget(QLabel('Captured Photo'))
    captured_photo.setObjectName('photo')
    side_bar_layout.addWidget(captured_photo)
    side_bar_layout.addWidget(QLabel("Similarity"))
    similarity.setObjectName('mainItem')
    side_bar_layout.addWidget(similarity)
    side_bar_layout.addSpacing(2 * em)
    # Button group
    side_bar_layout.addWidget(capture_button)
    #Bottom Margin
    side_bar_layout.addSpacerItem( \
        QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding) \
    )

    # Window layout
    window_layout.addWidget(main_area)
    window_layout.addWidget(side_bar)



def set_theme(theme_name = 'vs_dark'):
    path = 'theme/' + theme_name + '.css'
    style_sheet = None
    try:
        style_sheet = open(path, 'r')
    except:
        console.warn('UI Init Error (ui.py): Cannot load theme stylesheet ' + path)
        try:
            style_sheet = open('theme/vscode_dark.css', 'r')
        except:
            console.error('UI Init Error (ui.py): Cannot load basic theme stylesheet theme/straid_dark.css')
        
    if not style_sheet is None:
        style_string = style_sheet.read()
        window.setStyleSheet(style_string)
        style_sheet.close()

        theme_type = theme_name[-6:-1] + theme_name[-1]
        if theme_type == '_light':
            logo.load('icon/logo_light.png')
        else:
            logo.load('icon/logo_dark.png')




def set_size():
    width_fit_height = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    width_fit_height.setWidthForHeight(True)

    side_bar.layout().setSpacing(0.8 * em)
    side_bar.setFixedWidth(20 * em)
    console.setFixedHeight(12 * em)
    window.setMinimumSize(70 * em, 50 * em)

    stored_photo.setFixedHeight(8 * em)
    stored_photo.setSizePolicy(width_fit_height)
    captured_photo.setFixedHeight(8 * em)
    captured_photo.setSizePolicy(width_fit_height)
    logo.setFixedHeight(5 * em)
    logo.setSizePolicy(width_fit_height)
