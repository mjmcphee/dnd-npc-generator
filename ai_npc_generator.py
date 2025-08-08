#!/usr/bin/env python3
"""
AI-powered NPC Generator using Ollama
Extends the main NPC generator with AI-generated content
"""
import json
import random
import re
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3')

# --------------------------------------------------------------------------- #
#  Helper: Extract the first balanced JSON object from a string
# --------------------------------------------------------------------------- #
def extract_json_from_response(text: str):
    """
    Return a Python dict parsed from the *first* balanced JSON object found
    inside ``text``.  If nothing is found, raise ValueError.
    """
    # ``re.DOTALL`` lets the dot match newlines so we can capture
    # multi‑line JSON blobs.
    pattern = r'\{.*?\}'
    match = re.search(pattern, text, flags=re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in the response.")

    json_str = match.group(0)
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

# --------------------------------------------------------------------------- #
#  Core functions
# --------------------------------------------------------------------------- #
def query_ollama(prompt, model=None):
    """Send a query to Ollama and return the response"""
    if not model:
        model = OLLAMA_MODEL

    url = f"{OLLAMA_URL}/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, timeout=180)
        response.raise_for_status()

        result = response.json()
        return result.get('response', '')

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing Ollama response: {e}")
        return None


def generate_ai_npc_prompt(job_filter=None, gender_filter=None, challenge_rating=None, group_context=None):
    """Generate a detailed prompt for AI NPC creation"""

    base_prompt = """You are an expert D&D 5th Edition (2024) Dungeon Master creating a unique NPC. Generate a complete NPC with creative, engaging details that fit the D&D fantasy setting.
Return your response as valid JSON with exactly this structure:
{
    "name": "First Last",
    "species": "one of: Human, Elf, Dwarf, Halfling, Dragonborn, Gnome, Half-Elf, Half-Orc, Tiefling, Aasimar, Genasi, Goliath",
    "class": "specific job title",
    "gender": "Male, Female, or Non-binary",
    "personality": "a unique personality trait that makes them memorable",
    "speech_pattern": "how they speak or communicate uniquely",
    "voice": "voice inspiration or description",
    "motivation": "what drives them, their current goal or desire",
    "secret": "a hidden aspect of their background or current situation",
    "height": "physical height description",
    "build": "body type and build",
    "hair_color": "hair color",
    "hair_style": "how they wear their hair",
    "eye_color": "eye color",
    "distinctive_feature": "a memorable physical feature or marking",
    "clothing_style": "how they dress and present themselves"
}
Requirements:
- Make them feel like a real person with depth and complexity
- Avoid generic fantasy tropes - be creative and original
- Give them interesting quirks and memorable details
- Ensure all traits work together cohesively
- Keep everything appropriate for D&D fantasy setting
- Aside from species, use the supplied data like names as idea starts, but be creative
- Be creative, characters must be complex and deep"""

    # Add specific constraints based on arguments
    constraints = []

    if job_filter:
        job_categories = {
            "innkeeper": "tavern owner, barkeep, or inn manager",
            "merchant": "trader, shopkeeper, peddler, or business owner",
            "guard": "city watch, bouncer, sentry, or security personnel",
            "noble": "aristocrat, lord/lady, courtier, or diplomat",
            "criminal": "thief, smuggler, con artist, fence, or underworld figure",
            "artisan": "blacksmith, baker, tailor, carpenter, jeweler, or skilled craftsperson",
            "religious": "priest, acolyte, temple guard, oracle, or religious figure",
            "adventurer": "fighter, rogue, wizard, cleric, ranger, barbarian, bard, sorcerer, warlock, paladin, monk, or druid",
            "sailor": "sailor, ship captain, navigator, quartermaster, or maritime worker",
            "performer": "bard, dancer, actor, storyteller, or entertainer",
            "scholar": "scholar, librarian, scribe, teacher, or academic",
            "commoner": "farmer, laborer, servant, stable hand, cook, or common worker"
        }
        constraints.append(f"- The NPC must be a {job_categories.get(job_filter, job_filter)}")

    if gender_filter:
        constraints.append(f"- The NPC must be {gender_filter}")

    if challenge_rating:
        cr_context = {
            "0": "a completely non‑combative civilian",
            "1/8": "someone with minimal combat training",
            "1/4": "someone with basic combat skills",
            "1/2": "a capable combatant",
            "1": "a skilled fighter",
            "2": "a veteran combatant",
            "3": "a dangerous opponent",
            "4": "a formidable warrior",
            "5": "a legendary fighter"
        }
        if challenge_rating in cr_context:
            constraints.append(f"- This NPC should be {cr_context[challenge_rating]} (CR {challenge_rating})")

    if group_context:
        constraints.append(f"- This NPC is part of a {group_context['type']} and should fit that theme")
        if 'shared_traits' in group_context:
            for trait, value in group_context['shared_traits'].items():
                if trait == 'species':
                    constraints.append(f"- Must be a {value}")
                elif trait == 'motivation':
                    constraints.append(f"- Should share the motivation: {value}")

    if constraints:
        base_prompt += "\n\nSpecific requirements for this NPC:\n" + "\n".join(constraints)

    return base_prompt


def parse_ai_npc_response(response_text):
    """Parse the AI response and convert it to the expected NPC format"""
    try:
        # First pull out the pure JSON from the full response
        ai_npc = extract_json_from_response(response_text)

        # Validate required fields
        required_fields = [
            'name', 'species', 'class', 'gender', 'personality', 'speech_pattern',
            'voice', 'motivation', 'secret', 'height', 'build', 'hair_color',
            'hair_style', 'eye_color', 'distinctive_feature', 'clothing_style'
        ]

        for field in required_fields:
            if field not in ai_npc:
                print(f"Warning: AI response missing required field '{field}'")
                return None

        # Determine class category based on the class
        from npc_generator import JOBS
        class_category = "commoner"  # default

        for category, classes in JOBS.items():
            if any(ai_npc['class'].lower() in job.lower() for job in classes):
                class_category = category
                break

        # Add the class_category to the NPC data
        ai_npc['class_category'] = class_category

        return ai_npc

    except ValueError as e:
        # Raised by extract_json_from_response when no/invalid JSON
        print(f"Error extracting JSON: {e}")
        print(f"Response was: {response_text}")
        return None


def generate_ai_npc(job_filter=None, gender_filter=None, challenge_rating=None, shared_traits=None):
    """Generate an NPC using AI with the same interface as the regular generator"""

    # Prepare group context if shared traits are provided
    group_context = None
    if shared_traits:
        group_context = {
            'type': 'group member',
            'shared_traits': shared_traits
        }

    # Generate the prompt
    prompt = generate_ai_npc_prompt(job_filter, gender_filter, challenge_rating, group_context)

    # Query the AI
    print("🤖 Generating AI-powered NPC... (this may take a moment)")
    response = query_ollama(prompt)

    if not response:
        print("Failed to get response from AI. Falling back to regular generation.")
        return None

    # Parse the response
    ai_npc = parse_ai_npc_response(response)

    if not ai_npc:
        print("Failed to parse AI response. Falling back to regular generation.")
        return None

    # Apply shared traits if provided (override AI choices where necessary)
    if shared_traits:
        if "last_name" in shared_traits:
            # Split the AI-generated name and replace the last name
            name_parts = ai_npc["name"].split()
            if len(name_parts) > 1:
                ai_npc["name"] = f"{name_parts[0]} {shared_traits['last_name']}"

        if "species" in shared_traits:
            ai_npc["species"] = shared_traits["species"]

        if "motivation" in shared_traits:
            ai_npc["motivation"] = shared_traits["motivation"]

        if "class_category" in shared_traits and not job_filter:
            from npc_generator import JOBS
            if shared_traits["class_category"] in JOBS:
                ai_npc["class"] = random.choice(JOBS[shared_traits["class_category"]])
                ai_npc["class_category"] = shared_traits["class_category"]

    # Generate stat block if challenge rating is provided
    if challenge_rating:
        from npc_generator import generate_stat_block
        stat_block = generate_stat_block(ai_npc, challenge_rating)
        if stat_block:
            ai_npc["stat_block"] = stat_block

    return ai_npc


def generate_ai_group(group_type, count, job_filter=None, challenge_rating=None):
    """Generate a group of AI NPCs with shared traits"""
    from npc_generator import GROUP_TYPES

    if group_type not in GROUP_TYPES:
        raise ValueError(f"Unknown group type: {group_type}")

    group_info = GROUP_TYPES[group_type]
    npcs = []

    # Generate the first NPC to establish shared traits
    print(f"🤖 Generating AI-powered {group_info['name']} ({count} members)...")
    first_npc = generate_ai_npc(job_filter=job_filter, challenge_rating=challenge_rating)

    if not first_npc:
        print("Failed to generate first AI NPC. Cannot create group.")
        return None

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
        print(f"🤖 Generating member {i + 2}/{count}...")

        # Pick a unique relationship if possible
        available_relationships = [r for r in group_info["relationships"] if r not in used_relationships]
        if not available_relationships:
            available_relationships = group_info["relationships"]  # Allow repeats if we run out

        relationship = random.choice(available_relationships)
        used_relationships.append(relationship)

        npc = generate_ai_npc(job_filter=job_filter, shared_traits=shared_traits, challenge_rating=challenge_rating)

        if not npc:
            print(f"Failed to generate AI NPC {i + 2}. Skipping...")
            continue

        npc["relationship"] = relationship
        npcs.append(npc)

    return {
        "type": group_info["name"],
        "members": npcs
    }


def test_ollama_connection():
    """Test if Ollama is accessible and the model is available"""
    try:
        # Test basic connection
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
        response.raise_for_status()

        models = response.json().get('models', [])
        model_names = [model['name'] for model in models]

        if OLLAMA_MODEL not in model_names:
            print(f"Warning: Model '{OLLAMA_MODEL}' not found in Ollama.")
            print(f"Available models: {', '.join(model_names)}")
            return False

        return True

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama at {OLLAMA_URL}: {e}")
        print("Make sure Ollama is running and accessible.")
        return False


if __name__ == "__main__":
    # Test the AI NPC generator
    if test_ollama_connection():
        print("Testing AI NPC generation...")
        npc = generate_ai_npc(job_filter="innkeeper", challenge_rating="1/4")
        if npc:
            from npc_generator import display_npc
            display_npc(npc)
        else:
            print("Failed to generate test NPC")
    else:
        print("Cannot test AI generation - Ollama connection failed")