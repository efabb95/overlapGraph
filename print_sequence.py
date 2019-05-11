import gfapy

gfa = gfapy.Gfa.from_file("graph."+"{}".format("gfa"))                          #importazione grafo da file

num_of_nodes = len(gfa.segment_names)
linear_p = list()
sequence_of_nodes = ''

for i in range (0, num_of_nodes):                                               #creazione della sequenza di reads
    linear_p.append([str(i), 'R'])
    sequence_of_nodes = sequence_of_nodes + str(i) + '_'
sequence_of_nodes = sequence_of_nodes[0:len(sequence_of_nodes)-1]

gfa.merge_linear_path(linear_p)                                                 #ricostruzione dell'intero genoma tramite le reads

print('---------------GENOMA---------------')
print(gfa.segment(sequence_of_nodes).sequence)
