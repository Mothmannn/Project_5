import random

# Base Character class
class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.max_health = health
        self.sword_shield_next = False  # block incoming damage
        self.reflect_damage_next = False  # reflects damage back to wizard
        self.absorb_damage_next = False  # absorbs damage and heals for that amount
        self.evade_next = False  # evade the attack
        self.divine_shield_next = False  # blocks the attack
        self.divine_weakening_next = False  # take extra damage from using Divine Shield
        self.holy_barrage_active = False  # Holy Barrage damage on next attack
        self.temp_attack_bonus = 0
        self.temp_attack_penalty = 0
        self.attack_min = attack_power
        self.attack_max = attack_power
        
        

    def attack(self, opponent):
        bonus = getattr(self, 'temp_attack_bonus', 0)
        penalty = getattr(self, 'temp_attack_penalty', 0)
        # compute damage dynamically from a random range (include any temp bonus)
        base = random.randint(getattr(self, 'attack_min', self.attack_power),
                              getattr(self, 'attack_max', self.attack_power))
        damage = int(max(0, base + bonus - penalty))
        print(f"{self.name} attacks {opponent.name} for {damage} damage!")
        opponent.receive_attack(damage, attacker=self)
        # reset one-use modifiers after applying
        if bonus:
            self.temp_attack_bonus = 0
        if penalty:
            self.temp_attack_penalty = 0

        if opponent.health <= 0:
            print(f"{opponent.name} has been defeated!")
        

    def receive_attack(self, damage, attacker=None):
        # Clamp damage to prevent negative values
        damage = max(0, int(damage))
        
        if getattr(self, 'sword_shield_next', False):
            print(f"{self.name} raises their sword, ready to defend!")
            self.sword_shield_next = False
            return
        if getattr(self, 'reflect_damage_next', False) and attacker is not None:
            damage = int(damage)
            # split damage so defender and attacker each take half
            half = damage // 2
            other = damage - half 

            # defender (self) takes half
            self.health -= half
            print(f"{self.name}'s Magic Mirror splits the attack:")
            print(f"  {self.name} takes {half} damage (HP now {max(0, self.health)})")

            # attacker takes the other half
            attacker.health -= other
            print(f"  {attacker.name} takes {other} reflected damage.")
            self.reflect_damage_next = False

            if attacker.health <= 0:
                print(f"{attacker.name} has been defeated!")
            if self.health <= 0:
                print(f"{self.name} has been defeated!")

            return
        if getattr(self, 'absorb_damage_next', False):
            heal_amount = round(damage * .75)
            self.health = min(self.max_health, self.health + heal_amount)
            print(f"{self.name} absorbed the blast and healed {heal_amount} HP!")
            print(f"Current Health: {self.health}/{self.max_health}")
            self.temp_attack_penalty = int(self.attack_power // 2)
            print(f"{self.name}'s ATK is reduced by {self.temp_attack_penalty} for one turn.")
            self.absorb_damage_next = False
            return
        if getattr(self, 'evade_next', False):
            print(f"{self.name} evaded the attack!")
            self.evade_next = False
            return
        if getattr(self, 'divine_shield_next', False):
            print(f"{self.name} blocked the attack with their divine shield!")
            self.divine_shield_next = False
            return
        if getattr(self, 'holy_barrage_active', False):
            # Apply weakening damage bonus to barrage if active
            barrage_self_damage = 30
            barrage_attacker_damage = 60
            if getattr(self, 'divine_weakening_next', False):
                barrage_self_damage += 20
                print(f"The Holy Barrage hits harder due to the Paladin's exhaustion!")
                self.divine_weakening_next = False
            self.health -= barrage_self_damage
            attacker.health -= barrage_attacker_damage
            print(f"A Holy Barrage rains down on the battlefield!")
            print(f"  {self.name} takes {barrage_self_damage} damage (HP now {max(0, self.health)})")
            print(f"  {attacker.name} takes {barrage_attacker_damage} damage (HP now {max(0, attacker.health)})")
            self.holy_barrage_active = False
            return
        if getattr(self, 'divine_weakening_next', False):
            damage += 20
            print(f"The attack hits harder due to the Paladin's exhaustion!")
            self.divine_weakening_next = False
        
        # default damage receiver
        self.health -= damage
        self.health = max(0, self.health)  # Prevent negative health
        print(f"{self.name} takes {damage} damage (HP now {self.health}/{self.max_health}).")

    
    def display_stats(self):
        print(f"{self.name}'s Stats - Health: {self.health}/{self.max_health}, Attack Power: {self.attack_power}")
        if self.temp_attack_penalty > 0:
            print(f"  Attack penalty: {self.temp_attack_penalty}")
        if self.temp_attack_bonus > 0:
            print(f"  Attack bonus: {self.temp_attack_bonus}")
    
    def heal(self, amount=20):
        old_health = self.health
        self.health = min(self.max_health, self.health + amount)
        healed = self.health - old_health
        print(f"{self.name} heals for {healed} HP (HP now {self.health}/{self.max_health}).")
        
# Warrior class (inherits from Character)
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=140, attack_power=25)
        #small variability around base attack
        self.attack_min = 20
        self.attack_max = 30

    def sword_shield(self):
        self.sword_shield_next = True
        print(f"{self.name} blocks the attack with their Greatsword!")


    def rage(self):
        self.temp_attack_bonus = 20
        self.health -= 15  # Costs health to use
        self.health = max(0, self.health)  # Prevent negative
        print(f"{self.name} enters a rage: next attack +20 damage, but loses 15 HP!")
        print(f"Current Health: {self.health}/{self.max_health}")

# Mage class (inherits from Character)
class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=35)
        # Mage has higher variance
        self.attack_min = 30
        self.attack_max = 40

    def reflect_damage(self, opponent):
        self.reflect_damage_next = True
        self.health = max(0, self.health)  # Prevent negative
        print(f"{self.name} uses Magic Mirror!")

    def absorb_damage(self):
        # Check if attack penalty is active (from previous absorb use)
        if self.temp_attack_penalty > 0:
            print(f"{self.name} is still recovering from the last absorption! Must attack first to clear the penalty.")
            return False
        self.absorb_damage_next = True
        print(f"{self.name} uses Absorb!")
        return True

# Create Archer class
class Archer(Character):
    def __init__(self, name):
        super().__init__(name, health=125, attack_power=30)
        # Archer has moderate variance
        self.attack_min = 25
        self.attack_max = 35

    def double_shot(self, opponent):
        # 25% chance to miss entirely
        if random.random() < 0.40:
            print(f"{self.name} fires a Double Shot — but both arrows miss!")
            return
        bonus = getattr(self, 'temp_attack_bonus', 0)
        penalty = getattr(self, 'temp_attack_penalty', 0)
        base = max(0, self.attack_power + bonus - penalty)
        damage = int(0.75 * (2 * base))
        print(f"{self.name} fires a Double Shot at {opponent.name} for {damage} damage!")
        opponent.receive_attack(damage, attacker=self)
        # Consume one-use modifiers
        if bonus:
            self.temp_attack_bonus = 0
        if penalty:
            self.temp_attack_penalty = 0

    def evade(self):
        self.evade_next = True
        print(f"{self.name} swiftly evades the Dark Wizard's attack!")
        

# Create Paladin class
class Paladin(Character):
    def __init__(self, name):
        super().__init__(name, health=180, attack_power=20)
        # Paladin is more consistent
        self.attack_min = 18
        self.attack_max = 22

    def divine_shield(self):
        self.divine_shield_next = True
        print(f"{self.name} summons a divine shield!")
        # 40% chance to exhaust and take extra damage next turn
        if random.random() < 0.40:
            print(f"{self.name} used too much energy! They will take 20 extra damage on the next hit!")
            self.divine_weakening_next = True

    def holy_barrage_cast(self):
        self.holy_barrage_active = True
        print(f"{self.name} prepares a Holy Barrage!")
        
        

# EvilWizard class (inherits from Character)
class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=15)
        # Enemy has a small random range
        self.attack_min = 12
        self.attack_max = 18

    def regenerate(self):
        self.health += 5
        print(f"{self.name} regenerates 5 health! Current health: {self.health}")
        
def create_character():
    print("Choose your character class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Archer") 
    print("4. Paladin")  

    class_choice = input("Enter the number of your class choice: ")
    name = input("Enter your character's name: ")

    if class_choice == '1':
        return Warrior(name)
    elif class_choice == '2':
        return Mage(name)
    elif class_choice == '3':
        return  Archer(name)# Implement Archer class
    elif class_choice == '4':
        return Paladin(name) # Implement Paladin class
    else:
        print("Invalid choice. Defaulting to Warrior.")
        return Warrior(name)

def battle(player, wizard):
    while wizard.health > 0 and player.health > 0:
        print("\n--- Your Turn ---")
        print("1. Attack")
        print("2. Use Special Ability")
        print("3. Heal")
        print("4. View Stats")

        choice = input("Choose an action: ")

        if choice == '1':
            player.attack(wizard)
        elif choice == '2':
            if isinstance(player, Warrior):
                print("Choose an ability:")
                print("1) Sword Shield - Block incoming damage with your sword")
                print("2) Rage - Let your warrior rage consume you (+15DMG, -15HP)")
                abil = input("Enter ability number: ").strip()
                if abil == '1':
                    player.sword_shield() # method should set sword_shield_next to True
                elif abil == '2':
                    player.rage() # method should set rage = True and take health immediately
                else:
                    print("Invalid selection, turn wasted.")

            if isinstance(player, Mage):
                print("Choose an ability:")
                print("1) Magic Mirror: Player takes half the damage of the attack, and the attacker takes the other half")
                print("2) Energy Absorb: Player heals instead of taking damage. Player ATK is lowered for one turn.")
                abil = input("Enter ability number: ").strip()
                if abil == '1':
                    player.reflect_damage(wizard)
                elif abil == '2':
                    if not player.absorb_damage():
                        # If absorb_damage returns False, the turn wasn't used
                        continue
                else:
                    print("Invaild selection, turn wasted.")

            if isinstance(player, Archer):
                print("Choose an ability:")
                print("1) Double Shot: Player fires two blazing arrows, but there's a chance of missing the attack.")
                print("2) Evade: Evade the attack!")
                abil = input("Enter ability number: ").strip()
                if abil == '1':
                    player.double_shot(wizard)
                elif abil == '2':
                    player.evade()
                else:
                    print("Invaild selection, turn wasted.")

            if isinstance(player, Paladin):
                print("Choose an ability:")
                print("1) Divine Shield: Summon a holy shield to block the next attack. Chance to receive extra damage next time player is attacked.")
                print("2) Holy Barrage: Fire of justice rains down from above (60DMG), but player gets caught in the barrage (30DMG). Can only be used once.")
                abil = input("Enter ability number: ").strip()
                if abil == '1':
                    player.divine_shield()
                elif abil == '2':
                    player.holy_barrage_cast()
                else:
                    print("Invaild selection, turn wasted.")

        elif choice == '3':
            player.heal()
        elif choice == '4':
            player.display_stats()
        else:
            print("Invalid choice. Try again.")

        if wizard.health > 0:
            wizard.regenerate()
            wizard.attack(player)

        if player.health <= 0:
            print(f"{player.name} has been defeated!")
            break

    if wizard.health <= 0:
        print(f"The wizard {wizard.name} has been defeated by {player.name}!")

def main():
    player = create_character()
    wizard = EvilWizard("The Dark Wizard")
    battle(player, wizard)

if __name__ == "__main__":
    main()
