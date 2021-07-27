# Hugo's monster simulations!

Hayden Eastwood - 26/05/2020
----------------------------

Summary description
-------------------
This script takes a text input file of towns and their relative positions to each other. It constructs a map from this and then simualtes a monster invasion whereby monsters traverse the edges until they meet each other and destroy each other and their host town. 

After n movements (default is 10 000), the monsters stop moving. Alternatively, they may destroy each other in entirety, in which case the simulation will also stop.

The layout of the code is as follows:

monsters/
    README.md
    requirements.txt                # requirements for pip installation              
    main.py                         # The executable to run
    monster.py                      # Contains the necessary Python classes 
    test_monster.py                 # Basic tests
    /docs:
        description.text            # This holds a detailed description of the problem
    /data:                          # This contains all the input and output data
        world_map_medium.txt
        world_map_small.txt

Core assumptions of the model
-----------------------------
1. The file input will always be clean and in format of, for example, "town north=town1 west=town2" (ie no attempt has been made to deal with doublespaces or incorrect symbols)
2. Monsters can invade the same town on day0, but discover each other at the end of the day.
3. Monsters *have* to  move - they have no option to remain where they are
4. Towns only become inaccessible after they have been killed by monsters, they do not suffer any less likelihood of being invaded if a monster has already visited.
5. Any number of monsters can find each other in any given town (there is no upper or lower limit on the number that can, by chance, find themselves in the same place).


Installing
--------------------------
1. Install Python 3.9 (Earlier versions down to 3.7 will likely also work fine)
2. Install the package requirements: "pip install -r requirements.txt"

Configuring
--------------------------
1. In main.py you have the option to set:
    number_of_monster_steps -   Steps after which the monsters will stop moving
    monster_town_file -         Input file from which to read the initial towns
    output_file                 The output file name to write to
    monster_numbers             The number of monsters to put on the map

NB: If monster_numbsers is not set or is 0, the screen will prompt you for a number

Running
-------
1. In the root of the directory: 
    $ pytest
    You should see 5 tests pass
2. In the same directory:
    $ Python main.py
    if monster_numbers is set to 0 in main.py, you will be prompted to enter one


Feedback
--------
The end goal of the task itself was not entirely clear to me. Is it to make a highly generalisable set of function features that anyone without programming expertise can leverage to save time? Or is it for expert programmers who might require the ability to do very complex things, and thereby embed Pandas operations (for example) into the configuration file to achieve very specific and complex outcomes?

A bit more context on the use case for the code would help in designing the solution.

