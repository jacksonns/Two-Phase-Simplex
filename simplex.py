import numpy as np

#Retorna índice do primeiro valor negativo em cT no tableau
#retorna -1 caso não tenha esse valor
def getPivotColumn(cT):
    for i in range(len(cT)):
        if cT[i] < 0:
            return i
    return -1


#Retorna índice do pivô a partir da coluna escolhida 
#em getPivotColumn e de b
def getPivotRow(tabCol, b):
    index = -1
    for i in range(1,len(tabCol)):
        if tabCol[i] > 0:
            div = b[i] / tabCol[i]
            if index == -1:
                min = div
                index = i
            else:
                if div < min:
                    min = div
                    index = i
    return index


#Pivoteia tableau com pivô de índices (pivRow, pivCol)
def pivotTableau(tab, pivCol, pivRow, nRow):
    #Iguala pivô a 1 para iniciar pivoteamento
    pivot = tab[pivRow][pivCol]
    tab[pivRow, :] /= pivot
    for i in range(nRow+1):
        if i != pivRow and tab[i][pivCol] != 0:
            k = -1 * tab[i][pivCol]
            tab[i, :] += k* tab[pivRow, :]


#Retorna índice da base
def getBasisIdx(num, basis):
    for i in range(len(basis)):
        if basis[i] == num:
            return i
    return -1


#index: 1 = viável e ótimo, 2 = inviável, 3 = ilimitada
def output(Pl, index, n, mCol, m):
    #print(Pl.tab)
    Pl.basis -= n
    #print(Pl.basis)
    if index == 1:
        print("otima")
        print('{:.7f}'.format(Pl.tab[0][mCol-1]))
        for i in range(m):
            idx = getBasisIdx(i, Pl.basis)
            if idx == -1:
                print(0, end = '')
                print(' ', end = '')
            else:
                print('{:.7f}'.format(Pl.tab[idx+1][mCol-1]), end = '')
                print(' ', end = '')
        print()
        for i in range(n):
            print('{:.7f}'.format(Pl.tab[0][i]), end = '')
            print(' ', end = '')

    elif index == 2:
        print("inviavel")
        for i in range(n):
            print('{:.7f}'.format(Pl.tab[0][i]), end = '')
            print(' ', end = '')

    else:
        print("ilimitada")
        for i in range(m):
            idx = getBasisIdx(i, Pl.basis)
            if idx == -1:
                print(0, end = '')
                print(' ', end = '')
            else:
                print('{:.7f}'.format(Pl.tab[idx+1][mCol-1]), end = '')
                print(' ', end = '')
        print()
        pivCol = getPivotColumn(Pl.tab[0, n:mCol-1])
        for i in range(m):
            idx = getBasisIdx(i, Pl.basis)
            if i == pivCol:
                print('1 ', end = '')
            elif idx != -1:
                print('{:.7f}'.format(-1 * Pl.tab[idx+1][pivCol+n]), end = '')
                print(' ', end = '')
            else:
                print('0 ', end = '')


#Realiza simplex
def simplex(Pl, n, m, mCol, nRow):
    # Pega primeiro valor negativo em c e escolhe pivô
    while True:
        #Passa fração do tableau correspondente ao vetor cT
        pivCol = getPivotColumn(Pl.tab[0, n:mCol-1])
        if pivCol == -1:
            break     # Loop finalizado
        pivCol += n
        pivRow = getPivotRow(Pl.tab[:n+1,pivCol], Pl.tab[:n+1,mCol-1])
        if pivRow == -1:
            if nRow == n:
                output(Pl, 3, n, mCol, m)  # Ilimitada
            return
        pivotTableau(Pl.tab, pivCol, pivRow, nRow)
        Pl.basis[pivRow - 1] = pivCol
    if nRow == n:
        output(Pl, 1, n, mCol, m)      # Obteve valor ótimo


#Realiza as duas fases do simplex
def twoPhaseSimplex(Pl, n, m):
    #Fase 1: Pivoteamento inicial da auxiliar + simplex
    for i in range(1, n+1):
        Pl.tab[0, :] += -1 * Pl.tab[i, :] 
    simplex(Pl, n, m, 3*n+m+1, n+1)

    #Fase 2: Se obteve ótimo = 0, reconstrói PL original e chama simplex
    if np.isclose(Pl.tab[0][3*n+m], 0, rtol=1e-04):
        temp = Pl.tab
        Pl.tab = np.zeros((n+1,2*n+m+1))
        Pl.tab[1:n+1, :2*n+m] = temp[1:n+1, :2*n+m]
        Pl.tab[0, :2*n+m] = temp[n+1, :2*n+m]
        Pl.tab[1:n+1, 2*n+m] = temp[1:n+1, 3*n+m]
        Pl.tab[0][2*n+m] = temp[n+1][3*n+m]
        simplex(Pl, n, m, 2*n+m+1, n)

    else:
        output(Pl, 2, n, 3*n+m+1, m)      #Inviável