import json
from pathlib import Path

DATA_DIR = Path(__file__).parent

def load_single_token_names() -> list[str]:
    with open(DATA_DIR / 'single_token_names.json') as f:
        return json.load(f)

def load_single_token_words() -> list[str]:
    with open(DATA_DIR / 'single_token_words.json') as f:
        return json.load(f)
