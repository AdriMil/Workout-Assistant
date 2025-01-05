from app.myImports import *
from app.classes import GlobalSeanceChrono, MainChrono, Listbox
from app.buttons import myMainButtons, DefinedWidth, DefinedHeight
import app.buttons as button

#-------------------IHM-----------#
def gui(root):
    root.title("Musculation")

def init_button_state(state :str):
    """
    Will be call to lock or unclock actions buttons

    Args:
        state (str): lock or unlock depending of the need
    """
    for i in myMainButtons[1:-1]: #Execpt 1st and last button of the list
        i.availability(state)

#------------------------------#
def start():
    """
    This function will be triggered when Start button will be pressed. 
    Start hour will be displayed and the seance total time chrono will be triggered
    When pressed, the start button become a pause button
        Seance total time chrono will be stopped while start is not pressed
    """

    global counting, Image_Pause, Pause, selected_tempo_value

    #Display start_time
    global start_time, ImageReducer, Image_Play

    if(button.Start.click_number==0):
        start_time = datetime.now()
        label_start_time['text']= 'Heure de début : ' + start_time.strftime('%H:%M:%S') 
    
    if (button.Start.click_number%2 == 0):
        Pause = False
        counting = True
        init_button_state("unlock")
        undo_button_updating()      
        button.Start.button.configure(image=Image_Pause)   
        button.Start.action_click() 
        button.Start.button['text']='Pause'
        counter_action_start()

        if  button.Start.click_number > 0 : 
            chrono_counting_loop()                        
        selected_tempo_value = temporisation_listbox.object.select_set(0)  

    elif (button.Start.click_number%2 == 1):
        Pause = True
        MainChrono.running = False
        counter_action_pause()

#-----------------------------Button Position Calculation

def buttons_position(buttons_list :list, reference_x : int, refence_y :int, reference_width :int, line_break :bool) -> float:
    """
    This function will be use to place an amount of buttons on a given width. If the amount of button is too high for line width, then a new line will be created.

    Args:
        buttons_list (list): List with all buttons which should be placed
        reference_x (int): x point used to calculate button centering
        refence_y (int): y point used to calculate button centering
        reference_width (int): width substarcted to x position to know length where button will be centered
        line_break (bool): Do you allow a line break ?

    Returns:
        float: 1st button x position calculated to allow centering of all buttons
    """
    global place
    button_number = len(buttons_list)
    if debug==1 : print(button_number, "Button in my list")
    
    free_space = reference_width - (button_number * (DefinedWidth + SPACE_BETWEEN_BUTTON))

    if not line_break:
        place = reference_x + (free_space / 2)                                                #Buttons will be centered on reference, without line break
        calculate_button_position(buttons_list, place, refence_y) 
  
        return place

def calculate_button_position(buttons_list :list, x_position: int,y_position: int):           #Update button position.
    """
    Will be call to place an amount of button centered on one line.

    Args:
        buttons_list (list): all button which should be placed on one line
        x_position (int): x position for the first button of the buttons_list
        y_position (int): y position for the first button of the buttons_list
    """
    for mybutton in buttons_list:
        mybutton.update_button_position(xposition=x_position,yposition=y_position)
        if debug == 1 : print("My x position is : ",x_position, " My y position is : ", y_position)
        x_position = x_position + BUTTON_WIDTH + SPACE_BETWEEN_BUTTON

#------------------------------#      
def counter_action_pause():
    """
        Stop counting. 
        Pause button which become Start.
        Lock actions buttons
    """
    global counting
    counting = False                                       
    button.Start.action_click()
    button.Start.button['text']='Start'
    button.Start.button.configure(image=Image_Play)
    init_button_state("lock")
 
 #------------------------------#            
def counter_action_start(): 
    """
    Function call in loop when start button is pressed. 
    This function will do an auto-call every seconds
    """
    global counting
    if (counting==True):
        global counter, count,comptage    
        tt = datetime.fromtimestamp(GlobalSeanceChrono.value) 
        count=str(tt.strftime("%H:%M:%S"))
        GlobalSeanceChrono.value = GlobalSeanceChrono.value + 1 
        label_session_duration.after(1000, counter_action_start) 
        label_session_duration['text']= 'Durée de la séance :' + count

#------------------------------#     
def remember():
    """
    When Space is pressed, information are save in the main table, one a new line.
    If there is more lines than table's height, then table will autoscroll down to display last line.
    """
    button.Remember.action_click()
    undo_button_updating()
    tableau.yview_moveto(1)
    tableau.insert( '', 'end',values=(button.Remember.click_number,count))
    tableau.yview_moveto(1)                                      

#------------------------------#  
def undo_from_keyboard(event):
    """
    Detect Crtl+Z on keyboard and call undo function
    """
    delete_last_row_from_tab()

def delete_last_row_from_tab():
    """
    Used when the user wants to delete the last table line. 
    """
    if button.Remember.click_number > 0 :
        MainChrono.value = 82800
        MainChrono.state = "Pause" 
        nb_element_tableau = tableau.get_children()
        last_row = nb_element_tableau[-1]
        tableau.delete(last_row)
        button.Remember.click_number = button.Remember.click_number - 1 
        MainChrono.running = False
        undo_button_updating()
        
#------------------------------#
def reset_pressed():
    """
    Will reset all data : 
    Both Chrono temporisation and seance time are reseted to 00:00
    Table is cleaned
    """
    global Pause
    message_box = tk.messagebox.askquestion ('Reset stats','Really Reset?',icon = 'question')
    if message_box == 'yes':
        GlobalSeanceChrono.value= 82800
        Chrono_tempo['text']="00:00"
        label_session_duration['text']='Durée de la séance : 00:00:00' #Chrone reseted to 0
        tableau.delete(*tableau.get_children()) #Table is cleared
        counter_action_pause() #Stop counting loop
        MainChrono.running = False
        MainChrono.value = temporisation_listbox.object.get(0)
        Pause = True
        button.Start.click_number = 0      
        button.Remember.click_number = 0    

def undo_button_updating():
    """
    Will update state of undo button depending of number of line in the table
    """
    if button.Remember.click_number == 0 : 
        button.DeleteLastRaw.availability("lock") 
    else : 
        button.DeleteLastRaw.availability("unlock")

def space_bar_pressed(self):
    """
    Action when Space button is pressed : 
        if PAUSE = true and (MainChrono.state == "Positive" and MainChrono.running : Nothing 
        
    """
    if Pause:
        return None
    elif MainChrono.state == "Positive" and MainChrono.running:
        return None
    elif MainChrono.running and MainChrono.state == "Negative":
        MainChrono.running = False
    else:
        MainChrono.running = True
        get_tempo_from_list()
        remember()
        MainChrono.negative_count = 0
        MainChrono.value = selected_tempo_value
        chrono_counting_loop()
    
def touch_delete(self):
    reset_pressed()

#------------------------------#
def table_columns_width_definition():
    """
        Will adjust column width
    """
    for colonne in table_columns:
        tableau.column(colonne, width=tableau.bbox(colonne)[2])

#------------------------------#
def exit():
    """
    Function call when exot button is pressed.
    Stats can be save only if seance has been started else it is not necessary to save stats.
    """
    if(button.Start.click_number >= 1):
        save_stats()
    else:
        root.destroy()

#------------------------------#
def save_stats():
    """"
    Ask if you want to save statistics when exiting. Check if csv file already exist. If not it will be created
    """
    message_box = tk.messagebox.askquestion ('Sauvegarde des stats','Sauvegarder les stats ?',icon = 'question')
    if message_box == 'yes':   
        try:           
            open("Statistiques.csv")
            write_data_in_csv_file()
            root.destroy()
        except IOError:
            create_csv_file()
            write_data_in_csv_file()
            root.destroy()
    else : 
        root.destroy()

#------------------------------#
def data()-> list:
    """
    Will gather data to a list a add it in output
    """
    global start_time
    data=[]
    current_date= datetime.now().strftime('%d/%m/%y')
    end_hour = datetime.now()
    seance_time=end_hour-start_time
    
    data=[current_date,start_time.strftime('%H:%M:%S') ,end_hour.strftime('%H:%M:%S'),str(seance_time),button.Remember.click_number]
    return data
    
def create_csv_file():
    """
    Use to create csv file with colomn name
    """
    columns_names = ['Date', 'Heure debut', 'Heure Fin', 'Temps seance', 'Nombre de serie']
    with open(r'Statistiques.csv', 'a',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(columns_names) 
    f.close()

def write_data_in_csv_file():
    """
    Add data to csv file
    """
    stats = data()
    
    with open(r'Statistiques.csv', 'a',newline='') as f:  #newline='' needed otherwise there is 1 line empty each 2 lines
        writer = csv.writer(f)
        writer.writerow(stats)  
    f.close()  

#------------------------------# 
def chrono_counting(signe):
    global count_tempo
    if signe == '+':
        tt = datetime.fromtimestamp(MainChrono.value)   
        count_tempo=str(tt.strftime("%M:%S"))
        MainChrono.value=MainChrono.value-1
    elif signe == '-':
        tt = datetime.fromtimestamp(MainChrono.negative_count)   
        MainChrono.negative_count=MainChrono.negative_count+1
        count_tempo=str(tt.strftime("-%M:%S"))

def check_chrono_state():
    if debug == 1 : print("Start check_chrono_state ")
    if MainChrono.value > 0:
        MainChrono.state = "Positive"
        MainChrono.negative_count = 82800
    elif MainChrono.value < 1:
        MainChrono.state = "Negative"

def chrono_counting_loop():
    if MainChrono.running:
        check_chrono_state()
        if(MainChrono.state == "Positive"):
            chrono_counting('+')
        elif(MainChrono.state == "Negative"):
            chrono_counting('-')

        Chrono_tempo.after(1000,chrono_counting_loop)
        Chrono_tempo['text']=count_tempo

def temporisation_selected(event):
    get_tempo_from_list()

def get_tempo_from_list():
    """
    Will get selected value from listbox with all temporisations.
    """
    global selected_tempo_value
    selected_tempo_value = temporisation_listbox.object.get((temporisation_listbox.object.curselection()))
    button.SetTempo.button.configure(text=(str(selected_tempo_value)+"s"))
    temporisation_listbox.object.place_forget()

def display_lisbox():
    """
    Display or hide the listbow with all temporisations
    """
    if (temporisation_listbox.display_status == "Close") : 
        temporisation_listbox.display_status = "Open"
        temporisation_listbox.place_listbox(x_position_button=button.SetTempo.xposition,
                                             y_position_button=button.SetTempo.yposition,
                                                width=(BUTTON_WIDTH + SPACE_BETWEEN_BUTTON), height= 100)
    else:
        temporisation_listbox.display_status = "Close"
        temporisation_listbox.hide_listbox()

def left_clic(event):
    """
    close list box by left click anywhere outside the listbox. Check if listbox is open in case of left click. If yes it will close it. 
    """
    if((temporisation_listbox.display_status == "Open") and (str(event.widget) != ".!notebook.!frame.!listbox")):
        temporisation_listbox.hide_listbox()

#-------------------------------------------------------#
#                       Start Program                   #
#-------------------------------------------------------#
from app.InitComponent import *

WINDOW_HEIGHT = 510
WINDOW_WIDTH = 500
root.geometry(str(WINDOW_WIDTH)+"x"+str(WINDOW_HEIGHT)) # Window size
root.resizable(width=False, height=False)               # Lock window resizing

tabControl.add(tab1, text ='Ma Séance')                 #Tab1 created
tabControl.pack(expand= 1, fill ="both")

gui(root)

#----------------------Table initialisation----------------------#
TABLE_Y_INIT = 185 ; TABLE_WIDTH = 370 ; TABLEAU_HEIGHT = 245 ; TABLE_X_INIT = (WINDOW_WIDTH-TABLE_WIDTH)/2  ; 
table_columns = ['N_Série', 'Temps']
tableau = ttk.Treeview(tab1, columns=(table_columns[0], table_columns[1]))
tableau.heading(table_columns[0], text='N° de Série', command= table_columns_width_definition)
tableau.heading(table_columns[1], text='Temps', command= table_columns_width_definition)
tableau.column(table_columns[0], anchor='center')
tableau.column(table_columns[1], anchor='center')
tableau['show'] = 'headings' # Needed to avoid an empty column on left
tableau.place(x=TABLE_X_INIT, y=TABLE_Y_INIT, width=TABLE_WIDTH, height=TABLEAU_HEIGHT)

#----------------------Temporisation initialisation----------------------#
temporisation=[15,30, 60,90,120,300,600]
temporisation_listbox = Listbox(component=tab1, content= temporisation)
temporisation_listbox.object.bind('<<ListboxSelect>>', temporisation_selected)

#----------------------Buttons settings----------------------#
place = TABLE_X_INIT ; BUTTON_WIDTH = 40 ;BUTTON_HEIGHT = 40 ; POLICE_SIZE = 8; SPACE_BETWEEN_BUTTON=10 ; buttons_y_init = TABLE_Y_INIT - BUTTON_HEIGHT - 10

#----------------------Calculate centered position for my buttons----------------------#
buttons_position(buttons_list=myMainButtons, reference_x= TABLE_X_INIT, refence_y=(TABLE_Y_INIT - (DefinedHeight + SPACE_BETWEEN_BUTTON)), reference_width=TABLE_WIDTH, line_break=False)

#----------------------Associate new function to my Main buttons----------------------#
button.Start.associate_a_function(start)
button.SetTempo.associate_a_function(display_lisbox)
button.DeleteLastRaw.associate_a_function(delete_last_row_from_tab)
button.Reset.associate_a_function(reset_pressed)
button.Exit.associate_a_function(exit)
init_button_state("lock")

#----------------------Chrono settings and initialisation----------------------#
CHRONO_TEMPO_HEIGTH = 55; CHRONO_TEMPO_X = 200 ; CHRONO_TEMPO_Y= TABLE_Y_INIT - BUTTON_HEIGHT - (2*CHRONO_TEMPO_HEIGTH); CHRONO_TEMPO_WIDTH = 350; 
free_space = TABLE_WIDTH - (CHRONO_TEMPO_WIDTH)
position_x_tempo = TABLE_X_INIT + (free_space / 2)
Chrono_tempo= tk.Label(tab1, text = "00:00",fg="black", font="Verdana 40 bold ",)
Chrono_tempo.place(x=position_x_tempo, y=CHRONO_TEMPO_Y, width=CHRONO_TEMPO_WIDTH, height=CHRONO_TEMPO_HEIGTH)

#----------------------Labels initialisation----------------------#
label_start_time= tk.Label(tab1, text = 'Heure de début : 00:00:00')
label_start_time.place(x=TABLE_X_INIT, y=TABLE_Y_INIT + TABLEAU_HEIGHT +5, width=135, height=10)

label_session_duration= tk.Label(tab1, text = 'Durée de la séance : 00:00:00')
label_session_duration.place(x=TABLE_X_INIT, y=TABLE_Y_INIT + TABLEAU_HEIGHT  + 15, width=150, height=25)

#----------------------keyboard and mouse detection initialisation----------------------#
root.bind("<space>", space_bar_pressed )
root.bind("<BackSpace>", touch_delete )
root.bind('<Control-z>', undo_from_keyboard)
root.bind("<Button-1>", left_clic)

root.iconbitmap(resource_path('Pictures/iconeV2.ico'))
root.mainloop()
