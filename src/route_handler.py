import xml.etree.ElementTree as ElementTree
import jsonschema
import logging
import copy
import json
import os

from PyQt5.QtWidgets import QFileDialog
from typing import List

from src.config import Config
from ui.popup_ui import *


class RouteHandler:
    route_updated = None

    route_path = ""
    route = None
    rollback = None

    unsaved_popup = None
    save_warning_popup = None
    ignore_unsaved = False

    @staticmethod
    def load_route_btn():
        if RouteHandler.check_unsaved_changes():
            def save_and_load():
                RouteHandler.save_route(RouteHandler.route_path)
                file_path = RouteHandler.open_file()

                if file_path is not None:
                    RouteHandler.load_route(file_path)

            def load_without_saving():
                file_path = RouteHandler.open_file()

                if file_path is not None:
                    RouteHandler.load_route(file_path)

            RouteHandler.unsaved_popup = UnsavedChangesPopup()
            RouteHandler.unsaved_popup.sig_clicked_yes.connect(save_and_load)
            RouteHandler.unsaved_popup.sig_clicked_no.connect(load_without_saving)
            RouteHandler.unsaved_popup.show()
        else:
            file_path = RouteHandler.open_file()

            if file_path is not None:
                RouteHandler.load_route(file_path)

    @staticmethod
    def validate_route(json_data):
        schema = {
            "type": "object",
            "properties": {
                "version": {"type": "string"},
                "name": {"type": "string"},
                "start_condition": {"type": "string"},
                "splits": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "type": {"type": "string"},
                            "components": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "activations": {"type": "integer"},
                                        "min_moon_count": {"type": "integer"},
                                    },
                                    "required": ["name", "activations", "min_moon_count"]
                                }
                            },
                        },
                        "required": ["name", "type", "components"]
                    }
                },
            },
            "required": ["version", "name", "start_condition", "splits"]
        }

        try:
            jsonschema.validate(instance=json_data, schema=schema)
        except Exception as e:
            print("JSON schema validation failed")
            return False
        else:
            return True

    @staticmethod
    def save_route_btn():
        if os.path.splitext(RouteHandler.route_path)[1] == ".lss":
            RouteHandler.save_route_as_btn()
        RouteHandler.save_route(RouteHandler.route_path)

    @staticmethod
    def save_route_as_btn():
        file_path = RouteHandler.open_file(save=True)

        if RouteHandler.route is None:
            RouteHandler.route = Route()

        if file_path is not None:
            RouteHandler.save_route(file_path)
            RouteHandler.route_path = file_path

    @staticmethod
    def close_route_btn():
        if RouteHandler.check_unsaved_changes():
            def save_and_close():
                RouteHandler.save_route(RouteHandler.route_path)
                RouteHandler.close_route()

            def close_without_saving():
                RouteHandler.close_route()

            RouteHandler.unsaved_popup = UnsavedChangesPopup()
            RouteHandler.unsaved_popup.sig_clicked_yes.connect(save_and_close)
            RouteHandler.unsaved_popup.sig_clicked_no.connect(close_without_saving)
            RouteHandler.unsaved_popup.show()
        else:
            RouteHandler.close_route()

    @staticmethod
    def window_close_btn(main_window):
        def save_and_close():
            RouteHandler.save_route(RouteHandler.route_path)
            main_window.close()

        def close_without_saving():
            RouteHandler.ignore_unsaved = True
            main_window.close()

        RouteHandler.unsaved_popup = UnsavedChangesPopup()
        RouteHandler.unsaved_popup.sig_clicked_yes.connect(save_and_close)
        RouteHandler.unsaved_popup.sig_clicked_no.connect(close_without_saving)
        RouteHandler.unsaved_popup.show()

    @staticmethod
    def load_route(path):
        if path == "":
            return

        if path.endswith(".lss"):
            RouteHandler.load_livesplit_splits(path)
            return

        print(f"loading route: {path}")
        try:
            with open(path, "r") as file:
                route_object = json.load(file)
        except Exception as e:
            logging.exception(e)
            return

        val_success = RouteHandler.validate_route(route_object)

        if not val_success:
            load_failed_popup = RouteLoadFailedPopup()
            load_failed_popup.show()
        else:
            RouteHandler.route_path = path
            RouteHandler.route = RouteHandler.parse_route(route_object)
            RouteHandler.rollback = copy.deepcopy(RouteHandler.route)
            RouteHandler.route_updated()
            Config.set_key("current_route", path)

    @staticmethod
    def save_route(path):
        if not RouteHandler.route:
            logging.warning("No route is currently loaded")
            return

        print(path)
        print(os.path.dirname(__file__)[:-4].replace("\\", "/"))
        if path.startswith(os.path.dirname(__file__)[:-4].replace("\\", "/")):
            print("In Install Dir")
            RouteHandler.save_warning_popup = RouteSaveWarningPopup()
            RouteHandler.save_warning_popup.show()

        if os.path.splitext(path)[1] == ".smo":
            try:
                RouteHandler.route.name = os.path.splitext(path)[0].split('/')[-1]
                with open(path + "tmp", "w") as file:
                    json.dump(RouteHandler.serialize_route(RouteHandler.route), file, indent=4)
                    file.flush()
                    os.fsync(file)
                os.replace(path + "tmp", path)
                RouteHandler.rollback = copy.deepcopy(RouteHandler.route)
            except Exception as e:
                logging.exception(e)
                os.remove(path + "tmp")
                return
        else:
            logging.warning(f"Invalid route path \"{path}\"")
            return

        RouteHandler.route_updated()
        Config.set_key("current_route", path)

    @staticmethod
    def close_route():
        RouteHandler.route = None
        RouteHandler.rollback = None
        RouteHandler.route_path = ""
        RouteHandler.route_updated()
        Config.set_key("current_route", "")

    @staticmethod
    def load_livesplit_splits(path):
        tree = ElementTree.parse(path)
        root = tree.getroot()

        RouteHandler.route = Route(Config.version, os.path.splitext(path)[0].split('/')[-1], "", [])

        splits = []
        subsplits = []
        for element in root.findall('.//Segment/Name'):
            if element.text.startswith("-"):
                subsplits.append(element.text[1:])
            elif element.text.startswith("{"):
                subsplit_title = element.text[1:][:element.text.find("}") - 1]
                subsplits.append(element.text[element.text.find("}") + 1:])
                for split in subsplits:
                    splits.append(subsplit_title + " " + split)
                subsplits.clear()
            else:
                splits.append(element.text)

        for split in splits:
            RouteHandler.route.splits.append(Split(split, "", []))

        RouteHandler.route_path = path
        RouteHandler.rollback = copy.deepcopy(RouteHandler.route)
        RouteHandler.route_updated()
        Config.set_key("current_route", path)

    @staticmethod
    def check_unsaved_changes():
        if RouteHandler.ignore_unsaved:
            RouteHandler.ignore_unsaved = False
            return False

        if RouteHandler.route is None or RouteHandler.rollback is None:
            return False

        route_dict = RouteHandler.serialize_route(RouteHandler.route)
        rollback_dict = RouteHandler.serialize_route(RouteHandler.rollback)

        return route_dict != rollback_dict

    @staticmethod
    def parse_route(route_object):
        version = RouteHandler.get_key(route_object, "version")
        name = RouteHandler.get_key(route_object, "name")
        start_condition = RouteHandler.get_key(route_object, "start_condition")
        splits_object = RouteHandler.get_key(route_object, "splits")

        splits = []
        for split in splits_object:
            components_object = RouteHandler.get_key(split, "components")
            components = []
            for component in components_object:
                component_name = RouteHandler.get_key(component, "name")
                component_activations = RouteHandler.get_key(component, "activations")
                component_min_moons = RouteHandler.get_key(component, "min_moon_count")

                components.append(Component(component_name, component_activations, component_min_moons))

            split_name = RouteHandler.get_key(split, "name")
            split_type = RouteHandler.get_key(split, "type")
            split_components = components
            split_split = RouteHandler.get_key(split, "split")
            split_reset_moon_count = RouteHandler.get_key(split, "reset_moon_count")

            splits.append(Split(split_name, split_type, split_components, split_split, split_reset_moon_count))

        return Route(version, name, start_condition, splits)

    @staticmethod
    def serialize_route(route_object):
        splits = []
        for split in route_object.splits:
            components = []
            for component in split.components:
                component_dict = {
                    "name": component.name,
                    "activations": component.activations,
                    "min_moon_count": component.min_moons
                }
                components.append(component_dict)

            split_dict = {
                "name": split.name,
                "type": split.type,
                "components": components,
                "split": split.split,
                "reset_moon_count": split.reset_moon_count
            }
            splits.append(split_dict)

        route_dict = {
            "version": route_object.version,
            "name": route_object.name,
            "start_condition": route_object.start_condition,
            "splits": splits
        }
        return route_dict

    @staticmethod
    def get_key(json_object, key):
        if not json_object or not key:
            return None

        try:
            if key in json_object:
                return json_object[key]
            else:
                logging.warning(f"Key \"{key}\" not found in route")
                return None
        except Exception as e:
            logging.exception(e)
            return None

    @staticmethod
    def open_file(save=False):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setDirectory(os.path.dirname(RouteHandler.route_path))

        if save:
            file_dialog.setNameFilters(["SMO AutoSplit Route (*.smo)"])
            file_dialog.selectNameFilter("SMO AutoSplit Route (*.smo)")
        else:
            file_dialog.setNameFilters(["All Supported Files (*.smo *.lss)", "SMO AutoSplit Route (*.smo)",
                                        "LiveSplit Splits (*.lss)"])
            file_dialog.selectNameFilter("All Supported Files (*.smo *.lss)")

        if save:
            file_dialog.setWindowTitle("Save Route")
            file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        else:
            file_dialog.setWindowTitle("Load Route")

        if file_dialog.exec_():
            return file_dialog.selectedFiles()[0]
        else:
            return None


class Component:
    def __init__(self, name: str, activations: int = 1, min_moons: int = 0):
        self.name: str = name
        self.activations: int = activations
        self.min_moons: int = min_moons


class Split:
    def __init__(self, name: str, type: str, components: List[Component], split: bool = True,
                 reset_moon_count: bool = True):
        self.name: str = name
        self.type: str = type
        self.components: List[Component] = components
        self.split: bool = split
        self.reset_moon_count: bool = reset_moon_count


class Route:
    def __init__(self, version=Config.version, name: str = "", start_condition: str = None, splits: List[Split] = None):
        self.version: str = Config.version
        self.name: str = name
        self.start_condition: str = start_condition
        self.splits: List[Split] = splits
