# Imports library for GUI and Message box.
import tkinter as TK
from tkinter import messagebox

# Creates the class for the GUI, allowing all of its objects and attributes to be acted upon properly.
class Gradebook_Calculator:
    def __init__(self, root):
        self.root = root

    # Checks if the user has used the program before and skips the intro and instructions.
    def Returning_User_Check(self):

        # Reads config file to check user status.
        self.config = open('GBC_Config.txt', 'a+')
        self.config.seek(0)
        self.returning_user = self.config.readline()

        # First time user is sent through whole path and returning users are sent to main page.
        if self.returning_user != 'Returning':
            self.returning = False
            self.config.write('Returning')
            self.config.close()
            self.Get_Started()
            
        elif self.returning_user == 'Returning':
            self.returning = True
            self.Create_Gradebook()

    # Creates the first window.
    def Get_Started(self):

        # Moves to second page
        self.get_started = TK.Button(self.root, text='Get Started', command=self.Intro)
        self.get_started.pack()

    # Creates the instructions page.
    def Intro(self):
        
        # Removes the first page.
        self.get_started.destroy()

        # Auto maximizes the window.
        self.root.state('zoomed')

        # Pulls up the instructions.
        self.gradebook_instructions_intro = open('GBC_Instructions.txt', 'r')
        self.temp_GB_I_I = self.gradebook_instructions_intro.read()
        self.gradebook_instructions_intro.close()
        
        self.introduction = TK.Label(self.root, text=self.temp_GB_I_I)
        self.introduction.pack()
        
        # Moves to the next page.
        self.start_working = TK.Button(self.root, text='Start', command=self.Create_Gradebook)
        self.start_working.pack()

        self.config = open('GBC_Config.txt', 'w')
        self.temp_config = self.config.write('Returning')

    ''' Creates the space for the grade book, establishes the buttons for: pulling up reference instructions, adding a class cell, removing a class cell, 
    and calculating grades. This also allows the grade book to adapt to any screen size, and creates most of the variables to be used later.'''
    def Create_Gradebook(self):
        
        # Removes the previous page if user is first time.
        if self.returning == False:
            self.introduction.destroy()
            self.start_working.destroy()

        if self.returning == True:
            self.root.state('zoomed')

        # Creates function buttons.
        self.instructions_button = TK.Button(self.root, text='Instructions', command=self.Instructions)
        self.instructions_button.grid(row=0, column=0)

        self.add_class_button = TK.Button(self.root, text='Add Class', command=self.Add_Class)
        self.add_class_button.grid(row=0, column=1)

        self.remove_class_button = TK.Button(self.root, text='Remove Class', command=self.Remove_Class)
        self.remove_class_button.grid(row=0, column=2)

        self.calculate_button = TK.Button(self.root, text='Calculate Average', command=self.Calculate)
        self.calculate_button.grid(row=0, column=3)

        # Adapts GUI for any screen.
        for c in range(13):
            root.grid_columnconfigure(c, weight=1)
        for r in range(45):
            root.grid_rowconfigure(r, weight=1)

        # Variables for the one per class cell.
        self.class_name_labels = list()
        self.names_of_classes = list()
        self.category_name_labels = list()
        self.category_value_labels = list()
        self.category_average_labels = list()
        self.column_spacers = list()
        
        # Variables for the ten per class cell.
        self.names_of_categories = list()
        self.values_of_categories = list()
        self.category_grades = list()
        self.row_spacers = list()

        # Counts the number of classes and the cells within the class. 
        self.class_cell_counter = 0
        self.cell_counter = 0

        # Places the widgets in the proper location by tracking current row and column.
        self.grid_tracker_row = 0
        self.grid_tracker_column = 0

        # Is used to see if a calculation has been performed or not.
        self.calculated = False
        self.all_calculated = False

        # Variables for calculating and displaying averages.
        self.class_averages = list()
        self.averages_of_classes = list()

    # Pulls up the instructions in a separate window for reference.    
    def Instructions(self):

        self.gradebook_instructions = open('GBC_Instructions.txt', 'r')
        self.temp_GB_I = self.gradebook_instructions.read()
        self.gradebook_instructions.close()

        self.instructions_window = TK.Toplevel()
        self.instructions_window.title('Instructions')

        self.instructions = TK.Label(self.instructions_window, text=self.temp_GB_I)
        self.instructions.pack()

        self.close_instructions = TK.Button(self.instructions_window, text='Dismiss', command=self.instructions_window.destroy)
        self.close_instructions.pack()

        self.instructions_window.mainloop()    

 
    '''Adds a class(A class includes a name label with one name entry, a category name label with up to ten category name entries, a category value label 
    with up to ten category value entries, a category average label with ten category average entries. Also included are blank column, and row labels to 
    space and organize the grade book.)'''  
    def Add_Class(self):

        # Tells user about the class limit.
        if self.class_cell_counter == 9:
            self.class_limit_max = TK.messagebox.showinfo('', 'You may only have nine classes.')

        else:
            
            # Creates the one per class widgets.
            self.class_name_label = TK.Label(self.root, text='Class Name')
            self.class_name_label.grid(row=(1 + self.grid_tracker_row), column=(2 + self.grid_tracker_column))
            self.class_name_labels.append(self.class_name_label)
            
            self.name_of_class = TK.Entry(self.root)
            self.name_of_class.grid(row=(2 + self.grid_tracker_row), column=(2 + self.grid_tracker_column))
            self.names_of_classes.append(self.name_of_class)
            
            self.category_name_label = TK.Label(self.root, text='Category Name')
            self.category_name_label.grid(row=(3 + self.grid_tracker_row), column=(1 + self.grid_tracker_column))
            self.category_name_labels.append(self.category_name_label)

            self.category_value_label = TK.Label(self.root, text='Category Value')
            self.category_value_label.grid(row=(3 + self.grid_tracker_row), column=(2 + self.grid_tracker_column))
            self.category_value_labels.append(self.category_value_label)

            self.category_average_label = TK.Label(self.root, text='Category Average')
            self.category_average_label.grid(row=(3 + self.grid_tracker_row), column=(3 + self.grid_tracker_column))
            self.category_average_labels.append(self.category_average_label)

            
            self.column_spacer = TK.Label(self.root, text='                               ')
            self.column_spacer.grid(row=(3 + self.grid_tracker_row), column=(4 + self.grid_tracker_column))
            self.column_spacers.append(self.column_spacer)

            # Creates the ten per class widgets.
            for z in range(10):

                self.name_of_category = TK.Entry(self.root)
                self.name_of_category.grid(row=(4 + z + self.grid_tracker_row), column=(1 + self.grid_tracker_column))
                self.names_of_categories.append(self.name_of_category)

                self.value_of_category = TK.Entry(self.root)
                self.value_of_category.grid(row=(4 + z + self.grid_tracker_row), column=(2 + self.grid_tracker_column))
                self.values_of_categories.append(self.value_of_category)
                
                self.category_grade = TK.Entry(self.root)
                self.category_grade.grid(row=(4 + z + self.grid_tracker_row), column=(3 + self.grid_tracker_column))
                self.category_grades.append(self.category_grade)

                self.row_spacer = TK.Label(self.root, text='\n')
                self.row_spacer.grid(row=(15 + self.grid_tracker_row), column=(1 + self.grid_tracker_column))
                self.row_spacers.append(self.row_spacer)

            # Tracks amount of classes and amount of cells or widgets.
            self.class_cell_counter += 1
            self.cell_counter += 10

            # Tracks cell locations.
            self.grid_tracker_column += 4
            if self.class_cell_counter == 3 or self.class_cell_counter == 6:
                self.grid_tracker_row += 17
                self.grid_tracker_column = 0

            # This variable is used to prevent logic errors when calculating classes after adding.
            self.class_status = 'Add'

            # Prevents logic errors when classes are added and removed after a calculation and before another.
            if self.calculated == True:
                self.all_calculated = False

    # Removes an entire class along with the average label if it exists.
    def Remove_Class(self):

        # Tells user to add a class.
        if self.class_cell_counter < 1:            
            self.class_limit_min = TK.messagebox.showinfo('', 'Please add a class first.')

        else:
            
            # Removes the one per class widgets.
            self.class_name_labels[self.class_cell_counter - 1].destroy()
            del self.class_name_labels[self.class_cell_counter - 1]
                        
            self.names_of_classes[self.class_cell_counter - 1].destroy()
            del self.names_of_classes[self.class_cell_counter - 1]
            
            self.category_name_labels[self.class_cell_counter - 1].destroy()
            del self.category_name_labels[self.class_cell_counter - 1]
            
            self.category_value_labels[self.class_cell_counter - 1].destroy()
            del self.category_value_labels[self.class_cell_counter - 1]
            
            self.category_average_labels[self.class_cell_counter - 1].destroy()
            del self.category_average_labels[self.class_cell_counter - 1]
            
            self.column_spacers[self.class_cell_counter - 1].destroy()
            del self.column_spacers[self.class_cell_counter - 1]

            # Removes the ten per class widgets.
            for z in range(10):
                
                self.names_of_categories[self.cell_counter - z - 1].destroy()            
                del self.names_of_categories[self.cell_counter - z - 1]
                
                self.values_of_categories[self.cell_counter - z - 1].destroy()
                del self.values_of_categories[self.cell_counter - z - 1]
                
                self.category_grades[self.cell_counter - z - 1].destroy()
                del self.category_grades[self.cell_counter - z - 1]
               
                self.row_spacers[self.cell_counter - z - 1].destroy()
                del self.row_spacers[self.cell_counter - z - 1]

            # Tracks the amount of classes and cells or widgets.
            self.class_cell_counter -= 1
            self.cell_counter -= 10

            # Tracks cell locations.
            self.grid_tracker_column -= 4
            if self.class_cell_counter == 2 or self.class_cell_counter == 5:                
                self.grid_tracker_row -= 17
                self.grid_tracker_column = 8

            # Removes the average label if it exists and prevents indexing errors if a calculation has been preformed before classes are removed.
            if self.calculated == True:
                if self.all_calculated == True:
                    if self.class_status == 'Add':
                        self.averages_of_classes[self.temp_class_cell_counter - 1].destroy()
                        del self.averages_of_classes[self.temp_class_cell_counter - 1]
                        self.temp_class_cell_counter -= 1
                if self.class_status == 'Remove':
                    self.averages_of_classes[self.class_cell_counter].destroy()
                    del self.averages_of_classes[self.class_cell_counter]
                    self.temp_class_cell_counter -= 1

            # Resets the calculated variable if all classes are removed.
            if self.class_cell_counter == 0:
                self.calculated = False   

            # This variable is used to prevent logic errors when calculating classes after removing.
            self.class_status = 'Remove'   

    # Calculates the average 
    def Calculate(self):
        
        # Stores average calculations.
        self.class_averages.clear()

        # Gets proper values for calculations without disturbing the tracking of the cells.
        self.average_cell_counter = 0

        # Tracks the location for placing the average labels without disturbing the placement tracker for other cells.
        self.average_grid_tracker_row = 0
        self.average_grid_tracker_column = 0

        # Informs user a class must be added.
        if self.class_cell_counter < 1:            
            self.need_class = TK.messagebox.showinfo('', 'Please add at least one class.')
            
        # Calculates the average and then adds the average label to the display.      
        if self.class_cell_counter >= 1: 
            
            # Prevents the labels from overlapping on multiple calculations by delete the current widgets.
            if self.calculated == True:

                # Prevents a list indexing error if a class is added after a calculations.
                if self.class_status == 'Add':
                    for d in range(self.temp_class_cell_counter):
                        self.averages_of_classes[0].destroy()
                        del self.averages_of_classes[0]

                # Prevents a list indexing error if a class is removed after a calculations.
                if self.class_status == 'Remove':
                    for e in range(self.temp_class_cell_counter):
                        self.averages_of_classes[0].destroy()
                        del self.averages_of_classes[0]

            # Denotes that a calculation has been preformed.
            self.calculated = True
            self.all_calculated = True
            
            # Calculates the grade, and creates the label for all class cells that exist at the time.
            for n in range(self.class_cell_counter):
                self.category_averages = list()

                # Gets the values from the category value and category average entries if the entry is filled if not the entry is skipped.
                for m in range(10):
                    if self.values_of_categories[m + self.average_cell_counter].get() == '' or self.category_grades[m + self.average_cell_counter].get() == '':
                        self.category_averages.append(0)
                    else:
                        self.category_averages.append(float(self.values_of_categories[m + self.average_cell_counter].get())*float(self.category_grades[m + self.average_cell_counter].get()))

                # Converts the grade average to a percent.
                self.class_averages.append((sum(self.category_averages)*100))

                # Creates the label displaying the averages.
                self.average_of_class = TK.Label(self.root, text='Average for {} {} %'.format(self.names_of_classes[n].get(), self.class_averages[n]))
                self.average_of_class.grid(row=(15 + self.average_grid_tracker_row), column=(2 + self.average_grid_tracker_column))
                self.averages_of_classes.append(self.average_of_class)

                # Tracks the cell location for calculations.
                self.average_cell_counter += 10

                # Tracks the average label locations.
                self.average_grid_tracker_column += 4   
                if n == 2 or n == 5:
                    self.average_grid_tracker_row += 17
                    self.average_grid_tracker_column = 0

            # Stores the current amount of classes at the time of calculation to prevent list indexing errors.
            self.temp_class_cell_counter = self.class_cell_counter
                    
    # Method to start the GUI.
    def Run(self):

        # Calls the first method to allow the user to begin acting within the program.
        self.Returning_User_Check()

        # Keeps the GUI running.
        self.root.mainloop()

# Main (Where program begins.)
if __name__ =='__main__':

    # GUI function, title.
    root = TK.Tk()
    root.title('Gradebook Calculator')

    # Pulls the Gradebook_Calculator class and begin (runs) it.
    GBC = Gradebook_Calculator(root)
    GBC.Run()
    