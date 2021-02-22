from memoria import *
from controle import *

def leituraArquivo():
    print('digite o caminho do arquivo de entrada:')
    caminhoDoArquivo = input()
    entrada = open(caminhoDoArquivo, 'r')
    return entrada

def main():
    arquivo = leituraArquivo()
    for linha in arquivo:
        linha = int(linha)
        setInstrucao(linha)
    teste = controle()
    teste.variaveisControle(3)


if __name__ == "__main__":
    main()