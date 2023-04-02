import json
from functools import reduce
from IPython.display import clear_output

### Menus

def input_opcao(opcoes_validas):
    while True:
        opcao = input('Digite uma das opções: ')
        if opcao in opcoes_validas:
            return opcao
        
        print('Opção inválida.')

def menu_principal():
    print('------------------------')
    print('#### MENU PRINCIPAL ####')
    print('------------------------')
    print('[1] Logar como usuário')
    print('[2] Logar como admin')
    print('[3] Sair')
    opcao = input_opcao(['1', '2', '3'])
    return opcao

def menu_admin():
    print('------------------------')
    print('###### MENU ADMIN ######')
    print('------------------------')
    print('[1] Registrar artista')
    print('[2] Registrar álbum')
    print('[3] Sair')
    opcao = input_opcao(['1', '2', '3'])
    return opcao

def menu_user():
    print('------------------------')
    print('###### MENU USER #######')
    print('------------------------')
    print('[1] Buscar playlist')
    print('[2] Criar playlist')
    print('[3] Sair')
    opcao = input_opcao(['1', '2', '3'])
    return opcao

def menu_buscar_playlist():
    print('-----------------------')
    print('### BUSCAR PLAYLIST ###')
    print('-----------------------')
    print('[1] Buscar por música')
    print('[2] Buscar por artista')
    print('[3] Buscar por nome da playlist')
    opcao = input_opcao(['1', '2', '3'])
    return opcao

### Arquivos

def ler_arquivos(nome_arquivo: str) -> dict:
    try:
        with open(nome_arquivo, 'r') as arquivo:
            conteudo = arquivo.read()
            
        conteudo_json = json.loads(conteudo)

        return conteudo_json
    
    except (FileNotFoundError, TypeError):
        with open(nome_arquivo, 'w') as arquivo:
            conteudo = arquivo.write('{}')
        
        return dict()

    except:
        return dict()
    
def int_id_album(albuns: dict) -> dict:

    return {int(album_id): album for album_id, album in albuns.items()}

def ler_tudo():
    artistas = ler_arquivos('artistas.json')
    albuns = ler_arquivos('albuns.json')
    playlists = ler_arquivos('playlists.json')

    albuns = int_id_album(albuns)

    return artistas, albuns, playlists

def escrever(conteudo: dict, nome_arquivo: str) -> None:
    try:
        with open(nome_arquivo, 'w') as arquivo:
            arquivo.write(json.dumps(conteudo, indent = 4))
    except Exception as e:
        print(f'Erro: {e}')
        
    return None

### Cadastros

def max_ids(albuns):
    if albuns == {}:
        return 0, 0
    
    max_id_album = max(albuns.keys())
    max_id_musica = max([valor['id_musica'] if type(valor['id_musica']) == int else max(valor['id_musica']) for valor in albuns.values()])

    return max_id_album, max_id_musica

def cadastrar_artista(artistas):
    novo_artistas = artistas.copy()
    artista = input('Digite um novo artista: ')

    if artista not in artistas:
        novo_artistas[artista] = {'nome_album': [],
                                    'id_album': []}
        return novo_artistas
    
    print('Artista já cadastrado.')
    return novo_artistas

def cadastrar_album(artistas, albuns, max_id_album, max_id_musica):
    novo_artistas = artistas.copy()
    novo_albuns = albuns.copy()
    novo_max_id_album = max_id_album
    novo_max_id_musica = max_id_musica

    artista = input('Digite o nome do artista: ')
    if artista not in artistas:
        print('Artista não encontrado. Cancelando a operação.')
        return novo_artistas, novo_albuns, novo_max_id_album, novo_max_id_musica
    
    novo_album = input('Digite o nome do álbum: ')
    
    if novo_album in novo_artistas[artista]['nome_album']:
        print('Álbum já existe. Cancelando a operação.')
        return novo_artistas, novo_albuns, novo_max_id_album, novo_max_id_musica

    try:
        num_musicas = int(input('Digite o número de músicas no álbum: '))
    except:
        print('Número de músicas inválido. Cancelando a operação.')
        return novo_artistas, novo_albuns, novo_max_id_album, novo_max_id_musica
    
    nome_musicas = [input(f'Digite o nome da música {i+1}: ') for i in range(num_musicas)]
    id_musicas = [id for id in range(novo_max_id_musica+1, novo_max_id_musica+1+num_musicas)]

    novo_max_id_album += 1
    novo_max_id_musica += num_musicas

    novo_artistas[artista]['nome_album'].append(novo_album)
    novo_artistas[artista]['id_album'].append(novo_max_id_album)

    novo_albuns[novo_max_id_album] = {'nome_album': novo_album,
                                      'nome_musica': nome_musicas,
                                      'id_musica': id_musicas}
    
    return novo_artistas, novo_albuns, novo_max_id_album, novo_max_id_musica

def escolher_musica(artistas, albuns):
    print('Confira a lista de artistas:')
    [print(artista) for artista in sorted(artistas)]
    
    nome_artista = input('Digite o nome do artista: ')
    while nome_artista not in artistas:
        nome_artista = input('Artista não encontrado. Digite o nome do artista')
    
    ids_albuns = artistas[nome_artista]['id_album']

    clear_output(wait=True)
    print('-'*64)
    print(f'Confira os álbuns do artista {nome_artista}:')
    albuns_artista = [infos['nome_album'] for album, infos in albuns.items() if album in ids_albuns]
    [print(album) for album in albuns_artista]
    
    nome_album = input('Digite o nome do álbum: ')
    while nome_album not in albuns_artista:
        nome_album = input('Álbum não encontrado. Digite o nome do álbum: ')
    
    id_album = [id for album, id in zip(artistas[nome_artista]['nome_album'], artistas[nome_artista]['id_album']) if nome_album == album][0]

    clear_output(wait=True)
    print('-'*64)
    print(f'Confira as músicas do artista {nome_artista} no álbum {nome_album}: ')
    musicas_album = albuns[id_album]['nome_musica']
    [print(musica) for musica in musicas_album]
    
    nome_musica = input('Digite o nome da música: ')
    while nome_musica not in musicas_album:
        nome_musica = input('Música não encontrada. Digite o nome da música: ')
    
    id_musica = [id for musica, id in zip(albuns[id_album]['nome_musica'], albuns[id_album]['id_musica']) if nome_musica == musica][0]

    return nome_artista, nome_album, id_album, nome_musica, id_musica

def cadastrar_playlist(artistas, albuns, playlists):

    if albuns == {} or artistas == {}:
        print('Parece que não há dados de artistas e álbuns cadastrados, por favor consulte o seu administrador.')
        return None

    nome_playlist = input('Informe o nome para a sua playlist: ')
    while nome_playlist in playlists:
        nome_playlist = input('Nome já cadastrado. Informe o nome para a sua playlist: ')
    
    playlist_musicas = []
    playlist_ids = []
    playlist_artistas = []
    playlists_novas = playlists.copy()

    while True:
        nome_artista, *_,  nome_musica, id_musica = escolher_musica(artistas, albuns)
        playlist_musicas.append(nome_musica)
        playlist_ids.append(id_musica)
        playlist_artistas.append(nome_artista)

        opcao = input('Deseja continuar? (S/N) ').upper()
        while opcao != 'S' and opcao != 'N':
            opcao = input('Opção inválida. Deseja continuar? (S/N) ').upper()
            
        if opcao == 'N':
            playlists_novas[nome_playlist] = {'nome_musica': playlist_musicas,
                                        'id_musica': playlist_ids,
                                        'nome_artista': playlist_artistas}

            return playlists_novas
        
### Buscas

def filter_conteudo(dicionario, nome_playlist = None, match_exato = False, **kwargs):
    if nome_playlist != None:
        keys = [chave for chave in dicionario.keys() if chave == nome_playlist]
        return keys
    
    else:
        # para cada parametro em **kwargs, verificar se kwargs está em um conteúdo do dicionário, se estiver retornar a chave
        keys = [[chave for chave, conteudo in dicionario.items() if filtro in conteudo[parametro]] for parametro, filtro in kwargs.items()]
        
        # keys é uma lista que contém listas com todos as chaves que eram iguais aos valores de kwargs, para cada parametro de kwargs

        # se match_exato == False, quer dizer que iremos fazer a união entre as listas dentro da lista keys
        # caso match_exato == True, faremos a interseção das listas de keys

        if match_exato == False:
            keys = list(reduce(lambda x, y: set(x).union(set(y)), keys))
    
        else:
            keys = list(reduce(lambda x, y: set(x).intersection(set(y)), keys))
    
        return keys
    
def print_playlists(playlists:dict, nomes_playlists:list, nome_artista:str = None, nome_musica:str = None, nome_playlist:str = None) -> None:

    if nomes_playlists == []:
        print('Não encontramos playlists com os dados informados :(')
        return None

    if nome_artista != None:
        print(f'Playlists contendo [{nome_artista}]')
    
    if nome_musica != None:
        print(f'Playlists contendo [{nome_musica}]')

    if nome_playlist != None:
        print(f'Playlist [{nome_playlist}]')

    for playlist in nomes_playlists:
        print(f'\n>> {playlist} <<\n')
        [print(f'[{id}] {musica[1]} | {musica[0]}') for id, musica in enumerate(zip(playlists[playlist]['nome_musica'], playlists[playlist]['nome_artista']))]
        print('-'*64)
    return None

def buscar_playlist_musica(playlists):
    nome_musica = input('Digite o nome da música: ')

    filter_playlist = filter_conteudo(playlists, nome_musica = nome_musica)

    print_playlists(playlists, filter_playlist, nome_musica = nome_musica)

    return filter_playlist

def buscar_playlist_artista(playlists):
    nome_artista = input('Digite o nome do artista: ')

    filter_playlist = filter_conteudo(playlists, nome_artista = nome_artista)

    print_playlists(playlists, filter_playlist, nome_artista = nome_artista)

    return filter_playlist

def buscar_playlist_nome(playlists):
    nome_playlist = input('Digite o nome da playlist: ')

    filter_playlist = filter_conteudo(playlists, nome_playlist = nome_playlist)

    print_playlists(playlists, filter_playlist, nome_playlist = nome_playlist)

    return filter_playlist

### Main

def main():

    print('Bem-vindo(a) ao Vin Deezer!')

    # Inicializar os arquivos
    artistas, albuns, playlists = ler_tudo()

    while True:
        max_id_album, max_id_musica = max_ids(albuns)

        opcao = menu_principal()
        clear_output(wait=True)
        
        # Menu usuário
        if opcao == '1':
            while True:
                opcao = menu_user()

                if opcao == '1':
                    clear_output(wait=True)
                    print('------------------------')
                    print('Buscar playlist')
                    opcao = menu_buscar_playlist()

                    if opcao == '1':                        
                        clear_output(wait=True)
                        print('------------------------')
                        print('Buscar por música')
                        playlists = ler_arquivos('playlists.json')
                        buscar_playlist_musica(playlists)

                    elif opcao == '2':                    
                        clear_output(wait=True)    
                        print('------------------------')
                        print('Buscar por artista')
                        playlists = ler_arquivos('playlists.json')
                        buscar_playlist_artista(playlists)

                    elif opcao == '3':
                        clear_output(wait=True)
                        print('------------------------')
                        print('Buscar por nome da playlist')
                        playlists = ler_arquivos('playlists.json')
                        buscar_playlist_nome(playlists)


                elif opcao == '2':
                    clear_output(wait=True)
                    print('------------------------')
                    print('Criar playlist')
                    artistas, albuns, playlists = ler_tudo()
                    playlists = cadastrar_playlist(artistas, albuns, playlists)
                    escrever(playlists, 'playlists.json')

                else:
                    clear_output(wait=True)
                    print('------------------------')
                    print('Saindo.')
                    break
        
        # Menu admin
        elif opcao == '2':
            while True:
                opcao = menu_admin()

                if opcao == '1':
                    clear_output(wait=True)
                    print('------------------------')
                    print('Registrar artista')
                    artistas = ler_arquivos('artistas.json')
                    artistas = cadastrar_artista(artistas)
                    escrever(artistas, 'artistas.json')

                elif opcao == '2':
                    clear_output(wait=True)
                    print('------------------------')
                    print('Registrar álbum')
                    artistas, albuns, playlists = ler_tudo()
                    artistas, albuns, max_id_album, max_id_musica = cadastrar_album(artistas, albuns, max_id_album, max_id_musica)
                    escrever(artistas, 'artistas.json')
                    escrever(albuns, 'albuns.json')
                    
                else:
                    clear_output(wait=True)
                    print('------------------------')
                    print('Saindo.')
                    break
        
        # Sair
        else:
            print('Encerrando o programa! Obrigado por utilizá-lo :)')
            break

main()