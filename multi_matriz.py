import requests
import numpy as np


def melhor_ordem(lista_matrizes):
    """Calcula a matriz com melhor forma de multiplicar."""
    if len(lista_matrizes) > 2:
        dim = []
        for index in range(0, len(lista_matrizes)):
            # Gera a lista com as dimensoes das matrizes
            if index == 0:
                dim.append(lista_matrizes[index]['linhas'])
                dim.append(lista_matrizes[index]['colunas'])
            else:
                dim.append(lista_matrizes[index]['colunas'])

        n_dim = len(dim)
        matriz_temp = []
        matriz_saida = []

        for i in range(0, n_dim):
            matriz_saida.append([0 for _ in range(0, n_dim)])
            matriz_temp.append([0 for _ in range(0, n_dim)])

        # Calcula a matriz saida
        for d in range(1, n_dim):
            for i in range(1, n_dim - d):
                j = i + d
                for k in range(i, j):
                    q = matriz_temp[i][k] + matriz_temp[k + 1][j] +\
                        dim[i - 1] * dim[k] * dim[j]
                    if matriz_temp[i][j] == 0 or q < matriz_temp[i][j]:
                        matriz_temp[i][j] = q
                        matriz_saida[i][j] = k
        return matriz_saida

    return None


def array_ordem_mult(i, j, mo, saida):
    """
    A.

    Converte a matriz saida em um array informando o indice
    das matrizes na ordem que serao multiplicadas.
    """
    if i == j:
        return i - 1
    else:
        s1 = array_ordem_mult(mo[i][j] + 1, j, mo, saida)
        s2 = array_ordem_mult(i, mo[i][j], mo, saida)
        saida.append(s1)
        saida.append(s2)


def prod_matriz(matriza, matrizb):
    """Multiplica duas matrizes."""
    if isinstance(matriza, dict):
        matriza = matriza['matriz']
    if isinstance(matrizb, dict):
        matrizb = matrizb['matriz']

    sizela = len(matriza)
    sizeca = len(matriza[0])
    sizecb = len(matrizb[0])
    matrizr = []

    for i in range(sizela):
        matrizr.append([])
        for j in range(sizecb):
            val = 0
            for k in range(sizeca):
                val += matriza[i][k] * matrizb[k][j]
            matrizr[i].append(val)
    return matrizr


def executar_ordem(ordem, matrizes):
    """Executa a multiplicacao na ordem calculada."""
    if ordem[0] < ordem[1] and\
            matrizes[ordem[0]]['colunas'] == matrizes[ordem[1]]['linhas']:
        resultante = prod_matriz(matrizes[ordem[0]], matrizes[ordem[1]])
    else:
        resultante = prod_matriz(matrizes[ordem[1]], matrizes[ordem[0]])

    for index in range(2, len(ordem)):
        if len(resultante[0]) == matrizes[ordem[index]]['linhas'] and\
                len(resultante) == matrizes[ordem[index]]['colunas']:
            r1 = (len(resultante), matrizes[ordem[index]]['colunas'])

            if index + 1 == len(ordem):
                aux = index
            else:
                aux = index + 1

            if r1[1] in (matrizes[ordem[aux]]['linhas'],
                         matrizes[ordem[aux]]['colunas']):
                resultante = prod_matriz(resultante, matrizes[ordem[index]])
            else:
                resultante = prod_matriz(matrizes[ordem[index]], resultante)

        elif len(resultante[0]) == matrizes[ordem[index]]['linhas']:
            resultante = prod_matriz(resultante, matrizes[ordem[index]])
        else:
            resultante = prod_matriz(matrizes[ordem[index]], resultante)

    return resultante


def multiplicar_matrizes(matrizes):
    """Inicia a multiplicacao das matrizes."""
    mo = melhor_ordem(matrizes)

    if mo is not None:
        out = []
        array_ordem_mult(1, len(mo) - 1, mo, out)
        mo = filter(lambda x: x is not None, out)
    else:
        mo = [0, 1]

    result = executar_ordem(mo, matrizes)

    return (result, sum([sum(i) for i in result]))


def multiplicar_numpy(matrizes):
    """."""
    r = reduce(lambda x, y: x * y, [np.matrix(i['matriz']) for i in matrizes])

    return (r.tolist(), sum([sum(i) for i in r.tolist()]))


def main():
    """."""
    resp = requests.get('http://localhost:5000/p2').json()

    saida1 = multiplicar_matrizes(resp['matrizes'])

    saida2 = multiplicar_numpy(resp['matrizes'])

    print (saida1)
    print (saida2)

#==============================================================

main()
