import wumpus as wp


def save(data):
    with open("saves.txt", "w") as file:
        for i in data[0]:  # Room Type
            file.write(str(i) + "\n")
        for i in data[1]:  # Hazard rooms
            file.write(str(i) + "\n")
        file.write(str(data[2]) + "\n" + str(data[3]))


load = input("Play from saved file? Y/n ")
if load == "" or load.upper() == "Y":
    # Read data from saves and send load it to the game
    with open("saves.txt", "r") as file:
        data = file.read().splitlines()
    wp.load_map([
        data[:20], [int(i) for i in data[20:27]],
        int(data[27]),
        int(data[28])
    ])

else:
    # Create a new game
    wp.create()
# Saves the game
if wp.game():
    save([[i.type for i in wp.Cave], wp.Hazard, wp.Steve.location,
          wp.Steve.arrow])
