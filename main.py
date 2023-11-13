from functions import *


def main():
    pokemon_list = load_or_download_pokemons()
    player_profile = get_player_profile(pokemon_list)
    pprint(player_profile)

    while any_player_pokemon_lives(player_profile):
        enemy_pokemon = random.choice(pokemon_list)
        fight(player_profile, enemy_pokemon)
        item_lottery()

    print(f"You lost in battle number {player_profile['combats']}")


if __name__ == "__main__":
    main()