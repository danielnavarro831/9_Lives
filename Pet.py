import random
from datetime import datetime

class Pet: #V2
    def __init__(self):
        self.debug = False #Will print stats to console each time change_state() is called
        self.lives = 9
        self.alive = True
        self.asleep = False
        self.angry = False #Causes faster stat decay
        self.dirty = False #Causes emotes/anims to change slightly
        self.type = "None" #Displays animal type in console when debug is enabled
        self.angry_timer = 0 #How many decay cycles pet is angry for
        self.energy = self.add_stat_variant(50, 100) #if <=30: pet may fall asleep
        self.hunger = self.add_stat_variant(50, 100) #if 0, pet dies
        self.fun = self.add_stat_variant(50, 100) #determines boredom
        self.cleanliness = self.add_stat_variant(50, 100) #determines if dirty = True
        self.love = 0 #increases each decay cycle if avg of all stats are above 70
        self.state = "" #Current emotion displayed in pet area
        self.conditions = [] #Keeps track of multiple conditions applied to the pet like hungry, tired, bored, etc.

    def reset(self):
        self.alive = True
        self.asleep = False
        self.angry = False
        self.angry_timer = 0
        self.hunger = self.add_stat_variant(50, 100)
        self.energy = self.add_stat_variant(50, 100)
        self.cleanliness = self.add_stat_variant(50, 100)
        self.fun = self.add_stat_variant(50, 100)
        self.state = "Normal" #Default state
        self.conditions = []
        self.change_states()

    def print_stats(self):
        print("----------------" + str(datetime.now()))
        print("Animal: " + str(self.type))
        print("Lives: " + str(self.lives))
        print("Alive: " + str(self.alive))
        print("Asleep: " + str(self.asleep))
        print("Angry: " + str(self.angry))
        print("Angry Timer: " + str(self.angry_timer))
        print("Energy: " + str(self.energy))
        print("Hunger: " + str(self.hunger))
        print("Fun: " + str(self.fun))
        print("Cleanliness: " + str(self.cleanliness))
        print("Love: " + str(self.love))
        print("State: " + self.state)
        print("Conditions: " + str(self.conditions))

    def add_stat_variant(self, low, high):
        rando = random.randint(low, high)
        return rando

    def decay_stats(self):
        #Tick down angry timer
        if self.angry_timer > 0:
            self.angry_timer -= 1
        if self.angry_timer == 0:
            self.angry = False
        #Decay stats
        self.fun = self.decrease_stat(self.fun, 10)
        self.cleanliness = self.decrease_stat(self.cleanliness, 10)
        if self.asleep == False:
            self.hunger = self.decrease_stat(self.hunger, 10)
            self.energy = self.decrease_stat(self.energy, 10)
        else:
            if self.hunger > 30: #Don't starve while sleeping, pls
                self.hunger = self.decrease_stat(self.hunger, 10)
            self.energy = self.increase_stat(self.energy, 15) #Energy increases while sleeping
        self.increase_love()
        self.change_states()

    def increase_stat(self, stat, amount):
        increase_amount = amount
        if self.asleep == False:
            if self.check_happiness() == True: #If 0 conditions listed, pet is happy
                increase_amount = int(amount * 1.5) #stat increases more when happy
        stat += increase_amount
        if stat > 100:
            stat = 100
        return stat

    def decrease_stat(self, stat, amount):
        decrease_amount = amount
        if self.asleep == False:
            if self.angry == True: #If 2 or more conditions are listed, pet is angry OR if pet was rudely awakened
                decrease_amount = int(amount * 1.5) #Stat decreases more when angry
        stat -= decrease_amount
        if stat < 0:
            stat = 0
        return stat

    def increase_love(self):
        #If pet isn't angry and avg of energy, cleanliness, fun, and hunger >= 70, love will increase
        if self.get_stat_avg() >= 70 and self.angry != True:
            self.love += 10
        if self.angry == True:
            self.love -= 10
        if self.love > 100:
            self.love = 100
        if self.love < 0:
            self.love = 0

    def change_states(self):
        #Check stats
        self.conditions = []
        self.state = ""
        hunger = self.check_hunger()
        energy = self.check_energy()
        fun = self.check_fun()
        cleanliness = self.check_cleanliness()
        #THEN ->
        if hunger != "Dead": #Pet isn't dead
            if energy != "Asleep": #Pet isn't aslseep
                if self.angry == False: #Pet isn't angry
                    if hunger != "None":
                        self.state = "Hungry" #Hunger emote takes priority because 0 in stat causes death
                        self.conditions.append(hunger)
                    else:
                        if fun != "None":
                            self.conditions.append(fun)
                            self.state = "Bored"
                        if cleanliness != "None":
                            self.conditions.append(cleanliness)
                        if energy != "None":
                            self.conditions.append(energy)
                        if len(self.conditions) < 1:
                            self.state = "Happy"
                        elif len(self.conditions) >= 2:
                            self.state = "Angry"
                            self.angry = True
                            self.angry_timer = len(self.conditions)
                            self.conditions = ["Angry"]
                        else: #Conditions only has 1 listed condition
                            if self.state == "":
                                self.state = "Normal"
                else:
                    self.state = "Angry"
                    self.conditions = ["Angry"]
            else:
                self.asleep = True
                self.state = "Asleep"
                self.conditions = ["Asleep"]
        else:
            self.alive = False
            self.state = "Dead"
            self.conditions = ["Dead"]
        if self.debug == True:
            self.print_stats()

    def check_hunger(self):
        hunger_status = "None"
        if self.hunger < 40 and self.hunger > 0:
            hunger_status = "Hungry"
        elif self.hunger <= 0: #RIP
            hunger_status = "Dead"
        return hunger_status

    def check_energy(self):
        energy_status = "None"
        if self.asleep == False:
            if self.energy <= 30 and self.energy > 0:
                rando = random.randint(0, 1)
                if rando == 0:
                    energy_status = "Asleep"
                else:
                    energy_status = "Tired"
            elif self.energy <= 0:
                energy_status = "Asleep"
        else:
            if self.energy >= 70 and self.energy < 100: #If energy between 70 and 99, chance of waking up
                rando = random.randint(0, 1)
                if rando == 0:
                    self.asleep = False
                    energy_status = "None"
                else:
                    energy_status = "Asleep"
            elif self.energy == 100: #Automatically wakes up when fully rested
                self.asleep = False
                energy_status = "None"
            else:
                energy_status = "Asleep"
        return energy_status
                
    def check_fun(self):
        fun_status = "None"
        if self.fun < 40:
            fun_status = "Bored"
        return fun_status

    def check_cleanliness(self):
        cleanliness_status = "None"
        if self.cleanliness <= 30:
            cleanliness_status = "Dirty"
            self.dirty = True #Causes slightly different anims/emotes
        else:
            self.dirty = False
        return cleanliness_status

    def check_happiness(self):
        if self.angry == False:
            if len(self.conditions) < 1:
                return True
            else:
                return False
        else: #can't be happy if angry
            return False

    def get_stat_avg(self):
        a = self.hunger + self.fun + self.cleanliness + self.energy
        b = int(a/4)
        return b

    def groom(self):
        if self.angry == False:
            self.cleanliness = self.increase_stat(self.cleanliness, 100)
        else: #harder to clean if angry
            self.cleanliness = self.increase_stat(self.cleanliness, 50)

    def be_pet(self):
        hearts = ""
        if self.angry == False:
            if self.love >= 0 and self.love < 60:
                hearts = "  <3"
            if self.love >= 60:
                hearts = " <3 <3"
            if self.love >= 100:
                hearts += "<3 <3 <3"
        else:
            hearts = "  </3" # :'(
        return hearts

    def eat(self):
        self.hunger = self.increase_stat(self.hunger, 20)
        #Pets are messy eaters
        self.cleanliness = self.decrease_stat(self.cleanliness, 2)

    def play(self):
        #Decreases energy and cleanliness
        self.fun = self.increase_stat(self.fun, 10)
        self.energy = self.decrease_stat(self.energy, 2)
        self.cleanliness = self.decrease_stat(self.cleanliness, 2)

class Cat(Pet):
    def __init__(self):
        super().__init__()
        self.type = "Cat"
        self.sound = "Meow"

    def get_emotion(self, state):
        emotion = []
        if self.dirty == False: #Clean
            if state == "Asleep":
                emotion = [" {\_/}", "=(-.-)=", " /u u\\", "( ___ )___"] #Sleepy
            elif state == "Hungry":
                emotion = [" {\_/}", "=('O')=", " /n n\  /", "( ___ )/"] #Hungry
            elif state == "Angry":
                emotion = [" {\_/}", "=(>.<)=", " /n n\  /", "( ___ )/"] #Angry
            elif state == "Dead":
                emotion = [" {\_/}", "=(x.x)=", "</   \>", "( ___ )___"] #Dead
            elif state == "Happy":
                emotion = [" {\_/}", "=(^.^)=", " /u u\  /", "( ___ )/"] #Happy
            elif state == "Bored":
                emotion = [" {\_/}", "=(¬.¬)=", " /u u\\", "( ___ )___"]
            else:
                emotion = [" {\_/}", "=('.')=", " /u u\  /", "( ___ )/"] #Normal
        else: #Dirty
            if state == "Asleep":
                emotion = [" {\_/}", "=(-.-)=", " /u░u\\", "(░░░░░)___"] #Sleepy
            elif state == "Hungry":
                emotion = [" {\_/}", "=('O')=", " /n░n\  /", "(░░░░░)/"] #Hungry
            elif state == "Angry":
                emotion = [" {\_/}", "=(>.<)=", " /n░n\  /", "(░░░░░)/"] #Angry
            elif state == "Dead":
                emotion = [" {\_/}", "=(x.x)=", "</░░░\>", "(░░░░░)___"] #Dead
            elif state == "Happy":
                emotion = [" {\_/}", "=(^.^)=", " /u░u\  /", "(░░░░░)/"] #Happy
            elif state == "Bored":
                emotion = [" {\_/}", "=(¬.¬)=", " /u░u\\", "(░░░░░)___"]
            else:
                emotion = [" {\_/}", "=('.')=", " /u░u\  /", "(░░░░░)/"] #Normal
        return emotion
            
    def animate(self):
        animation = []
        if self.dirty == False: #clean
            if self.state == "Asleep":
                animation = [" {\_/}", "=(-.-)=", " /u u\\", "( ___ )___"] #Sleepy
            elif self.state == "Hungry":
                animation = [" {\_/}", "=('.')=", "</   \> /", "( ___ )/"] #Hungry
            elif self.state == "Angry":
                animation = [" {\_/}", "=(>.<)=", "</   \> /", "( ___ )/"] #Angry
            elif self.state == "Dead":
                animation = [" {\_/}", "=(x.x)=", "</   \>", "( ___ )___"] #Dead
            elif self.state == "Happy":
                animation = [" {\_/}", "=(^.^)=", "</   \> /", "( ___ )/"] #Happy
            elif self.state == "Bored":
                animation = [" {\_/}", "=(-.-)=", " /u u\\", "( ___ )___"] #Bored
            else:
                animation = [" {\_/}", "=(-.-)=", " /u u\  /", "( ___ )/"] #Normal/Blinking
        else:  #dirty
            if self.state == "Asleep":
                animation = [" {\_/}", "=(-.-)=", " /u░u\\", "(░░░░░)___"] #Sleepy
            elif self.state == "Hungry":
                animation = [" {\_/}", "=('.')=", "</░░░\> /", "(░░░░░)/"] #Hungry
            elif self.state == "Angry":
                animation = [" {\_/}", "=(>.<)=", "</░░░\> /", "(░░░░░)/"] #Angry
            elif self.state == "Dead":
                animation = [" {\_/}", "=(x.x)=", "</░░░\>", "(░░░░░)___"] #Dead
            elif self.state == "Happy":
                animation = [" {\_/}", "=(^.^)=", "</░░░\> /", "(░░░░░)/"] #Happy
            elif self.state == "Bored":
                animation = [" {\_/}", "=(-.-)=", " /u░u\\", "(░░░░░)___"] #Bored
            else:
                animation = [" {\_/}", "=(-.-)=", " /u░u\  /", "(░░░░░)/"] #Normal/Blinking
        return animation

class Dog(Pet):
    def __init__(self):
        super().__init__()
        self.type = "Dog"
        self.sound = "Woof"

    def get_emotion(self, state):
        emotion = []
        if self.dirty == False: #Clean
            if state == "Asleep":
                emotion = [" |\_/|", " \\-.-/", " /u u\\", "( ___ )___"] #Sleepy
            elif state == "Hungry":
                emotion = [" |\_/|", " \\'o'/", " /n n\  /", "( ___ )/"] #Hungry
            elif state == "Angry":
                emotion = [" |\_/|", " \\>.</", " /n n\  /", "( ___ )/"] #Angry
            elif state == "Dead":
                emotion = [" |\_/|", " \\x.x/", "</   \>", "( ___ )___"] #Dead
            elif state == "Happy":
                emotion = [" |\_/|", " \\^.^/", " /u u\  /", "( ___ )/"] #Happy
            elif state == "Bored":
                emotion = [" |\_/|", " \\¬.¬/", " /u u\\", "( ___ )___"] #Bored
            else:
                emotion = [" |\_/|", " \\'.'/", " /u u\  /", "( ___ )/"] #Normal
        else: #dirty
            if state == "Asleep":
                emotion = [" |\_/|", " \\-.-/", " /u░u\\", "(░░░░░)___"] #Sleepy
            elif state == "Hungry":
                emotion = [" |\_/|", " \\'o'/", " /n░n\  /", "(░░░░░)/"] #Hungry
            elif state == "Angry":
                emotion = [" |\_/|", " \\>.</", " /n░n\  /", "(░░░░░)/"] #Angry
            elif state == "Dead":
                emotion = [" |\_/|", " \\x.x/", "</░░░\>", "(░░░░░)___"] #Dead
            elif state == "Happy":
                emotion = [" |\_/|", " \\^.^/", " /u░u\  /", "(░░░░░)/"] #Happy
            elif state == "Bored":
                emotion = [" |\_/|", " \\¬.¬/", " /u░u\\", "(░░░░░)___"] #Bored
            else:
                emotion = [" |\_/|", " \\'.'/", " /u░u\  /", "(░░░░░)/"] #Normal
        return emotion
            
    def animate(self):
        animation = []
        if self.dirty == False: #clean
            if self.state == "Asleep":
                animation = [" |\_/|", " \\-.-/", " /u u\\", "( ___ )___"] #Sleepy
            elif self.state == "Hungry":
                animation = [" |\_/|", " \\'.'/", "</   \> /", "( ___ )/"] #Hungry
            elif self.state == "Angry":
                animation = [" |\_/|", " \\>.</", "</   \> /", "( ___ )/"] #Angry
            elif self.state == "Dead":
                animation = [" |\_/|", " \\x.x/", "</   \>", "( ___ )___"] #Dead
            elif self.state == "Happy":
                animation = [" |\_/|", " \\^.^/", "</   \> /", "( ___ )/"] #Happy
            elif self.state == "Bored":
                animation = [" |\_/|", " \\-.-/", " /u u\\", "( ___ )___"] #Bored
            else:
                animation = [" |\_/|", " \\-.-/", " /u u\  /", "( ___ )/"] #Normal/Blinking
        else:
            if self.state == "Asleep":
                animation = [" |\_/|", " \\-.-/", " /u░u\\", "(░░░░░)___"] #Sleepy
            elif self.state == "Hungry":
                animation = [" |\_/|", " \\'.'/", "</░░░\> /", "(░░░░░)/"] #Hungry
            elif self.state == "Angry":
                animation = [" |\_/|", " \\>.</", "</░░░\> /", "(░░░░░)/"] #Angry
            elif self.state == "Dead":
                animation = [" |\_/|", " \\x.x/", "</░░░\>", "(░░░░░)___"] #Dead
            elif self.state == "Happy":
                animation = [" |\_/|", " \\^.^/", "</░░░░\> /", "(░░░░░)/"] #Happy
            elif self.state == "Bored":
                animation = [" |\_/|", " \\-.-/", " /u░u\\", "(░░░░░)___"] #Bored
            else:
                animation = [" |\_/|", " \\-.-/", " /u░u\  /", "(░░░░░)/"] #Normal/Blinking
        return animation

class Bird(Pet):
    def __init__(self):
        super().__init__()
        self.type = "Bird"
        self.sound = "Chirp"

    def get_emotion(self, state):
        emotion = []
        if self.dirty == False: #clean
            if state == "Asleep":
                emotion = ["   w", " (-v-)", " ( w )", "  Y Y "] #Sleepy
            elif state == "Hungry":
                emotion = ["   w", " ('O')", "<( w )>", "  Y Y "] #Hungry
            elif state == "Angry":
                emotion = ["   w", " (>v<)", "<( w )>", "  Y Y "] #Angry
            elif state == "Dead":
                emotion = ["   w", " (×v×)", "<( w )>", "  Y Y "] #Dead
            elif state == "Happy":
                emotion = ["   w", " (^v^)", " ( w )", "  Y Y "] #Happy
            elif state == "Bored":
                emotion = ["   w", " (¬v¬)", " ( w )", "  Y Y "] #Bored
            else:
                emotion = ["   w", " ('v')", " ( w )", "  Y Y "] #Normal
        else: #dirty
            if state == "Asleep":
                emotion = ["   w", " (-v-)", " (░w░)", "  Y Y "] #Sleepy
            elif state == "Hungry":
                emotion = ["   w", " ('O')", "<(░w░)>", "  Y Y "] #Hungry
            elif state == "Angry":
                emotion = ["   w", " (>v<)", "<(░w░)>", "  Y Y "] #Angry
            elif state == "Dead":
                emotion = ["   w", " (×v×)", "<(░w░)>", "  Y Y "] #Dead
            elif state == "Happy":
                emotion = ["   w", " (^v^)", " (░w░)", "  Y Y "] #Happy
            elif state == "Bored":
                emotion = ["   w", " (¬v¬)", " (░w░)", "  Y Y "] #Bored
            else:
                emotion = ["   w", " ('v')", " (░w░)", "  Y Y "] #Normal
        return emotion
            
    def animate(self):
        animation = []
        if self.dirty == False: #clean
            if self.state == "Asleep":
                animation = ["   w", " (-v-)", " ( w )", "  Y Y "] #Sleepy
            elif self.state == "Hungry":
                animation = ["   w", " ('v')", " ( w )", "  Y Y "] #Hungry
            elif self.state == "Angry":
                animation = ["   w", " (>v<)", " ( w )", "  Y Y "] #Angry
            elif self.state == "Dead":
                animation = ["   w", " (×v×)", "<( w )>", "  Y Y "] #Dead
            elif self.state == "Happy":
                animation = ["   w", " (^v^)", "<( w )>", "  Y Y "] #Happy
            elif self.state == "Bored":
                animation = ["   w", " (-v-)", " ( w )", "  Y Y "] #Normal/Blinking
            else:
                animation = ["   w", " (-v-)", " ( w )", "  Y Y "] #Normal/Blinking
        else: #dirty
            if self.state == "Asleep":
                animation = ["   w", " (-v-)", " (░w░)", "  Y Y "] #Sleepy
            elif self.state == "Hungry":
                animation = ["   w", " ('v')", " (░w░)", "  Y Y "] #Hungry
            elif self.state == "Angry":
                animation = ["   w", " (>v<)", " (░w░)", "  Y Y "] #Angry
            elif self.state == "Dead":
                animation = ["   w", " (×v×)", "<(░w░)>", "  Y Y "] #Dead
            elif self.state == "Happy":
                animation = ["   w", " (^v^)", "<(░w░)>", "  Y Y "] #Happy
            elif self.state == "Bored":
                animation = ["   w", " (-v-)", " (░w░)", "  Y Y "] #Bored
            else:
                animation = ["   w", " (-v-)", " (░w░)", "  Y Y "] #Normal/Blinking
        return animation

class Monkey(Pet):
    def __init__(self):
        super().__init__()
        self.type = "Monkey"
        self.sound = "Oo Ee"

    def get_emotion(self, state):
        emotion = []
        if self.dirty == False: #clean
            if state == "Asleep":
                emotion = ["   w", "@(-.-)@", " /u u\\", "( ___ )___"] #Sleepy
            elif state == "Hungry":
                emotion = ["   w", "@('o')@", " /n n\\", "( ___ )~~"] #Hungry
            elif state == "Angry":
                emotion = ["   w", "@(>.<)@", " /n n\\", "( ___ )~~"] #Angry
            elif state == "Dead":
                emotion = ["   w", "@(x.x)@", "</   \>", "( ___ )___"] #Dead
            elif state == "Happy":
                emotion = ["   w", "@(^.^)@", " /u u\\", "( ___ )~~"] #Happy
            elif state == "Bored":
                emotion = ["   w", "@(¬.¬)@", " /u u\\", "( ___ )___"] #Bored
            else:
                emotion = ["   w", "@('.')@", " /u u\\", "( ___ )~~"] #Normal
        else: #dirty
            if state == "Asleep":
                emotion = ["   w", "@(-.-)@", " /u░u\\", "(░░░░░)___"] #Sleepy
            elif state == "Hungry":
                emotion = ["   w", "@('o')@", " /n░n\\", "(░░░░░)~~"] #Hungry
            elif state == "Angry":
                emotion = ["   w", "@(>.<)@", " /n░n\\", "(░░░░░)~~"] #Angry
            elif state == "Dead":
                emotion = ["   w", "@(x.x)@", "</░░░\>", "(░░░░░)___"] #Dead
            elif state == "Happy":
                emotion = ["   w", "@(^.^)@", " /u░u\\", "(░░░░░)~~"] #Happy
            elif state == "Bored":
                emotion = ["   w", "@(¬.¬)@", " /u░u\\", "(░░░░░)___"] #Bored
            else:
                emotion = ["   w", "@('.')@", " /u░u\\", "(░░░░░)~~"] #Normal
        return emotion
            
    def animate(self):
        animation = []
        if self.dirty == False: #clean
            if self.state == "Asleep":
                animation = ["   w", "@(-.-)@", " /u u\\", "( ___ )___"] #Sleepy
            elif self.state == "Hungry":
                animation = ["   w", "@('.')@", "</   \>", "( ___ )~~"] #Hungry
            elif self.state == "Angry":
                animation = ["   w", "@(>.<)@", "</   \>", "( ___ )~~"] #Angry
            elif self.state == "Dead":
                animation = ["   w", "@(x.x)@", "</   \>", "( ___ )___"] #Dead
            elif self.state == "Happy":
                animation = ["   w", "@(^.^)@", "</   \>", "( ___ )~~"] #Happy
            elif self.state == "Bored":
                animation = ["   w", "@(-.-)@", " /u u\\", "( ___ )___"] #Bored
            else:
                animation = ["   w", "@(-.-)@", " /u u\\", "( ___ )~~"] #Normal/Blinking
        else: #dirty
            if self.state == "Asleep":
                animation = ["   w", "@(-.-)@", " /u░u\\", "(░░░░░)___"] #Sleepy
            elif self.state == "Hungry":
                animation = ["   w", "@('.')@", "</░░░\>", "(░░░░░)~~"] #Hungry
            elif self.state == "Angry":
                animation = ["   w", "@(>.<)@", "</░░░\>", "(░░░░░)~~"] #Angry
            elif self.state == "Dead":
                animation = ["   w", "@(x.x)@", "</░░░\>", "(░░░░░)___"] #Dead
            elif self.state == "Happy":
                animation = ["   w", "@(^.^)@", "</░░░\>", "(░░░░░)~~"] #Happy
            elif self.state == "Bored":
                animation = ["   w", "@(-.-)@", " /u░u\\", "(░░░░░)___"]
            else:
                animation = ["   w", "@(-.-)@", " /u░u\\", "(░░░░░)~~"] #Normal/Blinking
        return animation

class Deer(Pet):
    def __init__(self):
        super().__init__()
        self.type = "Deer"
        self.sound = ""

    def get_emotion(self, state):
        emotion = []
        if self.dirty == False: #clean
            if state == "Asleep":
                emotion = [" ¥___¥", " \\-.-/", " /   \\", "( u_u )*"] #Sleepy
            elif state == "Hungry":
                emotion = [" ¥___¥", " \\'o'/", " /n n\\", "( ___ )*"] #Hungry
            elif state == "Angry":
                emotion = [" ¥___¥", " \\>.</", " /n n\\", "( ___ )*"] #Angry
            elif state == "Dead":
                emotion = [" ¥___¥", " \\x.x/", " /   \\", "( u_u )*"] #Dead
            elif state == "Happy":
                emotion = [" ¥___¥", " \\^.^/", " /n n\\", "( ___ )*"] #Happy
            elif state == "Bored":
                emotion = [" ¥___¥", " \\¬.¬/", " /   \\", "( u_u )*"] #Bored
            else:
                emotion = [" ¥___¥", " \\'.'/", " /   \\", "( u_u )*"] #Normal
        else: #dirty
            if state == "Asleep":
                emotion = [" ¥___¥", " \\-.-/", " /░░░\\", "(░u░u░)*"] #Sleepy
            elif state == "Hungry":
                emotion = [" ¥___¥", " \\'o'/", " /n░n\\", "(░░░░░)*"] #Hungry
            elif state == "Angry":
                emotion = [" ¥___¥", " \\>.</", " /n░n\\", "(░░░░░)*"] #Angry
            elif state == "Dead":
                emotion = [" ¥___¥", " \\x.x/", " /░░░\\", "(░u░u░)*"] #Dead
            elif state == "Happy":
                emotion = [" ¥___¥", " \\^.^/", " /n░n\\", "(░░░░░)*"] #Happy
            elif state == "Bored":
                emotion = [" ¥___¥", " \\¬.¬/", " /░░░\\", "(░u░u░)*"] #Bored
            else:
                emotion = [" ¥___¥", " \\'.'/", " /░░░\\", "(░u░u░)*"] #Normal
        return emotion
            
    def animate(self):
        animation = []
        if self.dirty == False: #clean
            if self.state == "Asleep":
                animation = [" ¥___¥", " \\-.-/", " /   \\", "( u_u )*"] #Sleepy
            elif self.state == "Hungry":
                animation = [" ¥___¥", " \\'.'/", " /   \\", "( u_u )*"] #Hungry
            elif self.state == "Angry":
                animation = [" ¥___¥", " \\>.</", " /   \\", "( u_u )*"] #Angry
            elif self.state == "Dead":
                animation = [" ¥___¥", " \\x.x/", " /   \\", "( u_u )*"] #Dead
            elif self.state == "Happy":
                animation = [" ¥___¥", " \\^.^/", " /   \\", "( u_u )*"] #Happy
            elif self.state == "Bored":
                animation = [" ¥___¥", " \\-.-/", " /   \\", "( u_u )*"] #Bored
            else:
                animation = [" ¥___¥", " \\-.-/", " /   \\", "( u_u )*"] #Normal/Blinking
        else: #dirty
            if self.state == "Asleep":
                animation = [" ¥___¥", " \\-.-/", " /░░░\\", "(░u░u░)*"] #Sleepy
            elif self.state == "Hungry":
                animation = [" ¥___¥", " \\'.'/", " /░░░\\", "(░u░u░)*"] #Hungry
            elif self.state == "Angry":
                animation = [" ¥___¥", " \\>.</", " /░░░\\", "(░u░u░)*"] #Angry
            elif self.state == "Dead":
                animation = [" ¥___¥", " \\x.x/", " /░░░\\", "(░u░u░)*"] #Dead
            elif self.state == "Happy":
                animation = [" ¥___¥", " \\^.^/", " /░░░\\", "(░u░u░)*"] #Happy
            elif self.state == "Bored":
                animation = [" ¥___¥", " \\-.-/", " /░░░\\", "(░u░u░)*"] #Bored
            else:
                animation = [" ¥___¥", " \\-.-/", " /░░░\\", "(░u░u░)*"] #Normal/Blinking
        return animation