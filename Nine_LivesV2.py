import time
from tkinter import *
from Pet import *
import random

class Game:
    def __init__(self):
        self.app = Tk()
        self.app.resizable(False, False)
        self.app.title("9 Lives")
        self.pet = self.randomize_pet() #Randomizes animal and starting stats
        self.sleep_counter = 0 #Used for sleeping animation Zzz...
        self.await_revival = False #Turns True when pet is dead and revive/say goodbye buttons are on screen/Prevents anims and stat decay
        self.reset_timers = False #Turns on when reseting pet to prevent previous pet anims from overriding
        self.decay_time = 60000 #How often stats decay (or sleep increases energy) automatically
        self.menu = Menu(self.app)
        self.app.config(menu=self.menu)
        self.file_menu = Menu(self.menu)
        self.file_menu.add_command(label="Reset Pet", command=self.reset_pet) #Gives new pet
        self.file_menu.add_command(label="Exit", command=self.app.quit)
        self.decay_settings = Menu(self.menu)
        self.decay_settings.add_command(label="1 Minute", command=lambda: self.change_decay_time(60000))
        self.decay_settings.add_command(label="5 Minutes", command=lambda: self.change_decay_time(300000))
        self.decay_settings.add_command(label="10 Minutes", command=lambda: self.change_decay_time(600000))
        self.decay_settings.add_command(label="30 Minutes", command=lambda: self.change_decay_time(1800000))
        self.decay_settings.add_command(label="1 Hour", command=lambda: self.change_decay_time(3600000))
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.menu.add_cascade(label="Decay Settings", menu=self.decay_settings)
        self.pet_button = Button(self.app, text="Pet", padx=38, pady=10, command=lambda: self.pet_pet(self.pet))
        self.feed_button = Button(self.app, text="Feed", padx=34, pady=10, command=lambda: self.feed_pet(self.pet))
        self.groom_button = Button(self.app, text="Groom", padx=35, pady=10, command=lambda: self.groom_pet(self.pet))
        self.play_button = Button(self.app, text="Play", padx=42, pady=10, command=lambda: self.play_with_pet(self.pet))
        self.name_bar = Entry(self.app, width=12, justify="center")
        self.name_bar.insert(0, self.randomize_name())

        self.revive_button = Button(self.app, text="Revive", pady=10, padx=80, command=lambda: self.revive_pet(self.pet))
        self.say_goodbye_button = Button(self.app, text="Say Goodbye", pady=10, padx=70, command=self.say_goodbye)
        self.pet_area = Text(self.app, height=7, width=24, state="disabled")
        self.header = "" #Line of text above pet's head
        self.emote = [] #Pet's current emotion/animation
        self.message = "" #Line of text below pet
        self.screen = [] #Header, Emote, and Message combined

        self.name_bar.grid(row=0, column=0, columnspan=2)
        self.pet_area.grid(row=1, column=0, columnspan=2) #Area that pet appears in
        self.pet_button.grid(row=2, column=0)
        self.play_button.grid(row=2, column=1)
        self.feed_button.grid(row=3, column=0)
        self.groom_button.grid(row=3, column=1)
        self.draw_pet(self.pet)
        self.pass_time(self.pet) #Starts the automatic decay process
        self.check_for_life(self.pet) #Checks every .5 seconds for life to see if buttons need to change
        self.app.mainloop()

    def randomize_name(self):
        #Used for populating initial name for new pet
        names = ["Jingles", "Spot", "Trixy", "George", "Marsha", "Bella", "Luna", "Charlie", "Lucy", "Max", "Cooper",
                 "Bailey", "Daisy", "Coco", "Roxy", "Rosie", "Barney", "Archie", "Toby", "Rocky", "Charlie", "Buddy",
                 "Duke", "Ruby", "Holly", "Jasper", "Monty", "Willow", "Poppy", "Jack", "Zeus", "Riley", "Milo", "Dexter",
                 "Schrody", "Mango", "Iroh", "Cookie", "Peaches", "Copper", "Belle", "Oliver", "Ollie", "Pablo"]
        rando = random.randint(0, len(names)-1)
        return names[rando]

    def randomize_pet(self):
        rando = random.randint(0, 4)
        if rando == 0:
            pet = Cat()
        elif rando == 1:
            pet = Dog()
        elif rando == 2:
            pet = Bird()
        elif rando == 3:
            pet = Monkey()
        elif rando == 4:
            pet = Deer()
        return pet

    def reset_pet(self):
        self.reset_timers = True #Prevents current pet anims/stat decay from progressing when active
        self.pet.alive = False #Kills current pet to prevent existing in background
        self.pet = self.randomize_pet() #randomizes animal
        self.pet.reset()
        self.pet.lives = 9
        self.pet.love = 0
        self.name_bar.delete(0, END)
        self.name_bar.insert(0, self.randomize_name())
        self.header = ""
        self.emote = ["Finding", "A New", "Friend", "Please Wait..."]
        self.message = ""
        self.update_pet_viewer(self.pet)
        self.app.after(5000, self.restart_timers)

    def restart_timers(self):
        self.reset_timers = False
        self.pass_time(self.pet) #Restarts stat decay for new pet
        self.check_for_life(self.pet) #Checks for life using new pet instead of old pet
        self.draw_pet(self.pet) #Draws new pet and starts anims for new pet

    def change_decay_time(self, amount):
        self.decay_time = amount

    def add_revive_button(self, pet):
        if pet.alive == False:
            self.await_revival = True #When enabled, stops buttons from being constantly redrawn
            self.feed_button.grid_remove()
            self.play_button.grid_remove()
            self.groom_button.grid_remove()
            self.pet_button.grid_remove()
            self.revive_button["text"] = "Revive(" + str(pet.lives) + ")" #Displays current lives for current pet
            self.revive_button.grid(row=2, column=0, columnspan=2)
            self.say_goodbye_button.grid(row=3, column=0, columnspan=2) #Resets pet to new animal
            if pet.lives <= 0:
                self.revive_button["state"] = "disabled"

    def say_goodbye(self):
        self.revive_button.grid_remove()
        self.say_goodbye_button.grid_remove()
        self.pet_button.grid(row=2, column=0)
        self.play_button.grid(row=2, column=1)
        self.feed_button.grid(row=3, column=0)
        self.groom_button.grid(row=3, column=1)
        self.await_revival = False #Helps recheck proof of life for new pet
        self.reset_pet()

    def revive_pet(self, pet):
        pet.lives -= 1
        self.revive_button.grid_remove()
        self.say_goodbye_button.grid_remove()
        self.pet_button.grid(row=2, column=0)
        self.play_button.grid(row=2, column=1)
        self.feed_button.grid(row=3, column=0)
        self.groom_button.grid(row=3, column=1)
        pet.reset()
        self.await_revival = False
        self.emote = pet.get_emotion("Normal")
        self.update_pet_viewer(pet)

    def check_for_life(self, pet):
        if self.reset_timers == False:
            if pet.alive == False:
                self.emote = pet.get_emotion("Dead")
                self.update_pet_viewer(pet)
                if self.await_revival == False:
                    self.add_revive_button(pet)
            self.app.after(500, self.check_for_life, pet)

    def get_pet_name(self):
        name = self.name_bar.get()
        name = name.strip()
        return name

    def pass_time(self, pet):
        if self.reset_timers == False:
            if pet.alive == True:
                pet.decay_stats()
                self.update_pet_viewer(pet)
            self.app.after(self.decay_time, self.pass_time, pet)

    def update_pet_viewer(self, pet):
        #Build the screen
        self.screen = [self.header]
        for a in range(len(self.emote)):
            self.screen.append(self.emote[a])
        #Get message if no message exists
        if self.message == "" and pet.asleep == False:
            rando = random.randint(0, 2)
            if rando == 1:
                if pet.state != "Normal":
                    self.message = "         " + pet.state
            elif rando == 2:
                self.message = "         " + pet.sound
        self.screen.append(self.message)
        #Clear and draw new screen
        self.pet_area["state"] = "normal" #enables text insert in pet area
        self.pet_area.delete(1.0, END)
        for b in range(len(self.screen)):
            if self.screen[b] != self.screen[-1]:
                self.pet_area.insert(END, "        "+ self.screen[b] + "\n")
            else:
                self.pet_area.insert(END, self.screen[b] + "\n")
        #Clear header and message text after time passes
        self.pet_area["state"] = "disabled" #disables text insert in pet area
        self.app.after(3000, self.clear_text, "Message")
        if pet.asleep == False:
            self.app.after(3000, self.clear_text, "Header")

    def clear_text(self, text):
        if text == "Header":
            self.header = ""
        elif text == "Message":
            self.message = ""

    def draw_pet(self, pet):
        #Get pet's current emotion
        if self.reset_timers == False:
            self.emote = pet.get_emotion(pet.state)
            if pet.state == "Asleep":
                if self.sleep_counter <= 0:
                    self.sleep_counter = 4 #Restarts sleeping animation when called
            self.update_pet_viewer(pet)
            if pet.asleep == False:
                self.app.after(3000, self.animate_pet, pet)
            else:
                self.app.after(500, self.animate_sleep, pet) #Zzz

    def animate_pet(self, pet):
        if self.reset_timers == False:
        #Get pet's animation for current emotion
            self.emote = pet.animate()
            self.update_pet_viewer(pet)
            self.app.after(200, self.draw_pet, pet)
    
    def animate_sleep(self, pet):
        if pet.asleep == True:
            if self.sleep_counter == 4:
                self.header = "  Z"
            elif self.sleep_counter == 3:
                self.header = "  Zz"
            elif self.sleep_counter == 2:
                self.header = "  Zzz"
            else: 
                self.header = ""
            self.sleep_counter -= 1
        else:
            self.header = ""
            self.sleep_counter = 0
        if self.reset_timers == False:
            self.app.after(500, self.draw_pet, pet)

    def pet_pet(self, pet):
        #Displays hearts above pet's head depending on love value
        if pet.asleep == False:
            hearts = pet.be_pet()
            self.header = hearts
        else:
            self.rudely_awaken(pet) #You're a bad person and you should feel bad
        self.update_pet_viewer(pet)

    def feed_pet(self, pet):
        if pet.asleep == False:
            pet.eat()
            pet.change_states()
            food_desc = [" noms the \nfood!", " crunches \nand munches!", " eats!"]
            choice = ""
            if "Hungry" in pet.conditions:
                food_desc.append(" excitedly \neats the food!")
            if "Bored" in pet.conditions:
                food_desc.append(" plays with \nthe food!")
            if "Tired" in pet.conditions:
                food_desc.append(" lazily \neats!")
            if "Dirty" in pet.conditions:
                food_desc.append(" makes a \nhuge mess!")
            if pet.state == "Happy":
                food_desc.append(" eats with a\n smile!")
            rando = random.randint(0, len(food_desc)-1)
            choice = food_desc[rando]
            sentence = self.get_pet_name() + choice
            if pet.angry == True:
                sentence = self.get_pet_name() + " knocks over\n the bowl!"
            self.message = sentence
        else:
            self.rudely_awaken(pet)
        self.update_pet_viewer(pet)

    def groom_pet(self, pet):
        if pet.asleep == False:
            pet.groom()
            pet.change_states()
            groom_desc = [" splashes \naround!", " enjoys the \nwater!", " feels \nclean!"]
            if "Bored" in pet.conditions:
                groom_desc.append(" plays with \nbubbles!")
            if "Hungry" in pet.conditions:
                groom_desc.append(" tries to \neat bubbles!")
            rando = random.randint(0, len(groom_desc)-1)
            choice = groom_desc[rando]
            sentence = self.get_pet_name() + choice
            if pet.angry == True:
                sentence = self.get_pet_name() + " attacks the\n water!"
            self.message = sentence
        else:
            self.rudely_awaken(pet)
        self.update_pet_viewer(pet)

    def play_with_pet(self, pet):
        if pet.asleep == False:
            pet.play()
            pet.change_states()
            play_desc = [" chases the \nball!", " bites the \ntoy!", " chases the \nlaser!"]
            if "Hungry" in pet.conditions:
                play_desc.append(" tries to \neat the stuffing!")
            rando = random.randint(0, len(play_desc) -1)
            choice = play_desc[rando]
            sentence = self.get_pet_name() + choice
            if pet.angry == True:
                sentence = self.get_pet_name() + " rips the \ntoy!"
            self.message = sentence
        else:
            self.rudely_awaken(pet)
        self.update_pet_viewer(pet)

    def rudely_awaken(self, pet):
        rando = random.randint(0, 1)
        if rando == 0:
            pet.angry = True #stats decay faster now
            pet.angry_timer = 1 #How many decay cycles pet is angry for
            pet.asleep = False
            pet.state = "Angry"
            pet.conditions = ["Angry"]
            self.header = ""
            self.emote = pet.get_emotion(pet.state)
            self.message = "    Rudely Awakened"
        else:
            self.message = "        Sleeping"

game = Game()