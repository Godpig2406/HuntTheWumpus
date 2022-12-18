import random

Playing = True
# Index is the room number, list is neighbor rooms connected to it
Map = [[1, 4, 7], [0, 2, 9], [1, 3, 11], [2, 4, 13], [0, 3, 5], [4, 6, 14],
       [5, 7, 16], [0, 6, 10], [9, 10, 11], [1, 8, 10], [7, 9, 19], [2, 8, 12],
       [11, 13, 17], [3, 12, 14], [5, 13, 15], [14, 16, 17], [7, 15, 19],
       [12, 15, 18], [8, 17, 19], [11, 16, 18]]


class room:
    def __init__(self, num, type="empty"):
        # Room number
        self.num = num
        # Type of the hazards within the room
        self.type = type
        # List of 3 rooms connected to it
        self.link = Map[num]

    def move_wumpus():
        # When arrow missed, wumpus will randomly move to it's neighbor room.
        wumpus = Hazard[0]
        # This generates a new location for wumpus
        move = Cave[wumpus].link[random.randint(0, 2)]
        Cave[move].type, Cave[wumpus].type = Cave[wumpus].type, Cave[move].type
        # Update the cavemap
        with open("cavemap.txt", "w") as file:
            for i in Cave:
                file.write(str(i.num) + str(i.type) + str(i.link) + "\n")
        # Check if wumpus is in player's room'
        if Steve.location == move:
            return True
        else:
            return False


class player:
    def __init__(self, location, arrow):
        # The room Steve is in
        self.location = location
        # Amount of arrow
        self.arrow = arrow

    def action(self):
        # Ask the player to choose an action.
        print(f"""-----------------------------------------
You are in room {self.location}.""")
        self.sense()
        get_input = input(f"""Exits go to:{Cave[self.location].link}
-----------------------------------------
What do you want to do? (M)ove/(S)hoot? """)
        destn = input("Where? ")
        if get_input.upper() == "M" and destn.isnumeric():
            if int(destn) in Map[self.location]:
                # Checks if destanation is reachable
                self.location = int(destn)
        # Player to shoot
        elif get_input.upper() == "S" and destn.isnumeric():
            if self.arrow > 0:
                self.shoot(int(destn))
            else:
                print(
                    "You don't have arrow left, you're trapped here forever!")
        else:
            if input("Do you want to save and quit? y/N ").upper() == "Y":
                return True

    def sense(self):
        if self.location == 7 and input(
                "Hi from the narrater! ").upper() == "SUS":
            import egg

        # Give hints, but avoids printing the same hint multiple times.
        repeats = [False for i in range(3)]
        for i in Cave[self.location].link:
            if Cave[i].type == "wumpus" and not repeats[0]:
                print("You smell something terrible nearby")
                repeats[0] = True
            elif Cave[i].type == "pit" and not repeats[1]:
                print("You feel a cold wind blowing from a nearby cavern.")
                repeats[1] = True
            elif Cave[i].type == "bat" and not repeats[2]:
                print("You hear a rustling sound nearby")
                repeats[2] = True

    def shoot(self, to):
        if to in Cave[self.location].link:
            # Loss an arrow
            self.arrow -= 1
            global Playing
            if Cave[to].type == "wumpus":
                print("YOU KILLED THE WUMPUS! GOOD JOB, BUDDY!!!")
                Playing = False
            else:
                print(f"You missed!\nYou have {str(self.arrow)} arrows left.")
                if room.move_wumpus():
                    # The wumpus moved to player's room
                    print("You woke up the wumpus......")
                    Playing = False
                else:
                    # The wumpus moves to another room
                    print("You heard a rumbling in a nearby cavern.")
        else:
            print("Not in range")

    def check(self):
        # Check if the player is in special rooms with hazard
        global Playing
        if Cave[self.location].type == "wumpus":
            Playing = False
            print("The wumpus ate you up!")
        elif Cave[self.location].type == "pit":
            Playing = False
            print("You fell into a bottomless pit. Enjoy the ride!")
        elif Cave[self.location].type == "bat":
            self.location = random.randint(0, 19)
            print("The bats whisk you away!")
            self.check()


def create():
    global Cave, Hazard, Steve
    # Creating the room objects
    Cave = [room(i) for i in range(20)]

    # This put the hazard in random rooms before the game starts
    Hazard = random.sample(range(20), 7)
    while True:
        Temp = random.randint(0, 19)
        if Temp not in Hazard:
            break
    Steve = player(Temp, 5)
    Cave[Hazard[0]].type = "wumpus"
    for i in range(3):
        Cave[Hazard[i + 1]].type = "pit"
    for i in range(3):
        Cave[Hazard[i + 4]].type = "bat"
    # Save it to the cavemap
    with open("cavemap.txt", "w") as file:
        for i in Cave:
            file.write(str(i.num) + str(i.type) + str(i.link) + "\n")


def load_map(data):
    global Cave, Hazard, Steve
    Cave = []
    for i in range(20):
        Cave.append(room(i, data[0][i]))
    Hazard = data[1]
    Steve = player(data[2], data[3])
    with open("cavemap.txt", "w") as file:
        for i in Cave:
            file.write(str(i.num) + str(i.type) + str(i.link) + "\n")


# The game loop
def game():
    while Playing:
        if Steve.action():
            # Check if player quits
            return True
        Steve.check()
