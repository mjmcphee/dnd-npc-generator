#!/usr/bin/env python3
"""
Simple D&D NPC Generator
A basic script to generate random NPCs for D&D campaigns
Built out of frustration with his lack of imagination by Mike McPhee
"""

import random
import argparse  # For command-line arguments
import json      # For saving/loading NPC data
import os        # For file and directory operations
import datetime  # For timestamps

# Data lists for generating NPCs
# Lists in Python are created with square brackets and comma-separated values

FIRST_NAMES = [
    "Aerdrie", "Berris", "Cithreth", "Drannor", "Enna", "Galinndan",
    "Halimath", "Ivellios", "Korfel", "Lamlis", "Mindartis", "Naal",
    "Nutae", "Paelynn", "Peren", "Riardon", "Rolen", "Suhnaal",
    "Thamior", "Theriatis", "Therivan", "Uthemar", "Vanuath", "Varis"
]

LAST_NAMES = [
    "Amakir", "Amosaith", "Caphaxath", "Floshin", "Galanodel", "Holimion",
    "Liadon", "Meliamne", "Nailo", "Siannodel", "Xiloscient", "Alderleaf",
    "Brushgather", "Goodbarrel", "Greenbottle", "High-hill", "Hilltopple",
    "Leagallow", "Tealeaf", "Thorngage", "Tosscobble", "Underbough"
]

SPECIES = [
    "Human", "Elf", "Dwarf", "Halfling", "Dragonborn", "Gnome",
    "Half-Elf", "Half-Orc", "Tiefling", "Aasimar", "Genasi", "Goliath"
]

# Job categories for easier filtering
JOBS = {
    "innkeeper": ["Innkeeper", "Tavern Owner", "Barkeep"],
    "merchant": ["Merchant", "Shopkeeper", "Trader", "Peddler"],
    "guard": ["Guard", "City Watch", "Bouncer", "Sentry"],
    "noble": ["Noble", "Lord/Lady", "Courtier", "Diplomat"],
    "criminal": ["Thief", "Smuggler", "Con Artist", "Fence"],
    "artisan": ["Blacksmith", "Baker", "Tailor", "Carpenter", "Jeweler"],
    "religious": ["Priest", "Acolyte", "Temple Guard", "Oracle"],
    "adventurer": ["Fighter", "Rogue", "Wizard", "Cleric", "Ranger", "Barbarian", "Bard", "Sorcerer", "Warlock", "Paladin", "Monk", "Druid"],
    "sailor": ["Sailor", "Ship Captain", "Navigator", "Quartermaster"],
    "performer": ["Bard", "Dancer", "Actor", "Storyteller"],
    "scholar": ["Scholar", "Librarian", "Scribe", "Teacher"],
    "commoner": ["Farmer", "Laborer", "Servant", "Stable Hand", "Cook"]
}

# All possible classes/jobs in one list for random generation
ALL_CLASSES = []
for job_list in JOBS.values():
    ALL_CLASSES.extend(job_list)

PERSONALITY_TRAITS = [
    "is always optimistic and cheerful",
    "speaks in whispers and seems nervous",
    "has a booming laugh and loves jokes",
    "is extremely curious about everything",
    "always seems to be in a hurry",
    "speaks very slowly and thoughtfully",
    "fidgets constantly with small objects",
    "has an excellent memory for faces and names",
    "is suspicious of strangers",
    "loves to tell long, rambling stories",
    "is incredibly polite and formal",
    "has a habit of humming while working",
    "is perpetually grumpy and complains about everything",
    "gets easily distracted by shiny objects",
    "always tries to one-up everyone's stories",
    "is overly dramatic about minor inconveniences",
    "speaks only in questions, never statements",
    "constantly quotes ancient proverbs (often incorrectly)",
    "has an obsession with cleanliness and organization",
    "is afraid of their own shadow",
    "laughs at inappropriate moments",
    "always speaks in rhymes when excited",
    "has an irrational fear of a common animal",
    "collects useless trinkets compulsively",
    "never remembers anyone's name correctly",
    "always hungry and talks about food",
    "speaks in third person about themselves",
    "has an unusual hobby they won't shut up about"
]

MOTIVATIONS = [
    "seeking revenge against a former partner",
    "trying to find their missing family member",
    "saving money to buy their own shop",
    "secretly in love with someone unattainable",
    "desperately wants to prove their worth",
    "hoping to uncover an ancient mystery",
    "trying to pay off a dangerous debt",
    "dreams of becoming famous or respected",
    "protecting a terrible family secret",
    "searching for a cure to a strange curse",
    "wants to restore their family's honor",
    "planning to retire to a peaceful farm"
]

SECRETS = [
    "is actually nobility in hiding",
    "knows the location of a hidden treasure",
    "is secretly working for a rival organization",
    "has magical abilities they keep hidden",
    "is related to someone important in town",
    "witnessed a crime but is too scared to report it",
    "is deeply in debt to dangerous people",
    "has a criminal past they're trying to escape",
    "is secretly supplying information to enemies",
    "knows a conspiracy is brewing in the government",
    "is the last member of a thought-extinct bloodline",
    "has been having prophetic dreams recently"
]

GENDERS = [
    "Male", "Female", "Non-binary", "Male", "Female"  # Weighted toward Male/Female for more traditional fantasy
]

SPEECH_PATTERNS = [
    "stutters when nervous",
    "speaks with a thick accent from the countryside", 
    "uses big words incorrectly to sound smart",
    "peppers speech with nautical terms",
    "speaks in a sing-song voice",
    "has a lisp and difficulty with 'S' sounds",
    "talks extremely fast, especially when excited",
    "pauses frequently to think of the right word",
    "speaks in a monotone, emotionless voice",
    "whispers secrets even when speaking normally",
    "has a nervous laugh after every sentence",
    "speaks very loudly, as if everyone is deaf",
    "mixes languages and dialects randomly",
    "uses outdated slang from decades ago",
    "speaks in elaborate, flowery metaphors",
    "can't pronounce 'R' sounds properly",
    "constantly clears throat before speaking",
    "speaks in short, clipped sentences",
    "adds 'eh?' or 'ya know?' to everything"
]

MALE_VOICES = [
    "sounds like Morgan Freeman (deep, authoritative)",
    "sounds like Sean Connery (Scottish accent)", 
    "sounds like Christopher Walken (unusual pauses)",
    "sounds like Darth Vader (deep, menacing)",
    "sounds like Arnold Schwarzenegger (Austrian accent)",
    "sounds like a gruff pirate captain",
    "sounds like a posh British aristocrat", 
    "sounds like a nervous accountant",
    "sounds like a wise old wizard",
    "sounds like a used car salesman",
    "sounds like Yoda (backwards sentence structure)",
    "sounds like Bugs Bunny (Brooklyn accent, witty)",
    "sounds like Elmer Fudd (can't pronounce R's)",
    "sounds like Kermit the Frog (high-pitched, enthusiastic)",
    "sounds like Mickey Mouse (high, cheerful)",
    "sounds like a game show host (overly enthusiastic)"
]

FEMALE_VOICES = [
    "sounds like Julia Child (warbling, enthusiastic)",
    "sounds like a gossipy neighbor",
    "sounds like Scarlett Johansson (sultry, smooth)",
    "sounds like Betty White (sweet but sassy)",
    "sounds like a posh British lady",
    "sounds like a Southern belle",
    "sounds like a strict schoolteacher",
    "sounds like a bubbly teenager",
    "sounds like a wise grandmother",
    "sounds like a sultry lounge singer",
    "sounds like Minnie Mouse (high, sweet)",
    "sounds like a pirate wench",
    "sounds like a dramatic Shakespearean actress",
    "sounds like a stern military officer",
    "sounds like a valley girl",
    "sounds like a mysterious fortune teller"
]

NONBINARY_VOICES = [
    "sounds like a mystical forest spirit",
    "sounds like an otherworldly entity",
    "sounds like a shape-shifting trickster",
    "sounds like an ancient being beyond gender",
    "sounds like a magical construct come to life",
    "sounds like wind chimes in human form",
    "sounds like a cosmic entity visiting mortals",
    "sounds like an ageless wanderer",
    "sounds like nature itself speaking",
    "sounds like a being from the fey realm"
]

# D&D 5e 2024 Challenge Rating system
CHALLENGE_RATINGS = [
    "0", "1/8", "1/4", "1/2", "1", "2", "3", "4", "5", 
    "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"
]

# Base stat templates by Challenge Rating (2024 rules)
CR_STAT_TEMPLATES = {
    "0": {"ac": 10, "hp": (1, 6), "prof": 2, "damage": (1, 1), "save_dc": 11, "xp": 0},
    "1/8": {"ac": 11, "hp": (6, 15), "prof": 2, "damage": (2, 3), "save_dc": 11, "xp": 25},
    "1/4": {"ac": 11, "hp": (8, 20), "prof": 2, "damage": (3, 5), "save_dc": 11, "xp": 50},
    "1/2": {"ac": 12, "hp": (16, 30), "prof": 2, "damage": (4, 8), "save_dc": 12, "xp": 100},
    "1": {"ac": 12, "hp": (26, 40), "prof": 2, "damage": (6, 12), "save_dc": 12, "xp": 200},
    "2": {"ac": 13, "hp": (36, 55), "prof": 2, "damage": (7, 17), "save_dc": 13, "xp": 450},
    "3": {"ac": 13, "hp": (50, 75), "prof": 2, "damage": (10, 20), "save_dc": 13, "xp": 700},
    "4": {"ac": 14, "hp": (71, 90), "prof": 2, "damage": (11, 26), "save_dc": 14, "xp": 1100},
    "5": {"ac": 15, "hp": (86, 105), "prof": 3, "damage": (15, 32), "save_dc": 14, "xp": 1800},
    "6": {"ac": 15, "hp": (101, 120), "prof": 3, "damage": (21, 38), "save_dc": 15, "xp": 2300},
    "7": {"ac": 15, "hp": (116, 135), "prof": 3, "damage": (23, 44), "save_dc": 15, "xp": 2900},
    "8": {"ac": 16, "hp": (131, 150), "prof": 3, "damage": (25, 50), "save_dc": 16, "xp": 3900},
    "9": {"ac": 16, "hp": (146, 165), "prof": 4, "damage": (27, 56), "save_dc": 16, "xp": 5000},
    "10": {"ac": 17, "hp": (161, 180), "prof": 4, "damage": (29, 62), "save_dc": 17, "xp": 5900},
    "11": {"ac": 17, "hp": (176, 195), "prof": 4, "damage": (31, 68), "save_dc": 17, "xp": 7200},
    "12": {"ac": 17, "hp": (191, 210), "prof": 4, "damage": (33, 74), "save_dc": 18, "xp": 8400},
    "13": {"ac": 18, "hp": (206, 225), "prof": 5, "damage": (35, 80), "save_dc": 18, "xp": 10000},
    "14": {"ac": 18, "hp": (221, 240), "prof": 5, "damage": (37, 86), "save_dc": 19, "xp": 11500},
    "15": {"ac": 18, "hp": (236, 255), "prof": 5, "damage": (39, 92), "save_dc": 19, "xp": 13000}
}

# Class-specific stat modifiers and abilities
CLASS_MODIFIERS = {
    "innkeeper": {
        "primary_stat": "charisma",
        "ac_bonus": 0,
        "hp_multiplier": 1.0,
        "skills": ["Insight", "Persuasion"],
        "saves": ["wisdom"],
        "abilities": ["Tavern Gossip: Knows local rumors and can gather information easily"]
    },
    "merchant": {
        "primary_stat": "charisma", 
        "ac_bonus": 1,
        "hp_multiplier": 0.9,
        "skills": ["Deception", "Insight", "Persuasion"],
        "saves": ["charisma"],
        "abilities": ["Appraise: Can determine the true value of items", "Silver Tongue: Advantage on Persuasion for commercial deals"]
    },
    "guard": {
        "primary_stat": "strength",
        "ac_bonus": 3,
        "hp_multiplier": 1.3,
        "skills": ["Athletics", "Intimidation", "Perception"],
        "saves": ["strength", "constitution"],
        "abilities": ["Protection: Can impose disadvantage on attacks against nearby allies", "Alert: Advantage on initiative rolls"]
    },
    "noble": {
        "primary_stat": "charisma",
        "ac_bonus": 1,
        "hp_multiplier": 0.8,
        "skills": ["History", "Insight", "Persuasion"],
        "saves": ["charisma"],
        "abilities": ["Position of Privilege: Can secure audiences with nobility", "Inspiring Presence: Allies gain advantage on next attack"]
    },
    "criminal": {
        "primary_stat": "dexterity",
        "ac_bonus": 1,
        "hp_multiplier": 0.9,
        "skills": ["Deception", "Sleight of Hand", "Stealth"],
        "saves": ["dexterity"],
        "abilities": ["Sneak Attack: +1d6 damage when attacking with advantage", "Criminal Contacts: Network of underworld connections"]
    },
    "artisan": {
        "primary_stat": "intelligence",
        "ac_bonus": 1,
        "hp_multiplier": 1.1,
        "skills": ["Investigation", "Sleight of Hand"],
        "saves": ["constitution"],
        "abilities": ["Craft Expertise: Can create masterwork items", "Tool Mastery: Proficient with all artisan's tools"]
    },
    "religious": {
        "primary_stat": "wisdom",
        "ac_bonus": 2,
        "hp_multiplier": 1.0,
        "skills": ["Insight", "Medicine", "Religion"],
        "saves": ["wisdom", "charisma"],
        "abilities": ["Divine Magic: Can cast Cure Wounds and Bless", "Turn Undead: Can frighten undead creatures within 30 feet"]
    },
    "adventurer": {
        "primary_stat": "varies",
        "ac_bonus": 3,
        "hp_multiplier": 1.4,
        "skills": ["Athletics", "Survival"],
        "saves": ["strength", "dexterity"],
        "abilities": ["Action Surge: Can take an additional action once per encounter", "Second Wind: Regain 1d10+level HP once per short rest"]
    },
    "sailor": {
        "primary_stat": "constitution",
        "ac_bonus": 1,
        "hp_multiplier": 1.2,
        "skills": ["Athletics", "Perception"],
        "saves": ["strength", "constitution"],
        "abilities": ["Sea Legs: Advantage on saves against being knocked prone", "Storm Sense: Can predict weather changes"]
    },
    "performer": {
        "primary_stat": "charisma",
        "ac_bonus": 0,
        "hp_multiplier": 0.9,
        "skills": ["Acrobatics", "Performance", "Persuasion"],
        "saves": ["dexterity", "charisma"],
        "abilities": ["Inspiring Performance: Grant allies temporary HP or advantage", "Cutting Words: Can reduce enemy attack rolls with mockery"]
    },
    "scholar": {
        "primary_stat": "intelligence",
        "ac_bonus": 0,
        "hp_multiplier": 0.8,
        "skills": ["Arcana", "History", "Investigation"],
        "saves": ["intelligence", "wisdom"],
        "abilities": ["Lore Master: Extensive knowledge of academic subjects", "Magical Insight: Can identify spells and magical effects"]
    },
    "commoner": {
        "primary_stat": "constitution",
        "ac_bonus": 0,
        "hp_multiplier": 1.0,
        "skills": ["Animal Handling", "Survival"],
        "saves": ["constitution"],
        "abilities": ["Hardy: Advantage on saves against disease and poison"]
    }
}

# Minimal species modifiers (2024 D&D simplified approach)
SPECIES_MODIFIERS = {
    "Human": {"speed": 30, "size": "Medium"},
    "Elf": {"speed": 30, "size": "Medium", "abilities": ["Darkvision 60 ft"]},
    "Dwarf": {"speed": 25, "size": "Medium", "abilities": ["Darkvision 60 ft", "Poison Resistance"]},
    "Halfling": {"speed": 25, "size": "Small", "abilities": ["Lucky: Reroll natural 1s"]},
    "Dragonborn": {"speed": 30, "size": "Medium", "abilities": ["Breath Weapon", "Damage Resistance"]},
    "Gnome": {"speed": 25, "size": "Small", "abilities": ["Darkvision 60 ft"]},
    "Half-Elf": {"speed": 30, "size": "Medium", "abilities": ["Darkvision 60 ft"]},
    "Half-Orc": {"speed": 30, "size": "Medium", "abilities": ["Darkvision 60 ft", "Relentless Endurance"]},
    "Tiefling": {"speed": 30, "size": "Medium", "abilities": ["Darkvision 60 ft", "Fire Resistance"]},
    "Aasimar": {"speed": 30, "size": "Medium", "abilities": ["Darkvision 60 ft", "Healing Touch"]},
    "Genasi": {"speed": 30, "size": "Medium", "abilities": ["Elemental Resistance"]},
    "Goliath": {"speed": 30, "size": "Medium", "abilities": ["Stone's Endurance"]}
}

# Group relationship types
GROUP_TYPES = {
    "family": {
        "name": "Family",
        "relationships": ["Parent", "Sibling", "Child", "Cousin", "Grandparent", "Uncle/Aunt"],
        "shared_traits": ["last_name", "species"]  # What they share
    },
    "crew": {
        "name": "Crew/Gang",
        "relationships": ["Leader", "Lieutenant", "Member", "Lookout", "Muscle", "Specialist"],
        "shared_traits": ["motivation"]  # Similar goals
    },
    "business": {
        "name": "Business Partners",
        "relationships": ["Owner", "Partner", "Employee", "Assistant", "Apprentice"],
        "shared_traits": ["class_category"]  # Similar jobs
    },
    "adventuring": {
        "name": "Adventuring Party",
        "relationships": ["Leader", "Tank", "Healer", "Scout", "Wizard", "Support"],
        "shared_traits": ["motivation"]
    }
}

# Physical appearance lists
HEIGHTS = [
    "unusually short", "short", "below average height", "average height", 
    "above average height", "tall", "very tall", "towering"
]

BUILDS = [
    "skeletal and gaunt", "very thin", "lean and wiry", "slender", 
    "average build", "stocky", "broad-shouldered", "muscular", 
    "heavyset", "rotund", "imposing and powerful"
]

HAIR_COLORS = [
    "jet black", "dark brown", "chestnut brown", "light brown", "dirty blonde", 
    "golden blonde", "platinum blonde", "auburn", "copper red", "fiery red", 
    "silver-gray", "stark white", "salt and pepper"
]

HAIR_STYLES = [
    "closely cropped", "short and neat", "shoulder-length", "long and flowing", 
    "braided", "in elaborate knots", "wild and unkempt", "carefully styled", 
    "partially shaved", "in a topknot", "covered by a hood", "balding", 
    "completely bald", "in ringlets", "straight as a board"
]

EYE_COLORS = [
    "deep brown", "warm brown", "amber", "hazel", "bright green", 
    "forest green", "blue-gray", "sky blue", "deep blue", "violet", 
    "steel gray", "almost black", "mismatched colors"
]

DISTINCTIVE_FEATURES = [
    "has a prominent scar across their cheek",
    "has intricate tattoos covering their arms", 
    "has a missing finger on their left hand",
    "has heterochromia (different colored eyes)",
    "has a distinctive birthmark on their neck",
    "has numerous small scars from old battles",
    "has an elaborate beard braided with beads",
    "has painted nails in bright colors",
    "has a gold tooth that glints when they smile",
    "has calloused hands from years of hard work",
    "has a walking stick they don't seem to need",
    "has jewelry that jingles softly when they move",
    "has a pet that follows them everywhere",
    "has burn scars on their hands",
    "has intricate henna designs on their palms",
    "has a nervous tic (eye twitch, finger tapping, etc.)",
    "has unusually long fingers",
    "has a crooked nose from an old break",
    "has laugh lines around their eyes",
    "has a beauty mark on their face"
]

CLOTHING_STYLES = [
    "wears practical, well-worn work clothes",
    "dresses in fine fabrics with subtle elegance", 
    "favors dark colors and simple cuts",
    "loves bright, eye-catching colors",
    "dresses in layers of mismatched clothing",
    "wears travel-stained but quality gear",
    "prefers loose, comfortable robes",
    "dresses to show off their wealth",
    "wears clothes that have seen better days",
    "favors leather and metal accessories",
    "dresses in the latest fashions",
    "wears traditional clothing from their homeland",
    "prefers functional gear over style", 
    "has an extensive collection of hats",
    "always wears a distinctive cloak or cape",
    "dresses modestly and conservatively",
    "loves ornate jewelry and accessories",
    "wears clothes adapted for their profession"
]

# File management constants
NPC_DATA_DIR = "npc_collection"
NPC_DATA_FILE = os.path.join(NPC_DATA_DIR, "npcs.json")


def calculate_ability_score(cr, primary_stat=None):
    """Calculate ability scores based on CR and primary stat"""
    # Base scores by CR (roughly)
    if cr in ["0", "1/8"]:
        base_score = 10
    elif cr in ["1/4", "1/2", "1"]:
        base_score = 12
    elif cr in ["2", "3", "4"]:
        base_score = 14
    elif cr in ["5", "6", "7", "8"]:
        base_score = 16
    else:  # CR 9+
        base_score = 18
    
    # Primary stat gets a +2 bonus
    primary_bonus = 2 if primary_stat else 0
    return min(20, base_score + primary_bonus)


def generate_stat_block(npc, challenge_rating):
    """Generate D&D 5e stat block for an NPC based on their CR and class"""
    if challenge_rating not in CR_STAT_TEMPLATES:
        return None
    
    cr_data = CR_STAT_TEMPLATES[challenge_rating]
    class_data = CLASS_MODIFIERS.get(npc["class_category"], CLASS_MODIFIERS["commoner"])
    species_data = SPECIES_MODIFIERS.get(npc["species"], SPECIES_MODIFIERS["Human"])
    
    # Calculate ability scores
    primary_stat = class_data["primary_stat"]
    ability_scores = {}
    stats = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
    
    for stat in stats:
        is_primary = (stat == primary_stat or primary_stat == "varies")
        ability_scores[stat] = calculate_ability_score(challenge_rating, is_primary)
    
    # Apply ability modifiers
    def get_modifier(score):
        return (score - 10) // 2
    
    ability_mods = {stat: get_modifier(score) for stat, score in ability_scores.items()}
    
    # Calculate final stats
    base_ac = cr_data["ac"] + class_data["ac_bonus"]
    final_ac = base_ac + ability_mods["dexterity"] if base_ac <= 12 else base_ac
    
    hp_min, hp_max = cr_data["hp"]
    hp_modifier = int((hp_max - hp_min) * class_data["hp_multiplier"])
    final_hp = random.randint(hp_min + hp_modifier, hp_max + hp_modifier)
    
    # Add constitution modifier to HP
    con_bonus = ability_mods["constitution"] * (challenge_rating_to_level(challenge_rating))
    final_hp = max(1, final_hp + con_bonus)
    
    # Calculate attack bonus and damage
    prof_bonus = cr_data["prof"]
    primary_mod = ability_mods.get(primary_stat, 0) if primary_stat != "varies" else max(ability_mods.values())
    attack_bonus = prof_bonus + primary_mod
    
    damage_min, damage_max = cr_data["damage"]
    base_damage = f"{damage_min}-{damage_max}"
    
    # Generate attacks based on class
    attacks = generate_attacks(npc, ability_mods, attack_bonus, challenge_rating)
    
    # Compile stat block
    stat_block = {
        "challenge_rating": challenge_rating,
        "xp_value": cr_data["xp"],
        "armor_class": final_ac,
        "hit_points": final_hp,
        "speed": species_data["speed"],
        "size": species_data["size"],
        "ability_scores": ability_scores,
        "ability_modifiers": ability_mods,
        "proficiency_bonus": prof_bonus,
        "saving_throws": {save: ability_mods[save] + prof_bonus for save in class_data["saves"]},
        "skills": {skill.lower(): ability_mods.get(skill_to_ability(skill), 0) + prof_bonus for skill in class_data["skills"]},
        "special_abilities": class_data["abilities"] + species_data.get("abilities", []),
        "attacks": attacks,
        "spell_save_dc": cr_data["save_dc"]
    }
    
    return stat_block


def challenge_rating_to_level(cr):
    """Convert CR to approximate character level for calculations"""
    cr_to_level = {
        "0": 1, "1/8": 1, "1/4": 1, "1/2": 2, "1": 2, "2": 3, "3": 4, "4": 5,
        "5": 6, "6": 7, "7": 8, "8": 9, "9": 10, "10": 11, "11": 12, "12": 13,
        "13": 14, "14": 15, "15": 16
    }
    return cr_to_level.get(cr, 1)


def skill_to_ability(skill):
    """Map skill names to their governing abilities"""
    skill_map = {
        "Athletics": "strength",
        "Acrobatics": "dexterity", "Sleight of Hand": "dexterity", "Stealth": "dexterity",
        "Arcana": "intelligence", "History": "intelligence", "Investigation": "intelligence",
        "Animal Handling": "wisdom", "Insight": "wisdom", "Medicine": "wisdom", "Perception": "wisdom", "Religion": "wisdom", "Survival": "wisdom",
        "Deception": "charisma", "Intimidation": "charisma", "Performance": "charisma", "Persuasion": "charisma"
    }
    return skill_map.get(skill, "wisdom")


def generate_attacks(npc, ability_mods, attack_bonus, cr):
    """Generate appropriate attacks for the NPC based on their class"""
    attacks = []
    class_category = npc["class_category"]
    
    # Determine attack type based on class
    if class_category in ["guard", "adventurer", "noble"]:
        # Melee weapon attack
        damage_dice = "1d8" if cr in ["0", "1/8", "1/4"] else "2d6" if cr in ["1/2", "1", "2"] else "2d8"
        damage_mod = ability_mods["strength"]
        attacks.append({
            "name": "Longsword",
            "type": "Melee Weapon Attack",
            "attack_bonus": f"+{attack_bonus}",
            "reach": "5 ft.",
            "target": "one target",
            "damage": f"{damage_dice} + {damage_mod} slashing damage"
        })
    
    elif class_category in ["criminal", "performer"]:
        # Ranged or finesse weapon
        damage_dice = "1d6" if cr in ["0", "1/8", "1/4"] else "2d4" if cr in ["1/2", "1", "2"] else "2d6"
        damage_mod = ability_mods["dexterity"]
        attacks.append({
            "name": "Shortbow",
            "type": "Ranged Weapon Attack",
            "attack_bonus": f"+{attack_bonus}",
            "range": "150/600 ft.",
            "target": "one target",
            "damage": f"{damage_dice} + {damage_mod} piercing damage"
        })
    
    elif class_category == "religious":
        # Spell attack
        damage_dice = "1d8" if cr in ["0", "1/8", "1/4"] else "2d6" if cr in ["1/2", "1", "2"] else "3d6"
        attacks.append({
            "name": "Sacred Flame",
            "type": "Spell Attack",
            "attack_bonus": f"DC {12 + ability_mods['wisdom']}",
            "range": "60 ft.",
            "target": "one creature",
            "damage": f"{damage_dice} radiant damage (Dex save for no damage)"
        })
    
    else:
        # Basic unarmed or improvised attack
        damage_dice = "1d4"
        damage_mod = ability_mods["strength"]
        attacks.append({
            "name": "Improvised Weapon",
            "type": "Melee Weapon Attack",
            "attack_bonus": f"+{attack_bonus}",
            "reach": "5 ft.",
            "target": "one target",
            "damage": f"{damage_dice} + {damage_mod} bludgeoning damage"
        })
    
    return attacks


def ensure_data_directory():
    """Create the NPC data directory if it doesn't exist"""
    if not os.path.exists(NPC_DATA_DIR):
        os.makedirs(NPC_DATA_DIR)


def load_npc_collection():
    """Load existing NPC collection from file"""
    ensure_data_directory()
    if os.path.exists(NPC_DATA_FILE):
        try:
            with open(NPC_DATA_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {"npcs": [], "next_id": 1}
    return {"npcs": [], "next_id": 1}


def save_npc_collection(collection):
    """Save NPC collection to file"""
    ensure_data_directory()
    with open(NPC_DATA_FILE, 'w') as f:
        json.dump(collection, f, indent=2)


def add_npc_to_collection(npc, group_info=None):
    """Add an NPC (or group) to the persistent collection"""
    collection = load_npc_collection()
    
    timestamp = datetime.datetime.now().isoformat()
    
    if group_info:
        # This is a group of NPCs
        group_entry = {
            "id": collection["next_id"],
            "type": "group",
            "group_type": group_info["type"],
            "timestamp": timestamp,
            "members": []
        }
        
        for member in group_info["members"]:
            member_data = member.copy()
            member_data["timestamp"] = timestamp
            group_entry["members"].append(member_data)
        
        collection["npcs"].append(group_entry)
    else:
        # Single NPC
        npc_data = npc.copy()
        npc_data["id"] = collection["next_id"]
        npc_data["type"] = "individual"
        npc_data["timestamp"] = timestamp
        collection["npcs"].append(npc_data)
    
    collection["next_id"] += 1
    save_npc_collection(collection)
    return collection["next_id"] - 1


def generate_npc(job_filter=None, gender_filter=None, shared_traits=None, challenge_rating=None):
    """
    Function to generate a random NPC with optional filters
    job_filter: specific job category like 'innkeeper' 
    gender_filter: 'Male', 'Female', or 'Non-binary'
    shared_traits: dict of traits to share with group members
    challenge_rating: CR string like '1/4' or '5' to generate stat block
    """
    # Apply filters or use defaults
    if job_filter and job_filter in JOBS:
        character_class = random.choice(JOBS[job_filter])
        class_category = job_filter
    else:
        character_class = random.choice(ALL_CLASSES)
        # Figure out what category this class belongs to
        class_category = "unknown"
        for category, classes in JOBS.items():
            if character_class in classes:
                class_category = category
                break
    
    if gender_filter:
        gender = gender_filter
    else:
        gender = random.choice(GENDERS)
    
    # Generate other traits
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    species = random.choice(SPECIES)
    personality = random.choice(PERSONALITY_TRAITS)
    motivation = random.choice(MOTIVATIONS)
    secret = random.choice(SECRETS)
    speech_pattern = random.choice(SPEECH_PATTERNS)
    
    # Generate physical appearance
    height = random.choice(HEIGHTS)
    build = random.choice(BUILDS)
    hair_color = random.choice(HAIR_COLORS)
    hair_style = random.choice(HAIR_STYLES)
    eye_color = random.choice(EYE_COLORS)
    distinctive_feature = random.choice(DISTINCTIVE_FEATURES)
    clothing_style = random.choice(CLOTHING_STYLES)
    
    # Apply shared traits if provided (for group generation)
    if shared_traits:
        if "last_name" in shared_traits:
            last_name = shared_traits["last_name"]
        if "species" in shared_traits:
            species = shared_traits["species"]
        if "motivation" in shared_traits:
            motivation = shared_traits["motivation"]
        if "class_category" in shared_traits and not job_filter:
            # Pick a job from the same category
            if shared_traits["class_category"] in JOBS:
                character_class = random.choice(JOBS[shared_traits["class_category"]])
                class_category = shared_traits["class_category"]
    
    # Choose voice based on gender
    if gender == "Male":
        voice = random.choice(MALE_VOICES)
    elif gender == "Female":
        voice = random.choice(FEMALE_VOICES)
    else:  # Non-binary
        voice = random.choice(NONBINARY_VOICES)
    
    # Create a dictionary to store all the NPC information
    npc = {
        "name": f"{first_name} {last_name}",
        "species": species,
        "class": character_class,
        "class_category": class_category,
        "gender": gender,
        "personality": personality,
        "speech_pattern": speech_pattern,
        "voice": voice,
        "motivation": motivation,
        "secret": secret,
        # Physical appearance
        "height": height,
        "build": build,
        "hair_color": hair_color,
        "hair_style": hair_style,
        "eye_color": eye_color,
        "distinctive_feature": distinctive_feature,
        "clothing_style": clothing_style
    }
    
    # Generate stat block if challenge rating is provided
    if challenge_rating:
        stat_block = generate_stat_block(npc, challenge_rating)
        if stat_block:
            npc["stat_block"] = stat_block
    
    return npc


def generate_group(group_type, count, job_filter=None, challenge_rating=None):
    """
    Generate a related group of NPCs
    group_type: 'family', 'crew', 'business', or 'adventuring'
    count: number of NPCs to generate
    job_filter: optional job category
    challenge_rating: CR string like '1/4' or '5' to generate stat blocks
    """
    if group_type not in GROUP_TYPES:
        raise ValueError(f"Unknown group type: {group_type}")
    
    group_info = GROUP_TYPES[group_type]
    npcs = []
    
    # Generate the first NPC to establish shared traits
    first_npc = generate_npc(job_filter=job_filter, challenge_rating=challenge_rating)
    
    # Determine what traits this group will share
    shared_traits = {}
    for trait in group_info["shared_traits"]:
        if trait == "last_name":
            shared_traits["last_name"] = first_npc["name"].split()[-1]
        elif trait == "species":
            shared_traits["species"] = first_npc["species"]
        elif trait == "motivation":
            shared_traits["motivation"] = first_npc["motivation"]
        elif trait == "class_category":
            shared_traits["class_category"] = first_npc["class_category"]
    
    # Add relationship to first NPC
    first_npc["relationship"] = random.choice(group_info["relationships"])
    npcs.append(first_npc)
    
    # Generate remaining NPCs with shared traits
    used_relationships = [first_npc["relationship"]]
    for i in range(count - 1):
        # Pick a unique relationship if possible
        available_relationships = [r for r in group_info["relationships"] if r not in used_relationships]
        if not available_relationships:
            available_relationships = group_info["relationships"]  # Allow repeats if we run out
        
        relationship = random.choice(available_relationships)
        used_relationships.append(relationship)
        
        npc = generate_npc(job_filter=job_filter, shared_traits=shared_traits, challenge_rating=challenge_rating)
        npc["relationship"] = relationship
        npcs.append(npc)
    
    return {
        "type": group_info["name"],
        "members": npcs
    }


def display_npc(npc):
    """
    Function to display an NPC in a nice format
    Takes an NPC dictionary as input
    """
    title = f"📜 {npc['name']} ({npc['gender']})"
    if "relationship" in npc:
        title += f" - {npc['relationship']}"
    print(title)
    print(f"Species: {npc['species']}")
    print(f"Class: {npc['class']}")
    
    print(f"\n👤 PHYSICAL APPEARANCE:")
    print(f"Height & Build: {npc['height']}, {npc['build']}")
    print(f"Hair: {npc['hair_color']} hair, {npc['hair_style']}")
    print(f"Eyes: {npc['eye_color']}")
    print(f"Notable: {npc['distinctive_feature']}")
    print(f"Style: {npc['clothing_style']}")
    
    print(f"\n🎭 ROLEPLAY NOTES:")
    print(f"Personality: {npc['personality']}")
    print(f"Speech pattern: {npc['speech_pattern']}")
    print(f"Voice inspiration: {npc['voice']}")
    
    print(f"\n📖 STORY HOOKS:")
    print(f"Motivation: {npc['motivation']}")
    print(f"Secret: {npc['secret']}")
    
    # Display stat block if present
    if "stat_block" in npc:
        display_stat_block(npc["stat_block"])


def display_stat_block(stat_block):
    """Display a formatted D&D 5e stat block"""
    print(f"\n⚔️  COMBAT STATISTICS (CR {stat_block['challenge_rating']}) - {stat_block['xp_value']} XP")
    print("=" * 50)
    
    # Basic stats
    print(f"Size: {stat_block['size']}")
    print(f"Armor Class: {stat_block['armor_class']}")
    print(f"Hit Points: {stat_block['hit_points']}")
    print(f"Speed: {stat_block['speed']} ft.")
    
    # Ability scores
    print(f"\n📊 ABILITY SCORES:")
    abilities = stat_block['ability_scores']
    mods = stat_block['ability_modifiers']
    print(f"STR: {abilities['strength']} ({mods['strength']:+}) | DEX: {abilities['dexterity']} ({mods['dexterity']:+}) | CON: {abilities['constitution']} ({mods['constitution']:+})")
    print(f"INT: {abilities['intelligence']} ({mods['intelligence']:+}) | WIS: {abilities['wisdom']} ({mods['wisdom']:+}) | CHA: {abilities['charisma']} ({mods['charisma']:+})")
    
    # Proficiencies
    print(f"\n🎯 PROFICIENCIES:")
    print(f"Proficiency Bonus: +{stat_block['proficiency_bonus']}")
    
    if stat_block['saving_throws']:
        saves = [f"{save.title()} {bonus:+}" for save, bonus in stat_block['saving_throws'].items()]
        print(f"Saving Throws: {', '.join(saves)}")
    
    if stat_block['skills']:
        skills = [f"{skill.title()} {bonus:+}" for skill, bonus in stat_block['skills'].items()]
        print(f"Skills: {', '.join(skills)}")
    
    # Special abilities
    if stat_block['special_abilities']:
        print(f"\n✨ SPECIAL ABILITIES:")
        for ability in stat_block['special_abilities']:
            print(f"• {ability}")
    
    # Actions/Attacks
    if stat_block['attacks']:
        print(f"\n⚔️  ACTIONS:")
        for attack in stat_block['attacks']:
            print(f"• {attack['name']}: {attack['type']}, {attack['attack_bonus']} to hit")
            if 'reach' in attack:
                print(f"  Reach {attack['reach']}, {attack['target']}. Hit: {attack['damage']}")
            elif 'range' in attack:
                print(f"  Range {attack['range']}, {attack['target']}. Hit: {attack['damage']}")


def display_group(group):
    """
    Display a group of related NPCs
    """
    print(f"\n🏛️  {group['type'].upper()}")
    print("=" * 50)
    
    for i, npc in enumerate(group['members']):
        if i > 0:
            print("\n" + "-" * 30)
        display_npc(npc)


def view_npc_collection(filter_job=None, filter_gender=None, filter_species=None):
    """View all saved NPCs with optional filtering"""
    collection = load_npc_collection()
    
    if not collection["npcs"]:
        print("No NPCs in collection yet. Generate some NPCs first!")
        return
    
    print(f"\n📚 NPC COLLECTION ({len(collection['npcs'])} entries)")
    print("=" * 60)
    
    for entry in collection["npcs"]:
        # Parse the timestamp for display
        timestamp = datetime.datetime.fromisoformat(entry["timestamp"])
        date_str = timestamp.strftime("%Y-%m-%d %H:%M")
        
        if entry["type"] == "group":
            print(f"\n#{entry['id']} - {entry['group_type']} ({len(entry['members'])} members) - {date_str}")
            print("-" * 40)
            
            for member in entry["members"]:
                if matches_filters(member, filter_job, filter_gender, filter_species):
                    print(f"  • {member['name']} ({member['gender']}) - {member['species']} {member['class']}")
                    if "relationship" in member:
                        print(f"    Role: {member['relationship']}")
        else:
            # Individual NPC
            if matches_filters(entry, filter_job, filter_gender, filter_species):
                print(f"\n#{entry['id']} - {entry['name']} ({entry['gender']}) - {date_str}")
                print(f"  {entry['species']} {entry['class']}")
                print(f"  {entry['height']}, {entry['build']}")
                print(f"  {entry['distinctive_feature']}")


def matches_filters(npc, filter_job, filter_gender, filter_species):
    """Check if an NPC matches the given filters"""
    if filter_job and npc.get("class_category") != filter_job:
        return False
    if filter_gender and npc.get("gender") != filter_gender:
        return False
    if filter_species and npc.get("species") != filter_species:
        return False
    return True


def view_npc_details(npc_id):
    """View detailed information about a specific NPC"""
    collection = load_npc_collection()
    
    for entry in collection["npcs"]:
        if entry["id"] == npc_id:
            timestamp = datetime.datetime.fromisoformat(entry["timestamp"])
            date_str = timestamp.strftime("%Y-%m-%d %H:%M")
            
            print(f"\n📜 NPC #{npc_id} (Created: {date_str})")
            print("=" * 50)
            
            if entry["type"] == "group":
                print(f"🏛️  {entry['group_type'].upper()}")
                print("=" * 50)
                
                for i, member in enumerate(entry["members"]):
                    if i > 0:
                        print("\n" + "-" * 30)
                    display_npc(member)
            else:
                display_npc(entry)
            return
    
    print(f"NPC #{npc_id} not found in collection.")


def main():
    parser = argparse.ArgumentParser(description='Generate D&D NPCs with specific traits')
    
    # Single NPC options
    parser.add_argument('--job', '-j', choices=list(JOBS.keys()), 
                       help='Specify job category (e.g., innkeeper, merchant, guard)')
    parser.add_argument('--gender', '-g', choices=['Male', 'Female', 'Non-binary'],
                       help='Specify gender')
    parser.add_argument('--cr', choices=CHALLENGE_RATINGS,
                       help='Challenge Rating for stat block generation (e.g. 1/4, 2, 5)')
    parser.add_argument('--ai', action='store_true',
                       help='Use AI (Ollama) to generate creative, unique NPCs')
    
    # Group options
    parser.add_argument('--group', '-gr', choices=list(GROUP_TYPES.keys()),
                       help='Generate a group (family, crew, business, adventuring)')
    parser.add_argument('--count', '-c', type=int, default=3, 
                       help='Number of NPCs in group (default: 3)')
    
    # Collection management options
    parser.add_argument('--view', '-v', action='store_true',
                       help='View all NPCs in your collection')
    parser.add_argument('--view-id', type=int, metavar='ID',
                       help='View detailed info for a specific NPC by ID')
    parser.add_argument('--no-save', action='store_true',
                       help='Generate NPC without saving to collection')
    
    # Filter options for viewing
    parser.add_argument('--filter-job', choices=list(JOBS.keys()),
                       help='Filter collection by job category')
    parser.add_argument('--filter-gender', choices=['Male', 'Female', 'Non-binary'],
                       help='Filter collection by gender')
    parser.add_argument('--filter-species', choices=SPECIES,
                       help='Filter collection by species')
    
    # Help options
    parser.add_argument('--list-jobs', action='store_true',
                       help='List all available job categories')
    
    args = parser.parse_args()
    
    # Handle collection viewing
    if args.view:
        view_npc_collection(args.filter_job, args.filter_gender, args.filter_species)
        return
    
    if args.view_id:
        view_npc_details(args.view_id)
        return
    
    # Handle help options
    if args.list_jobs:
        print("📋 Available Job Categories:")
        for category, jobs in JOBS.items():
            print(f"  {category}: {', '.join(jobs)}")
        return
    
    # Handle AI import if needed
    if args.ai:
        try:
            from ai_npc_generator import generate_ai_npc, generate_ai_group, test_ollama_connection
            
            # Test Ollama connection
            if not test_ollama_connection():
                print("❌ Cannot connect to Ollama. Please ensure:")
                print("  1. Ollama is installed and running")
                print("  2. Your .env file is configured correctly")
                print("  3. The specified model is available")
                print("\nFalling back to regular generation...")
                args.ai = False
            else:
                print("✅ Connected to Ollama successfully!")
                
        except ImportError as e:
            print(f"❌ AI dependencies not available: {e}")
            print("Install required packages:")
            print("  pip install python-dotenv requests")
            print("\nFalling back to regular generation...")
            args.ai = False
    
    print("Welcome to Mike's D&D NPC Generator!")
    if args.ai:
        print("🤖 AI-Powered Mode Enabled!")
    print("=" * 40)
    
    # Generate based on arguments
    if args.group:
        # Generate a group
        if args.ai:
            group = generate_ai_group(args.group, args.count, args.job, args.cr)
        else:
            group = generate_group(args.group, args.count, args.job, args.cr)
            
        if group:
            display_group(group)
            
            if not args.no_save:
                npc_id = add_npc_to_collection(None, group)
                print(f"\n💾 Saved as NPC #{npc_id}")
                print(f"Use '--view-id {npc_id}' to view again later")
        else:
            print("Failed to generate group. Try again or use regular generation.")
    else:
        # Generate a single NPC
        if args.ai:
            npc = generate_ai_npc(job_filter=args.job, gender_filter=args.gender, challenge_rating=args.cr)
        else:
            npc = generate_npc(job_filter=args.job, gender_filter=args.gender, challenge_rating=args.cr)
            
        if npc:
            display_npc(npc)
            
            if not args.no_save:
                npc_id = add_npc_to_collection(npc)
                print(f"\n💾 Saved as NPC #{npc_id}")
                print(f"Use '--view-id {npc_id}' to view again later")
        else:
            print("Failed to generate NPC. Try again or use regular generation.")
    
    print("\n" + "=" * 40)
    print("Happy DMing! 🎲")
    print("Use '--view' to see your full NPC collection")


if __name__ == "__main__":
    main()
