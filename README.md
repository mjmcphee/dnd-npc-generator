# D&D NPC Generator with Stat Blocks

A comprehensive D&D 5e (2024) NPC generator that creates rich, detailed characters with optional combat statistics. Perfect for Dungeon Masters who need quick, immersive NPCs for their campaigns.

## Features

### 🎭 **Rich Character Generation**
- **Detailed Personalities**: Unique traits, speech patterns, and voice inspirations
- **Physical Descriptions**: Height, build, hair, eyes, distinctive features, and clothing
- **Story Hooks**: Motivations and secrets to drive plot development
- **Species & Classes**: 12 species and 12+ class categories with job specializations

### ⚔️ **D&D 5e 2024 Combat Statistics**
- **Challenge Rating Support**: CR 0 to CR 15 stat blocks
- **Class-Specific Abilities**: Guards get armor and weapons, criminals get stealth, clerics get spells
- **Proper Scaling**: HP, AC, attack bonuses, and damage scale with CR
- **Complete Stat Blocks**: Ability scores, saves, skills, special abilities, and attacks

### 👥 **Group Generation**
- **Related Groups**: Generate families, crews, business partners, or adventuring parties
- **Shared Traits**: Groups share last names, species, motivations, or professions
- **Relationship Roles**: Each member has a specific role (Leader, Lieutenant, etc.)

### 💾 **Persistent Collection**
- **Save NPCs**: Automatically saves generated characters with timestamps
- **View Collection**: Browse all saved NPCs with filtering options
- **Detailed Lookup**: View complete NPC details by ID number

## Installation

### Prerequisites
- Python 3.6 or higher
- No additional dependencies required!

### Setup
1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/dnd-npc-generator.git
cd dnd-npc-generator
```

2. Make the script executable (optional):
```bash
chmod +x npc_generator.py
```

## Usage

### Basic Generation
```bash
# Generate a random NPC
python3 npc_generator.py

# Generate an innkeeper
python3 npc_generator.py --job innkeeper

# Generate a female guard
python3 npc_generator.py --job guard --gender Female

# Generate a NPC with AI (Ollama)
cp .env.example .env
# Edit .env with your environment variables and a model that you have on your Ollama server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python npc_generator.py --ai --job innkeeper --gender Female
```

### Combat-Ready NPCs
```bash
# Generate a CR 2 guard with combat stats
python3 npc_generator.py --job guard --cr 2

# Create a CR 1/4 merchant
python3 npc_generator.py --job merchant --cr 1/4

# High-level CR 5 adventurer
python3 npc_generator.py --job adventurer --cr 5
```

### Group Generation
```bash
# Generate a family of 4 NPCs
python3 npc_generator.py --group family --count 4

# Create a criminal crew with combat stats
python3 npc_generator.py --group crew --job criminal --cr 1/2 --count 3

# Business partners (merchants)
python3 npc_generator.py --group business --job merchant --count 2
```

### Collection Management
```bash
# View all saved NPCs
python3 npc_generator.py --view

# View specific NPC by ID
python3 npc_generator.py --view-id 5

# Filter by job category
python3 npc_generator.py --view --filter-job guard

# Generate without saving
python3 npc_generator.py --no-save
```

## Command Reference

### Core Options
- `--job`, `-j`: Job category (innkeeper, merchant, guard, noble, criminal, artisan, religious, adventurer, sailor, performer, scholar, commoner)
- `--gender`, `-g`: Gender (Male, Female, Non-binary)
- `--cr`: Challenge Rating for stat blocks (0, 1/8, 1/4, 1/2, 1-15)

### Group Options
- `--group`, `-gr`: Group type (family, crew, business, adventuring)
- `--count`, `-c`: Number of NPCs in group (default: 3)

### Collection Options
- `--view`, `-v`: View saved NPC collection
- `--view-id ID`: View specific NPC details
- `--no-save`: Generate without saving to collection

### Filters (for --view)
- `--filter-job`: Filter by job category
- `--filter-gender`: Filter by gender
- `--filter-species`: Filter by species

### Help Options
- `--list-jobs`: List all available job categories
- `--help`, `-h`: Show complete help

## Examples

### Quick Tavern Scene
```bash
# Generate an innkeeper and some patrons
python3 npc_generator.py --job innkeeper --cr 1/4
python3 npc_generator.py --job merchant --cr 0
python3 npc_generator.py --job adventurer --cr 1
```

### Combat Encounter
```bash
# Bandit crew for a roadside ambush
python3 npc_generator.py --group crew --job criminal --cr 1/2 --count 4
```

### Noble Court
```bash
# Generate nobles with influence but low combat ability
python3 npc_generator.py --job noble --cr 1/4
python3 npc_generator.py --group family --job noble --cr 0 --count 3
```

## File Structure

```
dnd-npc-generator/
├── npc_generator.py          # Main script
├── npc_collection/          # Created automatically
│   └── npcs.json           # Saved NPC database
├── README.md               # This file
└── .gitignore             # Git ignore rules
```

## Customization

The generator uses extensive lists of names, traits, and characteristics that can be easily modified in the script:

- **Names**: `FIRST_NAMES`, `LAST_NAMES`
- **Species**: `SPECIES` (12 D&D species)
- **Personality**: `PERSONALITY_TRAITS`, `MOTIVATIONS`, `SECRETS`
- **Physical**: `HEIGHTS`, `BUILDS`, `HAIR_COLORS`, `EYE_COLORS`, etc.
- **Classes**: `JOBS` dictionary with categories and specific roles

## D&D 2024 Compatibility

This generator is designed for D&D 5th Edition (2024 rules):
- Uses "Species" instead of "Race"
- Simplified species bonuses
- Modern CR scaling and stat block format
- Compatible with 2024 Player's Handbook and Monster Manual

## Contributing

Feel free to submit issues, feature requests, or pull requests! Some ideas for future enhancements:

- Additional species and classes
- More personality trait combinations  
- Spell lists for spellcasting NPCs
- Equipment generation
- Export to various formats (JSON, PDF)

## License

This project is open source and available under the MIT License.

## Author

Created by Mike McPhee - "Built out of frustration with his lack of imagination"

---

**Happy DMing! 🎲⚔️**