from kivy.app import App
from kivy.core.image import Image
from kivy.graphics.texture import Texture
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

import time
import webbrowser
import random
import threading

mutex = threading.Lock()

mutex.acquire()
startDate = float(open("data.txt").read())
mutex.release()

# Random quotes about quitting drinking. Make sure quotes and quote_authors are aligned.
quotes = [
    "You don't have to see the whole staircase, just take the first step.",
    "When you quit drinking, you stop waiting.",
    "Not drinking makes me a lot happier.",
    "The day I became free of alcohol was the day that I fully understood and embraced the truth that I would not be giving anything up by not drinking.",
    "First you take a drink, then the drink takes a drink, then the drink takes you."]

quote_authors = [
    "Anonymous",
    "Caroline Knapp",
    "Naomi Campbell",
    "Liz Hemingway",
    "Anonymous"
]


# The popup for when the person relapses.
def show_relapse_popup():
    relapsePopup = Popup(title="Sorry to see you relapse!",
                         size_hint=(None, None),
                         size=(400, 400))

    button1 = Button(text="Click for some helpful resources.",
                     size_hint=(0.3, 0.3),
                     pos=(0, 100),
                     color=("000000"),  # Black.
                     background_color=("#ffffff"))  # White.

    # Local function to link the user to a website about getting rid of drinking.
    def resources(button1):
        webbrowser.open(
            "https://www.canada.ca/en/health-canada/services/substance-use/get-help/get-help-problematic-substance-use.html")

    button1.bind(on_press=resources)  # Add the function to the button when pressed.
    relapsePopup.add_widget(button1)

    relapsePopup.open()  # Open the popup.


# Similar setup to the relapse popup but this is for the help popup.
def help_popup():
    relapsePopup = Popup(title="Hang in there! You can do it!",
                         size_hint=(None, None),
                         size=(400, 400))

    button1 = Button(text="Click for some helpful resources.",
                     size_hint=(0.3, 0.3),
                     pos=(0, 100),
                     color=("000000"),
                     background_color=("#ffffff"))

    def resources(button1):
        webbrowser.open(
            "https://www.rethinkingdrinking.niaaa.nih.gov/tools/Interactive-worksheets-and-more/Stay-in-control/Coping-With-Urges-To-drink.aspx")

    button1.bind(on_press=resources)
    relapsePopup.add_widget(button1)

    relapsePopup.open()


def randomQuote():
    num = random.randint(0, len(
        quotes) - 1)  # Random number between 0 and the last element of the quotes. Automatically updates.
    return quotes[num] + "\n-" + quote_authors[num]


def formatSeconds(seconds):  # helper function to convert an amount of seconds to a day hour minute second format
    days = 0
    hours = 0
    minutes = 0

    days = int(seconds / 86400)
    seconds = seconds - days * 86400
    hours = int(seconds / 3600)
    seconds = seconds - hours * 3600
    minutes = int(seconds / 60)
    seconds = seconds - minutes * 60

    seconds = int(seconds)

    return f"{days} days {hours} hours\n{minutes} minutes and {seconds} seconds"



class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class MainPage(Screen):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)

        quote = Label(text="",  # Text is empty as there is no quote.
                      color="000000",  # Black.
                      halign="left",  # Align text to the left.
                      size=(500, 200),
                      pos=(0, 250),
                      font_size="20sp")

        quote.text_size = quote.size  # Needed to wrap the text. Otherwise it will flow out of the screen.

        label = Label(text='Welcome to Sobriety!',
                      size_hint=(0.8, 0.8),  # 0.8 of the screen for both x and y.
                      halign="center",  # Center the text.
                      pos=(100, 150),
                      font_size="20sp",
                      color="000000")

        self.add_widget(label)  # Add the title to the layout.
        self.add_widget(quote)  # Add the quote.

        soberButton = Button(text="Press to join sobriety!",
                             size_hint=(0.5, 0.3),
                             pos_hint={"center_x": 0.8, "y": 0},
                             color="000000",
                             background_color="#ffeec2")

        helpButton = Button(text="Help! I wanna drink!",
                            size_hint=(0.5, 0.3),
                            pos_hint={"center_x": 0.2, "y": 0},
                            color="000000",
                            background_color="#ffeec2")

        def refreshTime():  # run function for the clock thread. Keeps clock active
            startDate = float(open("data.txt").read())
            f = open("message.sob", "w")
            f.write(str(0))
            f.close()
            while True:
                mutex.acquire()
                if str(open("message.sob").read()) != '0':
                    mutex.release()
                    break
                mutex.release()
                label.text = f"Welcome to Sobriety!\nYou are {formatSeconds(time.time() - startDate)} sober!"  # Update label text.

        if startDate != 0:
            clockThread = threading.Thread(target=refreshTime)
            clockThread.start()
            soberButton.text = "Press if you relapse"  # Update the text of the sober button button.

        # This is the function for when the sober button is pressed.
        def soberButtonFunc(soberButton):
            # Basically check if the person is sober already.

            if soberButton.text == "Press to join sobriety!":
                mutex.acquire()
                f = open("data.txt", "w")
                f.write(str(time.time()))
                f.close()
                soberButton.text = "Press if you relapse"  # Update the text of this button.

                startDate = float(open("data.txt").read())

                clockThread = threading.Thread(target=refreshTime)
                clockThread.start()
                mutex.release()

            elif soberButton.text == "Press if you relapse":
                mutex.acquire()
                f = open("data.txt", "w")
                f.write(str(0))
                f.close()
                mutex.release()
                startDate = 0
                f = open("message.sob", "w")
                f.write(str(1))
                f.close()
                label.text = "So sorry to see you relapse!"  # Update label to match.
                soberButton.text = "Press to join sobriety!"  # Reset the sobriety button text.
                quote.text = ""  # Get rid of the quote.
                show_relapse_popup()  # Call the function to show the relapse popup.

            # if self.startDate % 10 == 0:
            #    quote.text = randomQuote() # Generate random quote every 10 days.
        
        texture = Image('images/paradise.jpg').texture
        with Window.canvas:
            Rectangle(texture=texture, pos=(0, 0), size=(1280, 900))

        soberButton.bind(on_press=soberButtonFunc)  # Add the sober function to the sober button whenever pressed.
        self.add_widget(soberButton)

        helpButton.bind(on_press=self.screen_transition)
        self.add_widget(helpButton)
        # label.bold = True
        # label.italic = True
        # label.underline = True
        label.color = [0, 0, 0]
        label.outline_width = 2
        label.outline_color = [1, 1, 1]
        label.pos_hint = {"center_x": 0.5}
    
    def screen_transition(self, *args):
            self.manager.current = 'second'


class SecondPage(Screen):
    def __init__(self, **kwargs):
        super(SecondPage, self).__init__(**kwargs)
        
        label = Label(text="Don't give up just yet! You're doing great!",
                    size_hint=(0.8, 0.8),  # 0.8 of the screen for both x and y.
                    halign="center",  # Center the text.
                    pos=(100, 150),
                    font_size="20sp",
                    color="000000")
        self.add_widget(label)
        
        button1 = Button(text="Click to view 11 tips to deal with urges to drink!",
                        size_hint=(1, 0.2),
                        pos_hint={"center_x": 0.5, "y": 0},
                        color="000000",
                        background_color="#ffeec2")
        
        def resources(button1):
            webbrowser.open("https://checkupandchoices.com/11-tips-and-ways-to-deal-with-urges-and-cravings-to-drink-and-can-be-helpful-in-dealing-with-urges-to-use-drugs-too/")
        
        button1.bind(on_press=resources)
        self.add_widget(button1)
        
        button2 = Button(text="Click to view an article depicting dealing with the urge to drink!",
                        size_hint=(1, 0.2),
                        pos_hint={"center_x": 0.5, "y": 0.2},
                        color="000000",
                        background_color="#ffeec2")
        
        def resources2(button2):
            webbrowser.open("https://www.livewelldorset.co.uk/articles/dealing-with-the-urge-to-drink/")
        
        button2.bind(on_press=resources2)
        self.add_widget(button2)
        
        back = Button(text="<- Back",
                    color=("000000"),
                    background_color="#ffeec2",
                    size_hint=(0.2, 0.2),
                    pos_hint={"center_x": 0.1, "center_y": 0.9})
        
        back.bind(on_press=self.screen_transition)
        self.add_widget(back)
        
        texture = Image('images/paradise.jpg').texture
        with Window.canvas:
            Rectangle(texture=texture, pos=(0, 0), size=(1280, 900))
    
    def screen_transition(self, *args):
        self.manager.current = 'main'
    

class MainApp(App):
    Window.clearcolor = (1, 1, 1, 1)  # Set to white.

    def on_request_close(self, *args):
        f = open("message.sob", "w")
        f.write(str(1))
        f.close()
        self.stop()
        return True

    def build(self):
        
        Window.bind(on_request_close=self.on_request_close)
        
        sm = ScreenManagement()
        sm.add_widget(MainPage(name="main"))
        sm.add_widget(SecondPage(name="second"))
        return sm  # Basically returns the entire app setup.


# Just don't touch.
if __name__ == '__main__':
    app = MainApp()  # Create the app.
    app.run()  # Run the app.
