import pickle
import random
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from pprint import pprint

# Constants
POKEMON_BASE = {"name": "", "current_health": 100, "base_health": 100, "level": 1, "type": None, "current_exp": 0, "attacks": None}
URL_BASE = "https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/pkmn&pk="


def parse_type(types):
    parsed_type = ""
    for img in types[5:7]:
        parsed_type += ","
        for data_img in img[10:19]:
            if data_img != '"' and data_img != " ":
                parsed_type += data_img

    return parsed_type


def fetch_pokemon_info(index):
    url = "{}{}".format(URL_BASE, index)
    try:
        session = HTMLSession()
        pokemon_page = session.get(url)
        soup = BeautifulSoup(pokemon_page.text, "lxml")
    except Exception as e:
        print(f"Error fetching Pokémon data: {e}")
        return None

    new_pokemon = POKEMON_BASE.copy()

    name = pokemon_page.html.find(".mini", first=True).text
    for char in name:
        if char != "\n":
            new_pokemon["name"] += char
        else:
            break

    types = str(soup.body.find_all("img"))
    types = types.split(",")
    parsed_type = parse_type(types)
    parsed_type = parsed_type.split(",")
    new_pokemon["type"] = []

    for T in parsed_type:
        if T in ['planta', "veneno", "psiquico", "volador", "normal", "tierra"]:
            new_pokemon["type"].append(T)
        elif T in ["fuegos", "luchas", "bichos", "hielos"]:
            new_pokemon["type"].append(T[0:5])
        elif T in ["aguasr", "hadasr", "roca"]:
            new_pokemon["type"].append(T[0:4])
        elif T in ["electric"]:
            new_pokemon["type"].append("electrico")

    url = "{}{}".format("https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/movimientos_nivel&pk=", index)
    try:
        session = HTMLSession()
        pokemon_page = session.get(url)
    except Exception as e:
        print(f"Error fetching Pokémon attacks: {e}")
        return None

    new_pokemon["attacks"] = []

    for attacks_item in pokemon_page.html.find(".pkmain")[-1].find("tr .check3"):
        attack = {
            "name": attacks_item.find("td", first=True).find("a", first=True).text,
            "type": attacks_item.find("td")[1].find("img", first=True).attrs["alt"],
            "damage": int(attacks_item.find("td")[3].text.replace("--", "0")),
            "min_level": attacks_item.find("th", first=True).text,
        }
        new_pokemon["attacks"].append(attack)

    return new_pokemon


def load_or_download_pokemons():
    try:
        print("Loading the Pokémon data...")
        with open("pokedex.pkl", "rb") as pokedex:
            all_pokemons = pickle.load(pokedex)
    except FileNotFoundError:
        print("File not found, downloading from the internet...")
        all_pokemons = [fetch_pokemon_info(index + 1) for index in range(151)]
        all_pokemons = [pokemon for pokemon in all_pokemons if pokemon is not None]  # Remove None entries
        with open("pokedex.pkl", "wb") as pokedex:
            pickle.dump(all_pokemons, pokedex, -1)
        print("\nAll Pokémon data downloaded successfully and saved to 'pokedex.pkl'.")

    print("The list of Pokémon has been loaded successfully...")
    return all_pokemons


def get_player_profile(pokemon_list):
    return {
        "player_name": input("What is your name?: "),
        "pokemon_inventory": [random.choice(pokemon_list) for _ in range(3)],
        "combats": 0,
        "pokeballs": 0,
        "health_potion": 0,
    }


def any_player_pokemon_lives(profile):
    return sum([pokemon["current_health"] for pokemon in profile["pokemon_inventory"]]) > 0


def choose_pokemon(profile):
    chosen = None
    while not chosen:
        for index, pokemon in enumerate(profile["pokemon_inventory"]):
            print(f"{index} - {pokemon_info(pokemon)}")

        try:
            return profile["pokemon_inventory"][int(input("Which one do you choose?: "))]
        except (ValueError, IndexError):
            print("Invalid option!! Try again.")


def pokemon_info(pokemon):
    return "{} | lvl {} | type {} | HP {}/{}".format(
        pokemon["name"], pokemon["level"], pokemon["type"], pokemon["current_health"], pokemon["base_health"]
    )


def player_attack(my_pokemon, enemy):
    pass


def enemy_attack(my_pokemon, enemy):
    pass


def assign_exp(attacks_history):
    for pokemon in attacks_history:
        points = random.randint(1, 5)
        pokemon["current_exp"] += points

        while pokemon["current_exp"] > 20:
            pokemon["current_exp"] -= 20
            pokemon["level"] += 1
            pokemon["current_health"] = pokemon["base_health"]
            print(f"Your Pokémon has leveled up to {pokemon['level']}!")


def choose_action():
    pass


def heal_pokemon(profile, pokemon):
    if profile["health_potion"] > 0:
        print(f"Healing {pokemon['name']} with a health potion.")
        pokemon["current_health"] = min(pokemon["current_health"] + 50, pokemon["base_health"])
        profile["health_potion"] -= 1
        print(f"{pokemon['name']}'s health: {pokemon['current_health']}/{pokemon['base_health']}")
    else:
        print("No health potions available.")


def capture_with_pokeball(profile, enemy_pokemon):
    if profile["pokeballs"] > 0:
        capture_chance = min(0.5 + 0.5 * (enemy_pokemon["current_health"] / enemy_pokemon["base_health"]), 0.9)
        if random.random() < capture_chance:
            print(f"Success! You captured {enemy_pokemon['name']} with a Pokéball.")
            profile["pokeballs"] -= 1
            profile["pokemon_inventory"].append(enemy_pokemon)
            print(f"{enemy_pokemon['name']} has been added to your Pokémon inventory.")
        else:
            print(f"Oops! {enemy_pokemon['name']} broke free.")
    else:
        print("No Pokéballs available.")


def fight(profile, enemy_pokemon):
    print("--- NEW BATTLE ---")
    print(f"You will battle against {pokemon_info(enemy_pokemon)}")
    print("\nCHOOSE YOUR POKÉMON:")
    chosen_pokemon = choose_pokemon(profile)
    print(f"{chosen_pokemon['name']} VS {enemy_pokemon['name']}")
    attack_history = []

    while any_player_pokemon_lives(profile) and enemy_pokemon["current_health"] > 0:
        print(f"BEGIN --> {chosen_pokemon['name']}")
        action = None

        while action not in ["A", "P", "H", "S"]:
            action = input("What do you want to do?: [A]ttack, [P]okeball, [H]ealth Potion, [S]witch Pokémon")

        if action == "A":
            player_attack(chosen_pokemon, enemy_pokemon)
            attack_history.append(chosen_pokemon)
        elif action == "H":
            # Heal the Pokémon by 50 health if there are potions
            heal_pokemon(profile, chosen_pokemon)
        elif action == "P":
            # If the player has pokéballs, attempt to capture the Pokémon
            # with a probability relative to its health
            capture_with_pokeball(profile, enemy_pokemon)
        elif action == "S":
            # The player switches Pokémon
            chosen_pokemon = choose_pokemon(profile)

        enemy_attack(chosen_pokemon, enemy_pokemon)

        if chosen_pokemon["current_health"] == 0 and any_player_pokemon_lives(profile):
            chosen_pokemon = choose_pokemon(profile)

    if enemy_pokemon["current_health"] == 0:
        print("YOU WON!!")
        assign_exp(attack_history)

    print("--- BATTLE END ---")
    input("Press ENTER to continue")


def item_lottery():
    # According to the random factor, the player receives a health potion or a pokéball
    pass

