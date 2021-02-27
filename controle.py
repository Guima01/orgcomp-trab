class controle:
    def __init__(self):
        self.regDst = "0"
        self.regWrite = "0"
        self.aluSrcA = "0"
        self.memRead = "0"
        self.memWrite = "0"
        self.memToReg = "0"
        self.iorD = "0"
        self.irWrite = "0"
        self.pcWrite = "0"
        self.pcWriteCond = "0"
        self.aluOP = "00"
        self.aluSrcB = "00"
        self.pcSource = "00"

    def variaveisControle(self, functioncode, opcode,etapa):
        if (etapa == 1):
            self.memRead = "1"
            self.irWrite = "1"
            self.iorD = "0"
            self.aluSrcA = "0"
            self.aluSrcB = "01"
            self.aluOP = "00"
            self.pcSource = "00"
            self.pcWrite = "00"
        
        elif(etapa == 2):
            self.aluSrcA = "0"
            self.aluSrcB = "11"
            self.aluOP = "00"

        elif(etapa == 3):

            if(functioncode == "001000" or opcode == "000010" or opcode == "000011"): #Desvio incodicional
                self.pcWrite = "1"
                self.pcSource = "10"

            elif(opcode == "000000" and functioncode != "001000"): #tipo-R
                self.aluSrcA = "1"
                self.aluSrcB = "00"
                self.aluOP = "10"

            else:  
                self.aluSrcA = "1"
                self.aluSrcB = "10"
                self.aluOP = "00"
        
        elif(etapa == 4):
            #memRead = 1 ou  memWrite = 1
            self.iorD = "1"

        elif(etapa == 5):
            self.regDst = "1"
            self.regWrite = "0"
            self.memToReg = "0"