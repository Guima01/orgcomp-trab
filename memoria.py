
class memoria:
    def __init__(self):
        self.memoria = [1]*64
        self.pc = 0

    def setInstrucao(self,instrucao, index):
        self.memoria.insert(index, instrucao)

    def getInstrucao(self,posicao):
        return self.memoria[posicao]
        