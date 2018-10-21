import requests

resp = requests.get('http://localhost:5000/p2').json()


def melhor_ordem(lista_matrizes):
    if len(lista_matrizes) > 2:
        dim = []
        dim_teste = []
        for index, item in enumerate(lista_matrizes):
            if index == 0:
                dim.append(item['linhas'])
                dim.append(item['colunas'])
            else:
                dim.append(item['colunas'])

        n_dim = len(dim)
        matriz_temp = []
        matriz_saida = []

        for i in xrange(n_dim):
            matriz_saida.append([0 for _ in xrange(n_dim)])
            matriz_temp.append([0 for _ in xrange(n_dim)])

        for d in xrange(1, n_dim):
            for i in xrange(1, n_dim-d):
                j = i + d
                for k in xrange(i, j):
                    q = matriz_temp[i][k] + matriz_temp[k +
                        1][j] + dim[i-1]*dim[k]*dim[j]
                    if matriz_temp[i][j] == 0 or q < matriz_temp[i][j]:
                        matriz_temp[i][j] = q
                        matriz_saida[i][j] = k
        return matriz_saida

    return None


def array_ordem_mult(i, j, mo, saida):
    if i == j:
        return i-1
    else:
        s1 = array_ordem_mult(mo[i][j] + 1, j, mo, saida)
        s2 = array_ordem_mult(i, mo[i][j], mo, saida)
        saida.append(s1)
        saida.append(s2)


def prodMatriz(matrizA, matrizB):
    if isinstance(matrizA, dict):
        matrizA = matrizA['matriz']
    if isinstance(matrizB, dict):
        matrizB = matrizB['matriz']

    sizeLA = len(matrizA)
    sizeCA = len(matrizA[0])
    sizeCB = len(matrizB[0])
    matrizR = []

    for i in range(sizeLA):
        matrizR.append([])
        for j in range(sizeCB):
            val = 0
            for k in range(sizeCA):
                val += matrizA[i][k] * matrizB[k][j]
            matrizR[i].append(val)
    return matrizR

def executarOrdem(ordem, matrizes):
    resultante = prodMatriz(matrizes[ordem[0]],matrizes[ordem[1]])
    
    for index in range(2, len(ordem)):
        if len(resultante[0]) == matrizes[ordem[index]]['linhas']:
            resultante = prodMatriz(resultante, matrizes[ordem[index]])
        else:
            resultante = prodMatriz(matrizes[ordem[index]], resultante)

    return resultante

mo = melhor_ordem(resp['matrizes'])

if mo is not None:
    out = []
    array_ordem_mult(1, len(mo)-1, mo, out)
    mo = filter(lambda x: x is not None, out)
    if mo[0] > mo[1]:
        aux = mo[1]
        mo[1] = mo[0]
        mo[0] = aux
else:
    mo = [0, 1]

resultante = executarOrdem(mo, resp['matrizes'])

print resultante
