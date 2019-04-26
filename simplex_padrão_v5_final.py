from fractions import Fraction
from decimal import Decimal

linha_nome_variaveis = ['-']
coluna_base = []
Tableau = []

A = []
b = []
c = []
I = []

num_artificiais = 0
num_folga = 0
num_excesso = 0

# Variável para armazenar a expressão da função objetiva
exp_funcao_objetiva = ""
# Vetor para armazenar as expressões das restrições
exp_restricoes = []

# Variável responsável por identificar se é
# uma função de Maximização ou Minimização
# True para Minimização, e False para Maximização
funcao_objetiva = False

# Verifica o tamanho das matrizes
# Confere a quantidade de entradas
# if ((len(A) - len(b)) == 0 and (len(A[0]) - len(c)) == 0):

        
# Função que apresenta cada iteração do Tableau
def apresentar_Tableau(cont):
    # Apresenta qual iteração será apresentada
    print("Iteração número: ", cont)
    # Cria uma matriz local para receber os valores presentes no Tableau para serem apresentados
    # e garantir que o tipo de cada elemento não será alterado no Tableau original
    tableau_apresentacao = []

    # Para o Tableau de apresentação, coloca um cabeçalho com os nomes das variáveis preenchidas anteriormente
    tableau_apresentacao.append(linha_nome_variaveis)

    # Laço para preencher o Tableau de paresentação
    for i in range(0, len(Tableau)):
        # Inicializa uma matriz auxiliar para construir as linhas do Tableau de apresentação
        linha_tableau_apresentacao = []
        # Coloca como primeiro elemento da linha o nome da variável presente na base nesta iteração
        linha_tableau_apresentacao.append(coluna_base[i])
        # Laço para o restante da linha com os valores
        for j in range(0, len(Tableau[0])):
            # Armazena o valor atual em uma variável auxiliar 'aux'
            aux = Tableau[i][j]
            # Transforma em fração todos os valores
            dividendo = Fraction(Decimal(str(aux))).numerator
            divisor = Fraction(Decimal(str(aux))).denominator
            # Se o divisor da fração for igual a '1', armazena apenas o valor do dividendo
            if divisor == 1:
                valor = str(dividendo)
            # Se o divisor for diferente de '1', armazena o valor em forma de fração
            else:
                # valor = str(dividendo) + '/' + str(divisor)
                valor = round(dividendo / divisor, 1)
            # Armazena o valor na linha do Tableau de apresentação
            linha_tableau_apresentacao.append(valor)
        # Armazena a linha no Tableau de apresentação
        tableau_apresentacao.append(linha_tableau_apresentacao)
    # Laço que apresenta o Tableau
    for linha in tableau_apresentacao:
        print(linha)
    print()    

def atualizacao_Tableau(lin, col):
    # Divide a linha do pivo pelo valor do pivo
    valor_pivo = Tableau[lin][col]
    for j in range(0, len(Tableau[0])):
        Tableau[lin][j] = Tableau[lin][j] / valor_pivo

    # Zerar os demais valores da coluna do pivo
    for i in range(0, len(Tableau)):
        valor_coluna_pivo = Tableau[i][col]
        for j in range(0, len(Tableau[0])):
            if i != lin:
                Tableau[i][j] = Tableau[i][j] - Tableau[lin][j] * valor_coluna_pivo

def teste_Razao(pos):
    # Matriz auxiliar para seleção do pivo
    matriz_pivo = []
    # Preenchimento da matriz com 0
    for i in range(0, len(A)):
        matriz_pivo.append(0)
    # Divide a coluna referente a matriz 'b' pela coluna selecionada como menor custo
    for i in range(0, len(matriz_pivo)):
        # Efetua a divisão se o valor da coluna de menor custo for maior que zero
        if Tableau[i+1][pos] > 0:
            matriz_pivo[i] = Tableau[i+1][len(Tableau[0]) - 1] / Tableau[i + 1][pos]
        # Garante que os valores menores ou iguais a zero não sejam selecionados como pivo
        else:
            matriz_pivo[i] = 10000
    # Define valor 0 para inicializar a posição do pivo
    pivo = 0
    # Define o primeiro elemento da matriz_pivo como o menor valor
    menor_valor = matriz_pivo[0]
    # Verifica e seleciona o menor valor e sua posição
    for i in range(0, len(matriz_pivo)):
        if matriz_pivo[i] < menor_valor:
            menor_valor = matriz_pivo[i]
            pivo = i
    # Retorna a posição do pivo somando 1, pois deve ignorar a linah de custo
    return pivo + 1, menor_valor

def teste_Otimalidade():
    # Variável que garante a buscar a solução ótima
    otimo = False
    # Variável para contar o número de iterações do simplex
    cont = 0
    
    while otimo == False:
        # Para cada iteração
        # Verifica se há algum valor negativo presente na função objetiva
        for j in range(0, len(Tableau[0])):
            # Verifica se todos os valores são positivos para garantir otimalidade
            if Tableau[0][j] >= 0:
                otimo = True
            # Se houver valor negativo indica que a 'otimo' como False
            elif Tableau[0][j] < 0:
                otimo = False
                break
                
        # Se 'otimo' for False, continua a busca pela solução ótima
        if otimo == False:
            # menor_custo representa o menor valor na função objetiva
            menor_custo = Tableau[0][0]
            # coluna_pivo representa a posição da coluna com o menor custo
            coluna_pivo = 0
            # Laço que percorre as colunas do Tableau
            # Verficando qual é o menor valor presente na linha de custo
            # E armazena qual a posição da coluna pivo
            for j in range(0, len(Tableau[0]) - 1):
                if Tableau[0][j] < menor_custo:
                    menor_custo = Tableau[0][j]
                    coluna_pivo = j
            # Verifica se o menor valor na linha de custo é maior ou igual a zero
            # Pois se isso ocorrer, significa que a solução já é ótima
            if menor_custo >= 0:
                otimo = True
            else:
                # Armazena qual é a linha do pivo e quem é o pivo ('menor_valor')                
                linha_pivo, menor_valor = teste_Razao(coluna_pivo)
                #                 
                coluna_base[linha_pivo] = linha_nome_variaveis[coluna_pivo + 1]
                if menor_valor > 9999:
                    print("Problema Ilimitado")
                    break
                # Chama função de atualização do Tableau
                # Passa como parâmetros a posição do pivo
                atualizacao_Tableau(linha_pivo, coluna_pivo)
                # apresentar_Tableau();
                cont += 1
                apresentar_Tableau(cont);

    # Se 'otimo' for True, sai do laço, indica que a solução atual é ótima
    # e apresenta a matriz Tableau
    if otimo == True:
        print("A Solução atual é ótima")
        print("Solução encontrada em: ", cont, "iterações")


def func_BigM(valor):
    # Laço para percorrer todas as linhas do Tableau
    for i in range(1, len(Tableau)):
        # Verifica se a linha e referente a uma variável artificial
        if 'a' in coluna_base[i]:
            # Percorre toda a linha daquela artificial
            for j in range(0, len(Tableau[0])):
                # Multiplica toda a linha pelo valor do 'Big M', e subtrai a linha de custo
                # Com isso, zera o 'Big M', formando uma base Identidade
                Tableau[0][j] = Tableau[0][j] - valor * Tableau[i][j]
                
def montar_Tableau():
    # Declarar uso de variável global
    global Tableau
    # Preenche Tableau com 0
    for i in range(0, len(A) + 1):
        linha = []
        for j in range(0, len(c) + num_artificiais + num_folga + num_excesso + 1):
            linha.append(0)
        Tableau.append(linha)

    # Verificar se é um problema de Maximização ou de Minimização
    if funcao_objetiva == False:
        # Se for de maximização (False), multiplique por -1
        for i in range(0, len(c)):
            c[i] *= -1
        print("Função objetiva colocada na forma padrão")
    else:
        # Se for de minimização a função já está na forma padrão
        print("Função objetiva na forma padrão")
        
    # Preenche Tableau com matrizes 'A', 'b' e 'c'
    # Matriz 'c' (Linha dos custos / função objetiva)
    for i in range(0, len(c)):
        Tableau[0][i] = c[i]
    # Preenche Tableau com 'A', 'b' e a Matriz Identidade ('I')
    
    # Preenchimento do Tableau com a matriz 'A'
    for i in range(0, len(A)):
        for j in range(0, len(A[i])):
            Tableau[i+1][j] = A[i][j]
            
    # pos é uma variável para controlar a posição inicial para preenchimento
    # com a matriz identidade 'I'
    pos = len(c)
    # Preenchimento do Tableau com a matriz identidade 'I'
    for j in range(len(c), len(Tableau[0]) - 1):
        for i in range(1, len(Tableau)):
            Tableau[i][j] = I[j-len(c)][i - 1]

    
    # pos será iniciada com a ultima posição da linha (Última coluna do Tableau)
    pos = len(Tableau[0]) - 1
    linha_nome_variaveis.append('RHS')
    # Preenchimento do Tableau com a matriz 'b'
    for i in range(0, len(b)):
        Tableau[i+1][pos] = b[i]
    # Coloca 'Z' como primeiro item da coluna base
    coluna_base.append('Z')
    # Cria um laço para adicionar as variáveis que entram na base
    for i in range(len(c) + 1, len(linha_nome_variaveis) - 1):
        if 'e' not in linha_nome_variaveis[i]:
            coluna_base.append(linha_nome_variaveis[i])
    # Verifica se há variáveis artificiais, que serão zeradas pelo método Big M
    if num_artificiais > 0:
        maior_valor = 0
        aux = 0
        # Laço que percorre os elementos da linha de custo para encontrar o maior valor
        for i in range(len(c)):
            # Verifica se o valor é negativo, se for negativo torna-o positivo
            # e o armazena na variável auxiliar
            if c[i] < 0:
                aux = c[i] * -1
            # Se o valor for positivo, apenas o armazena em 'aux'
            else:
                aux = c[i]
            # Verifica se o valor atual é o maior valor e o seleciona como maior valor
            if aux > maior_valor:
                maior_valor = aux
        # Multiplica o maior valor por 100, para garantir que teremos um valor "M" muito grande
        maior_valor = maior_valor * 100
        # Laço que percorre a linha de custos, verificando qual coluna é
        # referente as variáveis artificiais para serem substituidas
        # pelo valor 'M' ('maior_valor')
        for j in range(0, len(Tableau[0]) - 1):
            if 'a' in linha_nome_variaveis[j+1]:
                Tableau[0][j] = maior_valor
        # Chama a função do 'Big M', indicando qual é o maior_valor
        func_BigM(maior_valor);
    # Apresenta a primeira forma do Tableau
    apresentar_Tableau(0);

def ler_Expressoes():
    global num_folga, num_excesso, num_artificiais
    global Tableau
    num_var = 0
    # Função para receber expressões algébricas como entrada para o programa
    # Apresenta um exemplo de entrada
    print("Exemplo:")
    print("A seguinte expressão: Z x1 - 4x2 + 3/4x3 - 5/6x4")
    print("Deve ser informada da seguinte forma: 1x_1 - 4x_2 + 3/4x_3 - 5/6x_4")
    print("O coeficiente deve ser separado dos sinais ('+', '-') com espaço (' ')")
    print("")
    # Armazena a expressão informada pelo usuário na variável 'exp_funcao_objetiva'
    exp_funcao_objetiva = input("Informe a expressão da função objetiva: ")
    # Variável auxiliar ('aux') que armazena os elementos da expressão informada
    # separadamente, para conseguir manipular os coeficientes da função objetiva
    aux = exp_funcao_objetiva.split(' ')
    # Na variável auxiliar podem estar contidos os seguintes elementos:
    # Sinais de operação ('+', '-') - Para determinar se o coeficiente será positivo ou negativo
    # Sinais de igualdade('=') e desigualdade ('<=', '>=') - Para determinar o tipo de restrição
    # Coefientes acompanhados da variável ('1x_1', '3x_2', '4/5x_3') - Para serem separados e montar o Tableau

    # Laço que percorre a matriz auxiliar para verificar os elementos da função objetiva
    for i in range(0, len(aux)):
        # Verifica se o elemento atual da matriz é um coeficiente acompanhado por sua variável
        # Para isso verifica se há um '_' presente na string
        if '_' in aux[i]:
            # Fragmenta o elemento, removendo o '_', separando o índice da variável de seu coeficiente
            aux2 = aux[i].split('_')
            # Fragmenta o primeiro elemento (coeficiente + letra)
            # Removendo a letra e armazenando o coeficiente em 'coeff'
            coeff = aux2[0].split('x')
            # Verifica seo coeficiente é um fração
            if '/' in coeff[0]:
                # Se for um fração, separa o dividendo do divisor
                dividendo = Fraction(coeff[0]).numerator
                divisor = Fraction(coeff[0]).denominator
                # Em seguida verifica se o elemento anterior é um sinal de negativo
                if '-' in aux[i -1]:
                    # Se o elemento anterior for um sinal negativo
                    # Transforma o resultado da fração em float e multiplica por '-1'
                    # E em seguida armazena o resultado em 'c'
                    c.append(float(dividendo /divisor) * -1)
                else:
                    # Se o elemento anterior for um sinal de positivo ou não houver sinal
                    # Transforma o resultado da fração em float e armazena o resultado em 'c'
                    c.append(float(dividendo /divisor))
            else:
                # Se não for uma fração, verifica se o elemento anterior é um sinal de negativo
                if '-' in aux[i -1]:
                    # Se for negativo, multiplica por '-1' e transforma o valor em float
                    # E em seguida armazena o resultado em 'c'
                    c.append(float(coeff[0]) * -1)
                else:
                    # Se não for negativo ou não houver sinal, transforma o valor em float
                    # E em seguida armazena o resultado em 'c'
                    c.append(float(coeff[0]))
            num_var += 1
            linha_nome_variaveis.append('x' + str(num_var))
                

    # Apresenta exemplos de restrições
    print("")
    print("Exemplos (Restrições):")
    print("1x_1 + 3/6x_4 >= 100")
    print("- 1x_1 + 3x_4 <= 100")
    print("1x_1 - 3x_4 = 100")

    # Armazena em 'rest' a quantidade de restrições que o o problema possui
    qtd_rest = int(input("Informe a quantidade de restrições:"))
    cont = 1
    num_var_a = 0
    num_var_e = 0
    num_var_f = 0
    # Se a quantidade restrições for maior que zero, entra no laço
    while cont <= qtd_rest:
        # Armazena cada uma das restrições em 'exp_restricoes'
        exp_restricoes.append(input("Informe a restrição:"))
        # Fragmenta o ultimo elemento colocado em 'exp_restricoes' e armazena
        # na variável auxiliar 'aux'
        aux = exp_restricoes[len(exp_restricoes) - 1].split(' ')
        # Cria uma matriz A auxiliar ('A_aux') para ser armazenada como uma linha de 'A'
        A_aux = []
        for i in range(0, len(c)):
            A_aux.append(0)

        # Laço que percorre os elementos presentes em 'aux'
        for i in range(0, len(aux)):
            # Verifica se o elemento atual da matriz é um coeficiente acompanhado por sua variável
            # Para isso verifica se há um '_' presente na string
            if '_' in aux[i]:
                # Fragmenta o elemento, removendo o '_', separando o índice da variável de seu coeficiente
                aux2 = aux[i].split('_')
                # Fragmenta o primeiro elemento (coeficiente + letra)
                # Removendo a letra e armazenando o coeficiente em 'coeff'
                coeff = aux2[0].split('x')
                # Verifica seo coeficiente é um fração
                if '/' in coeff[0]:
                    # Se for um fração, separa o dividendo do divisor
                    dividendo = Fraction(coeff[0]).numerator
                    divisor = Fraction(coeff[0]).denominator
                    # Em seguida verifica se o elemento anterior é um sinal de negativo
                    if '-' in aux[i -1]:
                        # Se o elemento anterior for um sinal negativo
                        # Transforma o resultado da fração em float e multiplica por '-1'
                        # E em seguida armazena o resultado em 'A_aux'
                        A_aux[int(aux2[1]) - 1] = float(dividendo / divisor) * -1
                    else:
                        # Se o elemento anterior for um sinal de positivo ou não houver sinal
                        # Transforma o resultado da fração em float e armazena o resultado em 'A_aux'
                        A_aux[int(aux2[1]) - 1] = float(dividendo /divisor)
                else:
                    # Se não for uma fração, verifica se o elemento anterior é um sinal de negativo
                    if '-' in aux[i -1]:
                        # Se for negativo, multiplica por '-1' e transforma o valor em float
                        # E em seguida armazena o resultado em 'A_aux'
                        A_aux[int(aux2[1]) - 1] = float(coeff[0]) * -1
                    else:
                        # Se não for negativo ou não houver sinal, transforma o valor em float
                        # E em seguida armazena o resultado em 'A_aux'
                        A_aux[int(aux2[1]) - 1] = float(coeff[0])
            # Verifica se não há '_' e se é o último elemento de 'aux'
            elif i == len(aux) - 1:
                # Se a verificação for positiva, transforma o elemento em float e armazena em 'b'
                b.append(float(aux[i]))
        # Variável auxiliar para a contrução da Matriz Identidade
        I_aux = []
        # Verifica se na expressão há um sinal de igualdade, que indica o uso de variáveis artificiais
        if aux[len(aux) - 2] == '=':
            # Aumenta a quantidade de variáveis artificiais em 1
            num_artificiais += 1
            num_var_a += 1
            # Acrescenta o nome da variável na 'linha_nome_variaveis' para futuramente construir o Tableau
            linha_nome_variaveis.append('a' + str(num_var_a))
        # Se não for de igualdade, verifica se é um sinal de "menor igual", para controle das variáveis de folga
        elif aux[len(aux) - 2] == '<=':
            # Aumenta a quantidade de variáveis de folga
            num_folga += 1
            num_var_f += 1
            # Acrescenta o nome da variável na 'linha_nome_variaveis' para futuramente construir o Tableau
            linha_nome_variaveis.append('f' + str(num_var_f))

        # Se não for nenhumas das opções anteriores, verifica se é um sinal de "maior igual" para controle das variáveis de excesso e de folga
        elif aux[len(aux) - 2] == '>=':
            # Auemnta o numero de variáveis de excesso
            num_excesso += 1
            num_var_e += 1
            # Acrescenta o nome da variável na 'linha_nome_variaveis' para futuramente construir o Tableau
            linha_nome_variaveis.append('e' + str(num_var_e))
            # Laço que indica como deve ser montada a matriz identidade, adicionando uma nova coluna e garantindo que o valor '-1' seja colocado na posição correta
            for i in range(0, qtd_rest):
                if i + 1 == cont:
                    I_aux.append(-1)
                else:
                    I_aux.append(0)
            # Adiciona a nova coluna à matriz Identidade
            I.append(I_aux)
            # Reseta a variável auxiliar
            I_aux = []
            # Aumenta o numero de variáveis artificiais
            num_artificiais += 1
            num_var_a += 1
            # Acrescenta o nome da nova variável artificial a 'linha_nome_colunas' para futuramente contruir o Tableau
            linha_nome_variaveis.append('a' + str(num_var_a))
        # Laço que indica como deve ser montada a matriz identidade, adicionando uma nova coluna e garantindo que o valor '1' seja colocado na posição correta
        for i in range(0, qtd_rest):
            if i + 1 == cont:
                I_aux.append(1)
            else:
                I_aux.append(0)
        # Adiciona a nova coluna a matriz Identidade
        I.append(I_aux)

        # Preenche a matriz 'A' com a matriz 'A_aux', criando a linha da restrição
        A.append(A_aux)
        # diminui o valor de 'rest' para indicar quantas restrição faltam ser informadas
        cont += 1


def menu():
    # Indica o uso da variável global 'funcao_objetiva'
    global funcao_objetiva
    # Apresenta as opções do menu
    print("Informe o tipo de função objetiva:")
    print("1 - Minimização")
    print("2 - Maximização")
    print("0 - Encerrrar programa")

    # Armazena a resposta do usuário
    resp = input("Informe a opção desejada: ")

    # Verifica a resposta do usuário
    if resp == '1':
        # Se a resposta for '1' (Minimização) chama a função que lê as expressões
        # e 'funcao_objetiva' recebe o valor lógico 'True'
        ler_Expressoes()
        funcao_objetiva = True
    elif resp == '2':
        # Se a resposta for '1' (Minimização) chama a função que lê as expressões
        # e 'funcao_objetiva' recebe o valor lógico 'False'
        ler_Expressoes()
        funcao_objetiva = False
    else:
        print("Programa encerrado!")
        
def apresentar_Resultados():
    # Verifica quantas variáveis existem na função objetiva
    qtd_var_func_objetiva = len(c) + 1
    # Laço que percorre a lista de nomes de variáveis utilizadas no problema
    for j in range(1,len(linha_nome_variaveis) - 1):
        # Verifica se é a coluna referente a uma variável da função objetiva
        if j < qtd_var_func_objetiva:
            # Atribui a 'valor' o nome da variável
            valor = linha_nome_variaveis[j]
            # E então percorre as linahs do Tableau
            for i in range(1, len(Tableau)):
                # Verifica se a linha é referente a variável da função objetiva
                if coluna_base[i] == valor:
                    # Se for, apresenta o valor da variável que está na base (arredondado)
                    print(valor, ": ", round(Tableau[i][len(Tableau[0]) - 1], 3))
    # Apresenta o resultado da função objetiva (arredondado)
    print("Resultado da função objetiva:", round(Tableau[0][len(Tableau[0]) - 1], 3))

"""
    Programa Principal
"""
menu();
# Verifica o tamanho das matrizes
# Confere a quantidade de entradas
if ((len(A) - len(b)) == 0 and (len(A[0]) - len(c)) == 0):
    # Função para montar Matriz Tableau
    montar_Tableau();
    # Função para fazer o teste da otimalidade
    teste_Otimalidade();
    # Apresentar Resultados (Valor das variáveis e resultado da função objetiva)
    apresentar_Resultados()
