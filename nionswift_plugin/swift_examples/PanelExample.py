# standard libraries
import gettext
import logging
import threading
import time

# third party libraries
# None

# local libraries
# None

_ = gettext.gettext


class PanelExampleDelegate:

    def __init__(self, api):
        self.__api = api
        self.panel_id = "example-panel"
        self.panel_name = _("Example")
        self.panel_positions = ["left", "right"]
        self.panel_position = "right"

    def create_panel_widget(self, ui, document_controller):
        column = ui.create_column_widget()

        edit_row = ui.create_row_widget()
        edit_row.add(ui.create_label_widget(_("Edit Field")))
        edit_row.add_spacing(12)
        edit_line_edit = ui.create_line_edit_widget()
        def editing_finished(text):
            logging.info(text)
            edit_line_edit.request_refocus()
        edit_line_edit.on_editing_finished = editing_finished
        edit_row.add(edit_line_edit)
        edit_row.add_stretch()

        button_row = ui.create_row_widget()
        button_widget = ui.create_push_button_widget(_("Push Me"))
        def button_clicked():
            edit_line_edit.text = str()
        button_widget.on_clicked = button_clicked
        button_row.add(button_widget)
        button_row.add_stretch()

        label_row = ui.create_row_widget()
        label = ui.create_label_widget(_("Time: "))
        time_label = ui.create_label_widget(time.strftime("%H:%M:%S"))
        label_row.add(label)
        label_row.add(time_label)
        label_row.add_stretch()

        column.add_spacing(8)
        column.add(edit_row)
        column.add(button_row)
        column.add_spacing(8)
        column.add(label_row)
        column.add_spacing(8)
        column.add_stretch()

        def update_time_label():
            time.sleep(5)
            while True:
                def do_update():
                    time_label.text = time.strftime("%H:%M:%S")
                self.__api.queue_task(do_update)
                time.sleep(1)

        threading.Thread(target=update_time_label).start()

        return column


class PanelExampleExtension(object):

    # required for Swift to recognize this as an extension class.
    extension_id = "nion.swift.examples.panel_example"

    def __init__(self, api_broker):
        # grab the api object.
        api = api_broker.get_api(version="1", ui_version="1")
        # be sure to keep a reference or it will be closed immediately.
        self.__panel_ref = api.create_panel(PanelExampleDelegate(api))

    def close(self):
        # close will be called when the extension is unloaded. in turn, close any references so they get closed. this
        # is not strictly necessary since the references will be deleted naturally when this object is deleted.
        self.__panel_ref.close()
        self.__panel_ref = None
