# -----------------------------------------------------------
# Ryzobus v1.6
# Basic tests for parameters module
#
# (C) 2021 Hayden Eastwood,
# Contact: hayden.eastwood@gmail.com, +263 779 451 256
# -----------------------------------------------------------
import pytest
from monster import MonsterInvasion
import random

@pytest.fixture
def monster_configuration(capfd):
    random.seed(11)
    monster = MonsterInvasion('world_map_small.txt')
    out, err = capfd.readouterr() # Discard error from missing user input
    monster.initial_number_of_monsters = 15
    return monster

class TestMonsterInvasion:    

    def test_parachute_monsters_in(self,monster_configuration):
        colonised_towns = monster_configuration.parachute_monsters_in()
        print (colonised_towns)
        assert len(colonised_towns) == monster_configuration.initial_number_of_monsters

    def test_move_monsters(self, monster_configuration):
        monster_configuration.parachute_monsters_in()
        original_towns = monster_configuration.colonised_towns        
        new_colonised_towns = monster_configuration.move_monsters()
        assert original_towns != new_colonised_towns

    def test_make_monster_battles(self, monster_configuration):
        monster_configuration.parachute_monsters_in()
        monster_configuration.move_monsters()
        monster_battles = monster_configuration.make_monster_battles()
        assert monster_battles == {'Asmismu': [2, 6], 'Dusmu': [3, 8, 12], 'Mesmina': [7, 10]}

    def test_monsters_die(self, monster_configuration):        
        monster_configuration.parachute_monsters_in()
        old_colonised_configuration = monster_configuration.colonised_towns
        monster_configuration.move_monsters()    
        monster_configuration.make_monster_battles()
        new_colonised_configuration = monster_configuration.monsters_die()                                
        assert len(new_colonised_configuration) < len(old_colonised_configuration)

    def test_monsters_die(self, monster_configuration):        
        monster_configuration.parachute_monsters_in()
        old_colonised_configuration = monster_configuration.colonised_towns
        monster_configuration.move_monsters()    
        monster_configuration.make_monster_battles()
        new_colonised_configuration = monster_configuration.monsters_die()                                
        assert len(new_colonised_configuration) < len(old_colonised_configuration)

    def test_towns_die(self, monster_configuration):        
        number_previous_towns = monster_configuration.number_of_remaining_towns()
        monster_configuration.parachute_monsters_in()
        monster_configuration.move_monsters()    
        monster_configuration.colonised_towns 
        monster_configuration.make_monster_battles() 
        remaining_towns = monster_configuration.towns_die()
        assert len(remaining_towns) < number_previous_towns
