# -----------------------------------------------------------
# Monsters v1.0 - Main file (run this!)
# Main script for a monster simulation to make monsters traverse a map of 
# countries. For more information see the Readme.MD
# 
# (C) 2021 Hayden Eastwood,
# Contact: hayden.eastwood@gmail.com, +263 779 451 256
# -----------------------------------------------------------

from monster import MonsterInvasion

# ---- Configurable settings ----
number_of_monster_steps = 10000
monster_town_file = 'data/world_map_small.txt'
output_file = 'data/map_after_monsters.txt'         # The output file name to write to
monster_numbers = 12                                # Set the number of monsters in the file 
                                                    # (if 0 it'll default to prompting on the GUI)
# -----------------------------

# Run the monster simulation
try:
    monster_numbers
except:    
    if monster_numbers < 1:
        monster_numbers = MonsterInvasion.get_cmdln_monsters()
monster = MonsterInvasion(monster_town_file, monster_numbers)
monster.output_file_name = output_file
monster.initial_number_of_monsters = monster_numbers
monster.run(steps=number_of_monster_steps)
