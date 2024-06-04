import gettext

from nion.typeshed import API_1_0 as API
from nion.swift.model import Notification
from nion.swift.model import PlugInManager

_ = gettext.gettext


class MenuItemDelegate:

    def __init__(self, api: API) -> None:
        self.__api = api
        self.menu_id = "example_menu"  # required, specify menu_id where this item will go
        self.menu_name = _("Examples")  # optional, specify default name if not a standard menu
        self.menu_before_id = "window_menu"  # optional, specify before menu_id if not a standard menu
        self.menu_item_name = _("Example Menu Item")  # menu item name

    def close(self) -> None:
        # close will be called if the extension is unloaded.
        pass

    def menu_item_execute(self, document_window: API.DocumentWindow) -> None:
        """This function will be called when a user clicks on the menu item.

        This example will just show a notification, but normally you would call some function with a custom
        processing or data acquisition routine.
        """
        Notification.notify(Notification.Notification('nion.examples.info', '\N{INFORMATION SOURCE} MenuExample',
                                                      'Example Message', 'MenuExample was executed.'))


class MenuExampleExtension:

    # required for Swift to recognize this as an extension class.
    extension_id = "nion.swift.examples.menu_example"

    def __init__(self, api_broker: PlugInManager.APIBroker) -> None:
        # grab the api object.
        api = api_broker.get_api(version="1", ui_version="1")
        # be sure to keep a reference or it will be closed immediately.
        self.__menu_item_ref = api.create_menu_item(MenuItemDelegate(api))

    def close(self) -> None:
        # close will be called when the extension is unloaded. in turn, close any references so they get closed. this
        # is not strictly necessary since the references will be deleted naturally when this object is deleted.
        self.__menu_item_ref.close()
        self.__menu_item_ref = None
