from app.myImports import PhotoImage,tk, resource_path
from app.myImports import tab1, root
import math

ImageReducer = 1 #Reduce image size automatically

Image_RESET = PhotoImage(file=resource_path("Pictures/Reset.png")).subsample(ImageReducer, ImageReducer)
Image_Quitter = PhotoImage(file=resource_path("Pictures/Quitter.png")).subsample(ImageReducer, ImageReducer)
Image_Play = PhotoImage(file=resource_path("Pictures/Start.png")).subsample(ImageReducer, ImageReducer)
Image_Pause = PhotoImage(file=resource_path("Pictures/Pause.png")).subsample(ImageReducer, ImageReducer)
Image_Pause = Image_Pause.subsample(ImageReducer, ImageReducer) #Because not constructed in for loop
Image_Undo = PhotoImage(file=resource_path("Pictures/Undo.png")).subsample(ImageReducer, ImageReducer)
Image_Tempo = PhotoImage(file=resource_path("Pictures/Tempo.png")).subsample(ImageReducer, ImageReducer)
Image_TypeSeance = PhotoImage(file=resource_path("Pictures/gym.png")).subsample(ImageReducer, ImageReducer)



