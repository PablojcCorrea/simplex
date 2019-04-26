"""
    Método Simplex - Implementação baseada na implementação
    do professor Thiago.
"""

"""
    Definição de variáveis globais
"""
"""
    Primeiro Exemplo (TCC da Bia):
        Função Objetiva - Maximização:
            Z = 50x1 + 40x2
            S.A 2x1 + 0x2 <= 300
                0x1 + 3x2 <= 540
                2x1 + 2x2 <= 440
                6/5x1 + 3/2x2 <= 300
        Solução Ótima = 10300
        Iterações: 2
"""

# Remover dos comentários a inicialização das variáveis do exemplo 1

# Vetor que representa os coeficientes das inequações das restrições
A = [(2, 0), (0, 3), (2, 2), (6/5, 3/2)]
# Vetor que representa o limite das restrições
b = [300, 540, 440, 300]
# Vetor que representa os custos da função objetiva
c = [50, 40]
# Variável responsável por identificar se é
# uma função de Maximização ou Minimização
# True para Minimização, e False para Maximização
funcao_objetiva = False


"""
    Segundo Exemplo:
        Função Objetiva - Minimização:
            Z = 1x1 + 2x2
            S.A -2x1 + 1x2 <= 2
                -1x1 + 2x2 <= 7
                1x1 + 0x2 <= 3
        Solução Ótima = 13
        Iterações: 3
"""

# Remover dos comentários a inicialização das variáveis do exemplo 2
"""
# Vetor que representa os coeficientes das inequações das restrições
A = [(-2, 1), (-1, 2), (1, 0)]
# Vetor que representa o limite das restrições
b = [2, 7, 3]
# Vetor que representa os custos da função objetiva
c = [-1, -2]
# Variável responsável por identificar se é
# uma função de Maximização ou Minimização
# True para Minimização, e False para Maximização
funcao_objetiva = True
"""

# Inicia vetor para criar o Tableau
Tableau = []


"""
    Funções do Programa
"""

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
    cont_int = 0
    
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
            
            for i in range(0, len(Tableau[0]) - 1):
                if Tableau[0][i] < menor_custo:
                    menor_custo = Tableau[0][i]
                    coluna_pivo = i
            if menor_custo >= 0:
                otimo = True
            else:
                linha_pivo, menor_valor = teste_Razao(coluna_pivo)
                if menor_valor > 9999:
                    print("Problema Ilimitado")
                    break
                # Chama função de atualização do Tableau
                # Passa como parâmetros a posição do pivo
                atualizacao_Tableau(linha_pivo, coluna_pivo)
                cont_int += 1
            

    # Se 'otimo' for True, sai do laço, indica que a solução atual é ótima
    # e apresenta a matriz Tableau
    if otimo == True:
        print("A Solução atual é ótima")
        print("Solução encontrada em: ", cont_int)
        for linha in Tableau:
            print(linha)
    
def montar_Tableau():
    # Declarar uso de variável global
    global Tableau
    # Preenche Tableau com 0
    for i in range(0, len(A) + 1):
        linha = []
        for j in range(0, len(A) + len(c) + 1):
            linha.append(0)
        Tableau.append(linha)
    """
    Teste (Remova este comentário para apresentar o Tableau preenchido):
    for linha in Tableau:
        print(linha)
    """

    # Verificar se é um problema de Maximização ou de Minimização
    if funcao_objetiva == False:
        # Se for de maximização, multiplique por -1
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
    for i in range(1, len(Tableau)):
        Tableau[i][pos] = 1
        pos += 1
        
    # pos será iniciada com a ultima posição da linha (Última coluna do Tableau)
    pos = len(Tableau[0]) - 1
    # Preenchimento do Tableau com a matriz 'b'
    for i in range(0, len(b)):
        Tableau[i+1][pos] = b[i]
        
"""
    Programa Principal
"""
# Verifica o tamanho das matrizes
# Confere a quantidade de entradas
if ((len(A) - len(b)) == 0 and (len(A[0]) - len(c)) == 0):
    # Função para montar Matriz Tableau
    montar_Tableau();
    # Função para fazer o teste da otimalidade
    teste_Otimalidade();
