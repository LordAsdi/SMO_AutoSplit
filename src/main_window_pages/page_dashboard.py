import numpy as np

from PyQt5.QtCore import QSize, QObject
from PyQt5.QtWidgets import QListWidgetItem, QAbstractItemView

from src.config import Config
from src.route_handler import RouteHandler
from ui.custom_widgets import SplitWidget


class PageDashboard(QObject):
    def __init__(self, ui, autosplitter):
        QObject.__init__(self)
        self.ui = ui
        self.autosplitter = autosplitter
        self.show_preview = True
        self.set_show_preview(Config.get_key("show_preview"))
        self.reload_splits = False

        self.ui.page_dashboard_preview.sig_clicked.connect(self.preview_clicked)
        self.ui.page_dashboard_undo_btn.clicked.connect(self.autosplitter.undo_split)
        self.ui.page_dashboard_skip_btn.clicked.connect(self.autosplitter.skip_split)

    def update_preview(self, frame):
        if not self.ui.page_dashboard_preview.overlay and self.show_preview:
            self.ui.page_dashboard_preview.setPixmap(frame)

    def disable_preview(self):
        if self.show_preview:
            self.set_show_preview(False)

    def clear_preview(self):
        if not self.ui.page_dashboard_preview.overlay and self.show_preview:
            self.ui.page_dashboard_preview.setText("Preview")

    def enable_preview(self):
        self.set_show_preview(True)

    def preview_clicked(self):
        self.set_show_preview(not self.show_preview)

    def set_show_preview(self, value):
        self.show_preview = value
        self.ui.page_dashboard_preview.enabled = self.show_preview
        self.ui.page_dashboard_preview.update_overlay()
        Config.set_key("show_preview", self.show_preview)

    def get_preview_size(self):
        width = self.ui.page_dashboard_preview.width()
        height = self.ui.page_dashboard_preview.height()
        return width, height

    def clear_splits(self):
        self.ui.splits_list.clear()

    def add_splits(self, splits):
        if splits:
            for split in splits:
                split_name = split.name

                widget = SplitWidget("ui/resources/icons/location_outline.png", split_name)

                item = QListWidgetItem(self.ui.splits_list)
                item.setSizeHint(QSize(100, 42))

                self.ui.splits_list.setItemWidget(item, widget)

    def component_changed(self, index):
        self.ui.page_dashboard_split_components_preview_scroll.set_selected(index)

    def moon_count_changed(self, value, required):
        # print("moo", value, required)
        self.ui.page_dashboard_moon_count_widget.rpb_set_value(0)
        self.ui.page_dashboard_moon_count_widget.rpb_set_range(required, 0)
        self.ui.page_dashboard_moon_count_widget.rpb_set_value(value)

    def component_activated(self, value, required):
        # print("act", value, required)
        self.ui.page_dashboard_activations_widget.rpb_set_value(0)
        self.ui.page_dashboard_activations_widget.rpb_set_range(required, 0)
        self.ui.page_dashboard_activations_widget.rpb_set_value(value)

    def next_split(self):
        current_index = self.get_active_split()

        if current_index is None:
            self.set_active_split(0)
        else:
            self.set_active_split(np.clip(current_index + 1, 0, len(self.ui.splits_list)))

    def prev_split(self):
        current_index = self.get_active_split()

        if current_index is None:
            self.set_active_split(0)
        else:
            self.set_active_split(np.clip(current_index - 1, 0, len(self.ui.splits_list) - 1))

    def get_active_split(self):
        selected_index = self.ui.splits_list.selectedIndexes()
        if len(selected_index) < 1:
            return None
        else:
            return selected_index[0].row()

    def set_active_split(self, row):
        for i in range(row):
            self.ui.splits_list.itemWidget(self.ui.splits_list.item(i)).set_complete()

        if row < len(self.ui.splits_list):
            for i in range(row, len(self.ui.splits_list)):
                self.ui.splits_list.itemWidget(self.ui.splits_list.item(i)).set_not_active()
            #
            self.ui.splits_list.setCurrentRow(row)
            selected_item = self.ui.splits_list.selectedItems()[0]
            self.ui.splits_list.itemWidget(selected_item).set_active()
            self.ui.splits_list.scrollToItem(selected_item, QAbstractItemView.PositionAtCenter)
        else:
            self.ui.splits_list.clearSelection()

        try:
            self.ui.page_dashboard_split_components_preview_scroll.set_components(
                RouteHandler.route.splits[row].components)
        except:
            pass

    def reset_splits(self):
        self.ui.page_dashboard_split_components_preview_scroll.clear()
        self.ui.page_dashboard_moon_count_widget.rpb_set_value(0)
        self.ui.page_dashboard_moon_count_widget.rpb_set_range(0, 0)
        self.ui.page_dashboard_activations_widget.rpb_set_value(0)
        self.ui.page_dashboard_activations_widget.rpb_set_range(0, 0)

        for i in range(len(self.ui.splits_list)):
            self.ui.splits_list.itemWidget(self.ui.splits_list.item(i)).set_not_active()

        self.ui.splits_list.clearSelection()

        if self.reload_splits:
            self.reload_splits = False
            self.route_updated()

    def route_updated(self):
        if self.autosplitter.run_started:
            self.reload_splits = True
            return
        else:
            self.autosplitter.wait_for_first_split = False

        self.clear_splits()

        if RouteHandler.route is not None:
            self.add_splits(RouteHandler.route.splits)
