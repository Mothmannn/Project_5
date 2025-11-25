#About
This is a submission for the Coding Temple assignment, "Defeat the Evil Wizard".
The program is written in Python.

This is a turn-based battle simulator where the player fights an evil wizard.
There are four classes the player can choose from, each with unique abilities.
Warrior, Mage, Archer, and Paladin. The player can either do a basic attack,
use a special ability, or heal. There is also a "View Stats" function. The game
consistently updates the health and attack of the player, and uses this data dynamically
The goal is to defeat the wizard using these abilities.

##How to Play
The game will start by asking the player which class they'd like to play as. The player
can choose by inputting the number associated with the class. The player will then input
their characters name to add a layer of customization. Now the battle begins.

A menu is displayed with the actions the player can commit: Attack, Special Abilities, Heal
and View Stats. The player can input the number associated with their choice. Attack will cause 
the player to attack the wizard for range of damage. The range possible is different with each class.
Special Abilities will provide the player with two options, and a small description of what the
ability does. The player can then input the number associated with their choice. Heal simply heals
the player by 20HP, and ensures the player isnt healing above their maximum health value. View 
Stats displays the players without consuming a turn.

Once either the player or the wizard health equals 0, the game ends by displaying who won the fight.

