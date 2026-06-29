# Sistema de Controle de Estoque e Vendas
# versao 2.0 - resolução de dívidas técnicas prioritárias
# autor: Lucas Cunha de Azevedo

import datetime
import os
from dotenv import load_dotenv

load_dotenv()  # carrega variáveis de ambiente do arquivo .env

# senha do administrador é lida de variável de ambiente para evitar hardcoding
# RESOLUÇÃO D7.1
SENHA_ADMIN = os.getenv("SENHA_ADMIN")

produtos = []

# funcao que adiciona produto
def add(n, p, q, hist=None):
    # cláusula de guarda para validar os dados do produto
    # RESOLUÇÃO D2.1
    if not n or p < 0 or q < 0:
        print("Dados do produto invalidos.")
        return

    # conferindo se hist é None para evitar o uso de listas mutáveis como valores padrão
    # RESOLUÇÃO D1.1
    if hist is None:
        hist = []

    produtos.append({"nome": n, "preco": p, "qtd": q})
    hist.append(n)
    print("Produto adicionado!")


# calcula o total de uma compra (usado no relatorio)
def calcular_total(preco, quantidade):
    # validação de entrada para evitar cálculos inválidos
    if preco < 0 or quantidade <= 0:
        return 0

    t = preco * quantidade

    # regra única de desconto
    # RESOLUÇÃO D5.5 E D5.6
    if t > 100:
        t = t - t * 0.10

    return t


def vender(nome, quantidade):
    # cláusula de guarda para validar os dados da venda
    # RESOLUÇÃO D2.1
    if not nome or quantidade <= 0:
        print("Dados da venda invalidos.")
        return 0

    for i in range(len(produtos)):
        if produtos[i]["nome"] == nome:
            if produtos[i]["qtd"] >= quantidade:
                produtos[i]["qtd"] -= quantidade
                # cálculo do total e regras de desconto são centralizadas na função calcular_total
                # RESOLUÇÃO D5.5 E D5.6
                total = calcular_total(produtos[i]["preco"], quantidade)
                print("Venda realizada. Total: " + str(total))
                return total
            else:
                print("Estoque insuficiente")
                return 0

    print("Produto nao encontrado")
    return 0


def listar():
    print("=== PRODUTOS ===")
    for x in produtos:
        print(x["nome"] + " - R$" + str(x["preco"]) + " - qtd: " + str(x["qtd"]))


def relatorio_estoque_baixo():
    print("=== ESTOQUE BAIXO ===")
    for x in produtos:
        if x["qtd"] < 5:
            print(x["nome"] + " esta com estoque baixo (" + str(x["qtd"]) + ")")


# funcao antiga, nao usamos mais
# def exportar():
#     f = open("dados.txt", "w")
#     for x in produtos:
#         f.write(str(x))
#     f.close()


def relatorio_vendas():
    # TODO: implementar de verdade
    pass


def menu():
    while True:
        print("\n1-Cadastrar  2-Vender  3-Listar  4-Estoque baixo  5-Admin  0-Sair")
        op = input("Opcao: ")

        if op == "1":
            n = input("Nome: ")

            # tratamento de exceções de entrada para preço e quantidade
            # RESOLUÇÃO D2.3
            try:
                p = float(input("Preco: "))
                q = int(input("Qtd: "))
            except ValueError:
                print("Preco ou quantidade invalidos.")
                continue
            
            # validações de entrada para preço e quantidade
            # RESOLUÇÃO D2.4 E D2.5
            if p < 0:
                print("Preco nao pode ser negativo.")
                continue

            if q < 0:
                print("Quantidade nao pode ser negativa.")
                continue

            add(n, p, q)

        elif op == "2":
            n = input("Nome do produto: ")

            # tratamento de exceções de entrada para quantidade
            # RESOLUÇÃO D2.3
            try:
                q = int(input("Quantidade: "))
            except ValueError:
                print("Quantidade invalida.")
                continue
            
            # validação de entrada para quantidade
            # RESOLUÇÃO D2.5
            if q <= 0:
                print("Quantidade deve ser maior que zero.")
                continue

            vender(n, q)

        elif op == "3":
            listar()

        elif op == "4":
            relatorio_estoque_baixo()

        elif op == "5":
            s = input("Senha: ")

            # validação de senha com base em variável protegida de ambiente
            # RESOLUÇÃO D7.1
            if SENHA_ADMIN is None:
                print("Senha do administrador nao configurada.")
            elif s == SENHA_ADMIN:
                print("Acesso liberado")
            else:
                print("Senha errada")

        elif op == "0":
            break

        else:
            print("Opcao invalida")

menu()