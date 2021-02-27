from memoria import *
from controle import *
from random import *


controle = controle()
memoria = memoria()
registradores = [1] * 32
aRegister = None
bRegister = None
aluOut = None
ir = None
mdr = None

def leituraArquivo():
    print('digite o caminho do arquivo de entrada:')
    caminhoDoArquivo = input()
    entrada = open(caminhoDoArquivo, 'r')
    return entrada


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

def complementoDois(number):
    bit = extractKBits(number, 1, 16)
    if(bit == 0):
        return extractKBits(number, 16, 1)
    else:
        return twos_complement(extractKBits(number, 16, 1))

def desvioIncondicional(function , opcode):
    global aRegister
    global bRegister
    global aluOut
    global ir

    if(opcode == "000010"):
        aux = extractKBits(ir,26,1)
        aux = aux
        aux2 = extractKBits(memoria.pc, 4, 28)
        aux2 = aux2 << 28
        memoria.pc = aux2 | aux

    elif(opcode == "000011"):
        registradores[31] = memoria.pc + 1
        aux = extractKBits(ir,26,1)
        aux = aux
        aux2 = extractKBits(memoria.pc, 4, 28)
        aux2 = aux2 << 28
        memoria.pc = aux2 | aux

    elif(function == "001000"):
        position = extractKBits(ir, 5, 22)
        memoria.pc = registradores[position]
    

def desvioCondicional(function, opcode):
    global aRegister
    global bRegister
    global aluOut
    global ir

    if(opcode == "000100"):
        if(aRegister == bRegister):
            memoria.pc = aluOut
    
    elif(opcode == "000101"):
        if(aRegister != bRegister):
            memoria.pc = aluOut
    
    elif(function == "101010"):
        position = extractKBits(ir, 5, 12)
        if(aRegister < bRegister):
            aluOut = 1
        else:
            aluOut = 0


def logicaOuAritmetica(function, opcode):
    global aRegister
    global bRegister
    global aluOut
    global ir

    if(function == "100000"):
        aluOut = aRegister + bRegister

    elif(function == "100010"):
        aluOut = aRegister - bRegister

    elif(function == "100100"):
        aluout = aRegister & bRegister

    elif(function == "100101"):
        aluout = aRegister | bRegister
    
    elif(function == "000000"):
        aux = extractKBits(ir, 5, 7)
        aluOut = bRegister << aux

    elif(opcode == "001000"):
        aux = extractKBits(ir, 16, 1)
        aluout = aRegister + aux

def acessoMemoria(function, opcode):
    
    global aRegister
    global bRegister
    global aluOut
    global ir

    if(opcode == "100011"):
        aux = complementoDois(ir)
        aluOut = aRegister + aux

    elif(opcode == "101011"):
        aux = complementoDois(ir)
        aluOut = aRegister + aux

    
def prints(etapa):
    print("")
    print("Etapa " + str(etapa))
    print("Instrução: jump")
    print("PC: " + str(memoria.pc))
    for i in range(len(registradores)):
        print("Registrador " + str(i) + ": " + str(registradores[i]))

def etapa1():
    global ir
    prints(1)
    controle.variaveisControle(None, None,1)
    if(controle.memRead == "1" and controle.irWrite == "1" and controle.iorD == "0"):
        ir = memoria.getInstrucao(memoria.pc)
    if(controle.aluSrcA == "0" and controle.aluSrcB == "01" and controle.aluOP == "00" and controle.pcSource == "00" and controle.pcWrite == "00"):
        memoria.pc = memoria.pc + 1

def etapa2():
    global ir
    global aluOut
    global aRegister
    global bRegister
    prints(2)
    controle.variaveisControle(None, None, 2)
    aRegister = extractKBits(ir,5,22)
    bRegister = extractKBits(ir,5,17)
    aux = complementoDois(ir)
    aluOut = memoria.pc + aux
    
    
def etapa3():
    global ir
    global aluOut
    global aRegister
    global bRegister
    #controle.variaveisControle(ir[26:32],ir[0:6],3)
    desvioIncondicional("001000", None)

def etapa4():

    #ainda precisa setar sinais de controle
    global ir
    global aluOut
    global aRegister
    global bRegister
    global mdr
    opcode = extractKBits(ir,6,27)
    function = extractKBits(ir, 6, 1)
    if(opcode == 35):
        mdr = memoria.memoria[aluOut]
    elif(opcode == 43):
        memoria.memoria[aluOut] = bRegister
    
    elif(function == 32 or function == 34 or function == 36 or function == 37 or function == 0 or opcode == 8):
        position = extractKBits(ir, 5, 12)
        registradores[position] = aluOut

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


def main():
    
    arquivo = leituraArquivo()
    for linha in arquivo.readlines():
        aux = int(linha.strip())
        memoria.setInstrucao(binarioParaDecimal(aux))
        etapa1()
        etapa2()
        etapa3()
        etapa4()
        etapa5()




if __name__ == "__main__":
    main()