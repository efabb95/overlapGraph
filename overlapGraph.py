import gfapy
import trimming
import overlapMatrix
import sys


reads_id = {}
line_occurrency = {}
g = gfapy.Gfa(vlevel = 3)
g.add_line('H\tVN:Z:1.0')

read_t, read_o = trimming.trimming()

list_of_valid_reads = list()

for i in range (0,len(read_t)):
    if (len(read_t[i]) >= 60):                                                                                                  #se il read trimmato ha lunghezzo pari o superiore a 60 caratteri lo utilizzo,
        list_of_valid_reads.append(read_t[i])
    else:                                                                                                                       #altrimenti mantengo quello originale
        list_of_valid_reads.append(read_o[i])

i = 0

for read in list_of_valid_reads:
    if not read in reads_id:
        reads_id[read]=i
        node = 'S\t' + str(reads_id[read]) + '\t' + ''.join(read)                                                               #definizione dei nodi del grafo
        g.add_line(node)
        i = i + 1

count_read=0

for read1 in list_of_valid_reads:
    count_read += 5.6
    sys.stdout.write("\r\t\t\t%d%%" % count_read)
    sys.stdout.flush()
    for read2 in list_of_valid_reads:
        if (read1 != read2):
            overlap_length, differences = overlapMatrix.overlapping(read2,read1)
            if (overlap_length > 25 and differences<10):                                                                        #verifica che l'overlap abbia una lunghezza almeno pari a 25 e che le differenze tra il suffisso di un read e il prefisso dell'altro siano meno di 10
                stringa = str(reads_id[read1]) + '_' + str(reads_id[read2])                                                     #viene creato un identificativo che ci permetterà di capire se è già stato creato un arco tra i due nodi in considerazione
                if(not(stringa in line_occurrency.keys())):                                                                     #line.occurency contiene gli archi già creati
                    line = 'L\t' + str(reads_id[read1]) + '\t+\t' + str(reads_id[read2]) + '\t+\t' + str(overlap_length) + 'M'  #definizione dei link tra i nodi
                    g.add_line(line)
                    line_occurrency[stringa] = 1

g.to_file('graph.'+format('gfa'))                                                                                               #scrittura su file .gfa del grafo creato
print("\n--------------TERMINATO-------------\n")

import print_sequence
print_sequence
