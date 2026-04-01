#Declarando dicionários
""" pessoa = {"Nome":"Lucas", "Idade":30}
print(pessoa)

pessoa = dict(nome="Lcs", idade=35)
print(pessoa) """

#Acessando dados
""" dados = {"nome": "Guilherme", "idade": 28, "telefone": "3333-1234"}

print(dados["nome"])  # "Guilherme"
print(dados["idade"])  # 28
print(dados["telefone"])  # "3333-1234"

dados["nome"] = "Maria"
dados["idade"] = 18
dados["telefone"] = "9988-1781"

print(dados)  # {"nome": "Maria", "idade": 18, "telefone": "9988-1781"} """

#Dicionários aninhados
""" contatos = {
    "lucas@e-mail.com":{"nome":"Lucas", "Telefone":"3333-3333"},
    "guilherme@gmail.com": {"nome": "Guilherme", "telefone": "3333-2221"},
    "giovanna@gmail.com": {"nome": "Giovanna", "telefone": "3443-2121"},
    "chappie@gmail.com": {"nome": "Chappie", "telefone": "3344-9871"},
    "melaine@gmail.com": {"nome": "Melaine", "telefone": "3333-7766"},
}

telefone = contatos["lucas@e-mail.com"]["Telefone"]

print(telefone) """