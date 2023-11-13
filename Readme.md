# Pokémon Battle Simulator
The Pokémon game is a Python program that simulates battles between trainers and Pokémon. Here's a step-by-step description of its main functions:

The game attempts to load Pokémon data from a file named pokedex.pkl. If the file doesn't exist, it tries to download Pokémon data from the internet using the requests_html library. Functions like fetch_pokemon_info are used to get detailed information for each Pokémon, including their name, type, and attacks.

Player Profile: The player is prompted to enter their name, and a player profile is created, including their name, a randomly chosen Pokémon inventory, and game statistics.

Pokémon Battles: The player faces randomly selected wild Pokémon. A Pokémon from the inventory is chosen for battle. During battle, the player can take actions such as attacking, using health potions, throwing Pokéballs to capture Pokémon, and switching Pokémon.

Experience and Levels: After battles, experience points are awarded to participating Pokémon. When a Pokémon accumulates enough experience points, it levels up, restoring its health, and notifying the player.

End of the Game: The game continues with battles until all of the player's Pokémon are knocked out. A message is displayed indicating the total number of battles lost.

The code uses libraries like HTMLSession and BeautifulSoup to extract information from web pages related to Pokémon. It also utilizes data serialization with pickle to save and load Pokémon data locally.

In summary, the game simulates a Pokémon trainer experience with strategic battles and RPG elements, including Pokémon capture and level progression.


## Installation

***Dependencias:*** requests_html

```bash
-pip install requests-html

```

## RUN


```bash
-Python main.py
```