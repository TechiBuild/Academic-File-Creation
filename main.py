import pygtk
import os
import logging, sys
import gtk

pygtk.require('2.0')

# ===DEBUGGING SETTINGS===
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


# ===DEBUGGING SETTINGS===

class AcademicProgram:
    course_week = {}  # Holds the course name and weeks in the dictionary type
    checker = []

    def add_course(self, widget):  # This method adds the course name and weeks to the table
        coursenameText = self.coursenameField.get_text()
        weeksText = self.weeksField.get_text()

        self.course_week[coursenameText] = weeksText  # Adds coursename as the key and weeks as the value to a dictionary
        logging.debug("\n" + "Added: " + coursenameText + "," + " Weeks: " + str(weeksText))

        self.tree_view(False)
        self.checker.append(coursenameText)

    def grab_path(self, widget):
        path_dialog = gtk.FileChooserDialog("Open..",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        path_dialog.set_default_response(gtk.RESPONSE_OK)
        response = path_dialog.run()

        if response == gtk.RESPONSE_OK:
            print path_dialog.get_filename(), 'selected'
            self.browseLocationLabel.set_text(path_dialog.get_filename())
            self.location_directory = path_dialog.get_filename()
            path_dialog.destroy()

        elif response == gtk.RESPONSE_CANCEL:
            path_dialog.destroy()

    def check_path(self, widget):
        if not os.path.exists(self.location_directory):
            logging.debug('Path not found: ' + self.location_directory)
            # NEEDS TO BE DIALOG WARNING NO DIR FOUND
        else:
            logging.debug('Path exists: ' + self.location_directory)
            self.create_folder(self.location_directory)

    def create_folder(self, folder):  # Creates the folder for each subject with the inputted week files
        for course, week in self.course_week.iteritems():
            path = folder + "\\" + course
            if not os.path.exists(path):
                os.makedirs(path)

            for weeks in range(1, int(week) + 1):
                path = folder + "\\" + course + "\\Week " + str(weeks)

                if not os.path.exists(path):
                    os.makedirs(path)
                    logging.debug("Created subfolder for " + course + " for week " + str(weeks))

    def tree_view(self, action):

        for a in self.course_week.iteritems():
            if a in self.checker:
                print("Course name already exists")
            else:
                self.course_week_list_store.clear()
                self.data_tree = [(a, b) for a, b in self.course_week.iteritems()]

                for item in self.data_tree:
                    self.course_week_list_store.append(list(item))
                    self.course_week_tree_view = gtk.TreeView(self.course_week_list_store)

                    for i, column_names in enumerate(["Course Name", "Weeks"]):
                        self.render_cell = gtk.CellRendererText()

                        self.column = gtk.TreeViewColumn(column_names, self.render_cell, text=i)

                        self.course_week_tree_view.append_column(self.column)

                    print(self.data_tree)

    def __init__(self):
        # Create a new window
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Academic Folder Setup")
        window.connect("destroy", lambda d: gtk.main_quit())
        window.set_size_request(600, 400)

        fixed = gtk.Fixed()
        window.add(fixed)
        fixed.show()

        # Tree View
        self.data_tree = ()
        self.course_week_list_store = gtk.ListStore(str, str)
        self.course_week_tree_view = gtk.TreeView(self.course_week_list_store)

        for i, column_names in enumerate(["Course Name", "Weeks"]):
            self.render_cell = gtk.CellRendererText()

            self.column = gtk.TreeViewColumn(column_names, self.render_cell, text=i)

            self.course_week_tree_view.append_column(self.column)

        fixed.put(self.course_week_tree_view, 300, 40)
        self.course_week_tree_view.show()

        # Course Name Label
        coursenameLabel = gtk.Label(str)
        fixed.put(coursenameLabel, 50, 25)
        coursenameLabel.set_text("Course name")
        coursenameLabel.show()

        # Course Name Text Field
        self.coursenameField = gtk.Entry(max=0)
        fixed.put(self.coursenameField, 50, 50)
        self.coursenameField.show()

        # Weeks Label
        weeksLabel = gtk.Label(str)
        fixed.put(weeksLabel, 50, 80)
        weeksLabel.set_text("Weeks")
        weeksLabel.show()

        # Weeks Text Field
        self.weeksField = gtk.Entry(max=2)
        fixed.put(self.weeksField, 50, 100)
        self.weeksField.show()

        # Add Button
        add_button = gtk.Button("Add")
        add_button.connect("clicked", self.add_course)
        fixed.put(add_button, 50, 140)
        add_button.show()

        # Browse Location Label
        self.browseLocationLabel = gtk.Label(str)
        fixed.put(self.browseLocationLabel, 50, 230)
        self.browseLocationLabel.set_text("")
        self.browseLocationLabel.show()

        # Create Button
        folder_button = gtk.Button("Select Folder Location")
        folder_button.connect("clicked", self.grab_path)
        fixed.put(folder_button, 50, 200)
        folder_button.show()

        # Create Button
        create_button = gtk.Button("Create Folders")
        create_button.connect("clicked", self.check_path)
        fixed.put(create_button, 50, 290)
        create_button.show()

        # Display the window
        window.show()


def main():
    gtk.main()
    return 0


if __name__ == "__main__":
    AcademicProgram()
    main()
