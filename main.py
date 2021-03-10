from memoria import *
from controle import *
from dicionario import *
from random import *


controle = controle()
memoria = memoria()
dicionario = dicionario()
numeroinstrucoes = 0
registradores = [1] * 32
saida = None
aRegister = None
bRegister = None
aluOut = None
ir = None
mdr = None
clock = 1


def printEtapas(etapa):
    global aluOut
    global mdr
    global ir
    global clock

    opcode = extractKBits(ir,6,27)
    functioncode = extractKBits(ir, 6, 1)

    with open("output.txt", "a") as saida:
        print("", file = saida)
        print("clock: " + str(clock), file = saida) 

        if(etapa == 1):
            print("Etapa: Busca da instrucao", file = saida)
        if(etapa == 2):
            print("Etapa: decodifica/leitura do banco de registradores", file = saida)
        if(etapa == 3):
            print("Etapa: ALU", file = saida)
        if(etapa == 4):
            print("Etapa: Acesso a memoria ou conclusao de instrucao do tipo-R", file = saida)
        if(etapa == 5):
            print("Etapa: Conclusao da leitura da memoria/Escrita no banco de registradores", file = saida)


        if(opcode == 0):
            rs = extractKBits(ir, 5, 22)
            rt = extractKBits(ir, 5, 17)
            rd = extractKBits(ir, 5, 12)
            sa = extractKBits(ir, 5, 7)
            if(functioncode != 0 and functioncode != 8):
                print("Instrucao: " + dicionario.tipoR[functioncode] + " " + dicionario.registradores[rd] + " " + dicionario.registradores[rs] + " " + dicionario.registradores[rt], file = saida)
            elif(functioncode == 0):
                print("Instrucao: " + dicionario.tipoR[functioncode] + " " + dicionario.registradores[rd] + " " + dicionario.registradores[rt] + " " + "0x{:04x}".format(sa), file = saida)            
            elif(functioncode == 8):
                print("Instrucao: " + dicionario.tipoR[functioncode] + " " + dicionario.registradores[rs], file = saida)     
                                        
        elif(opcode == 2 or opcode == 3):
            target = extractKBits(ir, 26, 1)
            print("Instrucao: " + dicionario.tipoJ[opcode] + " " + "0x{:04x}".format(target), file = saida)
        
        else:
            rs = extractKBits(ir, 5, 22)
            rt = extractKBits(ir, 5, 17)
            immediate = extractKBits(ir, 16, 1)
            if(opcode == 8):
                print("Instrucao: " + dicionario.tipoI[opcode] + " " + dicionario.registradores[rt] + " " + dicionario.registradores[rs] + " " + "0x{:04x}".format(immediate), file = saida)
            elif(opcode == 4 or opcode == 5):
                print("Instrucao: " + dicionario.tipoI[opcode] + " " + dicionario.registradores[rs] + " " + dicionario.registradores[rt] + " " + "0x{:04x}".format(immediate), file = saida)
            elif(opcode == 35 or opcode == 43):
                print("Instrucao: " + dicionario.tipoI[opcode] + " " + dicionario.registradores[rt] + " " + "0x{:04x}".format(immediate) + "({0})".format(dicionario.registradores[rs]), file = saida)   
        print("PC: " + str(memoria.pc * 4), file = saida)
        print("aluOut: " + str(aluOut), file = saida)
        print("MDR: " + str(mdr), file = saida)

        for i in range(len(registradores)):
            print("Registrador " + str(i) + ": " + str(registradores[i]), file = saida)
    
    clock +=1


def extractKBits(num,k,p): 
  
     binary = "{:032b}".format(num) 
     end = len(binary) - p 
     start = end - k + 1
     kBitSubStr = binary[start : end+1] 
     return (int(kBitSubStr,2)) 

def binarioParaDecimal(bits): 
      
    bits1 = bits 
    decimal, i, n = 0, 0, 0
    while(bits != 0): 
        dec = bits % 10
        decimal = decimal + dec * pow(2, i) 
        bits = bits//10
        i += 1
    return decimal 

def twos_complement(j):
   return j-(1<<(j.bit_length()))

def complementoDois(number, value):
    bit = extractKBits(number, 1, value)
    if(bit == 0):
        return extractKBits(number, value, 1)
    else:
        return twos_complement(extractKBits(number, value, 1))

def desvioIncondicional(function , opcode):
    global aRegister
    global bRegister
    global aluOut
    global ir

    if(opcode == 2):  #j
        aux = extractKBits(ir,26,1)
        aux2 = extractKBits(memoria.pc, 4, 29)
        aux2 = aux2 << 28
        aux = aux2 | aux
        memoria.pc = aux

    elif(opcode == 3): #jal
        
        aluOut = memoria.pc + 1
        aux = extractKBits(ir,26,1)
        aux2 = extractKBits(memoria.pc, 4, 29)
        aux2 = aux2 << 28
        aux = aux2 | aux
        memoria.pc = aux

    elif(function == 8): #jr
        position = extractKBits(ir, 5, 22)
        memoria.pc = registradores[position]
    

def desvioCondicional(function, opcode):
    global aRegister
    global bRegister
    global aluOut
    global ir

    if(opcode == 4):     #beq
        if(aRegister == bRegister):
            memoria.pc = aluOut
    
    elif(opcode == 5):   #bne
        if(aRegister != bRegister):
            memoria.pc = aluOut
    
    elif(function == 42):   #slt
        if(aRegister < bRegister):
            aluOut = 1
        else:
            aluOut = 0


def logicaOuAritmetica(function, opcode):
    global aRegister
    global bRegister
    global aluOut
    global ir

    if(function == 32):   #add
        aluOut = aRegister + bRegister

    elif(function == 34):   #sub
        aluOut = aRegister - bRegister

    elif(function == 36):   #and
        aluOut = aRegister & bRegister

    elif(function == 37):   #or
        aluOut = aRegister | bRegister
    
    elif(function == 0):   #sll
        aux = extractKBits(ir, 5, 7)
        aluOut = bRegister << aux

    elif(opcode == 8):     #addi
        aux = complementoDois(ir,16)
        aluOut = aRegister + aux

def acessoMemoria(function, opcode):
    
    global aRegister
    global bRegister
    global aluOut
    global ir

    if(opcode == 35):      #LW
        aux = complementoDois(ir,16)
        aluOut = aRegister + aux

    elif(opcode == 43):      #SW
        aux = complementoDois(ir,16)
        aluOut = aRegister + aux


def etapa1():

    global ir
    controle.variaveisControle(None, None,1)

    if(controle.memRead == 1 and controle.irWrite == 1 and controle.iorD == 0):
        ir = memoria.memoria[memoria.pc]
        
    if(controle.aluSrcA == 0 and controle.aluSrcB == 1 and controle.aluOP == 0 and controle.pcSource == 0 and controle.pcWrite == 1):
        memoria.pc = memoria.pc + 1
    
    printEtapas(1)


def etapa2():
    global ir
    global aluOut
    global aRegister
    global bRegister

    controle.variaveisControle(None, None, 2)
    aRegister = registradores[extractKBits(ir,5,22)]
    bRegister = registradores[extractKBits(ir,5,17)]
    aux = complementoDois(ir, 16)
    aluOut = memoria.pc + aux
    printEtapas(2)   
    
def etapa3():
    global ir
    global aluOut
    global aRegister
    global bRegister


    functioncode = extractKBits(ir, 6, 1)
    opcode = extractKBits(ir, 6, 27)

    controle.variaveisControle(functioncode, opcode, 3)

    if(controle.aluSrcA == 1 and controle.aluSrcB == 2 and controle.aluOP == 0): #Acesso a memória
        acessoMemoria(functioncode, opcode)

    if(controle.aluSrcA == 1 and controle.aluSrcB == 0 and controle.aluOP == 2):
        logicaOuAritmetica(functioncode, opcode)

    if(controle.aluSrcA == 1 and controle.aluSrcB == 0 and controle.aluOP == 1 and controle.pcWriteCond == 1 and controle.pcSource == 1):
        desvioCondicional(functioncode, opcode)
    
    if(controle.pcWrite== 1 and controle.pcSource == 2 ):
        desvioIncondicional(functioncode,opcode)

    printEtapas(3)


def etapa4():

    global ir
    global aluOut
    global aRegister
    global bRegister
    global mdr

    opcode = extractKBits(ir,6,27)
    functioncode = extractKBits(ir, 6, 1)

    controle.variaveisControle(functioncode, opcode, 4)

    if(controle.memRead == 1 and controle.iorD == 1 and opcode == 35):
        mdr = memoria.memoria[aluOut]
        printEtapas(4)        
   
    elif(controle.memWrite == 1 and controle.iorD == 1 and opcode == 43):
        memoria.memoria[aluOut] = bRegister
        printEtapas(4)
    elif(controle.regDst == 1 and controle.regWrite == 1 and controle.memToReg == 0):
        if(opcode == 0):
            registradores[extractKBits(ir, 5, 12)] = aluOut
            printEtapas(4)
        elif(opcode == 8):
            registradores[extractKBits(ir, 5, 17)] = aluOut
            printEtapas(4)
        elif(opcode == 3):
            registradores[31] = aluOut
            printEtapas(4)
    
def etapa5():

    #ainda precisa setar sinais de controle
    global ir
    global aluOut
    global aRegister
    global bRegister
    global mdr
    
    opcode = extractKBits(ir,6,27)

    if(opcode == 35):
        position = extractKBits(ir, 5, 17)
        registradores[position] = mdr
        printEtapas(5)

def leituraArquivo():
    print('digite o caminho do arquivo de entrada:')
    caminhoDoArquivo = input()
    entrada = open(caminhoDoArquivo, 'r')
    return entrada

def reset():
    global numeroinstrucoes
    global aluOut
    global clock
    global ir 
    global mdr 

    for i in range(32):
        registradores[i] = 1
    for i in range(64):
        memoria.memoria[i] = 3
    numeroinstrucoes = 0
    memoria.pc = 0
    aluOut = None
    ir = None
    mdr = None
    clock = 1

def menu():

    global numeroinstrucoes
    while(True):
        print("Menu")
        print("[1] leitura de arquivo de instruções")
        print("[2] leitura do arquivo via teclado")
        print("[3] Reset memória e registradores")
        print("[0] Sair")
        print()
        opcao = input()

        if(opcao == "1"):
            with open("output.txt", "w") as saida:
                print("RESULTADO",file = saida)
            arquivo = leituraArquivo()
            for linha in arquivo.readlines():
                aux = int(linha.strip())
                memoria.setInstrucao(binarioParaDecimal(aux), numeroinstrucoes)
                numeroinstrucoes +=1
            while(memoria.memoria[memoria.pc] != 3):
                etapa1()
                etapa2()
                etapa3()
                etapa4()
                etapa5()
        
        elif(opcao == "2"):
            
            print("digite a instrução:")
            instrucao = input()
            with open("output.txt", "w") as saida:
                print("",file = saida)
            if(len(instrucao) == 32):
                print(memoria.memoria[0])
                print(binarioParaDecimal(int(instrucao)))
                memoria.setInstrucao(binarioParaDecimal(int(instrucao)), numeroinstrucoes)
                print(memoria.memoria[0])
                etapa1()
                etapa2()
                etapa3()
                etapa4()
                etapa5()
            else:
                print("a instrução passada não é valida")
        
        elif(opcao == "3"):
            reset()
            print("valores resetados")

        elif(opcao == "0"):
            break
def main():
    menu()



if __name__ == "__main__":
    main()