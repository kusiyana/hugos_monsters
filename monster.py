import sys
import numpy as np
from matplotlib import pyplot as plt
import networkx as nx
import random
import collections
import time


class MonsterInvasion:    
    """ Class to govern all aspects of monster invasion of 
    global towns
    """
    
    def __init__(self, towns_file):
        self.town_file_name = towns_file
        self.initial_number_of_monsters = self.__get_cmdln_monsters()     
        self.town_graph = nx.DiGraph()                
        self.__make_towns_map(towns_file)
        self.town_initial_state = self.town_graph.copy()             
        self.colonised_towns = {}
        self.initial_number_of_towns = self.__number_of_remaining_towns()
        self.previous_colonised_towns = []
        self.trapped_monsters = []


    def parachute_monsters_in(self):
        """ Parachute monsters in to random towns to begin with """        
        random_landings = self.__make_random_number(self.initial_number_of_towns, self.initial_number_of_monsters) 
        monster_ids = self.__initialise_monster_names()
        towns=np.array(self.town_graph.nodes())
        self.colonised_towns = dict(zip(monster_ids, towns[random_landings]))                    
        return self.colonised_towns

    def move_monsters(self):
        """ Move monsters from one town to the next 
        Monsters walk to one of the possible connected towns
       
        Requires:
            self.colonised_towns - the list of colonised towns to consider
            self.town_graph.edges - the available walks from one town to the next
        Updates: self.colonised_towns
        Returns: self.colonised_towns
        """
        new_colonised_towns = {}                
        for monster, town in self.colonised_towns.items():
            town_possibilities = self.__get_town_possibilities(town)
            if town_possibilities:
                new_town = town_possibilities[
                    self.__make_random_number(len(town_possibilities),1)[0]
                    ]            
                new_colonised_towns[monster] = new_town
            else:
                new_colonised_towns[monster] = town                         # No possibilities, monster is trapped                        
        self.previous_colonised_towns = self.colonised_towns                # Get this so we can find trapped monsters later
        self.colonised_towns = new_colonised_towns        
        return new_colonised_towns
    
    def make_monster_battles(self):
        """ Given all the towns that are colonised
        find which towns will die in an epic monster battle
        Note: this reverses the dictionary so that 
        town keys -> list of monsters in them
        
        Requires:
            dict: self.colonised_towns - the list of colonised towns to consider
        Updates
            dict: self.monster_battles_by_town 
        Returns: 
            dict: self.monster_battles_by_town
        """
        k_v_exchanged = {}
        monster_battles_by_town = {}
        for monster, town in self.colonised_towns.items():
            if town not in k_v_exchanged:                
                k_v_exchanged[town] = [monster]
            else:                
                k_v_exchanged[town].append(monster)                
                if len(k_v_exchanged[town]) > 1:      
                    monster_battles_by_town[town] = k_v_exchanged[town]
        self.monster_battles_by_town = monster_battles_by_town
        return monster_battles_by_town

    def monsters_die(self):
        """ Kill a monster that has succumbed to a monster fight 
        and update the colonised towns list

        Requires:
            dict: self.monster_battles_by_town
            dict: self.colonised_towns
        Updates:
            dict: self.monster_battles_by_town
        Returns:
            dict: self.colonised_towns
        """                         
        for town, monsters in self.monster_battles_by_town.items():
            self.__log_io(f'monsters {monsters} die fighting in town {town}!',2)
            for monster in monsters:                
                del self.colonised_towns[monster]        
        return self.colonised_towns

    def towns_die(self):
        """ Kill off towns that die in monster carnage        
        Requires:
            dict: self.monster_battles_by_town            
        Updates:
            graph: self.town_graph graph instance
        Returns:
            dict: list of towns remaining
        """
        for town, monsters in self.monster_battles_by_town.items():            
            self.town_graph.remove_node(town)
        return (self.town_graph.nodes())


    def stats(self, day: int):
        """ Provide key stats on the invasion """
        print ('-----------------STATS - ---------------------')
        print (f'Day:\t\t\t\t\t {day}')        
        print (f'Number of alive monsters: \t\t {self.__number_of_alive_monsters()}')
        # print (f'Trapped monsters: \t\t {self.trapped_monsters}')
        print (f'Number of alive towns: \t\t\t {self.__number_of_remaining_towns()}')        
        print ('-----------------STATS---------------------')
        print (' ')

    def run(self, steps: int):
        """ Run a simulation for n steps """        
        self.parachute_monsters_in()
        self.stats(0)         
        before_towns = self.colonised_towns.copy()
        for d in range(1,steps+1):                                          
            self.move_monsters()                        
            if self.make_monster_battles():                
                self.monsters_die()                        
                self.towns_die()                                   
            if self.__number_of_alive_monsters() < 1:
                self.__log_io('Monsters killed all of each other!') 
                break
        self.stats(steps)
        return before_towns, self.colonised_towns, self.town_graph            

    def draw_towns(self, file_name: str):
        """ Plot graph of the towns if needed """                   
        nx.draw_networkx(self.town_graph, arrows=True)
        plt.tight_layout()
        plt.savefig(file_name, format="PNG")
        plt.clf()

    # - - - - Private methods - - - -
    @staticmethod
    def __log_io(message: str, level:int =1):
        if level==1:
            deco_num = 2
        elif level==2:
            deco_num = 4
        decos = '-' * deco_num
        print (f'-- \t {decos} {message} ')
    
    def __get_town_possibilities(self, town):
        """ Get the possible transitions for each town, 
        excluding the town that the monster is already in
        """
        possibilities = [possibility[1] for possibility in self.town_graph.edges(town) if possibility is not town]
        return possibilities


    def __initialise_monster_names(self):
        """ Create monster names 
        For now these are just numerical IDs
        """
        monster_names = range(1, self.initial_number_of_monsters+1) 
        return monster_names

    @staticmethod
    def __make_random_number(max_value: int, number_of_values: int) -> list:
        """ Return random numbers where needed 
        Input:
            int: max_value - the highest possible random number
            int: number_of_values - how many of them to return
        
        Returns:
            list: random values of size number_of_values
        """             
        return random.sample(range(0, max_value), number_of_values)

    def __add_1_town_to_map(self, town: str):
        """ Add edges to graph. Each town and 
        its placement go on to form the edges and nodes.
        """
        town_unpacked = town.replace('\n', '').split(' ')        
        town_name = town_unpacked[0]
        try:    
            for town in town_unpacked[1:]:                
                self.town_graph.add_edges_from([(town_name, town.split('=')[1])])
        except :
            raise RuntimeError ("Could not add 1 or more edges or nodes. Aborting.")
        return self.town_graph.edges()
            
    def __make_towns_map(self, town_file_name: str) -> list:
        """ Construct town map from town file """        
        town_entries = self.__read_town_file(town_file_name)
        try:
            for entry in town_entries:                 
                self.__add_1_town_to_map(entry)        
        except Exception:
            raise RuntimeError('Could not add one or more locations to map, aborting!')            
        return list(self.town_graph.nodes())

    def __free_towns(self):
        number_free_towns = self.__number_of_remaining_towns() - len(list(set(list(self.colonised_towns.values()))))
        return number_free_towns

    @staticmethod
    def __get_cmdln_monsters():
        """ Get number of monsters from command line """
        if len(sys.argv) < 2:            
            raise ValueError ('HELP: Please provide number of monsters!')    
        try:            
            return int(sys.argv[1])
        except:
            raise ValueError ('The number you enter has to be an integer!')
            
    
    @staticmethod
    def __read_town_file(town_file_name: str) -> list:
        try:
            towns_file = open(town_file_name, 'r')
            towns = [town for town in towns_file]                                 
            towns_file.close()        
        except FileNotFoundError:
            raise FileNotFoundError('Could not open file, please check its name and try again!')
        return towns

    def __number_of_remaining_towns(self):        
        return len(list(self.town_graph.nodes()))
    
    def __number_of_alive_monsters(self):
        return len(self.colonised_towns)

if __name__ == '__main__':
    monster = MonsterInvasion('data/world_map_medium.txt')
    monster.run(10000)
    