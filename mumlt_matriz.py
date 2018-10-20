import requests

resp = requests.get('http://localhost:5000/p2').json()

if len(resp['matrizes']) > 2:
	dim = []
	for item in resp['matrizes']:
		if item['linhas'] not in dim:
			dim.append(item['linhas'])
		if item['colunas'] not in dim:
			dim.append(item['colunas'])

	n_dim = len(dim)

	matriz_temp = []
	matriz_saida = []

	for i in xrange(0, n_dim):
		matriz_saida.append([0 for i in xrange(0, n_dim)])
		matriz_temp.append([0 for i in xrange(0, n_dim)])

	for d in xrange(1, n_dim):
		for i in xrange(1, n_dim-d):
			j = i + d
			matriz_temp[i][j] = 32767

			for k in xrange(i, j):
				q = matriz_temp[i][k] + matriz_temp[k+1][j] + dim[i-1]*dim[k]*dim[j]
				if q < matriz_temp[i][j]:
					matriz_temp[i][j] = q
					matriz_saida[i][j] = k

	print n_dim, dim
	print matriz_temp
	print matriz_saida
