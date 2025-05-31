#Sistema_Puc


import json
import os

# Função para carregar dados de um arquivo .json
# Se o arquivo não existir, retorna uma lista vazia (evita erro)
def carregar_dados(caminho):
    if os.path.exists(caminho):
        with open(caminho, 'r') as arquivo:
            return json.load(arquivo)
    return []

# Função para salvar os dados no arquivo .json correspondente
# Usada sempre ao sair do programa, garantindo persistência dos dados
def salvar_dados(caminho, dados):
    with open(caminho, 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)

# Função para gerar um novo ID automaticamente
# Pega o maior ID atual e soma 1 (evita IDs repetidos)
def gerar_id(lista):
    if not lista:
        return 1
    return max(item['id'] for item in lista) + 1

# Função para listar os registros de qualquer lista (estudantes, professores, etc.)
def listar_registros(lista):
    if not lista:
        print("\nNenhum registro encontrado.")
    else:
        for item in lista:
            print(item)

# Função genérica para adicionar um novo registro (pode ser estudante, professor, etc.)
# Campos podem incluir relacionamentos com outros dados (como ID do professor, disciplina, etc.)
def adicionar_registro(lista, campos, listas_relacionadas=None):
    registro = {"id": gerar_id(lista)}
    for campo in campos:
        while True:
            # Se o campo tiver relação com outra tabela, mostra os registros disponíveis
            if listas_relacionadas and campo in listas_relacionadas:
                rel_lista = listas_relacionadas[campo]
                print(f"\n--- Registros disponíveis para {campo} ---")
                listar_registros(rel_lista)

            valor = input(f"Digite {campo}: ").strip()
            if not valor:
                print(f"{campo} inválido. Tente novamente.")
                continue

            # Verifica se o ID informado existe na lista relacionada (relacionamento válido)
            if listas_relacionadas and campo in listas_relacionadas:
                try:
                    id_int = int(valor)
                    if any(item["id"] == id_int for item in listas_relacionadas[campo]):
                        registro[campo] = id_int
                        break
                    else:
                        print(f"ID informado para {campo} não existe.")
                except ValueError:
                    print("Digite um número inteiro válido.")
            else:
                registro[campo] = valor
                break

    lista.append(registro)
    print(f"Registro adicionado com ID {registro['id']}")

# Função para atualizar um registro existente
# O usuário escolhe o ID e pode alterar os campos (menos o ID)
def atualizar_registro(lista):
    try:
        id_alvo = int(input("Digite o ID do registro a ser atualizado: "))
        for item in lista:
            if item['id'] == id_alvo:
                for chave in item:
                    if chave != 'id':
                        novo_valor = input(f"Novo valor para {chave} (atual: {item[chave]}): ").strip()
                        if novo_valor:
                            item[chave] = novo_valor
                print("Registro atualizado com sucesso!")
                return
        print("Registro não encontrado.")
    except ValueError:
        print("ID inválido!")

# Função para excluir um registro pelo ID
def excluir_registro(lista):
    try:
        id_alvo = int(input("Digite o ID do registro a ser excluído: "))
        for item in lista:
            if item['id'] == id_alvo:
                lista.remove(item)
                print("Registro excluído com sucesso.")
                return
        print("Registro não encontrado.")
    except ValueError:
        print("ID inválido!")

# Menu com operações CRUD (Adicionar, Listar, Atualizar, Excluir)
# Serve para qualquer tipo de entidade (estudante, professor, etc.)
def menu_operacoes(nome_modulo, lista, campos, listas_relacionadas=None):
    while True:
        print(f"\n-- MENU {nome_modulo.upper()} --")
        print("1. Adicionar")
        print("2. Listar")
        print("3. Atualizar")
        print("4. Excluir")
        print("5. Voltar ao Menu Principal")

        try:
            opcao = int(input("Escolha uma opção: "))
            if opcao == 1:
                adicionar_registro(lista, campos, listas_relacionadas)
            elif opcao == 2:
                listar_registros(lista)
            elif opcao == 3:
                atualizar_registro(lista)
            elif opcao == 4:
                excluir_registro(lista)
            elif opcao == 5:
                break
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida! Digite um número inteiro.")

# Menu principal do sistema, onde o usuário escolhe qual módulo deseja acessar
def menu_principal():
    # Carrega os dados salvos anteriormente
    estudantes = carregar_dados("estudantes.json")
    professores = carregar_dados("professores.json")
    disciplinas = carregar_dados("disciplinas.json")
    turmas = carregar_dados("turmas.json")
    matriculas = carregar_dados("matriculas.json")

    while True:
        print("\n*** Sistema PUC ***")
        print("------ MENU PRINCIPAL ------")
        print("1. Gerenciar Estudantes")
        print("2. Gerenciar Professores")
        print("3. Gerenciar Disciplinas")
        print("4. Gerenciar Turmas")
        print("5. Gerenciar Matrículas")
        print("6. Sair")

        try:
            opcao = int(input("Escolha uma opção: "))

            if opcao == 6:
                # Salva os dados antes de sair
                print("Salvando dados e saindo...")
                salvar_dados("estudantes.json", estudantes)
                salvar_dados("professores.json", professores)
                salvar_dados("disciplinas.json", disciplinas)
                salvar_dados("turmas.json", turmas)
                salvar_dados("matriculas.json", matriculas)
                break
            elif opcao == 1:
                menu_operacoes("Estudantes", estudantes, ["nome", "cpf"])
            elif opcao == 2:
                menu_operacoes("Professores", professores, ["nome", "cpf"])
            elif opcao == 3:
                menu_operacoes("Disciplinas", disciplinas, ["nome"])
            elif opcao == 4:
                # Ao criar uma turma, é necessário informar um professor e uma disciplina existentes
                menu_operacoes("Turmas", turmas, ["id_professor", "id_disciplina"], {
                    "id_professor": professores,
                    "id_disciplina": disciplinas
                })
            elif opcao == 5:
                # Ao matricular um aluno, é necessário informar o ID de uma turma e de um estudante
                menu_operacoes("Matrículas", matriculas, ["id_turma", "id_estudante"], {
                    "id_turma": turmas,
                    "id_estudante": estudantes
                })
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida! Digite um número inteiro.")

# Ponto de entrada do programa
if __name__ == "__main__":
    # Inicia o sistema
    menu_principal()
