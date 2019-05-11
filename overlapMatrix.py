import numpy as np

indel = -4                                                                          #INDEL


def diffchecker(a, b, overlap):
    c = 0
    for i in range(overlap):
        if a[i]!=b[i]:
            c+=1
    return c

def matching(str1, str2, i, j):
    if(str1[i-1]==str2[j-1]):
        return 5                                                                    #MATCH
    return -2                                                                       #MISMATCH

def overlapping(str1, str2):                                                        #(suffix,prefix)
    str1 = ''.join(str1)
    str2 = ''.join(str2)
    d = indel
    matrix_overlap = np.zeros((len(str1)+1, len(str2)+1))                           #matrice per il calcolo dell'overlap
    matrix_path = np.zeros((len(str1)+1,len(str2)+1))                               #matrice di supporto per tenere traccia dei percorsi nella matrice
    len_str1 = len(str1)+1
    len_str2 = len(str2)+1

    for i in range(0, len_str1):
        for j in range(0, len_str2):
            if(j==0):
                matrix_overlap[i][j] = i*d                                          #caso base
                matrix_path[i][j] = "-100"                                          #terminatore per la prima colonna di matrix_path
            if(i==0):
                matrix_overlap[i][j] = 0                                            #caso base
                matrix_path[i][j] = "-200"                                          #terminatore per la prima riga di matrix_path
            if(i!=0 and j!=0):
                local_max = max(matrix_overlap[i-1][j-1]+matching(str1, str2, i, j), matrix_overlap[i][j-1]+d, matrix_overlap[i-1][j]+d) #equazione di ricorrenza
                if(local_max==matrix_overlap[i-1][j-1]+matching(str1, str2, i, j)):
                    matrix_path[i][j] = 3                                           #arrivo dalla cella [i-1][j-1]
                elif(local_max==matrix_overlap[i-1][j]+d):
                    matrix_path[i][j] = 2                                           #arrivo dalla cella [i-1][j]
                else:
                    matrix_path[i][j] = 1                                           #arrivo dalla cella [i][j-1]

                matrix_overlap[i][j] = local_max
    return reconstruction(matrix_overlap, matrix_path, str1, str2)

def reconstruction(matrix_overlap, matrix_path, str1, str2):
    j = len(str2)
    i=0
    s_opt = matrix_overlap[0][j]
    while(i<=len(str1)):
        if(matrix_overlap[i][j]>=s_opt):
            s_opt=matrix_overlap[i][j]                                              #definizione della cella massima presente nell'untima colonna di matrix_overlap
            trovato = i
        i+=1
    str_i = list()
    str_i.clear()
    str_j = list()
    str_j.clear()
    delimiter = max(len(str1),len(str2))
    count = 0
    while((matrix_path[trovato][j]!=-200) and count<=(delimiter*2)):                #delimiter settato come limite massimo di passi per evitare loop infiniti
        if(matrix_path[trovato][j]==3):
            trovato-=1
            j-=1
            str_i.append(str1[trovato])
            str_j.append(str2[j])
        elif(matrix_path[trovato][j]==2):
            trovato-=1
            str_i.append(str1[trovato])
            str_j.append('B')                                                       #inserisce il carattere B nella stringa j per insertion
        elif(matrix_path[trovato][j]==1):
            j-=1
            str_i.append('B')                                                       #inserisce il carattere B nella stringa i  per deletion
            str_j.append(str2[j])
        count = count + 1
    str_i.reverse()                                                                 #ricostruzione stringa i invertendone il verso
    str_j.reverse()                                                                 #ricostruzione stringa j invertendone il verso
    str_i = ''.join(str_i)
    str_j = ''.join(str_j)
    diff = diffchecker(str_i,str_j,len(str_i))                                      #conteggio delle differenze tra le due stringhe
    return len(str_i), diff
