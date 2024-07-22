
import requests
import json
import pandas as pd

def get_ingredients(dish_name):
    api_key = '9ef19e527e624035963d92e14934a465'
    deployment_url = 'https://carbonsustain-web.openai.azure.com/openai/deployments/carbonsustain-openai'
    url = f'{deployment_url}/chat/completions?api-version=2024-02-01'

    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Provide the ingredients and their quantities(grams) for making {dish_name}. For the output, output a tuple with (each ingredient, then the quantity, followed by the units). Output the number of servings and total dish carbon footprint as two tuples. Only leave the tuples."}
        ]
    }

    headers = {
        'api-key': api_key,
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        
        response_json = response.json()
        
        ingredients = response_json['choices'][0]['message']['content']
        print(ingredients)
        
        ingredients_list = []
        quantities_list = []
        # for line in ingredients.split('\n')[1:]:
        #     if ':' in line:
        #         ingredient, quantity = line.split(':', 1)
        #         ingredients_list.append(ingredient.strip())
        #         quantities_list.append(quantity.strip())
        
        #return pd.Series([ingredients_list, quantities_list])
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return pd.Series([None, None])

get_ingredients('sriracha aioli smoked tofu buddha bowl with vermecilli noodle (cucumber daikon carrot slaw | shaved purple cabbage ')