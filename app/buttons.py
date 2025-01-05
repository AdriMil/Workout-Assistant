from app.classes import Button
from app.InitComponent import *
from app.myImports import tab1

#Will be used to store all decalred buttons.
myMainButtons = []

DefinedWidth = 40
DefinedHeight = 40
Start = Button(component=tab1,text="Start",icone=Image_Play,width=DefinedWidth,height=DefinedHeight)
SetTempo = Button(component=tab1,text="Tempo",icone=Image_Tempo,width=DefinedWidth,height=DefinedHeight)
DeleteLastRaw = Button(component=tab1,text="Annuler",icone=Image_Undo,width=DefinedWidth,height=DefinedHeight)
Reset = Button(component=tab1,text="Reset",icone=Image_RESET,width=DefinedWidth,height=DefinedHeight)
Exit = Button(component=tab1,text="Quitter",icone=Image_Quitter,width=DefinedWidth,height=DefinedHeight)

Remember = Button(component=tab1,text=None,icone=None,width=None,height=None)

myMainButtons=[Start,SetTempo,DeleteLastRaw,Reset,Exit]