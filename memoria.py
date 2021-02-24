
class memoria:

    def __init__(self):
        self.memoria = []
        self.pc = 0
    def setInstrucao(self,instrucao):
        self.memoria.insert(len(self.memoria), instrucao)

    def getInstrucao(self,posicao):
        return self.memoria[posicao]
        