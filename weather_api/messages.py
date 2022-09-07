import tkinter.messagebox as mb


def get_manual():
    mb.showinfo("Manual", "Welcome to the Weather API Application Manual!\n"
                          "This application will show you the weather in selected cities or at given coordinates.\n"
                          "To search for information about the weather in one of the cities, select this city in the"
                          " drop-down list. The data itself will appear in the text box below.\n"
                          "To search for weather information by coordinates, enter the latitude of the place you are"
                          " looking for in the 'Latitude' field, and its longitude in the 'Longitude' field. Click on"
                          " the 'Search' button and enjoy the result given in the text field.\n"
                          "To save a place in the drop-down list, enter the coordinates, Click on"
                          " the 'Search' button, next click on the settings button, and then on the 'Add place' button."
                          "If the location has been successfully added, a notification will appear.\n"
                          "To remove a place from the list, select the"
                          " place from the list and press the 'Delete' button.\n"
                          "If the deletion was successful, a notification will appear.\n"
                          "Restart the program and enjoy the result.")


def show_mb(string):
    mb.showinfo("Information", f"Your data has been successfully {string}")


def show_err(ex):
    mb.showerror("Error", ex)
