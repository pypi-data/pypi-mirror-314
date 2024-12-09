from PySide6.QtGui import QTextCharFormat, QBrush, QColor, QFont


GREEN_COLOR_1 = '#739072'
BLUE_COLOR_1 = '#596FB7'
YELLOW_COLOR_1 = '#F3CA52'

FONT_PURE = """
    font-family: 'Microsoft YaHei';
"""

LINEEIDT_FONT = """
    font-family: 'Microsoft YaHei;
    font-size: 12px;
"""

BUTTON_STYLE = """
            QPushButton {
                font-family: "Microsoft YaHei";
                background-color: #7895B2;
                border: 2px solid #7895B2;
                color: #FFFFFF;
            }

            QPushButton:hover {
                font-family: "Microsoft YaHei";
                background-color: #9BB0C1;
                border: 2px solid #9BB0C1;
            }

            QPushButton:disabled {
                font-family: "Microsoft YaHei";
                background-color: #d4dbe4;
                border: 2px solid #d4dbe4;
                color: #A0A0A0;
            }

            QPushButton:pressed {
                font-family: "Microsoft YaHei";
                border: 4px solid #5a7c9d;
            }
        """

BUTTON_STYLE_ORANGE = """
            QPushButton {
                font-family: "Microsoft YaHei";
                background-color: #ED9455;
                border: 2px solid #ED9455;
                color: #FFFFFF;
            }

            QPushButton:hover {
                font-family: "Microsoft YaHei";
                background-color: #FFBB70;
                border: 2px solid #FFBB70;
            }

            QPushButton:disabled {
                font-family: "Microsoft YaHei";
                background-color: #f7ceb1;
                border: 2px solid #f7ceb1;
                color: #A0A0A0;
            }

            QPushButton:pressed {
                font-family: "Microsoft YaHei";
                border: 2px solid #de6a18;
            }
        """

BUTTON_STYLE_ORANGE_TRANSPARENT = """
            QPushButton {
                font-family: "Microsoft YaHei";
                background-color: transparent; /* 修改为透明背景 */
                border: 2px solid #ED9455;
                color: #ED9455; /* 修改为按钮文字的颜色 */
            }

            QPushButton:hover {
                font-family: "Microsoft YaHei";
                background-color: transparent; /* 修改为透明背景 */
                border: 2px solid #FFBB70;
                color: #FFBB70; /* 修改为按钮文字的颜色 */
            }

            QPushButton:disabled {
                font-family: "Microsoft YaHei";
                background-color: transparent; /* 修改为透明背景 */
                border: 2px solid #f7ceb1;
                color: #f7ceb1; /* 修改为按钮文字的颜色 */
            }

            QPushButton:pressed {
                font-family: "Microsoft YaHei";
                border: 2px solid #de6a18;
            }
        """

BUTTON_STYLE_GREEN = """
            QPushButton {
                font-family: "Microsoft YaHei";
                background-color: #739072;
                border: 2px solid #739072;
                color: #FFFFFF;
            }

            QPushButton:hover {
                font-family: "Microsoft YaHei";
                background-color: #86A789;
                border: 2px solid #86A789;
            }

            QPushButton:disabled {
                font-family: "Microsoft YaHei";
                background-color: #E7F0E2;
                border: 2px solid #E7F0E2;
                color: #A0A0A0;
            }

            QPushButton:pressed {
                font-family: "Microsoft YaHei";
                border: 4px solid #4F6F52;
            }
        """

BUTTON_STYLE_TRANSPARENT = """
            QPushButton {
                font-family: "Microsoft YaHei";
                background-color: transparent; /* 修改为透明背景 */
                border: 2px solid #7895B2;
                color: #7895B2; /* 修改为按钮文字的颜色 */
            }

            QPushButton:hover {
                font-family: "Microsoft YaHei";
                background-color: transparent; /* 修改为透明背景 */
                border: 2px solid #9BB0C1;
                color: #9BB0C1; /* 修改为按钮文字的颜色 */
            }

            QPushButton:disabled {
                font-family: "Microsoft YaHei";
                background-color: transparent; /* 修改为透明背景 */
                border: 2px solid #d4dbe4;
                color: #d4dbe4; /* 修改为按钮文字的颜色 */
            }

            QPushButton:pressed {
                font-family: "Microsoft YaHei";
                border: 4px solid #5a7c9d;
            }
        """

BUTTON_STYLE_PINK = """
            QPushButton {
                font-family: "Microsoft YaHei";
                background-color: #E195AB;
                border: 2px solid #E195AB;
                color: #FFFFFF;
            }

            QPushButton:hover {
                font-family: "Microsoft YaHei";
                background-color: #FFCCE1;
                border: 2px solid #FFCCE1;
            }

            QPushButton:disabled {
                font-family: "Microsoft YaHei";
                background-color: #F2F9FF;
                border: 2px solid #F2F9FF;
                color: #A0A0A0;
            }

            QPushButton:pressed {
                font-family: "Microsoft YaHei";
                border: 4px solid #d87693;
            }
        """

LABEL_STYLE = """
            font-family: "Microsoft YaHei";
            font-weight: bold;
            font-size: 10pt;
        """

LABEL_STYLE_STATUS = """
            font-family: "Microsoft YaHei";
            font-size: 9pt;
        """

LABEL_STYLE_NORMAL = """
            font-family: "Microsoft YaHei";
            font-size: 10pt;
        """

LABEL_STYLE_TITLE = """
            font-family: "Microsoft YaHei";
            font-weight: bold;
            font-size: 18pt;
        """
LABEL_STYLE_SUBTITLE = """
            font-family: "Microsoft YaHei";
            font-weight: bold;
            font-size: 12pt;
        """

TEXT_BOLD = """
            font-family: "Microsoft YaHei";
            font-size: 12px;
            font-weight: bold;
"""

LABEL_STATUS_GREEN = """
            background-color: #4bb762;
            padding: 5px;
"""

LABEL_STATUS_RED = """
            background-color: #BF3131;
            padding: 5px;
"""
LABEL_STATUS_YELLOW = """
            background-color: #FFB534;
            padding: 5px;
"""

COLOR = {
    "black": "#000000",
    "blue": "#40A2D8",
    "green": "#65B741",
    "red": "#BF3131",
    "orange": "#FFB534",
    "pink": "#FF90BC"
}

SCROLL_AREA_ORANGE = """
            QScrollArea{
                border: 2px solid #f7ceb1;
            }
        """

text_format_black = QTextCharFormat()
text_format_black.setForeground(QBrush(QColor(COLOR['black'])))
text_format_blue = QTextCharFormat()
text_format_blue.setForeground(QBrush(QColor(COLOR['blue'])))
text_format_green = QTextCharFormat()
text_format_green.setForeground(QBrush(QColor(COLOR['green'])))
text_format_red = QTextCharFormat()
text_format_red.setForeground(QBrush(QColor(COLOR['red'])))
text_format_orange = QTextCharFormat()
text_format_orange.setForeground(QBrush(QColor(COLOR['orange'])))
text_format_pink = QTextCharFormat()
text_format_pink.setForeground(QBrush(QColor(COLOR['pink'])))

text_bold = QTextCharFormat()
text_bold.setFontWeight(QFont.Bold)
