#Listas utilizadas:
lista_potencias = [3, 9, 27, 81, 243, 729, 2187, 6561, 19683, 59049]
restos = [3, 5, 7, 11, 13, 17, 25, 37, 50, 62, 75, 87, 100]

#Listas auxiliares:
restos_chutados, numeros_chutados, numeros_corretos, potencias_chutadas = [], [], [], []

#Flags:
modo_potencia, modo_resto, modo_intervalo, buscando_bordas, tem_resto, bateu_maior = False, False, False, False, False, False

#Contadores:
contador_intervalo, contador_restos, contador_divisor = 1, 1, 0

#Variáveis que salvam valores relevantes:
chao, teto, meio_intervalo, possivel_chao, possivel_teto = 0, 0, 0, 0, 0

def verificador(num=0):
    """Verifica se um int é maior, igual ou menor ao número mais próximo que pertence à regra.

    Parâmetros:
        num -- int a ser verificado, o qual deve ser um número que já foi chutado. Por padrão ('verificador()'), verifica o último número chutado.

    Retorna:
        "maior" -- se o número verificado é menor que o número mais próximo que pertence à regra.
        "menor" -- se o número verificado é maior que o número mais próximo que pertence à regra.
        "igual" -- se o número verificado pertence à regra.
    """
    if num == 0:
        return respostas[-1][1]
    else:
        ind = numeros_chutados.index(num)
        return respostas[ind][1]

def regra_das_potencias():
    """Responsável por determinar a regra da potência a partir das potências perfeitas de base 3. 

    A função é chamada somente se 1 pertence à regra. Então, chuta até a nona potência perfeita de 3 até que uma pertença à regra; nesse caso, imediatamente chuta a regra da potência na forma ["pot", p, 999], sendo 'p' o tamanho da lista das potências chutadas (que coincide com o logaritmo na base 3 do último número chutado). Se nenhuma das potências chutadas pertencer à regra, chuta a regra ["pot", 10, 999], alterando o modo de player de 'potências' para 'resto' ou encerrando o jogo (se, de fato, a regra for da potência perfeita de ordem 10).

    Retorna:
        tipo_chute -- "NUMBER" (se o chute for de uma potência de dois), ou; "RULE" (se o chute for de regra).
        chute -- Uma potência de dois a ser chutada (se tipo_chute == "NUMBER"), ou; a regra da potência a ser chutada (se tipo_chute == "RULE"). 
    """

    # Se uma potência pertencer à regra, chuta a regra (ps: se 3 pertencer à regra, muda de modo para intervalo).
    if len(potencias_chutadas) != 0 and verificador(potencias_chutadas[-1]) == "igual":
        tipo_chute = "RULE"
        chute = ["pot", len(potencias_chutadas), 999]
        if len(potencias_chutadas) == 1:
            chute = ["pot", 10, 999]

    # Se nenhuma das potências pertencer à regra, chuta a potência de 3 (começando da primeira e indo até a nona).
    if len(lista_potencias) == 10 or verificador(potencias_chutadas[-1]) != "igual":#atencao cuidado erro
        chute = lista_potencias[0] 
        potencias_chutadas.append(chute)
        lista_potencias.pop(0)
        tipo_chute = "NUMBER"

    # Se todas as potências foram chutadas e nenhuma pertenceu à regra, chuta para trocar de modo.
    if len(lista_potencias) == 0 and len(regras) == 0:
        tipo_chute = "RULE"
        chute = ["pot", 10, 999]

    return tipo_chute, chute

def acha_divisor():
    """Encontra o divisor 'k' da regra do resto a partir do primeiro resto 'r' (ou seja, do menor 'n' que pertence à regra, tal que n % k = r = n).

    A função passa a ser chamada dentro da função 'modo_resto' após que o primeiro resto 'r' for encontrado. Então, chuta todos os números a partir de 2r, aumentando em duas unidades a cada vez que tal função for convocada até que o segundo valor 'q' (ou seja, o segundo menor 'n' que pertence à regra, tal que n % k = q = k+r) seja encontrado (e diminuindo em uma unidade caso passe desse valor). Assim que o segundo valor 'q' for encontrado, chuta a regra ["mod", q - r, r]. Vale ressaltar que, se o divisor encontrado 'k' é múltiplo do primeiro resto 'r', temos que suposto primeiro resto 'r' é o divisor 'k', e o resto, na realidade, é 0, chutando assim ["mod", r, 0].
    
    Retorna:
        tipo_chute -- "NUMBER" (se for um chute de número), ou; "RULE" (se for um chute de regra)
        chute -- Um inteiro a partir de 2r (se tipo_chute == "NUMBER"), aumentado em uma unidade a cada vez que a função for chamada, ou; uma regra (se tipo_chute == "RULE").
    """
    global contador_divisor, valor_resto, bateu_maior

    # Na primeira vez que a função for convocada, chuta o dobro do valor resto e adiciona 1 no contador.
    if numeros_chutados[-1] == valor_resto:
        tipo_chute = "NUMBER"
        chute = 2*valor_resto
        contador_divisor += 1
    
    # Se não for a primeira vez e o chute for correto, chuta a regra com 'k' e 'r' conforme a documentação.
    elif verificador() == "igual":
        tipo_chute = "RULE"
        chute = ["mod", numeros_chutados[-1] - valor_resto, valor_resto]
        # Caso do resto 0, se 'k' = '2r', chutando a regra apontada na documentação.
        if numeros_chutados[-1] - valor_resto == valor_resto:
            chute = ["mod", valor_resto, 0]

    # Se não for a primeira vez e o chute for maior ou menor que o número mais próximo, chuta de 2 em 2 até que seja correto.
    elif verificador() == "menor":
        if bateu_maior == False:
            tipo_chute = "NUMBER"
            chute = 2*valor_resto + contador_divisor
            contador_divisor += 2
            if chute > 101:
                tipo_chute = "RULE"
                chute = ["mod", valor_resto, 0]
        else:
            tipo_chute = "RULE"
            chute = ["mod", numeros_chutados[-1] - valor_resto - 1, valor_resto]

    else:
        tipo_chute = "NUMBER"
        chute = 2*valor_resto + contador_divisor
        contador_divisor += 2
        if bateu_maior == False:
            bateu_maior = True

    return tipo_chute, chute 

def regra_do_resto():
    """Determina a regra do resto a partir de chutes consecutivos de valores ideais para encontrar o primeiro resto 'r' (ou seja, do menor 'n' que pertence à regra, tal que n % k = r = n).

    A função é chamada se 1 não pertencer à regra ou se o jogo não foi finalizado após o primeiro chute de regra feito em 'regra_das_potencias'. Então, chuta números pertencentes à lista 'restos', que contém valores ideais de chutes de números para que se encontre o primeiro resto 'r'. Se tal lista é finalizada e nenhum dos valores é maior do que o número mais próximo pertencente à lista (ou seja, se nunca é retornado 'menor' pelo jogo em 'rule_guesses'), então chuta a regra ["mod", 2, 1] e ativa o modo intervalo. Se um dos valores for maior do que o número mais próximo pertencente à lista, então faz-se uma busca binária até que se encontre um valor que pertença à lista; este será o primeiro resto 'r'. Então, com ele, chama-se a função 'acha_divisor', que encontra o divisor 'k' da regra do resto e chuta a regra do resto.

    Retorna:
        tipo_chute -- "NUMBER" (se for um chute de número), ou; "RULE" (se for um chute de regra).
        chute -- int elaborados a partir da lista inicial.
    """
    global tipo_chute, contador_restos, tem_resto, valor_resto, contador_divisor

    #Caso não tenha valores pertencentes à regra menores que 100, sabemos que não é regra do resto; chutamos uma regra para mudar de modo.
    if len(restos) == 0 and verificador(restos_chutados[-1]) == "maior":   
        tipo_chute = "RULE"
        chute = ["mod", 2, 1]

    # Chuta os primeiro item da lista de números verificadores de resto. Caso em algum momento o mais próximo seja menor, sabemos que provavelmente é um resto.
    if len(restos) == 13 or (verificador(restos_chutados[-1]) == "maior" and len(restos) > 0):
        tipo_chute = "NUMBER"
        chute = restos[0]
        restos_chutados.append(restos[0])
        restos.pop(0)

    elif verificador() != "maior":
        if contador_restos == 1 and tem_resto == False:
            tem_resto = True
    
    if tem_resto:
        if contador_divisor == 0:
            # Busca binaria para achar o valor pertencente à regra.
            if verificador() == "menor":
                if int(numeros_chutados[-1]/2**contador_restos) > 1:
                    chute = numeros_chutados[-1] - int(numeros_chutados[-1]/2**contador_restos)
                else:
                    chute = numeros_chutados[-1] - 1

            if verificador() == "maior":
                if int(numeros_chutados[-1]/2**contador_restos) > 1:
                    chute = numeros_chutados[-1] + int(numeros_chutados[-1]/2**contador_restos)
                else:
                    chute = numeros_chutados[-1] + 1
        
            contador_restos += 1 

        #Caso tenhamos achado o igual, chama a função 'acha_divisor'.
        if verificador() == "igual" or contador_divisor > 0 or numeros_corretos != []:
            if contador_divisor == 0:
                valor_resto = min(numeros_corretos)
            tipo_chute, chute = acha_divisor()

    return tipo_chute, chute

def busca_bordas():
    """Chamado pelo 'regra_do_intervalo', acha os valores máximo e mínimo do intervalo, após saber do primeiro valor encontrado que pertence ao intervalo.

    Começa buscando o teto do intervalo, chutando de 2 em 2. Após achar, volta para o menor valor conhecido do intervalo e chuta de -2 em -2, buscando o chão.

    Retorna:
        tipo_chute -- "NUMBER" (se for um chute de número), ou; "RULE" (se for um chute de regra)
        chute -- o valor atual da busca (se tipo_chute == "NUMBER") ou; a regra do intervalo, após achar o chão e o teto (se tipo_chute == "RULE").
    """
    global chao, teto, buscando_bordas, meio_intervalo, modo_intervalo, possivel_chao, possivel_teto
    tipo_chute = "NUMBER"


    #Caso o chão e o teto ainda não tenham sido achados, busca de 2 em 2.
    if chao == 0 or teto == 0:

        if teto == 0:

            if possivel_teto == 0:
                if verificador() == "igual":
                    # Ainda está dentro do intervalo.
                    chute = numeros_chutados[-1] + 2
                    if chute > 100_000:
                        chute = 100_000
                else:
                    # Saiu do intervalo, chuta o de baixo pra verificar possível teto.
                    possivel_teto = numeros_chutados[-1]
                    chute = numeros_chutados[-1] - 1
            
            else:
                # Após ter chutado o de baixo, verifica o resultado e atribui o teto.
                if verificador() == "igual":
                    teto = possivel_teto - 1
                else:
                    teto = possivel_teto - 2
                # Prepara o chute para achar o chão.
                chute = meio_intervalo - 1

        
        elif chao == 0:

            if possivel_chao == 0:
                if verificador() == "igual":
                    # Ainda está dentro do intervalo.
                    chute = numeros_chutados[-1] - 2
                    if chute < 1:
                        chute = 1
                else:
                    # Saiu do intervalo, chuta o de baixo pra verificar possível chão.
                    possivel_chao = numeros_chutados[-1]
                    chute = numeros_chutados[-1] + 1
            else:
                # Após ter chutado o de cima, verifica o resultado e atribui o chão.
                if verificador() == "igual":
                    chao = possivel_chao + 1
                else:
                    chao = possivel_chao + 2

    # Casos de borda.
    if 100_000 in numeros_chutados and verificador(100_000) == "igual":
        teto = 100_000
    if 1 in numeros_chutados and verificador(1) == "igual":
        chao = 1
    
    if chao != 0 and teto != 0:
        #Caso tenha achado o chão e o teto, chuta a regra.
        tipo_chute = "RULE"
        chute = ["int", chao, teto]
    
    return tipo_chute, chute

def regra_do_intervalo():
    """Responsável por achar os valores do intervalo. Realiza uma busca binária para encontrar algum valor pertencente, e, após, chama a função 'busca_bordas()' para encontrar os valores máximo e mínimo.

    É chamada após a regra da potência e do resto serem descartadas. De começo, chuta 50_000 e inicia uma busca binária. Ao encontrar um valor que satisfaz a regra, passa a chamar a função 'busca_bordas()'. 
    
    Retorna:
        tipo_chute -- "NUMBER" (se for um chute de número), ou; "RULE" (se for um chute de regra)
        chute -- o valor atual da busca (se tipo_chute == "NUMBER") ou; a regra do intervalo, após achar o chão e o teto (se tipo_chute == "RULE").
    """
    global chao, teto, buscando_bordas, meio_intervalo, modo_intervalo, possivel_chao, possivel_teto
    tipo_chute = "NUMBER"

    # Caso ainda não tenha sido achado nenhum valor que esteja na regra.
    if not buscando_bordas:
        # Define o primeiro chute como 50_000
        if contador_intervalo == 1:
            chute = 50_000
        
        # Caso ainda não tenha sido achado um número que esteja na regra, faz busca binária.
        elif verificador() != "igual":
            if verificador() == "menor":
                if (100_000/(2**contador_intervalo)) > 1:
                    chute = int(numeros_chutados[-1] + (-1)*(100_000/(2**contador_intervalo)))
                else:
                    chute = numeros_chutados[-1] - 1
            else:
                if (100_000/(2**contador_intervalo)) > 1:
                    chute = int(numeros_chutados[-1] + (100_000/(2**contador_intervalo)))
                else:
                    chute = numeros_chutados[-1] + 1

        else:
            # Achado um valor dentro da regra, salva o número e inicia a busca por bordas.
            meio_intervalo = numeros_chutados[-1]
            buscando_bordas = True
        
    if buscando_bordas:
        tipo_chute, chute = busca_bordas()
    
    return tipo_chute, chute

def player(number_guesses, rule_guesses):
    """Função entregue pelo projeto que efetivamente joga o jogo.

    A partir de flags (valores booleanos que trocam de False para True quando necessário), a função player convoca outras funções (que estão acima) para desenvolver tanto chutes de regras quanto de números. Inicialmente, chutamos o número 1. Se 1 pertence à regra, convoca a função 'regra_das_potências'. Se 1 não pertencer à regra ou se a 'regra_da_potência' não foi capaz de acertar a regra, 'player' chama a função 'regra_do_resto'. Se tal função não foi capaz de acertar a regra, por fim, é convocada a função 'regra_do_intervalo'. Vale ressaltar que, a cada chute de número, salvamos o número chutado na lista 'numeros_chutados'; e, que, a cada chute de número correto, salvamos tal valor na lista 'numeros_corretos'.

    Parâmetros:
        number_guesses -- Lista de listas que indicam as respostas para os chutes numéricos anteriores. Chamamos-a de 'respostas' globalmente.
        rule_guesses -- Lista de respostas aos chutes de regras anteriores. Chamamos-a de 'regras' globalmente.

    Retorna:
        tipo_chute -- "NUMBER" (se for um chute de número), ou; "RULE" (se for um chute de regra).
        chute -- Um int (se for um tipo_chute == "NUMBER"), ou; uma lista (se tipo_chute == "RULE").
    """

    global respostas, regras, modo_intervalo, modo_potencia, modo_resto, contador_intervalo, numeros_corretos

    regras, respostas = rule_guesses, number_guesses

    tipo_chute = "NUMBER"

    # Se o número pertencer à regra, salvamos seu valor na lista 'números corretos'.
    if respostas != []:
        if verificador() == "igual":
            numeros_corretos.append(numeros_chutados[-1])

    # Se ainda nenhum número foi chutado, chutamos o número 1.
    if respostas == []:
        tipo_chute = "NUMBER"
        chute = 1

    # Se o número 1 pertencer à regra e nenhum outro modo estiver ativo, ativamos o modo potência.
    elif (respostas[0][2] == True) and (modo_resto == False) and (modo_intervalo == False):
        modo_potencia = True

    # Se o modo intervalo não estiver ativo ou as condições acima não forem atendidas, ativa o modo resto.
    elif (modo_intervalo == False):
        modo_resto = True

    # Se houve um chute e o modo intervalo não está ativo, ativa o modo resto.
    if regras != [] and modo_intervalo == False:
            modo_resto = True
            modo_potencia = False 

    # Caso o modo esteja ativado, chama sua função respectiva para o chute.
    if modo_potencia == True:
        tipo_chute, chute = regra_das_potencias()

    if modo_resto == True:
        tipo_chute, chute = regra_do_resto()
    
    if len(regras) >= 2 and len(restos) == 0 or (len(regras) >= 3):
        modo_intervalo = True
        modo_resto = False
        modo_potencia = False

    if modo_intervalo == True:
        tipo_chute, chute = regra_do_intervalo()
        contador_intervalo += 1
        
    # Toda vez que chutar, adiciona o valor em 'numeros_chutados'.
    if tipo_chute == "NUMBER":
        numeros_chutados.append(chute)     
        
    return [tipo_chute, chute]
