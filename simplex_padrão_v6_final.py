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
num_excesso = 0
num_folga = 0

# Variáveis de acesso aos arquivos que serão utilizados por este programa
sc50b = "C:\TCC_BIA\SIMPLEX\Arquivos csv\Problemas beatriz - SC50B(50x78).csv"
afiro = "C:\TCC_BIA\SIMPLEX\Arquivos csv\Problemas beatriz - AFIRO(27x51).csv"
km3 = "C:\TCC_BIA\SIMPLEX\Arquivos csv\Problemas beatriz - KM3 (3x3).csv"
km10 = "C:\TCC_BIA\SIMPLEX\Arquivos csv\Problemas beatriz - KM10 (10x10).csv"


# Variável responsável por identificar se é
# uma função de Maximização ou Minimização
# True para Minimização, e False para Maximização
funcao_objetiva = True

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


# Função para preenchimento dos vetores a partir do arquivo lido
def preenche_Vetores():
    # Garante que serão utilizadas as variáveis globais
    global A, b, c, I, num_folga

    # Variáveis que controlam qual vetor será preenchido
    preenche_A = False
    preenche_b = False
    preenche_c = False

    # Abertura do arquivo selecionado
    with open(km10) as file:
        # Contador de quantidade de variáveis presentes no problema
        num_var = 0

        # Laço que percorre o arquivo linha por linha
        for line in file:
            # Variável auxiliar para preencher os vetores
            aux = []

            # Verifica se encontrou a primeira linha do vetor 'A'
            # Se isso ocorre, indica que 'A' será preenchida e garante que
            # 'b' e 'c' não serão utilizadas
            if 'A' in line[0]:
                preenche_A = True
                preenche_b = False
                preenche_c = False

            # Verifica se encontrou a primeira linha do vetor 'b'
            # Se isso ocorre, indica que 'b' será preenchida e garante que
            # 'A' e 'c' não serão utilizadas
            if 'b' in line[0]:
                preenche_A = False
                preenche_b = True
                preenche_c = False

            # Verifica se encontrou a primeira linha do vetor 'c'
            # Se isso ocorre, idica que 'c' será preenchida e garante que
            # 'A' e 'b' não serão utilizadas
            if 'c' in line[0]:
                preenche_A = False
                preenche_b = False
                preenche_c = True

            # Remove os símbolos da linha(Como o '\n') e a transforma em um vetor
            # Para que possam ser utilizados cada um dos elementos por vez
            l = line.strip()
            l = l.split(',')

            # Se for uma linha da tabela 'A', preenche a auxiliar
            # com os elementos a partir da posição 1, uma vez que
            # a posição 0 contém o indicador da tabela ou estará vazia
            # E em seguida preenche 'A' com a auxiliar
            if preenche_A == True:
                for i in range(1, len(l)):
                    aux.append(float(l[i]))
                A.append(aux)

            # Se for uma linha da tabela 'b', preenche a 'b' com
            # os elementos a partir da posição 1, uma vez que
            # a posição 0 contém o indicador da tabela ou estará vazia
            if preenche_b == True:
                b.append(float(l[1]))

            # Se for uma linha da tabela 'c', preenche a 'c' com os
            # elementos a partir da posição 1, uma vez que
            # a posição 0 contém o indicador da tabela ou estará vazia
            # Em seguida indica que há uma nova variável
            # e determina o nome da variável na 'linha_nome_variaveis'
            # para a contrução do Tableau mais adiante
            if preenche_c == True:
                c.append(float(l[1]))
                num_var += 1
                linha_nome_variaveis.append('x' + str(num_var))
        
    # Preenche a matriz Identidade ('I') com 0 no seu tamanho final
    for i in range(0, len(A)):
        I_aux = []
        for j in range(0, len(A)):
            I_aux.append(0)
        I.append(I_aux)

    # Substitui o 0 por 1 na posição relacionada àquela variável de folga
    for i in range(0, len(A)):
        linha_nome_variaveis.append('f' + str(i + 1))
        num_folga += 1
        for j in range(0, len(A)):
            if i == j:
                I[i][j] = 1

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
    
    # Apresenta a primeira forma do Tableau
    apresentar_Tableau(0);

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
preenche_Vetores()
# Verifica o tamanho das matrizes
# Confere a quantidade de entradas
if ((len(A) - len(b)) == 0 and (len(A[0]) - len(c)) == 0):
    # Função para montar Matriz Tableau
    montar_Tableau();
    # Função para fazer o teste da otimalidade
    teste_Otimalidade();
    # Apresentar Resultados (Valor das variáveis e resultado da função objetiva)
    apresentar_Resultados()
