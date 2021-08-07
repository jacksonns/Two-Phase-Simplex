import sys
import numpy as np
from simplex import twoPhaseSimplex

class PL:
    #Elementos: tab, basis
    #Define tableau inicial e base inicial (A partir da PL auxiliar)
    def __init__(self, n, m):
        #Possui n+2 linhas, com a linha adicional para armazenar cT
        self.tab = np.zeros((n+2,3*n+m+1))
        self.basis = np.zeros(n)

        #Cria vetor c a partir da entrada
        cT = input().split()
        cT = np.asarray(cT, dtype = np.int32)
        self.tab[n+1, n:n+m] = -1 * cT

        #Inicia tableau inicial com auxiliar + linha adicional para vetor cT
        for i in range(n):
            constraint = input().split()
            constraint = np.asarray(constraint, dtype = np.int32)
            self.tab[i+1][i] = 1                    #Registro de operações
            self.tab[i+1, n:n+m] = constraint[:m]   #Restrição
            self.tab[i+1][n+m+i] = 1                #Variável de folga
            self.tab[0][2*n+m+i] = 1                #Coloca cT = 1 para a auxiliar
            self.tab[i+1][3*n+m] = constraint[m]    #Valor de b
            if constraint[m] < 0:                   #Caso b < 0, multiplica por -1
                self.tab[i+1, :] *= -1
            self.tab[i+1][2*n+m+i] = 1              #Identidade da auxiliar
            self.basis[i] = n + m + i               #Define a base inicial



if __name__ == "__main__":
    #Pega num. de restrições (n) e num de variáveis (m)
    firstLine = input().split()
    n = int(firstLine[0])
    m = int(firstLine[1])

    initialPL = PL(n, m)
    twoPhaseSimplex(initialPL, n, m)