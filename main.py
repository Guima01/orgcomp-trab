from memoria import *
from controle import *


controle = controle()
memoria = memoria()
registradores = [0] * 32
aRegister = None
bRegister = None
aluOut = None
ir = None

def leituraArquivo():
    print('digite o caminho do arquivo de entrada:')
    caminhoDoArquivo = input()
    entrada = open(caminhoDoArquivo, 'r')
    return entrada


def binarioParaDecimal(bits): 
      
    bits1 = bits 
    decimal, i, n = 0, 0, 0
    while(bits != 0): 
        dec = bits % 10
        decimal = decimal + dec * pow(2, i) 
        bits = bits//10
        i += 1
    return decimal  

def estendeSinal(bits):
    while(len(bits) != 32):
        bits = bits + bits[15]
    #print(bits)
    return bits

def complementoDois(bits):
    if(bits[0] == "0"):
        print(bits)
        return binarioParaDecimal(int(bits))
    else:
        boolean = False
        aux = ""
        for i in range(len(bits)-1, 0 , -1):
            if(boolean == True):
                if(bits[i] == "1"):
                    aux = aux + "0"
                elif(bits[i] == "0"):
                    aux = aux + "1"
            elif(bits[i] == "1"):
                boolean = True
                aux = aux + bits[i]
            else:
                aux = aux + bits[i]
        print(aux)




def etapa1():
    global ir
    controle.variaveisControle(None,1)
    if(controle.memRead == "1" and controle.irWrite == "1" and controle.iorD == "0"):
        ir = memoria.getInstrucao(int(memoria.pc/4))
    if(controle.aluSrcA == "0" and controle.aluSrcB == "01" and controle.aluOP == "00" and controle.pcSource == "00" and controle.pcWrite == "00"):
        memoria.pc = memoria.pc + 4

def etapa2():
    global ir
    controle.variaveisControle(None, 2)
    aux = ''.join(reversed(ir))
    pos1 = ''.join(reversed(aux[21:26]))
    pos2 = ''.join(reversed(aux[16:21]))
    pos1 = binarioParaDecimal(int(pos1))
    pos2 = binarioParaDecimal(int(pos2))
    aRegister = registradores[pos1]
    bRegister = registradores[pos2]
    aux = estendeSinal(aux[0:16])
    aux = ''.join(reversed(aux))
    complementoDois(aux)
    
    #tenho q fazer o aluOut ainda




def main():
    arquivo = leituraArquivo()
    for linha in arquivo.readlines():
        memoria.setInstrucao(linha.strip())
        etapa1()
        etapa2()




if __name__ == "__main__":
    main()