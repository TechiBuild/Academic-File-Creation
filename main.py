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

    def check_path(self, widget):
        location_directory = self.browseLocationField.get_text()

        if not os.path.exists(location_directory):
            logging.debug('Path not found: ' + location_directory)
            # NEEDS TO BE DIALOG WARNING NO DIR FOUND
        else:
            logging.debug('Path exists: ' + location_directory)
            self.create_folder(location_directory)

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

        for a, b in self.course_week.iteritems():
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

    def setup_tree_view(self):
        pass

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
        button = gtk.Button("Add")
        button.connect("clicked", self.add_course)
        fixed.put(button, 178, 140)
        button.show()

        # Browse Location Text Field
        self.browseLocationField = gtk.Entry(max=0)
        fixed.put(self.browseLocationField, 50, 250)
        self.browseLocationField.show()

        # Browse Location Label
        weeksLabel = gtk.Label(str)
        fixed.put(weeksLabel, 50, 230)
        weeksLabel.set_text("File Creation Location")
        weeksLabel.show()

        # Create Button
        button = gtk.Button("Create Folders")
        button.connect("clicked", self.check_path)
        fixed.put(button, 125, 290)
        button.show()

        # Display the window
        window.show()


def main():
    gtk.main()
    return 0


if __name__ == "__main__":
    AcademicProgram()
    main()
