import requests
import pickle
import sys
import time

def get_pokemon_data(pokemon_id, retries=3):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
    
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Verifica si la solicitud fue exitosa
            data = response.json()
            
            name = data['name']
            types = [t['type']['name'] for t in data['types']]
            
            attacks = []
            for move in data['moves']:
                move_url = move['move']['url']
                move_response = requests.get(move_url)
                move_response.raise_for_status()
                move_data = move_response.json()
                
                move_name = move['move']['name']
                move_type = move_data['type']['name']
                power = move_data['power'] if move_data['power'] is not None else 0
                
                level_learned_at = next(
                    (version['level_learned_at'] for version in move['version_group_details'] if version['level_learned_at'] > 0), 
                    0
                )
                
                attacks.append({
                    'name': move_name,
                    'level_learned_at': level_learned_at,
                    'type': move_type,
                    'power': power
                })
            
            return {
                'name': name,
                'types': types,
                'attacks': attacks,
                'current_health': 100,
                'base_health': 100,
                'current_exp': 0,
                'level': 0
            }
        
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener los datos del Pokemon {pokemon_id}: {e}")
            if attempt < retries - 1:
                print("Reintentando...")
                time.sleep(2)  # Esperar 2 segundos antes de reintentar
            else:
                print(f"Error persistente al obtener los datos del Pokemon {pokemon_id}. Saltando...")
                return None
    
    return None

def get_all_pokemons():
    try:
        print('Cargando el archivo de pokemons...')
        with open('pokefile.pkl', 'rb') as pokefile:
            pokemon_list = pickle.load(pokefile)
        
        print('¡Archivo pickle cargado con éxito!')

    except FileNotFoundError:
        print('Archivo no encontrado. Cargando de internet...')
        pokemon_list = []
        for i in range(1, 151):
            pokemon_data = get_pokemon_data(i)
            if pokemon_data:
                pokemon_list.append(pokemon_data)
                print('*', end='')
                sys.stdout.flush()
        
        print('\n¡Pokemons descargados de internet con éxito!')
        
        with open('pokefile.pkl', 'wb') as pokefile:
            pickle.dump(pokemon_list, pokefile)

    return pokemon_list

def main():
    pokemons = get_all_pokemons()
    for pokemon in pokemons:
        print(f"Nombre: {pokemon['name']}")
        print(f"Tipo: {', '.join(pokemon['types'])}")
        print(f'Vida: {pokemon['current_health']}')
        print(f'Experiencia: {pokemon['current_exp']}')
        print(f'Level: {pokemon['level']}')
        print("Ataques:")
        for attack in pokemon['attacks']:
            print(f"  - Nombre del ataque: {attack['name']}")
            print(f"    Nivel mínimo requerido: {attack['level_learned_at']}")
            print(type(attack['level_learned_at']))
            print(f"    Tipo de ataque: {attack['type']}")
            print(f"    Daño que inflinge el ataque: {attack['power']}")
        print("\n" + "-"*50 + "\n")

if __name__ == '__main__':
    main()