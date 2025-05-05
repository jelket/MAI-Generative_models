from io import BytesIO

from functools import reduce
import datetime
import re
import numpy as np

from sqlalchemy import create_engine, Text, text

import requests
import json

with open('game_data.json', 'r') as file:
    game_data = json.load(file)

def search_context(location_queries, character_queries, data):
    """Поиск контекста в данных"""
    context = []
    
    for location_query in location_queries:
        for location in data['world']['locations']:
            if location_query.lower() in location['name'].lower() or location_query.lower() in location['description'].lower():
                context.append(f"Локация: {location['name']}, Описание: {location['description']}")
    
    for character_query in character_queries:
        for character in data['characters']:
            if character_query.lower() in character['name'].lower() or any(character_query.lower() in dialogue.lower() for dialogue in character['dialogues']):
                context.append(f"Квест от персонажа: {character['name']}, Описание: {character['description']}")
    
    return "\n".join(context)

location_queries = ["Лесные руины", "Затерянный город"]
character_queries = ["Никитос", "Даник", "Макс"]
context = search_context(location_queries, character_queries, game_data)

prompt = f"""Придумай мне сюжет квеста для видеоигры.
Для нескольких локаций нужно указать взаимодействие, например, как предмет с одной локации может помочь на другой.
Точно также нужно придумать взаимодействие между персонажами, если их указано несколько.
Они могут как обьединиться заранее и выдать квест вместе, так и добавляться уже в процессе выполнения квеста. Контекст: {context}"""

res = requests.post(
    url=".../api/generate", # развернута на корпоративном сервере, не могу указать
    json={
        "model": "t-pro-it-32k:latest", 
        "prompt": prompt, 
        "stream": False, 
        "context_size": 45000
    },
    verify=False,
    headers={"Authorization": "..."}
)

print(res.json()["response"])