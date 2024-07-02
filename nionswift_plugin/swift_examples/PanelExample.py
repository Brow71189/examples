# standard libraries
import gettext
import typing

# third party libraries
# None

# local libraries
from nion.swift.model import PlugInManager
from nion.ui import Declarative
from nion.utils import Converter
from nion.utils import Event
from nion.swift import Panel
from nion.swift import DocumentController
from nion.swift import Workspace

_ = gettext.gettext


class ExamplePanelUIHandler(Declarative.HandlerLike):

    def __init__(self):
        self.ui_view = typing.cast(Declarative.UIDescription, None)
        self.property_changed_event = Event.Event()
        self.integer_to_string_converter = Converter.IntegerToStringConverter()
        self.__click_count = 0
        self.__line_edit_text = ""
        self.__reverted_line_edit_text = ""
        self.__radio_button_index = 3

    def close(self) -> None:
        pass

    @property
    def click_count(self) -> int:
        return self.__click_count

    @click_count.setter
    def click_count(self, count: int) -> None:
        self.__click_count = count
        self.property_changed_event.fire("click_count")

    def button_clicked(self, widget: Declarative.UIWidget) -> None:
        self.click_count += 1

    @property
    def line_edit_text(self) -> str:
        return self.__line_edit_text

    @line_edit_text.setter
    def line_edit_text(self, text: str) -> None:
        self.__line_edit_text = text
        self.property_changed_event.fire("line_edit_text")
        self.property_changed_event.fire("line_edit_reverse_text")

    @property
    def line_edit_reverse_text(self) -> str:
        return self.__line_edit_text[::-1]

    @property
    def radio_button_index(self) -> int:
        return self.__radio_button_index

    @radio_button_index.setter
    def radio_button_index(self, index: int) -> None:
        self.__radio_button_index = index
        self.property_changed_event.fire('radio_button_index')

    def move_left_clicked(self, widget: Declarative.UIWidget) -> None:
        if self.radio_button_index > 0:
            self.radio_button_index -= 1

    def move_right_clicked(self, widget: Declarative.UIWidget) -> None:
        if self.radio_button_index < 6:
            self.radio_button_index += 1



class ExampleUI:

    def get_ui_handler(self) -> Declarative.HandlerLike:
        handler = ExamplePanelUIHandler()
        handler.ui_view = self.__create_ui_view()
        return handler

    def __create_ui_view(self) -> Declarative.UIDescription:
        ui = Declarative.DeclarativeUI()
        button = ui.create_push_button(text=_("Click me"), on_clicked="button_clicked")
        label = ui.create_label(text='@binding(click_count, converter=integer_to_string_converter)')
        row = ui.create_row(button, label, ui.create_stretch(), spacing=5)
        line_edit = ui.create_line_edit(text='@binding(line_edit_text)')
        reverted_label = ui.create_label(text='@binding(line_edit_reverse_text)')
        radio_buttons = [ui.create_radio_button(value=i, group_value='@binding(radio_button_index)') for i in range(7)]
        radio_buttons_row = ui.create_row(*radio_buttons, spacing=5, margin=5)
        move_left_button = ui.create_push_button(text='<-', on_clicked='move_left_clicked')
        index_label = ui.create_label(text='@binding(radio_button_index, converter=integer_to_string_converter)')
        move_right_button = ui.create_push_button(text='->', on_clicked='move_right_clicked')
        move_row = ui.create_row(move_left_button, ui.create_stretch(), index_label, ui.create_stretch(), move_right_button, ui.create_stretch(), spacing=5, margin=5)
        column = ui.create_column(row, line_edit, reverted_label, radio_buttons_row, move_row, ui.create_stretch(), spacing=5, margin=5)
        return column


class ExamplePanel(Panel.Panel):

    def __init__(self, document_controller: DocumentController.DocumentController, panel_id: str, properties: typing.Mapping[str, typing.Any]) -> None:
        super().__init__(document_controller, panel_id, "example-panel")
        self.widget = Declarative.DeclarativeWidget(document_controller.ui, document_controller.event_loop, ExampleUI().get_ui_handler())


class PanelExampleExtension:

    # required for Swift to recognize this as an extension class.
    extension_id = "nion.swift.examples.panel_example"

    def __init__(self, api_broker: PlugInManager.APIBroker) -> None:
        Workspace.WorkspaceManager().register_panel(ExamplePanel, "example-panel", _("Example Panel"), ["left", "right"], "right")

    def close(self):
        pass
