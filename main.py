from monster import MonsterInvasion

# ---- Configurable settings ----
number_of_monster_steps = 10000
monster_town_file = 'data/world_map_medium.txt'
monster_numbers = 0                       # set the number of monsters in the file (
                                          # if 0 it'll default to prompting on the GUI)
output_file = 'data/map_after_monsters.txt'
# -----------------------------

# Run the monster simulation
if monster_numbers < 1:
    monster_numbers = MonsterInvasion.get_cmdln_monsters()
monster = MonsterInvasion(monster_town_file, monster_numbers)
monster.initial_number_of_monsters = monster_numbers
monster.run(steps=number_of_monster_steps)
