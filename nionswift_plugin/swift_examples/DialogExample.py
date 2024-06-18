# standard libraries
import gettext
import typing

from nion.ui import Dialog, UserInterface

# third party libraries
# None

# local libraries
from nion.ui import Declarative
from nion.utils import Converter
from nion.utils import Event
from nion.typeshed import API_1_0 as API
from nion.swift import DocumentController

_ = gettext.gettext


class ExamplePanelUIHandler(Declarative.HandlerLike):

    def __init__(self):
        self.ui_view = typing.cast(Declarative.UIDescription, None)
        self.property_changed_event = Event.Event()
        self.integer_to_string_converter = Converter.IntegerToStringConverter()
        self.__click_count = 0
        self.__line_edit_text = ""
        self.__reverted_line_edit_text = ""

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
        column = ui.create_column(row, line_edit, reverted_label, ui.create_stretch(), spacing=5, margin=5)
        return column


class ExampleDialog(Dialog.ActionDialog):
        """
        Create a modeless dialog that always stays on top of the UI by default (can be controlled with the
        parameter 'window_style').

        Parameters:
        -----------
        ui : An instance of nion.ui.UserInterface, required.
        on_accept : callable, optional.
            This method will be called when the user clicks 'OK'
        on_reject : callable, optional.
            This method will be called when the user clicks 'Cancel' or the 'X'-button
        include_ok : bool, optional
            Whether to include the 'OK' button.
        include_cancel : bool, optional
            Whether to include the 'Cancel' button.
        window_style : str, optional
            Pass in 'dialog' here if you want the Dialog to move into the background when clicking outside
            of it. The default value 'tool' will cause it to always stay on top of Swift.
        """
        def __init__(self,
                     document_controller: DocumentController.DocumentController, *,
                     include_ok: bool=True,
                     include_cancel: bool=True,
                     window_style: typing.Optional[str]=None):

            super().__init__(document_controller.ui, window_style=window_style)

            def on_ok_clicked():
                print('OK clicked')
                # Return 'True' to tell Swift to close the Dialog
                return True

            if include_ok:
                self.add_button('OK', on_ok_clicked)

            def on_cancel_clicked():
                print('Cancel clicked')
                # Return 'True' to tell Swift to close the Dialog
                return True

            if include_cancel:
                self.add_button('Cancel', on_cancel_clicked)

            self.content.add(Declarative.DeclarativeWidget(document_controller.ui, document_controller.event_loop, ExampleUI().get_ui_handler()))


class MenuItemDelegate:

    def __init__(self, api: API) -> None:
        self.__api = api
        self.menu_id = "example_menu"  # required, specify menu_id where this item will go
        self.menu_name = _("Examples")  # optional, specify default name if not a standard menu
        self.menu_before_id = "window_menu"  # optional, specify before menu_id if not a standard menu
        self.menu_item_name = _("Example Dialog")  # menu item name

        self.__action_dialog_open = False

    def close(self) -> None:
        # close will be called if the extension is unloaded.
        pass

    def menu_item_execute(self, document_window: API.DocumentWindow) -> None:
        """This function will be called when a user clicks on the menu item.

        We use a menu item to launch the dialog here, but you could also do that from a button in a panel or any other
        function.
        """
        # We track open dialogs to ensure that only one dialog can be open at a time
        if not self.__action_dialog_open:
            document_controller = document_window._document_controller
            self.__action_dialog_open = True

            dialog = ExampleDialog(document_controller)
            # Add a listener to the dialog close event to perform some cleanup actions.
            def wc(w: typing.Any) -> None:
                self.__action_dialog_open = False
                self.__dialog_close_listener = typing.cast(Event.EventListener, None)
            self.__dialog_close_listener = dialog._window_close_event.listen(wc)

            dialog.show()


class DialogExampleExtension(object):

    # required for Swift to recognize this as an extension class.
    extension_id = "nion.swift.examples.dialog_example"

    def __init__(self, api_broker):
        # grab the api object.
        api = api_broker.get_api(version="1", ui_version="1")
        # be sure to keep a reference or it will be closed immediately.
        self.__menu_item_ref = api.create_menu_item(MenuItemDelegate(api))

    def close(self) -> None:
        # close will be called when the extension is unloaded. in turn, close any references so they get closed. this
        # is not strictly necessary since the references will be deleted naturally when this object is deleted.
        self.__menu_item_ref.close()
        self.__menu_item_ref = None
