"""
The follwing code uses functions to execute the adventure from Week 4 and extends
it with Week 5 content.
"""

import random #In order to use random.choice() and random.random()

def acquire_item(inventory, item):
    """Appends the item to the inventory list."""
    added_to_inventory = []
    if item:
        #The .append() function will add an item into aquired_items as the last element.
        #It is useful when lists need to gain additional elements.
        inventory.append(item)
        #The + is list concatenation, so the items of inventory get copied into added_to_inventory.
        #This is useful when two lists have elements that need to be combined into one large list.
        added_to_inventory = added_to_inventory + inventory
        print(f"You acquired a {item}!")
    return added_to_inventory

def display_inventory(inventory):
    """This function will display and format the player's inventory list."""
    number = 1
    if inventory:
        print("Your inventory:")
        #The in operator takes every element inventory and assigns them to item.
        #It is very useful in loops like the below for loop.
        for item in inventory:
            print(f"{number}. {item}")
            number += 1
    else:
        print("Your inventory is empty.")

def display_player_status(player_stats):
    """Prints the player's current health to the console in a user-friendly format."""
    player_health_value = player_stats["health"]
    player_attack_value = player_stats["attack"]
    print(f"Your current health: {player_health_value}")
    print(f"Your current attack: {player_attack_value}")

def handle_path_choice(player_stats):
    """Randomly chooses a path for the player."""
    player_health = player_stats["health"]
    player_path = random.choice(["left","right"])
    if player_path == "left":
        print("You encounter a friendly gnome who heals you for 10 health points.")
        player_health += 10
        player_health = min(player_health, 100)
    if player_path == "right":
        print("You fall into a pit and lose 15 health points.")
        player_health -= 15
        if player_health < 0:
            player_health = 0
            print("You are barely alive!")
    player_stats["health"] = player_health
    return player_stats

def player_attack(monster_health):
    """Simulates the player's attack."""

    print("You strike the monster for 15 damage!")
    updated_monster_health = monster_health - 15
    return updated_monster_health

def monster_attack(player_health):
    """Simulates the monster's attack."""

    critical_num = random.random() #Generates number between (0,1)
    if critical_num < 0.5:
        print("The monster lands a critical hit for 20 damage!")
        updated_player_health = player_health - 20
    else:
        print("The monster hits you for 10 damage!")
        updated_player_health = player_health - 10
    return updated_player_health

def combat_encounter(player_stats, monster_health, has_treasure):
    """Manages the combat encounter using a while loop."""
    player_health = player_stats["health"]
    while player_health > 0 and monster_health > 0:
        monster_health = player_attack(monster_health)
        if monster_health <= 0:
            print("You defeated the monster!")
            break
        player_health = monster_attack(player_health)
        if player_health <= 0:
            print("Game Over!")
            has_treasure = False
            break
        player_stats["health"] = player_health
        display_player_status(player_stats)
    return has_treasure # boolean

def check_for_treasure(has_treasure):
    """Checks the value of has_treasure."""

    if has_treasure:
        print("You found the hidden treasure! You win!")
    else:
        print("The monster did not have the treasure. You continue your journey.")

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues):
    """Iterates through each room in dungeon_rooms and prints the room_description."""
    updated_inventory = []
    temp_player_health = player_stats["health"]
    #The in operator takes every element of dungeon_rooms and assigns them to room.
    # This is very useful in loops like the below for loop.
    for room in dungeon_rooms:
        print(room[0])
        if room[0] == "Cryptic Library":
            possible_clues = ["The treasure is hidden where the dragon sleeps.",
            "The key lies with the gnome.", "Beware the shadows.", "The amulet "
            "unlocks the final door."]
            selected_clues = random.sample(possible_clues, 2)
            print(selected_clues)
            for clue in selected_clues:
                find_clue(clues, clue)
            if player_stats["can_bypass_puzzle"]:
                print("You understand the meaning of the clues and can bypass a "
                "puzzle challenge in one other room.")
        if room[1]:
            print(f"You found a {room[1]} in the room.")
            updated_inventory = acquire_item(inventory, room[1])
        if room[2] == "puzzle":
            print("You encounter a puzzle!")
            if player_stats["can_bypass_puzzle"]:
                puzzle_decision = input("Would you like to solve or skip the puzzle?")
            else:
                puzzle_decision = "solve"
            puzzle_success = random.choice([True, False])
            if puzzle_decision == "solve" and puzzle_success:
                print(room[3][0])
                temp_player_health = temp_player_health + room[3][2]
            elif puzzle_decision == "solve" and not puzzle_success:
                print(room[3][1])
                temp_player_health = temp_player_health + room[3][2]
            elif puzzle_decision == "skip":
                print("You used your knowledge from the staff of wisdom to bypass "
                    "the puzzle.")
                temp_player_health = temp_player_health + room[3][2]
                player_stats["can_bypass_puzzle"] = False
            if temp_player_health < 0:
                temp_player_health = 0
                print("You are barely alive!")
        if room[2] == "trap":
            print("You see a potential trap!")
            trap_decision = input("Do you want to disarm or bypass the trap?")
            trap_success = random.choice([True, False])
            if trap_decision == "disarm" and trap_success:
                print(room[3][0])
                temp_player_health = temp_player_health + room[3][2]
            elif trap_decision == "disarm" and not trap_success:
                print(room[3][1])
                temp_player_health = temp_player_health + room[3][2]
            if temp_player_health < 0:
                temp_player_health = 0
                print("You are barely alive!")
        if room[2] == "none":
            print("There doesn't seem to be a challenge in this room. You move on.")
            temp_player_health += 0

        player_stats["health"] = temp_player_health
        display_inventory(updated_inventory)
        display_player_status(player_stats)
    try:
        #The del method will take the element in index 1 of room and remove it from room
        del dungeon_rooms[0] #Here, we try to remove the first room
    except TypeError:
        print("Error: Tuples like room in dungeon_rooms are immutable. This means that the rooms "
            "cannot be changed once they are defined. Thus, del dungeon_rooms[0][1] produces "
            "an error.")
    return player_stats, updated_inventory, clues

def discover_artifact(player_stats, artifacts, artifact_name):
    """Player discovers an artifact, it is then removed from the dictionary so
    it can only be found once."""
    if artifact_name in artifacts: #The in operator checks if the artifact is in the dictionary
        print(artifacts[artifact_name]["description"])
        if artifacts[artifact_name]["effect"] == "increases health":
            player_stats["health"] += artifacts[artifact_name]["power"]
        elif artifacts[artifact_name]["effect"] == "enhances attack":
            player_stats["attack"] += artifacts[artifact_name]["power"]
        elif artifacts[artifact_name]["effect"] == "solves puzzles":
            player_stats["can_bypass_puzzle"] = True
        print(f"This artifact had this effect: {artifacts[artifact_name]["effect"]}" )
        del artifacts[artifact_name] #The remove operation removes the specific artifact
    else:
        print("You found nothing of interest.")
    return player_stats, artifacts

def find_clue(clues, new_clue):
    """If a clue is found, it is added to the clues set."""
    if new_clue in clues:
        print("You already know this clue.")
    else:
        clues.add(new_clue) #.add() will add the clue string to the clues set
        print(f"You discovered a new clue: {new_clue}")
    return clues

def main():
    """Executes the adventure using all previously defined functions."""

    dungeon_rooms = [
        ("Cryptic Library", None, "library", None),
        ("Dusty library", "key", "puzzle",
        ("Solved puzzle!", "Puzzle unsolved.", -5)),
        ("Narrow passage, creaky floor", "torch", "trap",
        ("Avoided trap!", "Triggered trap!", -10)),
        ("Grand hall, shimmering pool", "healing potion", "none", None),
        ("Small room, locked chest", "treasure", "puzzle",
        ("Cracked code!", "Chest locked.", -5)),
        ]

    player_stats = {'health': 100, 'attack': 5, 'can_bypass_puzzle': False}

    monster_health = 70

    inventory = []

    clues = set()

    artifacts = {

        "amulet_of_vitality": {
            "description": "Glowing amulet, life force.",
            "power": 15,
            "effect": "increases health"
        },
        "ring_of_strength": {
            "description": "Powerful ring, attack boost.",
            "power": 10,
            "effect": "enhances attack"
        },
        "staff_of_wisdom": {
            "description": "Staff of wisdom, ancient.",
            "power": 5,
            "effect": "solves puzzles"
        }
    }

    has_treasure = random.choice([True, False])

    display_player_status(player_stats)

    player_stats = handle_path_choice(player_stats)

    if player_stats['health'] > 0:
        treasure_obtained_in_combat = combat_encounter(player_stats, monster_health, has_treasure)
        if treasure_obtained_in_combat is not None:
            check_for_treasure(treasure_obtained_in_combat)

        if random.random() < 0.3:
            artifact_keys = list(artifacts.keys())
            if artifact_keys:
                artifact_name = random.choice(artifact_keys)
                player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name)
                display_player_status(player_stats)

        if player_stats['health'] > 0:
            player_stats, inventory, clues = enter_dungeon(player_stats, inventory, dungeon_rooms,
                clues)

            print("\n--- Game End ---")
            display_player_status(player_stats)
            print("Final Inventory:")
            display_inventory(inventory)
            print("Clues:")
            if clues:
                for clue in clues:
                    print(f"- {clue}")
            else:
                print("No clues.")

#Will run the main function
if __name__ == "__main__":
    main()
