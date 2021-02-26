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

def leituraArquivo():
    print('digite o caminho do arquivo de entrada:')
    caminhoDoArquivo = input()
    entrada = open(caminhoDoArquivo, 'r')
    return entrada


def extractKBits(num,k,p): 
  
     binary = bin(num) 
     binary = binary[2:] 
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
    print(bit)
    print(number)
    if(bit == 0):
        return extractKBits(number, 16, 1)
    else:
        return twos_complement(extractKBits(number, 16, 1))

# def functionJ(value):
#     global aRegister
#     global bRegister
#     global aluOut
#     global ir

#     if(value == "000010"):
#         aux = decimalParaBinario(memoria.pc, 31)
#         aux = aux[0:4]
#         aux2 = (ir[6:32])
#         aux2 = (int(aux2))<<2
#         print(aux2)
#         aux2 = decimalParaBinario(aux2,28)
#         print(aux2)
#         #memoria.pc = (aux + aux2)
#         print(memoria.pc)



# def functionsR(functioncode):
#     global aRegister
#     global bRegister
#     global aluOut
#     global ir
#     if(functioncode == "100000"):
#         aluOut = aRegister + bRegister

#     elif(functioncode == "100010"):
#         aluOut = aRegister - bRegister

#     elif(functioncode == "100100"):
#         aux = decimalParaBinario(aRegister, 31)
#         aux2 = decimalParaBinario(bRegister, 31)
#         result = ""
#         for j in range(len(aux)):
#             if(aux[j] == "1" and aux2[j] == "1"):
#                 result = result + "1"
#             else:
#                 result = result + "0"
#                 result 
#         aluOut = binarioParaDecimal(int(result))

#     elif(functioncode == "100101"):
#         aux = decimalParaBinario(aRegister, 31)
#         aux2 = decimalParaBinario(bRegister, 31)
#         result = ""
#         for j in range(len(aux)):
#             if(aux[j] == "1" or aux2[j] == "1"):
#                 result = result + "1"
#             else:
#                 result = result + "0"
#                 result 
#         aluOut = binarioParaDecimal(int(result))
    
#     elif(functioncode == "101010"):
#         if(aRegister < bRegister):
#             aluOut = True
#         else:
#             aluOut = False
    
#     elif(functioncode == "000000"):
#         aluOut = bRegister << binarioParaDecimal(int("00100"))
    
def prints(etapa):
    print("")
    print("Etapa " + str(etapa))
    print("Instrução: jump")
    print("PC: " + str(memoria.pc))
    for i in range(len(registradores)):
        print("Resgistrador " + str(i) + ": " + str(registradores[i]))

def etapa1():
    global ir
    prints(1)
    controle.variaveisControle(None, None,1)
    if(controle.memRead == "1" and controle.irWrite == "1" and controle.iorD == "0"):
        ir = memoria.getInstrucao(int(memoria.pc/4))
    if(controle.aluSrcA == "0" and controle.aluSrcB == "01" and controle.aluOP == "00" and controle.pcSource == "00" and controle.pcWrite == "00"):
        memoria.pc = memoria.pc + 4

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
    aluOut = memoria.pc + (aux*4)
    
    
def etapa3():
    controle.variaveisControle(ir[26:32],ir[0:6],3)
    if(controle.aluSrcA == "1" and controle.aluSrcB == "00" and controle.aluOP == "10"):
        print("a")
    if(controle.pcWrite == "1" and controle.pcSource == "10"):
        print("a")



def main():
    global aRegister
    global bRegister
    global registradores
    arquivo = leituraArquivo()
    for linha in arquivo.readlines():
        aux = int(linha.strip())
        memoria.setInstrucao(binarioParaDecimal(aux))
        etapa1()
        etapa2()
    #     etapa3()




if __name__ == "__main__":
    main()