import logging
import copy

from PyQt5.QtCore import QSize, QObject, pyqtSignal
from PyQt5.QtWidgets import QListWidgetItem, QLabel, QSpacerItem
from PyQt5.QtGui import QPixmap

from src.route_handler import *
from ui.custom_widgets import *


class PageRoute(QObject):
    sig_route_modified = pyqtSignal()

    def __init__(self, ui):
        QObject.__init__(self)
        self.ui = ui
        self.selected_widget = None

        # Widgets
        self.splits_list = self.ui.route_splits_list
        self.splits_add_btn = self.ui.route_splits_add_btn
        self.split_types_layout = self.ui.page_route_split_types_layout
        self.start_condition_dropdown = self.ui.page_route_route_option_start_condition
        self.option_name_input = self.ui.page_route_split_option_name
        self.option_split_checkbox = self.ui.page_route_split_option_split
        self.option_reset_count_checkbox = self.ui.page_route_split_option_reset_count
        self.component_types_layout = self.ui.page_route_split_component_types_layout
        self.component_preview_scroll = self.ui.page_route_split_components_preview_scroll
        self.components_options_scroll = self.ui.page_route_split_components_options_scroll

        # Signals
        self.splits_list.sig_dropped.connect(self.apply_changes_to_route)
        self.splits_list.itemSelectionChanged.connect(self.selection_changed)

        # Add Button
        self.splits_add_btn.clicked.connect(self.add_split_clicked)

        # Route Options
        # ------------------------------

        # Start Condition
        self.start_conditions = {
            "livesplit": "LiveSplit Timer Started",
            "start_button": "Start Game Button",
            "time_date_ok_button": "Date Time Ok Button",
            "first_split": "First Split"
        }
        self.start_condition_dropdown.set_options(self.start_conditions)
        self.start_condition_dropdown.dropdown.currentTextChanged.connect(self.start_condition_changed)

        # Split Options
        # ------------------------------

        # Name
        self.option_name_input.input_field.textEdited.connect(self.name_edited)

        # Split
        self.option_split_checkbox.checkbox.clicked.connect(self.split_toggled)

        # Reset Moon Count
        self.option_reset_count_checkbox.checkbox.clicked.connect(self.reset_count_toggled)

        icon_path = "ui/resources/icons/"
        video_path = "ui/resources/videos/"
        component_types = [
            [["moon_get"], icon_path + "moon_alt.png", video_path + "moon.avi"],
            [["moon_story"], icon_path + "moon_story.png", video_path + "moon story.avi"],
            [["moon_multi", "black_screen"], icon_path + "moon_multi.png", video_path + "moon multi.avi"],
            [["cap_end", "black_screen"], icon_path + "castle_cap.png", video_path + "kingdom cap.avi"],
            [["odyssey", "black_screen"], icon_path + "castle_odyssey.png", video_path + "kingdom odyssey.avi"],
            [["moon_end"], icon_path + "castle_moon.png", video_path + "kingdom moon.avi"],
            [["odyssey"], icon_path + "odyssey.png", video_path + "odyssey.avi"],
            [["world_map_fadeout"], icon_path + "globe.png", video_path + "world map.avi"],
            [["cutscene_skip"], icon_path + "cutscene.png", video_path + "cutscene.avi"],
            [["black_screen"], icon_path + "monitor.png", video_path + "black screen.avi"],
            [["white_screen"], icon_path + "monitor_white.png", video_path + "white screen.avi"],
            [["subarea"], icon_path + "door.png", video_path + "subarea.avi"],
            [["compass"], icon_path + "compass.png", video_path + "compass.avi"]
        ]

        for components, icon, video in component_types:
            button = ComponentButton(video.split("/")[-1][:-4], [Component(x) for x in components], icon, video)
            self.component_types_layout.addWidget(button)
            button.clicked.connect(self.add_component_clicked)

    def add_component_clicked(self):
        btn_widget = self.sender()

        if self.selected_widget is None:
            return

        self.selected_widget.split.components += copy.deepcopy(btn_widget.components)

        self.apply_changes_to_route()

    def add_btn_clicked(self):
        btn_widget = self.sender()

        if len(self.splits_list) > 0 and len(self.splits_list.selectedItems()) != 1:
            return

        clicked_widget = btn_widget.parent().parent()

        inserted_item = QListWidgetItem()
        inserted_item.setSizeHint(QSize(100, 46))
        inserted_widget = RouteSplitWidget(inserted_item, copy.deepcopy(clicked_widget.split))
        inserted_widget.delete_button.clicked.connect(self.delete_btn_clicked)
        inserted_widget.split.name = ""
        inserted_widget.set_text("")

        if len(self.splits_list) > 0:
            selected_item = self.splits_list.selectedItems()[0]
            selected_row = self.splits_list.row(selected_item)

            if selected_row + 1 >= len(self.splits_list):
                self.splits_list.addItem(inserted_item)
            else:
                self.splits_list.insertItem(selected_row + 1, inserted_item)
        else:
            RouteHandler.route = Route()
            self.splits_list.addItem(inserted_item)

        self.splits_list.setItemWidget(inserted_item, inserted_widget)
        self.splits_list.setCurrentRow(self.splits_list.row(inserted_item))
        self.option_name_input.focus()

        self.apply_changes_to_route()

    def add_split_clicked(self):
        if len(self.splits_list) > 0 and len(self.splits_list.selectedItems()) != 1:
            self.splits_list.setCurrentRow(0)

        inserted_item, inserted_widget = self.get_empty_list_item()

        if len(self.splits_list) > 0:
            selected_item = self.splits_list.selectedItems()[0]
            selected_row = self.splits_list.row(selected_item)

            if selected_row + 1 >= len(self.splits_list):
                self.splits_list.addItem(inserted_item)
            else:
                self.splits_list.insertItem(selected_row + 1, inserted_item)
        else:
            RouteHandler.route = Route()
            self.splits_list.addItem(inserted_item)

        self.splits_list.setItemWidget(inserted_item, inserted_widget)
        self.splits_list.setCurrentRow(self.splits_list.row(inserted_item))
        self.option_name_input.focus()

        self.apply_changes_to_route()

    def get_empty_list_item(self):
        item = QListWidgetItem()
        item.setSizeHint(QSize(100, 46))
        widget = RouteSplitWidget(item, Split("", "", []))
        widget.delete_button.clicked.connect(self.delete_btn_clicked)
        widget.duplicate_button.clicked.connect(self.duplicate_btn_clicked)
        widget.split.name = ""
        widget.set_text("")

        return item, widget

    def update_component_preview(self, preview_only=False):
        if not preview_only:
            self.components_options_scroll.clear()

        if self.selected_widget is not None and self.selected_widget.split is not None and \
                self.selected_widget.split.components is not None:

            self.component_preview_scroll.set_components(self.selected_widget.split.components)

            for i, component in enumerate(self.selected_widget.split.components):

                if not preview_only:
                    option_widget = ComponentOptionWidget(component)
                    list_widget_item = QListWidgetItem(self.components_options_scroll)
                    list_widget_item.setFlags(list_widget_item.flags() & ~QtCore.Qt.ItemIsSelectable)
                    list_widget_item.setSizeHint(QSize(100, 44))
                    self.components_options_scroll.addItem(list_widget_item)
                    self.components_options_scroll.setItemWidget(list_widget_item, option_widget)

                    option_widget.activations.spin_box.valueChanged.connect(self.activations_changed)
                    option_widget.min_moons.spin_box.valueChanged.connect(self.min_moons_changed)
                    option_widget.delete_button.clicked.connect(self.delete_component_clicked)

                    option_widget.activations.set_value(component.activations)
                    option_widget.min_moons.set_value(component.min_moons)

    def delete_component_clicked(self):
        sender = self.sender()

        try:
            component = sender.parent().component
        except:
            return

        self.selected_widget.split.components.remove(component)

        self.apply_changes_to_route()

    def delete_btn_clicked(self):
        btn_widget = self.sender()
        parent = btn_widget.parent()
        self.splits_list.takeItem(self.splits_list.row(parent.list_widget_item))
        parent.deleteLater()

        self.update_split_option_widgets()
        self.apply_changes_to_route()

    def duplicate_btn_clicked(self):
        btn_widget = self.sender()
        parent = btn_widget.parent()

        item = QListWidgetItem(self.splits_list)
        item.setSizeHint(QSize(100, 42))

        widget = RouteSplitWidget(item, copy.deepcopy(parent.split))
        widget.delete_button.clicked.connect(self.delete_btn_clicked)
        widget.duplicate_button.clicked.connect(self.duplicate_btn_clicked)

        self.splits_list.setItemWidget(item, widget)

    def clear_splits(self):
        self.splits_list.clear()

    def add_splits(self, splits):
        if splits:
            for split in splits:
                item = QListWidgetItem(self.splits_list)
                item.setSizeHint(QSize(100, 42))

                widget = RouteSplitWidget(item, split)
                widget.delete_button.clicked.connect(self.delete_btn_clicked)
                widget.duplicate_button.clicked.connect(self.duplicate_btn_clicked)

                self.splits_list.setItemWidget(item, widget)

    def route_updated(self):
        self.clear_splits()

        if RouteHandler.route is not None:
            self.add_splits(RouteHandler.route.splits)

            if RouteHandler.route.start_condition not in list(self.start_conditions.keys()):
                RouteHandler.route.start_condition = list(self.start_conditions.keys())[0]

        self.update_route_option_widgets()
        self.update_split_option_widgets()

        if len(self.splits_list) > 0:
            self.splits_list.setCurrentRow(0)

    def apply_changes_to_route(self):
        if RouteHandler.route is None:
            return

        # Splits
        splits = []
        try:
            for list_widget_item in [self.splits_list.item(x) for x in
                                     range(len(self.splits_list))]:
                split = self.splits_list.itemWidget(list_widget_item).split
                splits.append(split)
        except Exception as e:
            logging.exception(e)
            return

        RouteHandler.route.splits = splits

        # Start Condition
        start_condition = self.start_condition_dropdown.get_current_key()
        if start_condition is not None:
            RouteHandler.route.start_condition = start_condition
        else:
            RouteHandler.route.start_condition = self.start_conditions[0]
            self.start_condition_dropdown.set_index(0)

        try:
            selected_split = self.selected_widget.split
            if len(selected_split.components) == 0:
                selected_split.type = ""
            elif len(selected_split.components) > 1:
                names = ["moon_multi", "cap_end", "odyssey"]
                if selected_split.components[-1].name == "black_screen" and selected_split.components[-2].name in names:
                    selected_split.type = selected_split.components[-2].name
                else:
                    selected_split.type = selected_split.components[-1].name
            else:
                selected_split.type = selected_split.components[-1].name

            self.selected_widget.update_icon()
        except:
            pass

        self.update_component_preview()

        self.sig_route_modified.emit()

    def selection_changed(self):
        if len(self.splits_list.selectedItems()) != 1:
            return

        try:
            selected_item = self.splits_list.selectedItems()[0]
            self.selected_widget = self.splits_list.itemWidget(selected_item)
        except Exception as e:
            logging.exception(e)
            return

        self.update_split_option_widgets()
        self.option_name_input.focus()
        self.update_component_preview()

    # Route Options
    # ------------------------------

    def start_condition_changed(self):
        self.apply_changes_to_route()

    # Split Options
    # ------------------------------

    def name_edited(self):
        if self.selected_widget is None or len(self.splits_list) == 0:
            return

        try:
            entered_text = self.option_name_input.get_text()
            self.selected_widget.split.name = entered_text
            self.selected_widget.set_text(entered_text)
        except Exception as e:
            logging.exception(e)
            return

        self.apply_changes_to_route()

    def split_toggled(self):
        if self.selected_widget is None or len(self.splits_list) == 0:
            return

        try:
            split_state = self.option_split_checkbox.get_state()
            self.selected_widget.split.split = split_state
        except Exception as e:
            logging.exception(e)
            return

        self.apply_changes_to_route()

    def activations_changed(self, value):
        sender = self.sender()

        try:
            component = sender.parent().parent().parent().component
        except:
            return

        component.activations = value

        self.update_component_preview(preview_only=True)

    def min_moons_changed(self, value):
        sender = self.sender()

        try:
            component = sender.parent().parent().parent().component
        except:
            return

        component.min_moons = value

    def reset_count_toggled(self):
        if self.selected_widget is None or len(self.splits_list) == 0:
            return

        try:
            reset_count_state = self.option_reset_count_checkbox.get_state()
            self.selected_widget.split.reset_moon_count = reset_count_state
        except Exception as e:
            logging.exception(e)
            return

        self.apply_changes_to_route()

    def update_route_option_widgets(self):
        if RouteHandler.route is None:
            return

        # Start Condition
        self.start_condition_dropdown.set_current_key(RouteHandler.route.start_condition)

    def update_split_option_widgets(self):
        if self.selected_widget is None or self.selected_widget.split is None:
            return

        # Name
        if len(self.splits_list) == 0:
            self.option_name_input.set_text("")
        else:
            self.option_name_input.set_text(self.selected_widget.split.name)

        # Split
        self.option_split_checkbox.set_state(self.selected_widget.split.split)

        # Reset Moon Count
        self.option_reset_count_checkbox.set_state(self.selected_widget.split.reset_moon_count)
