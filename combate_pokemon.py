import pokeload
import random
import os
import time

def get_player_profile(pokemon_list):
    return {
        'player_name': input('¿Cuál es tu nombre? '),
        'pokemon_inventory': [random.choice(pokemon_list) for a in range(3)],
        'combats': 0,
        'pokeballs': 0,
        'health_potion': 0,
    }


def any_player_pokemon_lives(player_profile):
    return  sum([pokemon['current_health'] for pokemon in player_profile['pokemon_inventory']]) > 0


def get_pokemon_info(pokemon):
    return f'{pokemon['name']} | level: {pokemon['level']} | health: {pokemon['current_health']}/{pokemon['base_health']}'


def choose_pokemon(player_profile):
    chosen = None
    while not chosen:
        print('ELIGE CON QUE POKEMON LUCHARÁS')
        for index in range(len(player_profile['pokemon_inventory'])):
            print(f'{index}. {get_pokemon_info(player_profile['pokemon_inventory'][index])}')
        
        try:
            if player_profile['pokemon_inventory'][int(input('¿Qué pokemon eliges? '))]['current_health'] > 0:
                return player_profile['pokemon_inventory'][int(input('¿Qué pokemon eliges? '))]
            else:
                print('No es posible cambiar ha ese pokemon')
        except (ValueError, IndexError):
            print('Opción no valida')

def player_attack(player_pokemon, enemy_pokemon):
    for attack in player_pokemon['attacks'][0:3]:
        print(f'{(player_pokemon['attacks'].index(attack)) + 1}) {attack['name']} | {attack['power']} | {attack['type']} | {attack['level_learned_at']}')

    move = None
    while move not in ['1', '2', '3']:
        move = input('¿Qué ataque deseas realizar? [1/2/3] ')

    if move == '1':
        if player_pokemon['attacks'][0]['level_learned_at'] == 'N/A' or player_pokemon['attacks'][0]['level_learned_at'] <= player_pokemon['level']:
            print(f'{player_pokemon['name']} ha realizado el ataque {player_pokemon['attacks'][0]['name']}')

            if player_pokemon['attacks'][0]['type'] in player_pokemon['types']:
                enemy_pokemon['current_health'] -= (player_pokemon['attacks'][0]['power']) * 2

            else:
                enemy_pokemon['current_health'] -= player_pokemon['attacks'][0]['power']
        else:
            print('No tienes nivel suficiente para realizar este ataque')
    
    if move == '2':
        if player_pokemon['attacks'][1]['level_learned_at'] == 'N/A' or player_pokemon['attacks'][1]['level_learned_at'] <= player_pokemon['level']:
            print(f'{player_pokemon['name']} ha realizado el ataque {player_pokemon['attacks'][1]['name']}')
            
            if player_pokemon['attacks'][0]['type'] in player_pokemon['types']:
                enemy_pokemon['current_health'] -= (player_pokemon['attacks'][0]['power']) * 2

            else:
                enemy_pokemon['current_health'] -= player_pokemon['attacks'][0]['power']
        else:
            print('No tienes nivel suficiente para realizar este ataque')

    if move == '3':
        if player_pokemon['attacks'][2]['level_learned_at'] == 'N/A' or player_pokemon['attacks'][2]['level_learned_at'] <= player_pokemon['level']:
            print(f'{player_pokemon['name']} ha realizado el ataque {player_pokemon['attacks'][2]['name']}')
            
            if player_pokemon['attacks'][0]['type'] in player_pokemon['types']:
                enemy_pokemon['current_health'] -= (player_pokemon['attacks'][0]['power']) * 2

            else:
                enemy_pokemon['current_health'] -= player_pokemon['attacks'][0]['power']
        else:
            print('No tienes nivel suficiente para realizar este ataque')

    if enemy_pokemon['current_health'] < 0:
        enemy_pokemon['current_health'] = 0

def enemy_attack(player_pokemon, enemy_pokemon):
    move = random.choice(enemy_pokemon['attacks'])
    print(f'{enemy_pokemon['name']} ha atacado con {move['name']}')
    if move['power'] == 'N/A':
        print('El ataque ha sido cancelado')
    else:
        player_pokemon['current_health'] -= move['power']

    if player_pokemon['current_health'] < 0:
        player_pokemon['current_health'] = 0

def assign_experience(attack_history):
    for pokemon in attack_history:
        points = random.randint(1, 5)
        pokemon['current_exp'] += points
    
    while pokemon['current_exp'] > 20:
        pokemon['current_exp'] -= 20
        pokemon['level'] += 1
        pokemon['current_health'] = pokemon['base_health']
        print(f'Tu pokemon ha subiduo al nivel {get_pokemon_info(pokemon)}')


def cure_pokemon(player_profile, player_pokemon):
    if player_profile['health_potion'] > 0:
        player_pokemon['current_health'] += 50
        player_profile['health_potion'] -= 1
        if player_pokemon['current_health'] > 100:
            player_pokemon['current_health'] = 100
        print(f'Te has curado: {player_pokemon['current_health']}/{player_pokemon['base_health']}')
    
    else:
        print('No puedes curarte porque no tienes pociones de vida')

def capture_with_pokeball(player_profile, enemy_pokemon):
    if player_profile['pokeballs'] > 0:
        if random.randint(1,100) > enemy_pokemon['current_health']:
            player_profile['pokemon_inventory'].append(enemy_pokemon)
            print(f'Has capturado el pokemon {enemy_pokemon['name']}')
            
            return True
        else:
            print('No has capturado al pokemon')
        
        player_profile['pokeballs'] -= 1
    else:
        print('No puedes capturar al pokemon porque no tienes pokeballs')

def item_lottery(player_profile):
        print('\nBIENVENIDO AL SORTEO DE ITEMS')
        #Pokeball
        print('Veamos si te toca una pokeball...')
        time.sleep(1.5)
        random_number = random.randint(1,10)
        if random_number >= 5:
            print('¡WOW! Te ha tocado una pokeball')
            player_profile['pokeballs'] += 1
        else:
            print('Oh vaya... No te ha tocado ninguna pokeball')
        
        #Cure potion
        print('Veamos si te toca una poción de vida...')
        time.sleep(1.5)
        random_number = random.randint(1,10)
        if random_number >= 5:
            print('¡WOW! Te ha tocado una poción de vida')
            player_profile['health_potion'] += 1
        else:
            print('Oh vaya... No te ha tocado ninguna poción de vida')

        print(f'Pokeballs: {player_profile['pokeballs']}')
        print(f'Pociones de curación: {player_profile['health_potion']}')

def fight(player_profile, enemy_pokemon):
    print('---NUEVO COMBATE---')

    attack_history = []
    player_pokemon = choose_pokemon(player_profile)
    
    while any_player_pokemon_lives(player_profile) and enemy_pokemon['current_health'] > 0:
        print(get_pokemon_info(player_pokemon))
        print(get_pokemon_info(enemy_pokemon))
        action = None
        while action not in ['A', 'P', 'V', 'C']:
            action = input('¿Qué deseas hacer? [A]tacar, [P]okeball, Poción de [V]ida, [C]ambiar: ')

        if action == 'A':
            player_attack(player_pokemon, enemy_pokemon)
            attack_history.append(player_pokemon)
        
        elif action == 'P':
            if capture_with_pokeball(player_profile, enemy_pokemon) == True:
                break

        elif action == 'V':
            cure_pokemon(player_profile, player_pokemon)

        elif action == 'C':
            player_pokemon = choose_pokemon(player_profile)

        if enemy_pokemon['current_health'] == 0:
            print('HAS GANADO EL COMBATE')
            assign_experience(attack_history)
            break
        else:
            enemy_attack(player_pokemon, enemy_pokemon)

        if player_pokemon['current_health'] == 0:
            if any_player_pokemon_lives(player_profile):
                player_pokemon = choose_pokemon(player_profile)
            else:
                print('GAME OVER')
                exit()

    #oajdf
    
    print('---FIN DEL COMBATE---')
    item_lottery(player_profile)

    input('Presiona ENTER para continuar...')
    os.system('cls')


def main():
    pokemon_list = pokeload.get_all_pokemons()
    player_profile = get_player_profile(pokemon_list)

    print(f'Hola {player_profile['player_name']} bienvenido a POKEMON FIGHT\n')

    while any_player_pokemon_lives(player_profile):

        enemy_pokemon = random.choice(pokemon_list)
        fight(player_profile, enemy_pokemon)
        player_profile['combats'] += 1

    print(f'Has perdido en el combate n{player_profile['combats']}')


if __name__ == '__main__':
    main()