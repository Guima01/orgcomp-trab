class controle:
    def __init__(self):
        self.regDst = 0
        self.regWrite = 0
        self.aluSrcA = 0
        self.memRead = 0
        self.memWrite = 0
        self.memToReg = 0
        self.iorD = 0
        self.irWrite = 0
        self.pcWrite = 0
        self.pcWriteCond = 0
        self.aluOP = 0
        self.aluSrcB = 0
        self.pcSource = 0

    def variaveisControle(self, functioncode, opcode,etapa):

        if (etapa == 1):
            self.memRead = 1
            self.irWrite = 1
            self.iorD = 0
            self.aluSrcA = 0
            self.aluSrcB = 1
            self.aluOP = 0
            self.pcSource = 0
            self.pcWrite = 1
        
        elif(etapa == 2):
            self.aluSrcA = 0
            self.aluSrcB = 3
            self.aluOP = 0

        elif(etapa == 3):

            if(functioncode == 32 or functioncode == 34 or functioncode == 36 or functioncode == 37 or functioncode == 0 or opcode == 8): #Lógica ou aritmética
                
                self.aluSrcA = 1
                self.aluSrcB = 0
                self.aluOP = 2

            if(functioncode == 8 or opcode == 2 or opcode == 3): #Desvio incodicional
                self.pcWrite = 1
                self.pcSource = 2

            elif(opcode == 4 or opcode == 5 or functioncode == 42): #Desvio condicional
                self.aluSrcA = 1
                self.aluSrcB = 0
                self.aluOP = 1
                self.pcWriteCond = 1
                self.pcSource = 1

            elif(opcode == 35 or opcode == 43):  #Acesso a memória
                self.aluSrcA = 1
                self.aluSrcB = 2
                self.aluOP = 0
        
        elif(etapa == 4):

            if(opcode == 0 or opcode == 8 or opcode == 3):
                self.regDst = 1
                self.regWrite = 1
                self.memToReg = 0
            elif(opcode == 35):
                self.memRead = 1
                self.iorD = 1
            elif(opcode == 43):
                self.memWrite = 1
                self.iorD = 1


        elif(etapa == 5):
            self.regDst = 1
            self.regWrite = 0
            self.memToReg = 0
    
    def printVariaveisControle(self, functioncode, opcode, etapa):
        with open("output.txt", "a") as saida:
            print("", file = saida)          
            print("SINAIS DE CONTROLE", file = saida)
            print("", file = saida)
            if (etapa == 1):
                print("MemRead: " + str(self.memRead), file = saida)
                print("IRWrite: " + str(self.irWrite), file = saida)
                print("IorD: " + str(self.iorD), file = saida)
                print("ALUSrcA: " + str(self.aluSrcA), file = saida)
                print("ALUSrcB: " + str(self.aluSrcB), file = saida)
                print("ALUOP: " + str(self.aluOP), file = saida)
                print("PCSource: " + str(self.pcSource), file = saida)
                print("PCWrite: " + str(self.pcWrite), file = saida)
            
            elif(etapa == 2):
                print("ALUSrcA: " + str(self.aluSrcA), file = saida)
                print("ALUSrcB: " + str(self.aluSrcB), file = saida)
                print("ALUOP: " + str(self.aluOP), file = saida)

            elif(etapa == 3):

                if(functioncode == 32 or functioncode == 34 or functioncode == 36 or functioncode == 37 or functioncode == 0 or opcode == 8): #Lógica ou aritmética
                    
                    print("ALUSrcA: " + str(self.aluSrcA), file = saida)
                    print("ALUSrcB: " + str(self.aluSrcB), file = saida)
                    print("ALUOP: " + str(self.aluOP), file = saida)

                if(functioncode == 8 or opcode == 2 or opcode == 3): #Desvio incodicional
                    print("PCWrite: " + str(self.pcWrite), file = saida)
                    print("PCSource: " + str(self.pcSource), file = saida)

                elif(opcode == 4 or opcode == 5 or functioncode == 42): #Desvio condicional
                    
                    print("ALUSrcA: " + str(self.aluSrcA), file = saida)
                    print("ALUSrcB: " + str(self.aluSrcB), file = saida)
                    print("ALUOP: " + str(self.aluOP), file = saida)
                    print("PCWriteCond: " + str(self.pcWriteCond), file = saida)
                    print("PCSource" + str(self.pcSource), file = saida)

                elif(opcode == 35 or opcode == 43):  #Acesso a memória
                    print("ALUSrcA: " + str(self.aluSrcA), file = saida)
                    print("ALUSrcB: " + str(self.aluSrcB), file = saida)
                    print("ALUOP: " + str(self.aluOP), file = saida)
            
            elif(etapa == 4):

                if(opcode == 0 or opcode == 8 or opcode == 3):
                    print("RegDst: " + str(self.regDst), file = saida)
                    print("RegWrite: " + str(self.regWrite), file = saida)
                    print("MemToReg: " + str(self.memToReg), file = saida)
                elif(opcode == 35):

                    print("MemRead: " + str(self.memRead), file = saida)
                    print("IorD: " + str(self.iorD), file = saida)

                elif(opcode == 43):
                    print("MemWrite: " + str(self.memWrite), file = saida)
                    print("IorD: " + str(self.iorD), file = saida)


            elif(etapa == 5):

                print("RegDst: " + str(self.regDst), file = saida)
                print("RegWrite: " + str(self.regWrite), file = saida)
                print("MemToReg: " + str(self.memToReg), file = saida)