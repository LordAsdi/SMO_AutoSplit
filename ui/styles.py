from ui.colors import Color


class Style:
    btn_tabs = (
            """
            QPushButton {
                border: none;
                border-left: 16px solid """ + Color.foreground + """;
                background-color: """ + Color.foreground + """;
                text-align: left;
                outline: 0;
            }
            QPushButton[Active=true] {
                border: none;
                border-left: 16px solid """ + Color.foreground + """;
                border-right: 5px solid """ + Color.background + """;
                background-color: """ + Color.foreground + """;
                text-align: left;
            }
            QPushButton:hover {
                background-color: """ + Color.button_hover + """;
                border-left: 16px solid """ + Color.button_hover + """;
            }
            QPushButton:pressed {
                background-color: """ + Color.button_pressed + """;
                border-left: 16px solid """ + Color.button_pressed + """;
            }
            """
    )

    main_window = (
            """
            QMainWindow {background: transparent; }
            QToolTip {
                color: """ + Color.text_white + """;
                background-color: """ + Color.foreground + """;
                border: 1px solid rgb(40, 40, 40);
                border-radius: 2px;
            }
            """
    )

    route_list = (
            """
            ::item {
                background-color: """ + Color.foreground + """;
                color: """ + Color.text_white + """;
                margin: 0px 0px 6px 0px;
            }
            ::item:selected {
                border: 2px solid white;
            }
            QListWidget {
                background: transparent;
                outline: 0;
                border: 0px;
            }
            QLabel {
                color: """ + Color.text_white + """;
            }
            """
    )

    beta_tag = (
            """
            QLabel {
                border-radius: 8px;
                padding-left: 4px;
                padding-right: 4px;
                padding-bottom: 2px;
                margin-top: 4px;
                margin-bottom: 4px;
                margin-left: 5px;
                color: """ + Color.text_white + """;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop: 0 #f77f0e, stop:1 #f7480e);
            }
            """
    )

    btn_centered = (
            """
            QPushButton {
                border: none;
                background-color: """ + Color.foreground + """;
                color: """ + Color.text_white + """;
                text-align: center;
                padding: 8px;
                outline: 0;
            }
            QPushButton[Active=true] {
                background-color: """ + Color.foreground + """;
            }
            QPushButton:hover {
                background-color: """ + Color.button_hover + """;
            }
            QPushButton:pressed {
                background-color: """ + Color.button_pressed + """;
            }
            """
    )

    title_label = (
            """
            QLabel {
                border: none;
                background-color: """ + Color.foreground + """;
                color: """ + Color.text_white + """;
                text-align: center;
                padding-top: 4px;
                padding-bottom: 8px;
                padding-left: 6px;
                margin-bottom: 0px;
            }
            """
    )

    btn_rounded = (
            """
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 14px;
                outline: 0;
            }
            QPushButton:hover {
                background-color: """ + Color.button_hover_light + """;
            }
            QPushButton:pressed {
                background-color: """ + Color.button_pressed + """;
            }
            """
    )

    input_field = (
        """
        QLineEdit {
            background-color: #131519;
            border: none;
            border-bottom: 3px solid white;
            border-radius: 0px;
            padding-left: 4px;
            padding-right: 4px;
        }
        """
    )

    spin_box = (
        """
        QSpinBox {
            background-color: #131519;
            border: none;
            border-bottom: 3px solid white;
            border-radius: 0px;
            padding-left: 4px;
            padding-right: 4px;
            outline: 0;
        }
        """
    )

    dropdown = (
            """
            QComboBox{
                    background-color: """ + Color.foreground + """;
                    border: none;
                    padding: 5px;
                    padding-left: 10px;
                    outline: 0;
                }
                QComboBox:hover{
                    border: none;
                    outline: 0;
                }
                QComboBox::drop-down {
                    subcontrol-origin: padding;
                    subcontrol-position: top right;
                    width: 25px;
                    background-position: center;
                    background-repeat: no-reperat;
                    outline: 0;
                }
                QComboBox::drop-down:button {
                    border: none;
                }
                QComboBox QAbstractItemView {
                    background-color: """ + Color.foreground + """;
                    padding: 10px;
                    selection-background-color: rgb(50, 56, 65);
                    outline: 0;
                }
                QComboBox::down-arrow {
                    image: url(ui/resources/icons/dropdown_arrow_50.png);
                }
        """
    )

    splitter = (
        """
        QSplitter::handle:vertical {
            height: 5px;
            background-color: rgba(27, 29, 35, 50)
        }
        QSplitter::handle:horizontal {
            width: 5px;
            background-color: rgba(27, 29, 35, 50)
        }
        """
    )

    checkbox = (
        """
        QCheckBox::indicator:unchecked {
            image: url(ui/resources/icons/checkbox_unchecked.png);
        }
        QCheckBox::indicator:checked {
            image: url(ui/resources/icons/checkbox_checked.png);
        }
        """
    )

    video_tooltip_button = (
            """
            QPushButton {
                border: none;
                background-color: """ + Color.foreground + """;
        color: """ + Color.text_white + """;
        text-align: center;
        padding: 8px;
        outline: 0;
        }
        QPushButton[Active=true] {
            background-color: """ + Color.background + """;
        }
        QPushButton:hover {
            background-color: """ + Color.button_hover + """;
        }
        QPushButton:pressed {
            background-color: """ + Color.button_pressed + """;
        }
        """
    )

    components_options_list = (
        """
        ::item {
            background-color: rgb(27, 29, 35);
            color: rgb(255, 255, 255);
            margin: 0px 0px 6px 0px;
        }
        ::item:selected {
            border: none;
        }
        QListWidget {
            background: transparent;
            outline: 0;
            border: none;
        }
        QLabel {
            color: rgb(255, 255, 255);
        }
        QScrollBar:vertical
        {
            background-color: rgb(64, 64, 73);
            width: 16px;
            margin: 0px 3px 0px 3px;
            border: 1px transparent #2A2929;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical
        {
            background-color: rgb(27, 29, 35);
            min-height: 5px;
            border-radius: 5px;
        }

        QScrollBar::sub-line:vertical
        {
            border: none;
            background: none;
            width: 0px;
            height: 0px;
        }

        QScrollBar::add-line:vertical
        {
            border: none;
            background: none;
            width: 0px;
            height: 0px;
        }

        QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on
        {
            border: none;
            background: none;
            width: 0px;
            height: 0px;
        }

        QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
        {
            border: none;
            background: none;
            width: 0px;
            height: 0px;
        }

        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
        {
            border: none;
            background: none;
            width: 0px;
            height: 0px;
        }

        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
        {
            border: none;
            background: none;
            width: 0px;
            height: 0px;
        }
        """
    )
