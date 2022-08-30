from PyQt5.QtCore import QMetaObject
from PyQt5.QtGui import QMovie

from ui.custom_widgets import *
from src.config import Config
from src.route_handler import RouteHandler


class MainWindowUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.close_callback = None

        self.dragPos = None

        # ----------------------------------------
        #                Widgets
        # ----------------------------------------
        # Window
        self.central_widget = None
        self.frame_main = None
        self.central_widget_layout = None
        # Header
        self.label_title_bar_top = None
        self.frame_label_top_btns = None
        self.btn_minimize = None
        self.btn_maximize_restore = None
        self.btn_close = None
        # Menus
        self.layout_menu_bottom = None
        self.frame_menu_spacer = None
        self.layout_menus = None
        self.frame_left_menu = None
        # Footer
        self.label_version = None
        self.label_beta = None
        self.label_status = None
        self.status_busy_anim = None
        self.label_livesplit_status = None
        self.label_cpu_usage_percent = None
        self.label_fps_value = None
        self.frame_size_grip = None
        # Center
        self.stacked_widget_pages = None

        # Pages
        self.page_dashboard = None
        self.page_route = None
        self.page_settings = None

        # Page Dashboard
        self.page_dashboard_splitter = None
        self.page_dashboard_preview = None
        self.splits_list = None
        self.page_dashboard_undo_btn = None
        self.page_dashboard_skip_btn = None
        self.page_dashboard_split_components_preview_scroll = None
        self.page_dashboard_moon_count_widget = None
        self.page_dashboard_activations_widget = None
        # Route Buttons
        self.page_dashboard_close_route_btn = None
        self.page_dashboard_load_route_btn = None
        self.page_dashboard_save_route_btn = None
        self.page_dashboard_save_route_as_btn = None

        # Page Route
        self.page_route_splitter = None
        self.route_splits_list = None
        self.route_splits_add_btn = None
        self.page_route_split_types_layout = None
        # Route Buttons
        self.page_route_close_route_btn = None
        self.page_route_load_route_btn = None
        self.page_route_save_route_btn = None
        self.page_route_save_route_as_btn = None
        # Options
        self.page_route_route_option_start_condition = None
        self.page_route_split_option_name = None
        self.page_route_split_option_split = None
        self.page_route_split_option_reset_count = None
        self.page_route_split_component_types_layout = None
        self.page_route_split_components_preview_scroll = None
        self.page_route_split_components_options_scroll = None

        # Page Settings
        self.page_settings_checkbox_check_updates = None
        self.page_settings_checkbox_auto_update = None
        self.page_settings_dropdown_capture_device = None
        self.page_settings_button_edit_crop_area = None

    def setup_ui(self):
        if self.objectName():
            self.setObjectName("MainWindow")

        self.setMinimumSize(QSize(622, 300))
        self.setStyleSheet(Style.main_window)

        self.central_widget = QWidget(self)
        self.central_widget.setStyleSheet(f"color: {Color.text_white};")

        self.central_widget_layout = QHBoxLayout(self.central_widget)
        self.central_widget_layout.setSpacing(0)
        self.central_widget_layout.setContentsMargins(0, 0, 0, 0)

        self.frame_main = QFrame(self.central_widget)
        self.frame_main.setFrameShape(QFrame.NoFrame)
        self.frame_main.setFrameShadow(QFrame.Raised)

        frame_main_layout = QVBoxLayout(self.frame_main)
        frame_main_layout.setSpacing(0)
        frame_main_layout.setContentsMargins(0, 0, 0, 0)

        # ----------------------------------------------------------
        #                         Header
        # ----------------------------------------------------------

        frame_top = QFrame(self.frame_main)
        frame_top.setFixedHeight(28)
        frame_top.setStyleSheet("background-color: transparent;")
        frame_top.setFrameShape(QFrame.NoFrame)
        frame_top.setFrameShadow(QFrame.Raised)

        frame_top_layout = QHBoxLayout(frame_top)
        frame_top_layout.setSpacing(0)
        frame_top_layout.setContentsMargins(0, 0, 0, 0)

        # Icon
        # ----------------------
        frame_icon = QFrame(frame_top)
        frame_icon.setStyleSheet(f"background-color: {Color.foreground};")
        frame_icon.setFrameShape(QFrame.NoFrame)
        frame_icon.setFrameShadow(QFrame.Raised)

        frame_icon_layout = QVBoxLayout(frame_icon)
        frame_icon_layout.setSpacing(0)
        frame_icon_layout.setContentsMargins(18, 0, 22, 0)

        label_icon = QLabel(frame_icon)
        label_icon.setPixmap(QPixmap("ui/resources/icons/icon_alt.png"))
        label_icon.setScaledContents(True)
        label_icon.setContentsMargins(0, 0, 0, 0)
        label_icon.setFixedSize(QSize(18, 18))

        frame_icon_layout.addWidget(label_icon)

        # ----------------------

        frame_top_layout.addWidget(frame_icon)

        frame_top_right = QFrame(frame_top)
        frame_top_right.setStyleSheet("background: transparent;")
        frame_top_right.setFrameShape(QFrame.NoFrame)
        frame_top_right.setFrameShadow(QFrame.Raised)

        frame_top_right_layout = QVBoxLayout(frame_top_right)
        frame_top_right_layout.setSpacing(0)
        frame_top_right_layout.setContentsMargins(0, 0, 0, 0)

        # Header Buttons
        # ----------------------
        frame_top_btns = QFrame(frame_top_right)
        frame_top_btns.setMaximumHeight(42)
        frame_top_btns.setStyleSheet("background-color: rgba(27, 29, 35, 200)")
        frame_top_btns.setFrameShape(QFrame.NoFrame)
        frame_top_btns.setFrameShadow(QFrame.Raised)

        frame_top_btns_layout = QHBoxLayout(frame_top_btns)
        frame_top_btns_layout.setSpacing(0)
        frame_top_btns_layout.setContentsMargins(0, 0, 0, 0)

        frame_label_top_btns_size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        frame_label_top_btns_size_policy.setHorizontalStretch(0)
        frame_label_top_btns_size_policy.setVerticalStretch(0)

        self.frame_label_top_btns = QFrame(frame_top_btns)
        self.frame_label_top_btns.setSizePolicy(frame_label_top_btns_size_policy)
        self.frame_label_top_btns.setFrameShape(QFrame.NoFrame)
        self.frame_label_top_btns.setFrameShadow(QFrame.Raised)

        frame_label_top_btns_size_policy.setHeightForWidth(self.frame_label_top_btns.sizePolicy().hasHeightForWidth())

        frame_label_top_btns_layout = QHBoxLayout(self.frame_label_top_btns)
        frame_label_top_btns_layout.setSpacing(0)
        frame_label_top_btns_layout.setContentsMargins(0, 0, 10, 0)

        self.label_title_bar_top = QLabel(self.frame_label_top_btns)
        self.label_title_bar_top.setFont(font_8pt)

        frame_label_top_btns_layout.addWidget(self.label_title_bar_top)

        frame_top_btns_layout.addWidget(self.frame_label_top_btns)

        frame_btns_right = QFrame(frame_top_btns)
        frame_label_top_btns_size_policy.setHeightForWidth(frame_btns_right.sizePolicy().hasHeightForWidth())
        frame_btns_right.setSizePolicy(frame_label_top_btns_size_policy)
        frame_btns_right.setMaximumWidth(120)
        frame_btns_right.setFrameShape(QFrame.NoFrame)
        frame_btns_right.setFrameShadow(QFrame.Raised)

        btns_right_layout = QHBoxLayout()
        btns_right_layout.setContentsMargins(0, 0, 0, 0)

        frame_btns_right.setLayout(btns_right_layout)

        self.btn_minimize = QPushButton()
        self.btn_minimize.setIcon(QIcon(QPixmap("ui/resources/icons/minimize.png")))
        self.btn_minimize.setFixedSize(QSize(28, 28))
        self.btn_minimize.setStyleSheet(Style.btn_centered)
        self.btn_minimize.setToolTip("Minimize")

        self.btn_maximize_restore = QPushButton()
        self.btn_maximize_restore.setIcon(QIcon(QPixmap("ui/resources/icons/fullscreen.png")))
        self.btn_maximize_restore.setFixedSize(QSize(28, 28))
        self.btn_maximize_restore.setStyleSheet(Style.btn_centered)
        self.btn_maximize_restore.setToolTip("Maximize")

        self.btn_close = QPushButton()
        self.btn_close.setIcon(QIcon(QPixmap("ui/resources/icons/close.png")))
        self.btn_close.setFixedSize(QSize(28, 28))
        self.btn_close.setStyleSheet(Style.btn_centered)
        self.btn_close.setToolTip("Close")

        btns_right_layout.addWidget(self.btn_minimize)
        btns_right_layout.addWidget(self.btn_maximize_restore)
        btns_right_layout.addWidget(self.btn_close)

        # ----------------------

        frame_top_btns_layout.addWidget(frame_btns_right, 0, Qt.AlignRight)

        frame_top_right_layout.addWidget(frame_top_btns)

        frame_top_layout.addWidget(frame_top_right)

        # ----------------------------------------------------------

        frame_main_layout.addWidget(frame_top)

        frame_center = QFrame(self.frame_main)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(label_icon.sizePolicy().hasHeightForWidth())
        size_policy.setHeightForWidth(frame_center.sizePolicy().hasHeightForWidth())
        frame_center.setSizePolicy(size_policy)
        frame_center.setStyleSheet("background-color: rgb(40, 44, 52);")
        frame_center.setFrameShape(QFrame.NoFrame)
        frame_center.setFrameShadow(QFrame.Raised)

        frame_center_layout = QHBoxLayout(frame_center)
        frame_center_layout.setSpacing(0)
        frame_center_layout.setContentsMargins(0, 0, 0, 0)

        # ----------------------------------------------------------
        #                       Menu Left
        # ----------------------------------------------------------

        self.frame_left_menu = QFrame(frame_center)
        size_policy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy3.setHorizontalStretch(0)
        size_policy3.setVerticalStretch(0)
        size_policy3.setHeightForWidth(self.frame_left_menu.sizePolicy().hasHeightForWidth())
        self.frame_left_menu.setSizePolicy(size_policy3)
        self.frame_left_menu.setFixedWidth(55)
        self.frame_left_menu.setLayoutDirection(Qt.LeftToRight)
        self.frame_left_menu.setStyleSheet(f"background-color: {Color.foreground};")
        self.frame_left_menu.setFrameShape(QFrame.NoFrame)
        self.frame_left_menu.setFrameShadow(QFrame.Raised)

        frame_left_menu_layout = QVBoxLayout(self.frame_left_menu)
        frame_left_menu_layout.setSpacing(1)
        frame_left_menu_layout.setContentsMargins(0, 0, 0, 0)

        frame_menus = QFrame(self.frame_left_menu)
        frame_menus.setFrameShape(QFrame.NoFrame)
        frame_menus.setFrameShadow(QFrame.Raised)

        self.layout_menus = QVBoxLayout(frame_menus)
        self.layout_menus.setSpacing(0)
        self.layout_menus.setContentsMargins(0, 0, 0, 0)

        frame_left_menu_layout.addWidget(frame_menus, 0, Qt.AlignTop)

        frame_extra_menus = QFrame(self.frame_left_menu)
        size_policy3.setHeightForWidth(frame_extra_menus.sizePolicy().hasHeightForWidth())
        frame_extra_menus.setSizePolicy(size_policy3)
        frame_extra_menus.setFrameShape(QFrame.NoFrame)
        frame_extra_menus.setFrameShadow(QFrame.Raised)

        self.layout_menu_bottom = QVBoxLayout(frame_extra_menus)
        self.layout_menu_bottom.setSpacing(0)
        self.layout_menu_bottom.setContentsMargins(0, 0, 0, 0)

        self.frame_menu_spacer = QFrame(self)
        self.frame_menu_spacer.setMinimumSize(QSize(0, 25))
        self.frame_menu_spacer.setStyleSheet("background-color: rgb(33, 37, 43);")

        frame_left_menu_layout.addWidget(frame_extra_menus, 0, Qt.AlignBottom)

        # ----------------------------------------------------------

        frame_center_layout.addWidget(self.frame_left_menu)

        frame_content_right = QFrame(frame_center)
        frame_content_right.setStyleSheet("background-color: rgb(44, 49, 60);")
        frame_content_right.setFrameShape(QFrame.NoFrame)
        frame_content_right.setFrameShadow(QFrame.Raised)

        frame_content_right_layout = QVBoxLayout(frame_content_right)
        frame_content_right_layout.setSpacing(0)
        frame_content_right_layout.setContentsMargins(0, 0, 0, 0)

        frame_content = QFrame(frame_content_right)
        frame_content.setFrameShape(QFrame.NoFrame)
        frame_content.setFrameShadow(QFrame.Raised)

        frame_content_layout = QVBoxLayout(frame_content)
        frame_content_layout.setSpacing(0)
        frame_content_layout.setContentsMargins(0, 0, 0, 0)

        self.stacked_widget_pages = QStackedWidget(frame_content)
        self.stacked_widget_pages.setMinimumWidth(20)

        # ----------------------------------------------------------
        #                     Dashboard Page
        # ----------------------------------------------------------

        self.page_dashboard = QWidget()

        page_dashboard_hbox_layout = QHBoxLayout(self.page_dashboard)
        page_dashboard_hbox_layout.setContentsMargins(18, 18, 18, 18)

        self.page_dashboard_splitter = QSplitter(Qt.Horizontal)
        self.page_dashboard_splitter.setStyleSheet(Style.splitter)

        page_dashboard_left_layout = QVBoxLayout()
        page_dashboard_left_layout.setContentsMargins(0, 0, 18, 0)

        page_dashboard_left_widget = QWidget()
        page_dashboard_left_widget.setLayout(page_dashboard_left_layout)

        self.splits_list = SplitList()
        self.splits_list.setStyle(CustomDropIndicator())
        self.splits_list.setStyleSheet(Style.route_list)
        self.splits_list.setSpacing(0)
        self.splits_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.splits_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        page_dashboard_skip_undo_layout = QHBoxLayout()
        page_dashboard_skip_undo_layout.setContentsMargins(0, 0, 0, 0)
        page_dashboard_skip_undo_layout.setSpacing(8)

        page_dashboard_skip_undo_widget = QWidget()
        page_dashboard_skip_undo_widget.setLayout(page_dashboard_skip_undo_layout)

        self.page_dashboard_undo_btn = QPushButton("Undo Split")
        self.page_dashboard_undo_btn.setFont(font_9pt)
        self.page_dashboard_undo_btn.setStyleSheet(Style.btn_centered)

        self.page_dashboard_skip_btn = QPushButton("Skip Split")
        self.page_dashboard_skip_btn.setFont(font_9pt)
        self.page_dashboard_skip_btn.setStyleSheet(Style.btn_centered)

        page_dashboard_skip_undo_layout.addWidget(self.page_dashboard_undo_btn)
        page_dashboard_skip_undo_layout.addWidget(self.page_dashboard_skip_btn)

        page_dashboard_left_layout.addWidget(self.splits_list)
        page_dashboard_left_layout.addWidget(page_dashboard_skip_undo_widget)

        # Route Buttons
        # ----------------------
        page_dashboard_buttons_layout = QHBoxLayout()
        page_dashboard_buttons_layout.setContentsMargins(0, 0, 0, 0)
        page_dashboard_buttons_layout.setSpacing(8)

        page_dashboard_buttons_widget = QWidget()
        page_dashboard_buttons_widget.setLayout(page_dashboard_buttons_layout)

        self.page_dashboard_close_route_btn = QPushButton("Close route")
        self.page_dashboard_close_route_btn.setFont(font_9pt)
        self.page_dashboard_close_route_btn.setStyleSheet(Style.btn_centered)

        self.page_dashboard_load_route_btn = QPushButton("Load route")
        self.page_dashboard_load_route_btn.setFont(font_9pt)
        self.page_dashboard_load_route_btn.setStyleSheet(Style.btn_centered)

        self.page_dashboard_save_route_btn = QPushButton("Save route")
        self.page_dashboard_save_route_btn.setFont(font_9pt)
        self.page_dashboard_save_route_btn.setStyleSheet(Style.btn_centered)

        self.page_dashboard_save_route_as_btn = QPushButton("Save route as")
        self.page_dashboard_save_route_as_btn.setFont(font_9pt)
        self.page_dashboard_save_route_as_btn.setStyleSheet(Style.btn_centered)

        page_dashboard_buttons_layout.addWidget(self.page_dashboard_close_route_btn)
        page_dashboard_buttons_layout.addWidget(self.page_dashboard_load_route_btn)
        page_dashboard_buttons_layout.addWidget(self.page_dashboard_save_route_btn)
        page_dashboard_buttons_layout.addWidget(self.page_dashboard_save_route_as_btn)

        # ----------------------

        page_dashboard_right_layout = QVBoxLayout()
        page_dashboard_right_layout.setContentsMargins(18, 0, 0, 0)

        page_dashboard_right_widget = QWidget()
        page_dashboard_right_widget.setLayout(page_dashboard_right_layout)

        self.page_dashboard_preview = PreviewLabel("Preview")
        self.page_dashboard_preview.setFont(font_12pt)
        self.page_dashboard_preview.setAlignment(Qt.AlignCenter)
        self.page_dashboard_preview.setMinimumSize(QSize(160, 90))
        self.page_dashboard_preview.setMaximumSize(QSize(640, 360))
        self.page_dashboard_preview.setStyleSheet("background-color: rgba(27, 29, 35, 200); color: rgb(44, 49, 60);")

        self.page_dashboard_split_components_preview_scroll = ComponentPreview()

        self.page_dashboard_moon_count_widget = QRoundProgressBar("Moon Count")
        self.page_dashboard_moon_count_widget.rpb_set_minimum(0)
        self.page_dashboard_moon_count_widget.rpb_set_maximum(0)
        self.page_dashboard_moon_count_widget.rpb_set_value(0)

        self.page_dashboard_activations_widget = QRoundProgressBar("Activations")
        self.page_dashboard_activations_widget.rpb_set_minimum(0)
        self.page_dashboard_activations_widget.rpb_set_maximum(1)
        self.page_dashboard_activations_widget.rpb_set_value(0)

        page_dashboard_counter_layout = QHBoxLayout()
        page_dashboard_counter_layout.setContentsMargins(0, 10, 0, 0)
        page_dashboard_counter_layout.setSpacing(20)

        page_dashboard_counter_widget = QWidget()
        page_dashboard_counter_widget.setLayout(page_dashboard_counter_layout)

        page_dashboard_counter_layout.addWidget(self.page_dashboard_activations_widget)
        page_dashboard_counter_layout.addWidget(self.page_dashboard_moon_count_widget)
        page_dashboard_counter_layout.addStretch()

        page_dashboard_right_layout.addWidget(self.page_dashboard_preview)
        page_dashboard_right_layout.addWidget(self.page_dashboard_split_components_preview_scroll)
        page_dashboard_right_layout.addWidget(page_dashboard_counter_widget)
        page_dashboard_right_layout.addStretch()
        page_dashboard_right_layout.addWidget(page_dashboard_buttons_widget)

        self.page_dashboard_splitter.addWidget(page_dashboard_left_widget)
        self.page_dashboard_splitter.addWidget(page_dashboard_right_widget)

        self.page_dashboard_splitter.setStretchFactor(1, 1)
        self.page_dashboard_splitter.setSizes(Config.get_key("dashboard_splitter_1"))

        page_dashboard_hbox_layout.addWidget(self.page_dashboard_splitter)

        self.stacked_widget_pages.addWidget(self.page_dashboard)

        # ----------------------------------------------------------
        #                       Route Page
        # ----------------------------------------------------------

        self.page_route = QWidget()

        page_route_hbox_layout = QHBoxLayout(self.page_route)
        page_route_hbox_layout.setContentsMargins(18, 18, 18, 18)

        self.page_route_splitter = QSplitter(Qt.Horizontal)
        self.page_route_splitter.setStyleSheet(Style.splitter)

        page_route_left_layout = QVBoxLayout()
        page_route_left_layout.setContentsMargins(0, 0, 18, 0)

        page_route_left_widget = QWidget()
        page_route_left_widget.setLayout(page_route_left_layout)

        self.route_splits_list = RouteSplitList()
        self.route_splits_list.setStyle(CustomDropIndicator())
        self.route_splits_list.setStyleSheet(Style.route_list)
        self.route_splits_list.setSpacing(0)
        self.route_splits_list.setDragDropMode(QAbstractItemView.InternalMove)
        self.route_splits_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.route_splits_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.route_splits_add_btn = QPushButton("Add Split")
        self.route_splits_add_btn.setFont(font_9pt)
        self.route_splits_add_btn.setStyleSheet(Style.btn_centered)

        page_route_left_layout.addWidget(self.route_splits_list)
        page_route_left_layout.addWidget(self.route_splits_add_btn)

        page_route_route_options_title = Title("Route Options")

        self.page_route_route_option_start_condition = DropdownWide("Start Condition")

        self.page_route_split_types_layout = FlowLayout()
        self.page_route_split_types_layout.setContentsMargins(0, 0, 0, 0)
        self.page_route_split_types_layout.setSpacing(7)

        page_route_split_options_title = Title("Split Options", False)

        self.page_route_split_option_name = TextInput("Name")
        self.page_route_split_option_split = Checkbox("Split")
        self.page_route_split_option_reset_count = Checkbox("Reset Moon Count")

        page_route_split_options_layout = QGridLayout()
        page_route_split_options_layout.setContentsMargins(0, 0, 0, 0)
        page_route_split_options_layout.setSpacing(6)
        page_route_split_options_layout.setColumnStretch(0, 1)
        page_route_split_options_layout.setColumnStretch(1, 1)

        page_route_split_options_widget = QWidget()
        page_route_split_options_widget.setLayout(page_route_split_options_layout)

        page_route_split_options_layout.addWidget(self.page_route_split_option_name, 0, 0)
        page_route_split_options_layout.addWidget(self.page_route_split_option_split, 0, 1)
        page_route_split_options_layout.addWidget(self.page_route_split_option_reset_count, 1, 0)

        # Split Components
        # ----------------------

        page_route_split_components_add_title = Title("Add Split Components", False)

        page_route_split_component_types_widget = QWidget()
        self.page_route_split_component_types_layout = FlowLayout()
        self.page_route_split_component_types_layout.setContentsMargins(0, 0, 0, 0)
        self.page_route_split_component_types_layout.setSpacing(6)

        page_route_split_component_types_widget.setLayout(self.page_route_split_component_types_layout)

        page_route_split_components_title = Title("Split Components", False)

        # Component Preview
        # ----------------------

        self.page_route_split_components_preview_scroll = ComponentPreview()

        # Component Options
        # ----------------------

        self.page_route_split_components_options_scroll = QListWidget(self)
        self.page_route_split_components_options_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.page_route_split_components_options_scroll.setStyleSheet(Style.components_options_list)

        # Route Buttons
        # ----------------------
        page_route_buttons_layout = QHBoxLayout()
        page_route_buttons_layout.setContentsMargins(0, 10, 0, 0)
        page_route_buttons_layout.setSpacing(8)

        page_route_buttons_widget = QWidget()
        page_route_buttons_widget.setLayout(page_route_buttons_layout)

        self.page_route_close_route_btn = QPushButton("Close route")
        self.page_route_close_route_btn.setFont(font_9pt)
        self.page_route_close_route_btn.setStyleSheet(Style.btn_centered)

        self.page_route_load_route_btn = QPushButton("Load route")
        self.page_route_load_route_btn.setFont(font_9pt)
        self.page_route_load_route_btn.setStyleSheet(Style.btn_centered)

        self.page_route_save_route_btn = QPushButton("Save route")
        self.page_route_save_route_btn.setFont(font_9pt)
        self.page_route_save_route_btn.setStyleSheet(Style.btn_centered)

        self.page_route_save_route_as_btn = QPushButton("Save route as")
        self.page_route_save_route_as_btn.setFont(font_9pt)
        self.page_route_save_route_as_btn.setStyleSheet(Style.btn_centered)

        page_route_buttons_layout.addWidget(self.page_route_close_route_btn)
        page_route_buttons_layout.addWidget(self.page_route_load_route_btn)
        page_route_buttons_layout.addWidget(self.page_route_save_route_btn)
        page_route_buttons_layout.addWidget(self.page_route_save_route_as_btn)

        # ----------------------

        page_route_right_layout = QVBoxLayout()
        page_route_right_layout.setContentsMargins(18, 0, 0, 0)

        page_route_right_widget = QWidget()
        page_route_right_widget.setLayout(page_route_right_layout)

        page_route_right_layout.addWidget(page_route_route_options_title)
        page_route_right_layout.addWidget(self.page_route_route_option_start_condition)
        page_route_right_layout.addWidget(page_route_split_options_title)
        page_route_right_layout.addWidget(page_route_split_options_widget)
        page_route_right_layout.addWidget(page_route_split_components_add_title)
        page_route_right_layout.addWidget(page_route_split_component_types_widget)
        page_route_right_layout.addWidget(page_route_split_components_title)
        page_route_right_layout.addWidget(self.page_route_split_components_preview_scroll)
        page_route_right_layout.addWidget(self.page_route_split_components_options_scroll)
        page_route_right_layout.addStretch()
        page_route_right_layout.addWidget(page_route_buttons_widget)

        self.page_route_splitter.addWidget(page_route_left_widget)
        self.page_route_splitter.addWidget(page_route_right_widget)

        self.page_route_splitter.setStretchFactor(1, 1)
        self.page_route_splitter.setSizes([350, 500])

        page_route_hbox_layout.addWidget(self.page_route_splitter)

        self.stacked_widget_pages.addWidget(self.page_route)

        # ----------------------------------------------------------
        #                       Settings Page
        # ----------------------------------------------------------

        self.page_settings = QWidget()

        page_settings_layout = QVBoxLayout(self.page_settings)
        page_settings_layout.setContentsMargins(18, 18, 18, 18)

        page_settings_title_general = Title("General")

        self.page_settings_checkbox_check_updates = Checkbox("Check for updates")
        self.page_settings_checkbox_check_updates.setMaximumWidth(262)

        self.page_settings_checkbox_auto_update = Checkbox("Auto apply updates")
        self.page_settings_checkbox_auto_update.setMaximumWidth(262)

        page_settings_title_video_capture = Title("Video Capture", False)

        self.page_settings_dropdown_capture_device = DropdownWide("Capture Device")
        self.page_settings_dropdown_capture_device.setMaximumWidth(530)
        self.page_settings_dropdown_capture_device.right_layout.parent().setMaximumWidth(262)

        page_settings_restart_label = QLabel("Restart required for setting to take effect.")
        page_settings_restart_label.setFont(font_8pt)
        page_settings_restart_label.setStyleSheet("margin-left: 1px;")

        # self.page_settings_button_edit_crop_area = QPushButton("Edit Crop Area")
        # self.page_settings_button_edit_crop_area.setFont(font_9pt)
        # self.page_settings_button_edit_crop_area.setStyleSheet(Style.btn_centered)
        # self.page_settings_button_edit_crop_area.setMaximumWidth(262)

        page_settings_layout.addWidget(page_settings_title_general)
        page_settings_layout.addWidget(self.page_settings_checkbox_check_updates)
        page_settings_layout.addWidget(self.page_settings_checkbox_auto_update)
        page_settings_layout.addWidget(page_settings_title_video_capture)
        page_settings_layout.addWidget(self.page_settings_dropdown_capture_device)
        page_settings_layout.addWidget(page_settings_restart_label)
        # page_settings_layout.addWidget(self.page_settings_button_edit_crop_area)
        page_settings_layout.addStretch()

        self.stacked_widget_pages.addWidget(self.page_settings)

        # ----------------------------------------------------------

        frame_content_layout.addWidget(self.stacked_widget_pages)

        frame_content_right_layout.addWidget(frame_content)

        # ----------------------------------------------------------
        #                       Status Bar
        # ----------------------------------------------------------

        frame_bottom = QFrame(frame_content_right)
        frame_bottom.setFixedHeight(25)
        frame_bottom.setStyleSheet("background-color: rgb(33, 37, 43);")
        frame_bottom.setFrameShape(QFrame.NoFrame)
        frame_bottom.setFrameShadow(QFrame.Raised)
        frame_bottom.setContentsMargins(0, 0, 0, 0)

        frame_bottom_layout = QHBoxLayout(frame_bottom)
        frame_bottom_layout.setSpacing(0)
        frame_bottom_layout.setContentsMargins(0, 0, 2, 0)

        frame_label_bottom = QFrame(frame_bottom)
        frame_label_bottom.setFrameShape(QFrame.NoFrame)
        frame_label_bottom.setFrameShadow(QFrame.Raised)
        frame_label_bottom.setContentsMargins(0, 0, 0, 0)

        layout_bottom_status_bar = QHBoxLayout(frame_label_bottom)
        layout_bottom_status_bar.setSpacing(4)
        layout_bottom_status_bar.setContentsMargins(0, 0, 10, 0)

        label_status_busy_anim = QLabel(self)
        label_status_busy_anim.setMaximumWidth(21)
        self.status_busy_anim = QMovie("ui/resources/icons/load_anim.gif")
        self.status_busy_anim.setScaledSize(QSize(21, 21))
        label_status_busy_anim.setMovie(self.status_busy_anim)

        self.label_status = QLabel(frame_label_bottom)
        self.label_status.setMinimumHeight(25)
        self.label_status.setFont(font_7pt)
        self.label_status.setStyleSheet(f"color: {Color.text_dark_gray};")

        layout_footer_status = QHBoxLayout()
        layout_footer_status.setContentsMargins(0, 0, 0, 0)
        layout_footer_status.setSpacing(5)
        layout_footer_status.setAlignment(Qt.AlignLeft)

        label_livesplit = QLabel("LiveSplit")
        label_livesplit.setMinimumHeight(25)
        label_livesplit.setFont(font_7pt)
        label_livesplit.setStyleSheet(f"color: {Color.text_dark_gray};")
        label_livesplit.adjustSize()

        self.label_livesplit_status = QLabel("Disconnected")
        self.label_livesplit_status.setMinimumHeight(25)
        self.label_livesplit_status.setFont(font_7pt)
        self.label_livesplit_status.setStyleSheet("color: rgb(153, 61, 61);")
        self.label_livesplit_status.adjustSize()

        label_cpu_usage = QLabel("| CPU")
        label_cpu_usage.setMinimumHeight(25)
        label_cpu_usage.setFont(font_7pt)
        label_cpu_usage.setStyleSheet(f"color: {Color.text_dark_gray};")
        label_cpu_usage.adjustSize()

        self.label_cpu_usage_percent = QLabel("0.0%")
        self.label_cpu_usage_percent.setMinimumHeight(25)
        self.label_cpu_usage_percent.setFont(font_7pt)
        self.label_cpu_usage_percent.setStyleSheet(f"color: {Color.text_light_gray};")
        self.label_cpu_usage_percent.adjustSize()

        label_fps = QLabel("| FPS")
        label_fps.setMinimumHeight(25)
        label_fps.setFont(font_7pt)
        label_fps.setStyleSheet(f"color: {Color.text_dark_gray};")
        label_fps.adjustSize()

        self.label_fps_value = QLabel("0.0")
        self.label_fps_value.setMinimumHeight(25)
        self.label_fps_value.setFont(font_7pt)
        self.label_fps_value.setStyleSheet(f"color: {Color.text_light_gray};")
        self.label_fps_value.adjustSize()

        layout_footer_status.addWidget(label_livesplit)
        layout_footer_status.addWidget(self.label_livesplit_status)
        layout_footer_status.addWidget(label_cpu_usage)
        layout_footer_status.addWidget(self.label_cpu_usage_percent)
        layout_footer_status.addWidget(label_fps)
        layout_footer_status.addWidget(self.label_fps_value)

        self.label_version = QLabel(frame_label_bottom)
        self.label_version.setMinimumHeight(25)
        self.label_version.setMaximumWidth(100)
        self.label_version.setFont(font_7pt)
        self.label_version.setStyleSheet(f"color: {Color.text_dark_gray};")
        self.label_version.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.label_beta = QLabel("BETA")
        self.label_beta.setFont(font_7pt)
        self.label_beta.setFixedWidth(45)
        self.label_beta.setStyleSheet(Style.beta_tag)

        layout_bottom_status_bar.addWidget(label_status_busy_anim)
        layout_bottom_status_bar.addWidget(self.label_status)
        layout_bottom_status_bar.addLayout(layout_footer_status)
        layout_bottom_status_bar.addWidget(self.label_version)
        layout_bottom_status_bar.addWidget(self.label_beta)

        self.frame_size_grip = QLabel()
        self.frame_size_grip.setPixmap(QPixmap("ui/resources/icons/resize_grip.png"))
        self.frame_size_grip.setScaledContents(True)
        self.frame_size_grip.setContentsMargins(6, 6, 2, 2)
        self.frame_size_grip.setMaximumSize(QSize(20, 20))

        frame_bottom_layout.addWidget(frame_label_bottom)
        frame_bottom_layout.addWidget(self.frame_size_grip)

        frame_content_right_layout.addWidget(frame_bottom)

        # ----------------------------------------------------------

        frame_center_layout.addWidget(frame_content_right)

        frame_main_layout.addWidget(frame_center)

        self.central_widget_layout.addWidget(self.frame_main)

        self.setCentralWidget(self.central_widget)

        self.stacked_widget_pages.setCurrentIndex(1)

        QMetaObject.connectSlotsByName(self)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def closeEvent(self, event):
        if RouteHandler.check_unsaved_changes():
            event.ignore()
            RouteHandler.window_close_btn(self)
            return

        Config.set_key("fullscreen", self.isMaximized())
        Config.set_key("window_position", [self.pos().x(), self.pos().y()])
        if self.isMaximized():
            Config.set_key("window_size", [self.normalGeometry().width(), self.normalGeometry().height()])
        else:
            Config.set_key("window_size", [self.size().width(), self.size().height()])
        Config.set_key("dashboard_splitter_1", self.page_dashboard_splitter.sizes())
        Config.set_key("route_splitter_1", self.page_route_splitter.sizes())

        if not isinstance(self.close_callback, type(None)):
            self.close_callback()

        event.accept()
