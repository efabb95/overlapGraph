#path_to_reads="reads.fq"                                                        #file formato FASTQ ORIGINALE
path_to_reads="reads_mod.fq"                                                    #file formato FASTQ MODIFICATO
q_threshold = 85                                                                #soglia di qualità minima corrispondente al carattere 'U'

def trimming():
    
    valid_reads = list()                                                        #valid_reads contiene il trimming dei reads
    original_reads = list()                                                     #original_read contiene i read interi originali

    num_lines = sum(1 for line in open(path_to_reads))

    for i in range(1,(num_lines//4)+1):
        valid_read,original_read = get_subsequence(i)
        string = ''.join(valid_read)
        valid_reads.append(string)
        original_reads.append(original_read)
    return valid_reads,original_reads                                           #valid_reads: lista di read trimmati, original_reads: lista di reads interi originali


def get_subsequence(read_position):                                             #funzione che ritorna il read trimmato e il read originale
    new_read = list()
    new_read.clear()
    new_valid_read = list()
    new_valid_read.clear()
    is_sequence_valid = False

    elements, elements_q = get_read(read_position)

    for j in range(0,len(elements)-1):                                          #ciclo carattere per carattere il read originale
        character = elements[j]                                                 #carattere della sequenza {A,C,G,T}
        character_quality = elements_q[j]                                       #carattere di qualità
        if (ord(character_quality) >= q_threshold):                             #ord() restituisce il valore ASCII in decimale di un carattere
            if (not(is_sequence_valid)):
                new_read.clear()
                is_sequence_valid = True
            new_read.append(character)
        else:
            is_sequence_valid = False
            if (len(new_read)>len(new_valid_read)):
                new_valid_read.clear()
                new_valid_read = new_read[0:len(new_read)]
    if (len(new_read)>len(new_valid_read)):
                new_valid_read.clear()
                new_valid_read = new_read[0:len(new_read)]
    if (len(new_valid_read)==0):
        new_valid_read = new_read[0:len(new_read)]

    elements = ''.join(elements[0:len(elements)-1])

    return new_valid_read, elements


def get_read(read_pos):                                                         #funzione che dato in input il numero del read richiesto lo restituisce insieme alla sequenza di qualità corrispondente
    read_position = (read_pos-1)*4

    fileTxt = open(path_to_reads,'r')
    lines = fileTxt.readlines()
    list_of_element = list(lines[read_position+1])                              #contiene la sequenza del read
    list_of_qualities = list(lines[read_position+3])                            #contiene la sequenza di qualità

    return list_of_element,list_of_qualities