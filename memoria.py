

memoria = []

def setInstrucao(instrucao):
    global memoria
    memoria.insert(len(memoria), instrucao)

def getInstrucao(posicao):
    global memoria
    return memoria[posicao]
        