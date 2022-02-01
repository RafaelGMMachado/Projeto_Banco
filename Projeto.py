import os
from datetime import datetime
# Funções Extras
def ValidarNumerico(numero): # Verifica se os caracteres são numéricos
    validado = False
    if numero.isnumeric(): # Se a senha for numérica, ela é validada
        validado = True
    return validado
def ValidarConta (): # Valida se a conta existe e se a senha está correta
    cpf = input("Digite o CPF vinculado à conta: ")
    if os.path.isfile("./users/" + cpf + ".txt"): # Verifica se o usuário existe
        arquivo = open("./users/" + cpf + ".txt", "r")
        conteudo = arquivo.read()
        arquivo.close()
        senha_conta = conteudo.split()
        for n in range ( len (senha_conta) ): # Percorre os conteúdos do arquivo até encontrar a senha, depois a salva na variável 'senha_conta'
            if senha_conta[n] == "Senha:":
                senha_conta = senha_conta[n+1]
                break
        senha = input("Digite a senha: ")
        if senha_conta == senha: # Se a senha digitada pelo usuário é igual a senha digitada, se for, ela retorna um valor True
            return True, cpf
        else:
            print("\nSenha incorreta!")
            return False, cpf
    else:
        print("\nA conta não existe!")
        return False, cpf
def DebitarDepositar (cpf, saldo, palavras): # Debita ou deposita o dinheiro da conta
    arquivo = open("./users/" + cpf + ".txt", "w")
    n = 0
    while n < len(palavras): # Reescreve o arquivo com o novo saldo
        if n == 2 and palavras[n] != "CPF:": # Se a pessoa tiver nome composto ou digitar os sobrenomes não dará nenhum erro
            arquivo.write(" %s" % palavras[n] )
            palavras.pop(n)
            n -= 1
        if n == 0: # A primeira linha é escrita sem a quebra de linha para caso a pessoa tenha digitado o sobrenome ela poder pegar
            arquivo.write("{0} {1}".format ( palavras[n], palavras[n+1] ) )
        elif n%2 == 0:
            if palavras[n] == "Saldo:": # Na hora de escrever o saldo, altera o valor antigo pelo novo e deixa sempre 2 casas depois da vírgula
                palavras[n+1] = saldo
                arquivo.write("\n{0} {1:.2f}".format ( palavras[n], palavras[n+1] ) )
            else:
                arquivo.write("\n{0} {1}".format ( palavras[n], palavras[n+1] ) )
        n += 1
    arquivo.close()
def AtualizarExtrato (cpf, tipo, valor, tarifa, saldo): # Atualiza o Extrato
    arquivo = open("./extratos/Extrato_" + cpf + ".txt","a")
    data_hora = datetime.now() # Pega a data e hora
    data_hora = data_hora.strftime(r"%d-%m-%Y %H:%M") # Transforma a data e hora para o formato certo
    arquivo.write("Data: {0}   {1} {2:8.2f}   Tarifa: {3:6.2f}   Saldo: {4:8.2f}\n".format (data_hora , tipo, valor, tarifa, saldo) )
    arquivo.close()
# Funções do Menu
def NovaConta ():
    print("Para criar a sua conta, precisaremos de algumas informações\n")
    # Pegar as informações da conta
    nome =  ( input("Nome: ") ).title() # .title() transforma a primeira letra de cada palavra da str em maiúscula
    cpf = input("CPF: ")
    validado = ValidarNumerico (cpf)
    if validado == False: # Verifica se o CPF é válido
        print("\nCPF inválido!")
    else:
        if os.path.isfile("./users/" + cpf + ".txt"): # Verificar se o arquivo já existe
            print("\nCPF já registrado!")
        else: # Continuar o processo caso não exista
            tipo_conta = ( input ("Tipo de conta desejado: ") ).title()
            if tipo_conta == "Salário": # Padroniza o tipo de conta 'Salário'
                tipo_conta = "Salario"
            if tipo_conta != "Salario" and tipo_conta != "Comum" and tipo_conta != "Plus": # Verifica se o tipo de conta é válida
                print("\nTipo de conta inválida!")
            else: # Continua o código se o tipo de conta for válido
                senha = input("Senha: ")
                validado = ValidarNumerico(senha)
                if validado == False: # Verifica se a senha é válida
                    print("\nA senha deve ser numérica!")
                else:
                    valor_inicial = input("Valor inicial da conta: ")
                    if valor_inicial.replace(".","",1).isdigit(): # Se o valor for inteiro ou decimal, a conta é criada
                        valor_inicial = float(valor_inicial)
                        arquivo = open("./users/" + cpf + ".txt", "w")
                        arquivo.write("Nome: {0}\nCPF: {1}\nSenha: {2}\nConta: {3}\nSaldo: {4:.2f}".format (nome, cpf, senha, tipo_conta, valor_inicial ) )
                        arquivo.close()
                        AtualizarExtrato(cpf, "+", valor_inicial, 0, valor_inicial)
                        print("\nConta criada com sucesso!")
                    else:
                        print("\nValor inválido!")    
def ApagarConta ():
    print("Para prosseguir com a exclusão da conta, precisaremos de algumas informações\n")
    validado, cpf = ValidarConta()
    if validado == True: # Se o cpf e a senha forem validados, ele apaga a conta e o extrato
        os.remove("./users/" + cpf + ".txt")
        os.remove("./extratos/Extrato_" + cpf + ".txt")
        print ("\nConta excluída com sucesso!")       
def Debitar ():
    print("Para debitar um valor da sua conta, precisaremos de alguns dados\n")
    validado, cpf = ValidarConta()
    if validado == True: # Se o cpf e a senha forem validados, ele prossegue com a função
        arquivo = open("./users/" + cpf + ".txt", "r")
        conteudo = arquivo.read()
        arquivo.close()
        palavras = conteudo.split()
        
        for n in range ( len (palavras) ): # Armazena o tipo da conta e o saldo
            if palavras[n] == "Conta:":
                tipo_conta = palavras[n+1]
            if palavras[n] == "Saldo:":
                saldo = float(palavras[n+1])
                break

        debito = input("Valor do débito: ") # Adiciona a taxa cobrada para cada tipo de conta e não permite o débito caso ele ultrapasse o limite da conta
        if debito.isnumeric(): # Se o valor for inteiro ou decimal, continua com a função
            debito = float(debito)
            if debito > 0: # Verifica qual tarifa usa de acordo com o tipo de conta
                if tipo_conta == "Salario":
                    tarifa = debito*0.05
                    debito += debito*0.05
                    if (saldo - debito) < 0:
                        validado = False
                if tipo_conta == "Comum":
                    tarifa = debito*0.03
                    debito += debito*0.03
                    if saldo - debito < -500:
                        validado = False
                if tipo_conta == "Plus":
                    tarifa = debito*0.01
                    debito += debito*0.01
                    if saldo - debito < -5000:
                        validado = False

                if validado == False:
                    print("\nSaldo insuficiente!")
                else: # Se o saldo for suficiente, debita o dinheiro da conta
                    saldo = round(saldo - debito,2)
                    DebitarDepositar(cpf, saldo, palavras)
                    AtualizarExtrato(cpf, "-", (debito-tarifa), tarifa, saldo)
                    print("\nO valor foi debitado da conta!")
            else:
                print("\nDepósito muito baixo!")
        else:
            print("\nValor inválido!")
def Depositar ():
    print("Para depositar um valor em uma conta, precisaremos de alguns dados\n")
    cpf = input("CPF da conta que deseja depositar: ")
    if os.path.isfile("./users/" + cpf + ".txt"): # Verifica se o usuário existe
        arquivo = open("./users/" + cpf + ".txt", "r")
        conteudo = arquivo.read()
        arquivo.close()
        palavras = conteudo.split()
        for n in range ( len (palavras) ): # Armazena o saldo da conta
            if palavras[n] == "Saldo:":
                saldo = float(palavras[n+1])
                break
        deposito = input("Valor do depósito: ")
        if deposito.replace(".","",1).isdigit(): # Se o valor for inteiro ou decimal, continua com a função
            deposito = float(deposito)
            if deposito > 0:
                saldo = round(saldo + deposito,2)
                DebitarDepositar(cpf, saldo, palavras)
                AtualizarExtrato(cpf, "+", deposito, 0, saldo)
                print("\nO valor foi depositado na conta!")
            else:
                print("\nValor muito baixo!")
        else:
            print("\nValor inválido!")
    else:
        print("\nA conta não existe!")
def MostrarSaldo ():
    print("Para mostrar o saldo, precisaremos de algumas informações\n")
    validado, cpf = ValidarConta()
    if validado == True: # Se o cpf e a senha forem validados, ele prossegue com a função
        arquivo = open("./users/" + cpf + ".txt", "r")
        conteudo = arquivo.read()
        arquivo.close()
        palavras = conteudo.split()
        for n in range ( len (palavras) ): # Armazena o saldo da conta
            if palavras[n] == "Saldo:":
                saldo = float(palavras[n+1])
                break
        print ("\nSeu saldo é de: R$%.2f" % saldo)
def Extrato ():
    print("Para mostrar o extrato, precisaremos de algumas informações\n")
    validado, cpf = ValidarConta()
    if validado == True: # Se o cpf e a senha forem validados, ele prossegue com a função
        arquivo = open("./extratos/Extrato_" + cpf + ".txt","r")
        conteudo = arquivo.read()
        arquivo.close()
        os.system("cls") or None
        print("_______________________________ Extrato _______________________________\n" + conteudo)
# Função Menu
def main ():
    while True:
        input("Aperte 'ENTER' para continuar")
        os.system("cls") or None # Limpa o terminal para não ficar muito poluído
        print("1 - Criar nova conta\n2 - Apagar conta\n3 - Debitar\n4 - Depositar\n5 - Saldo\n6 - Extrato\n0 - Sair")

        opcao = int(input("Escolha uma das opções: "))

        if opcao == 1:
            os.system("cls") or None
            NovaConta()
        elif opcao == 2:
            os.system("cls") or None
            ApagarConta ()
        elif opcao == 3:
            os.system("cls") or None
            Debitar ()
        elif opcao == 4:
            os.system("cls") or None
            Depositar ()
        elif opcao == 5:
            os.system("cls") or None
            MostrarSaldo ()
        elif opcao == 6:
            os.system("cls") or None
            Extrato ()
        elif opcao == 0:
            break
        else:
            print("Opção Inválida!")
            break
os.system("cls") or None
print("Informações importantes:\n\nDigitar o CPF sem '.'\nA senha é apenas numérica e não tem limite de caracteres\nNosso banco oferece 3 tipos de conta: Salário, Comum e Plus")
main()