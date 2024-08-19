from GUI import GUI_objects

"""Main menu"""
MainMenuWindow = GUI_objects.Container(400, 400, 195, 150, title='Dev tools')

MainMenuButton1 = GUI_objects.button(10, 10, -1, 25, text='Sine wave effect', container=MainMenuWindow.container)

MainMenuButton2 = GUI_objects.button(10, 45, -1, 25, text='CRT effect', container=MainMenuWindow.container)

MainMenuWindow.container.hide()

"""Sine wave effect control"""
SineWaveWindow = GUI_objects.Container(400, 400, 195, 150, title='Sine wave effect control')

SineWaveSlider1 = GUI_objects.HoriSlider(10, 0, 150, 25, container=SineWaveWindow.container, label=True,
                                         labeltext='Amplitude', sliderange=(0, 100), clickincrement=5)

SineWaveSlider2 = GUI_objects.HoriSlider(10, 50, 150, 25, container=SineWaveWindow.container, label=True,
                                         labeltext='Rate', sliderange=(0, 150), clickincrement=5)

SineWaveWindow.container.hide()

"""CRT effect control"""
CRTWindow = GUI_objects.Container(400, 400, 195, 250, title='CRT effect control')

CRTSlider1 = GUI_objects.HoriSlider(10, 0, 150, 25, container=CRTWindow.container, label=True,
                                    labeltext='Center X', sliderange=(0.0, 1.0), startvalue=0.5,
                                    clickincrement=0.1)

CRTSlider2 = GUI_objects.HoriSlider(10, 50, 150, 25, container=CRTWindow.container, label=True,
                                    labeltext='Center Y', sliderange=(0.0, 1.0), startvalue=0.5, clickincrement=0.1)

CRTSlider3 = GUI_objects.HoriSlider(10, 100, 150, 25, container=CRTWindow.container, label=True,
                                    labeltext='Warp', sliderange=(1.0, 10.0), startvalue=10, clickincrement=0.1)

CRTButton1 = GUI_objects.button(10, 175, 50, 25, text='Reset', container=CRTWindow.container)

CRTWindow.container.hide()
