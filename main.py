import pygtk
import os
import logging, sys
import gtk

pygtk.require('2.0')

# ===DEBUGGING SETTINGS===
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


# ===DEBUGGING SETTINGS===

class AcademicProgram:
    courses = []

    def add_course(self, widget):  # This method adds the course name and weeks to the table
        coursenameText = self.coursenameField.get_text()
        weeksText = self.weeksField.get_text()

        self.courses.append(coursenameText + ":" + weeksText)

        logging.debug("\n" + "Added: " + coursenameText + "," + " Weeks: " + str(weeksText))

    def check_path(self, widget):
       location_directory = self.browseLocationField.get_text()

        if not os.path.exists(location_directory):
            logging.debug('Path not found: ' + location_directory)
            # NEEDS TO BE DIALOG WARNING NO DIR FOUND
        else:
            logging.debug('Path exists: ' + location_directory)
            self.split_list(location_directory)  # will need to send list of course name and week

    def split_list(self, location_directory):
        self.subjectList = []

        for split in self.courses:
            courses = split.split(':')
            self.subjectList.append(courses[0])
            week = courses[1]
            self.create_folder(self.subjectList, week, location_directory)

    def create_folder(self, subject, week, folder):  # Creates the folder for each subject with the inputted week files
        for courses in subject:
            path = folder + "\\" + courses
            if not os.path.exists(path):
                os.makedirs(path)

            for weeks in range(1, int(week) + 1):
                path = folder + "\\" + courses + "\\Week " + str(weeks)

                if not os.path.exists(path):
                    os.makedirs(path)
                    logging.debug("Created subfolder for " + courses + " for week " + str(weeks))
        self.subjectList.pop(0)
    def __init__(self):
        # Create a new window
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Academic Folder Setup")
        window.connect("destroy", lambda d: gtk.main_quit())
        window.set_size_request(600, 400)

        fixed = gtk.Fixed()
        window.add(fixed)
        fixed.show()

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