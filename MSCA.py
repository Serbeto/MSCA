import time
import numpy as np
import cmath
import math

# Premissas principais: Número de barras e Potencia base do Sistema
# Inicialização da matriz base e coleta de dados
S_base = float(input("Potência base do Sistema (MVA): "))
barras = int(input("Quantas barras existem no sistema? "))
n_barras = barras
# Captura a tensão base de cada barra
V_base_barras = []
for i in range(barras):
    V_base = float(input(f"Tensão base da barra {i + 1} (kV): "))
    V_base_barras.append(V_base)

# Calcula a corrente base para cada tensão base na lista V_base_barras
I_base_barras = []
for V_base in V_base_barras:
    I_base = S_base / (math.sqrt(3) * V_base)
    I_base_barras.append(I_base)

################################################################################

"Matrizes e Listas Bases"
# Matriz base para criação de Ybarra
matriz_base = [[0 for _ in range(barras)] for _ in range(barras)]

# Lista que irá conter a localização dos transformadotes e será usada como premissa para definição de áreas
transformadores = []

# Início da Matriz com a defasagem da barra coluna(m) em relação a barra linha(k)
Multi_def = np.array([[0 for _ in range(barras)] for _ in range(barras)])

################################################################################

"Obtendo os dados necessários para criação do elemento transformador"

# Função para configurar a matriz T
def configurar_matriz_T(barras):
    T = [row[:] for row in matriz_base]
    while True:
        try:
            print("Diga entre quais barras está o transformador.")
            k = int(input(f"Informe a primeira barra de interesse (1 a {barras}): ")) - 1
            m = int(input(f"Informe a segunda barra de interesse (1 a {barras}): ")) - 1
            if not (0 <= k < barras and 0 <= m < barras):
                print("Índices fora do intervalo. Tente novamente.")
                continue
            transformadores.append((k, m))
            tap = float(input("Tap do transformador (p.u): "))
            conect_P = int(input(
                f"Conexão do lado conectado à barra {k + 1} :\n1 para Estrela;\n2 para Delta;\n3 para Estrela aterrada\nEscolha: "))
            conect_S = int(input(
                f"Conexão do lado conectado à barra {m + 1} :\n1 para Estrela;\n2 para Delta;\n3 para Estrela aterrada\nEscolha: "))
            # Verifica se as conexões estão no intervalo correto
            if conect_P not in [1, 2, 3] or conect_S not in [1, 2, 3]:
                print("Conexão inválida. Escolha 1, 2 ou 3. Tente novamente.")
                continue
            defasamento = complex(0, 0)
            trafo_def = input('Transformador defasador especial? (S/N): ').upper()
            if trafo_def == 'S':
                try:
                    defasamento = float(input(f"Defasamento do lado conectado à barra {m + 1} em\n"
                                              f"relaçao ao lado conectado à barra {k + 1} em graus: "))
                except ValueError:
                    # Se houver erro ao inserir os números, retorna uma mensagem de erro
                    print("Erro! Por favor, insira valores numéricos válidos.")
                    return None  # Retorna None para indicar erro e permitir a chamada da função novamente
            elif trafo_def == 'N':
                if conect_P == 1 and conect_S == 1:
                    defasamento = 0
                elif conect_P == 1 and conect_S == 2:
                    defasamento = -30
                elif conect_P == 1 and conect_S == 3:
                    defasamento = 0
                elif conect_P == 2 and conect_S == 1:
                    defasamento = 30
                elif conect_P == 2 and conect_S == 2:
                    defasamento = 0
                elif conect_P == 2 and conect_S == 3:
                    defasamento = 30
                elif conect_P == 3 and conect_S == 1:
                    defasamento = 0
                elif conect_P == 3 and conect_S == 2:
                    defasamento = -30
                elif conect_P == 3 and conect_S == 3:
                    defasamento = 0
            else:
                print("Opção inválida. Por favor, insira S para Sim ou N para Não.")
                return None  # Retorna None para indicar erro e permitir a chamada da função novamente

            Multi_def[k][m] = defasamento
            Multi_def[m][k] = -defasamento
            # Atualiza a matriz T com o defasamento
            T[k][m] = -tap
            T[m][k] = -tap
            T[k][k] = tap ** 2
            T[m][m] = 1

            # Armazena as informações associadas às barras
            return T, k, m, tap, conect_P, conect_S, defasamento, Multi_def

        except ValueError:
            print("Entrada inválida. Por favor, insira números inteiros para os índices.")

        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            return None  # Retorna None em caso de interrupção

def configurar_matriz_T_0(conect_P, conect_S):
    T0 = [row[:] for row in matriz_base]

    # Estrela (primário) e Estrela (secundário)
    if conect_P == 1 and conect_S == 1:
        T0[k][k] = 0
        T0[k][m] = 0
        T0[m][k] = 0
        T0[m][m] = 0
    # Estrela (primário) e Delta (secundário)
    elif conect_P == 1 and conect_S == 2:
        T0[k][k] = 0
        T0[k][m] = 0
        T0[m][k] = 0
        T0[m][m] = 0
    # Estrela (primário) e Estrela aterrada (secundário)
    elif conect_P == 1 and conect_S == 3:
        T0[k][k] = 0
        T0[k][m] = 0
        T0[m][k] = 0
        T0[m][m] = 0
    # Delta (primário) e Estrela (secundário)
    elif conect_P == 2 and conect_S == 1:
        T0[k][k] = 0
        T0[k][m] = 0
        T0[m][k] = 0
        T0[m][m] = 0
    # Delta (primário) e Delta (secundário)
    elif conect_P == 2 and conect_S == 2:
        T0[k][k] = 0
        T0[k][m] = 0
        T0[m][k] = 0
        T0[m][m] = 0
    # Delta (primário) e Estrela aterrada (secundário)
    elif conect_P == 2 and conect_S == 3:
        T0[k][k] = 0
        T0[k][m] = 0
        T0[m][k] = 0
        T0[m][m] = 1
    # Estrela aterrada (primário) e Estrela (secundário)
    elif conect_P == 3 and conect_S == 1:
        T0[k][k] = 0
        T0[k][m] = 0
        T0[m][k] = 0
        T0[m][m] = 0
    # Estrela aterrada (primário) e Delta (secundário)
    elif conect_P == 3 and conect_S == 2:
        T0[k][k] = tap ** 2
        T0[k][m] = 0
        T0[m][k] = 0
        T0[m][m] = 0
    # Estrela aterrada (primário) e Estrela aterrada (secundário)
    elif conect_P == 3 and conect_S == 3:
        T0[k][k] = tap ** 2
        T0[k][m] = -tap
        T0[m][k] = -tap
        T0[m][m] = 1

    return T0

# Função para capturar os dados do transformador
def capturar_dados_transformador():
    pot = float(input("Potência do transformador (MVA): "))
    V_k = float(input(f"Tensão nominal do lado do transformador conectado à barra {k + 1} (kV): "))
    V_m = float(input(f"Tensão nominal do lado do transformador conectado à barra {m + 1} (kV): "))
    Res_1 = float(input("Resistência de Sequência Positiva (p.u): "))
    Res_0 = float(input("Resistência de Sequência Zero (p.u): "))
    Rea_1 = float(input("Reatância de Sequência Positiva (p.u): "))
    Rea_0 = float(input("Reatância de Sequência Zero (p.u): "))
    # Inicializa as impedâncias de aterramento como 0 (não aterrada por padrão)
    Res_0_Tp, Rea_0_Tp = 0, 0
    Res_0_Ts, Rea_0_Ts = 0, 0
    # Caso o lado seja estrela aterrada, pergunta se há impedância de aterramento
    if conect_P == 3:
            try:
                # Se houver impedância, solicita os valores
                Res_0_Tp = float(input(f'Resistência de aterramento na conexão da barra {k + 1}(p.u): '))
                Rea_0_Tp = float(input(f'Reatância de aterramento na conexão da barra {k + 1}(p.u): '))
            except ValueError:
                # Se houver erro ao inserir os números, retorna uma mensagem de erro
                print("Erro! Por favor, insira valores numéricos válidos.")
                return None  # Retorna None para indicar erro e permitir a chamada da função novamente

    # Caso o lado seja estrela aterrada, pergunta se há impedância de aterramento
    if conect_S == 3:
            try:
                # Se houver impedância, solicita os valores
                Res_0_Ts = float(input(f'Resistência de aterramento na conexão da barra {m + 1} (p.u): '))
                Rea_0_Ts = float(input(f'Reatância de aterramento na conexão da barra {m + 1} (p.u): '))
            except ValueError:
                # Se houver erro ao inserir os números, retorna uma mensagem de erro
                print("Erro! Por favor, insira valores numéricos válidos.")
                return None  # Retorna None para indicar erro e permitir a chamada da função novamente

    return pot, V_k, V_m, Res_1, Rea_1, Res_0, Rea_0, Res_0_Tp, Rea_0_Tp, Res_0_Ts, Rea_0_Ts

################################################################################

"Obtendo os dados necessários para criação do elemento gerador"

# Função para configurar a matriz G para o gerador
def configurar_matriz_G(barras):
    G = [row[:] for row in matriz_base]
    while True:
        try:
            k = int(input(f"A qual barra está conectado o gerador (1 a {barras}): ")) - 1
            if 0 <= k < barras:
                G[k][k] = 1
                break
            else:
                print("Índices fora do intervalo. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira números inteiros para os índices.")
    return G, k  # Retorna G e o índice da barra


# Função para capturar os dados do gerador
def capturar_dados_gerador():
    pot = float(input("Potência do gerador (MVA): "))
    V_nom = float(input("Tensão nominal do gerador (kV): "))
    Res_1 = float(input("Resistência de Sequência Positiva (p.u): "))
    Res_0 = float(input("Resistência de Sequência Zero (p.u): "))
    Rea_1 = float(input("Reatância subtransitória (p.u): "))
    Rea_0 = float(input("Reatância de Sequência Zero (p.u): "))
    conect = int(
        input(f"Conexão o gerador:\n1 para Estrela;\n2 para Delta;\n3 para Estrela aterrada\nEscolha: "))
    Res_0_T, Rea_0_T = 0, 0
    if conect == 3:  # Estrela aterrada
            try:
                # Se houver impedância, solicita os valores
                Res_0_T = float(input('Resistência de aterramento do gerador (p.u): '))
                Rea_0_T = float(input('Reatância de aterramento do gerador (p.u): '))
            except ValueError:
                # Se houver erro ao inserir os números, retorna uma mensagem de erro
                print("Erro! Por favor, insira valores numéricos válidos.")
                return None  # Retorna None para indicar erro e permitir a chamada da função novamente

    return pot, V_nom, Res_1, Rea_1, Res_0, Rea_0, conect, Res_0_T, Rea_0_T

def configurar_matriz_G_0(conect):
    G0 = [row[:] for row in matriz_base]
    # Estrela aterrada (conect == 3)
    if conect == 3:
        G0[k][k] = 1
    else:
        G0[k][k] = 0  # Para qualquer outro tipo de conexão

    return G0

################################################################################

"Obtendo os dados necessários para criação do elemento linha de transmissão"

# Função para configurar a matriz LT para as linhas entre barras especificadas
def configurar_matriz_LT(barras):
    LT = [row[:] for row in matriz_base]
    while True:
        try:
            print("Diga entre quais barras está a linha de interesse.")
            k = int(input(f"Informe a primeira barra de interesse (1 a {barras}): ")) - 1
            m = int(input(f"Informe a segunda barra de interesse (1 a {barras}): ")) - 1

            if 0 <= k < barras and 0 <= m < barras:
                LT[k][m] = -1
                LT[m][k] = -1
                LT[k][k] = 1
                LT[m][m] = 1
                break
            else:
                print("Índices fora do intervalo. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira números inteiros para os índices.")

    return LT, k, m  # Retorna LT e o índice da barra correspondente

# Função para configurar a matriz LT_PI com as adimitancias do modelo PI
def configurar_PI_LT():
    LT_PI = [row[:] for row in matriz_base]

    LT_PI[k][k] = 1
    LT_PI[m][m] = 1

    return LT_PI

# Função para capturar os dados da linha
def capturar_dados_linha():
    V_nom = float(input("Tensão nominal da linha (kV): "))
    Res_1 = float(input("Resistência de Sequência Positiva (p.u): "))
    Res_0 = float(input("Resistência de Sequência Zero (p.u): "))
    Rea_1 = float(input("Reatância de Sequência Positiva (p.u): "))
    Rea_0 = float(input("Reatância de Sequência Zero (p.u): "))
    print("\nCaso deseje modelo de linha curta, os valores abaixo devem ser 0!")
    G_shunt = float(input("Condutância do shunt da linha (p.u): "))
    B_shunt = float(input("Susceptância do shunt da linha (p.u): "))
    return V_nom, Res_1, Rea_1, Res_0, Rea_0, G_shunt, B_shunt

################################################################################

"Obtendo os dados necessários para criação do elemento motor"

def configurar_matriz_M(barras):
    M = [row[:] for row in matriz_base]
    while True:
        try:
            k = int(input(f"A qual barra está conectado o motor (1 a {barras}): ")) - 1
            if 0 <= k < barras:
                M[k][k] = 1
                break
            else:
                print("Índices fora do intervalo. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira números inteiros para os índices.")
    return M, k  # Retorna M e o índice da barra

def capturar_dados_motor():
    pot = float(input("Potência do motor (MVA): "))
    V_nom = float(input("Tensão nominal do motor (kV): "))
    Res_1 = float(input("Resistência de Sequência Positiva (p.u): "))
    Res_0 = float(input("Resistência de Sequência Zero (p.u): "))
    Rea_1 = float(input("Reatância subtransitória (p.u): "))
    Rea_0 = float(input("Reatância de Sequência Zero (p.u): "))
    conect = int(
        input(f"Conexão do motor:\n1 para Estrela;\n2 para Delta;\n3 para Estrela aterrada\nEscolha: "))
    Res_0_T, Rea_0_T = 0, 0
    if conect == 3:  # Estrela aterrada
            try:
                # Se houver impedância, solicita os valores
                Res_0_T = float(input('Resistência de aterramento do motor (p.u): '))
                Rea_0_T = float(input('Reatância de aterramento do motor (p.u): '))
            except ValueError:
                # Se der erro ao inserir os números, retorna uma mensagem de erro
                print("Erro! Por favor, insira valores numéricos válidos.")
                return None

    return pot, V_nom, Res_1, Rea_1, Res_0, Rea_0, conect, Res_0_T, Rea_0_T

def configurar_matriz_M_0(conect):
    M0 = [row[:] for row in matriz_base]
    # Estrela aterrada (conect == 3)
    if conect == 3:
        M0[k][k] = 1
    else:
        M0[k][k] = 0  # Para qualquer outro tipo de conexão

    return M0

################################################################################

"Obtendo os dados necessários para criação do elemento shunt"

def configurar_matriz_S(barras):
    S = [row[:] for row in matriz_base]
    while True:
        try:
            k = int(input(f"A qual barra está conectado o shunt (1 a {barras}): ")) - 1
            if 0 <= k < barras:
                S[k][k] = 1
                break
            else:
                print("Índices fora do intervalo. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira números inteiros para os índices.")
    return S, k

def capturar_dados_shunt():
    P, Q = float(), float()
    while True:
        try:
            tipo = int(input(
                "Tipo de elemento shunt conectado:\n1 para Carga\n2 para Capacitor Shunt\n3 para Reator Shunt\nEscolha: "))
            if tipo not in [1, 2, 3]:
                print("Escolha inválida! Por favor, insira 1, 2 ou 3.")
                continue

            if tipo == 1:  # Carga
                while True:
                    P = float(input("Potência ativa da carga (MW): "))
                    if P < 0:
                        print("Potência ativa não pode ser negativa para uma carga! Tente novamente.")
                        continue
                    Q = float(input("Potência reativa da carga (Mvar): "))
                    if not (P == 0 and Q == 0):  # Não permite cargas (0,0)
                        break
                    else:
                        print("A Carga não pode ser 0! Tente novamente.")
            elif tipo == 2:  # Capacitor Shunt
                P = 0
                while True:
                    Q = -float(input("Potência reativa do capacitor (Mvar): -"))
                    if Q >= 0:  # Valor de Q deve ser negativo
                        print("Insira o valor em módulo, diferente de 0! Tente novamente.")
                    else:
                        break
            elif tipo == 3:  # Reator Shunt
                P = 0
                while True:
                    Q = float(input("Potência reativa do reator (Mvar): "))
                    if Q <= 0:
                        print("Insira o valor em módulo e maior que 0! Tente novamente.")
                    else:
                        break

            return tipo, P, Q

        except ValueError:
            print("Entrada inválida. Por favor, insira números válidos.")

def configurar_matriz_S_0():
    S0 = [row[:] for row in matriz_base]  # Copia a matriz base para inicialização
    S0[k][k] = 1

    return S0

################################################################################

"Cálculo das admitâncias corrigidas em p.u"

# Listas para armazenar as matrizes de admitância
lista_Y_t = []
lista_Y_t0 = []
lista_Y_g = []
lista_Y_g0 = []
lista_Y_lt = []
lista_Y_lt0 = []
lista_Y_m = []  # Motores - Sequência Positiva
lista_Y_m0 = []  # Motores - Sequência Zero
lista_Y_s = []  # Shunts - Sequência Positiva
lista_Y_s0 = []  # Shunts - Sequência Zero

# Função para calcular a matriz de admitância Y_t
def calcular_Y_t(T, Res_1, Rea_1, pot, V_k, barra_idx):
    z_pu_new = (Res_1 + 1j * Rea_1) * ((S_base / pot) * ((V_k / V_base_barras[barra_idx]) ** 2))
    admitancia = 1 / z_pu_new
    Y_t = admitancia * np.array(T)
    return Y_t

# Função para calcular Y_t0 com impedância de aterramento
def calcular_Y_t0(T0, Res_0, Rea_0, pot, V_k, V_m, k, m, Res_0_Tp, Rea_0_Tp, Res_0_Ts, Rea_0_Ts):
    z_pu_new = (Res_0 + 1j * Rea_0) * ((S_base / pot) * ((V_k / V_base_barras[k]) ** 2))
    z_pu_new_p = (Res_0_Tp + 1j * Rea_0_Tp) * ((S_base / pot) * ((V_k / V_base_barras[k]) ** 2))
    z_pu_new_s = (Res_0_Ts + 1j * Rea_0_Ts) * ((S_base / pot) * ((V_m / V_base_barras[m]) ** 2))
    admitancia = 1 / (z_pu_new + 3 * z_pu_new_p + 3 * z_pu_new_s)
    Y_t0 = admitancia * np.array(T0)
    return Y_t0

def calcular_Y_g(G, Res_1, Rea_1, pot, V_nom, barra_idx):
    z_pu_new = (Res_1 + 1j * Rea_1) * ((S_base / pot) * ((V_nom / V_base_barras[barra_idx]) ** 2))
    admitancia = 1 / z_pu_new
    Y_g = admitancia * np.array(G)
    return Y_g

def calcular_Y_g0(G0, Res_0, Rea_0, Res_0_T, Rea_0_T, pot, V_nom, barra_idx):
    z_pu_new = (Res_0 + 1j * Rea_0) * ((S_base / pot) * ((V_nom / V_base_barras[barra_idx]) ** 2))
    z_pu_new_t = (Res_0_T + 1j * Rea_0_T) * ((S_base / pot) * ((V_nom / V_base_barras[barra_idx]) ** 2))
    admitancia = 1 / (z_pu_new + (3 * z_pu_new_t))
    Y_g0 = admitancia * np.array(G0)
    return Y_g0

# Função para calcular a matriz de admitância Y_lt
def calcular_Y_lt(LT, Res_1, Rea_1, V_nom, barra_idx):
    z_pu_new = (Res_1 + 1j * Rea_1) * ((V_nom / V_base_barras[barra_idx]) ** 2)
    admitancia = 1 / z_pu_new
    Y_lt = admitancia * np.array(LT)
    return Y_lt

def calcular_Y_lt_PI(LT_PI, G_shunt, B_shunt, V_nom, barra_idx):
    admitancia = (G_shunt + B_shunt * 1j) * ((V_base_barras[barra_idx] / V_nom) ** 2)
    Y_lt_shunt = (admitancia / 2) * np.array(LT_PI)
    return Y_lt_shunt

def calcular_Y_lt0(LT0, Res_0, Rea_0, V_nom, barra_idx):
    z_pu_new = (Res_0 + 1j * Rea_0) * ((V_nom / V_base_barras[barra_idx]) ** 2)
    admitancia = 1 / z_pu_new
    Y_lt0 = admitancia * np.array(LT0)
    return Y_lt0

def calcular_Y_lt_PI_0(LT_PI_0, G_shunt, B_shunt, V_nom, barra_idx):
    admitancia = (G_shunt + B_shunt * 1j) * ((V_base_barras[barra_idx] / V_nom) ** 2)
    Y_lt_shunt_0 = (admitancia / 2) * np.array(LT_PI_0)
    return Y_lt_shunt_0

def calcular_Y_m(M, Res_1, Rea_1, pot, V_nom, barra_idx):
    z_pu_new = (Res_1 + 1j * Rea_1) * ((S_base / pot) * ((V_nom / V_base_barras[barra_idx]) ** 2))
    admitancia = 1 / z_pu_new
    Y_m = admitancia * np.array(M)  # Usa a matriz M para o motor
    return Y_m

def calcular_Y_m0(M0, Res_0, Rea_0, Res_0_T, Rea_0_T, pot, V_nom, barra_idx):
    z_pu_new = (Res_0 + 1j * Rea_0) * ((S_base / pot) * ((V_nom / V_base_barras[barra_idx]) ** 2))
    z_pu_new_t = (Res_0_T + 1j * Rea_0_T) * ((S_base / pot) * ((V_nom / V_base_barras[barra_idx]) ** 2))
    admitancia = 1 / (z_pu_new + (3 * z_pu_new_t))  # Considera as impedâncias de aterramento
    Y_m0 = admitancia * np.array(M0)  # Usa a matriz M0 para sequência zero do motor
    return Y_m0

def calcular_Y_s(S, P, Q, V_conectada, S_base):
    # Passo 1: Calcular Z_ohm usando P e Q
    z_ohm = (V_conectada ** 2) / (P - 1j * Q)
    # Passo 2: Calcular Z_base da área do shunt
    Z_base = (V_conectada ** 2) / S_base  # V em kV, S_base em MVA
    # Passo 3: Calcular impedância em p.u.
    z_pu = z_ohm / Z_base
    # Passo 4: Calcular admitância (inversa da impedância)
    admitancia = 1 / z_pu
    # Passo 5: Calcular matriz Y_s
    Y_s = admitancia * np.array(S)  # Multiplica pela matriz S correspondente ao shunt
    return Y_s

# Para o elemento shunt está sendo considerado que seq+, - e 0 são iguais
# Para o elemento shunt está sendo considerado que não há imp_terra
def calcular_Y_s0(S0, P, Q, V_conectada, S_base):
    # Passo 1: Calcular Z_ohm usando P e Q
    z_ohm = (V_conectada ** 2) / (P - 1j * Q)
    # Passo 2: Calcular Z_base da área do shunt
    Z_base = (V_conectada ** 2) / S_base  # V em kV, S_base em MVA
    # Passo 3: Calcular impedância em p.u.
    z_pu = z_ohm / Z_base
    # Passo 4: Calcular admitância (inversa da impedância)
    admitancia = 1 / z_pu
    # Passo 5: Calcular matriz Y_s0
    Y_s0 = admitancia * np.array(S0)  # Multiplica pela matriz S0 correspondente ao shunt
    return Y_s0

################################################################################

"Capturando as impedâncias dos diagramas de impedâncias"

# Listas para armazenar as impedâncias
lista_imp_t_1 = []
lista_imp_t_0 = []
lista_imp_g_1 = []
lista_imp_g_0 = []
lista_imp_lt_1 = []
lista_adm_lt_1 = []
lista_imp_lt_0 = []
lista_adm_lt_0 = []
lista_imp_m_1 = []  # Motores - Sequência Positiva
lista_imp_m_0 = []  # Motores - Sequência Zero
lista_imp_s_1 = []  # Shunts - Sequência Positiva
lista_imp_s_0 = []  # Shunts - Sequência Zero

def imp_t_1(Res_1, Rea_1, pot, V_k, barra_idx):
    z_pu_1 = (Res_1 + 1j * Rea_1) * ((S_base / pot) * ((V_k / V_base_barras[barra_idx]) ** 2))
    return z_pu_1

# Função para calcular imp_t_0 com a nova impedância
def imp_t_0(Res_0, Rea_0, pot, V_k, V_m, k, m, Res_0_Tp, Rea_0_Tp, Res_0_Ts, Rea_0_Ts):
    z_pu_new = (Res_0 + 1j * Rea_0) * ((S_base / pot) * ((V_k / V_base_barras[k]) ** 2))
    z_pu_new_p = (Res_0_Tp + 1j * Rea_0_Tp) * ((S_base / pot) * ((V_k / V_base_barras[k]) ** 2))
    z_pu_new_s = (Res_0_Ts + 1j * Rea_0_Ts) * ((S_base / pot) * ((V_m / V_base_barras[m]) ** 2))
    z_pu_0 = z_pu_new + 3 * z_pu_new_p + 3 * z_pu_new_s
    return z_pu_0

def imp_g_1(Res_1, Rea_1, pot, V_nom, barra_idx):
    z_pu_1 = (Res_1 + 1j * Rea_1) * ((S_base / pot) * ((V_nom / V_base_barras[barra_idx]) ** 2))
    return z_pu_1

def imp_g_0(Res_0, Rea_0, Res_0_T, Rea_0_T, pot, V_nom, barra_idx):
    z_pu_new = (Res_0 + 1j * Rea_0) * ((S_base / pot) * ((V_nom / V_base_barras[barra_idx]) ** 2))
    z_pu_new_t = (Res_0_T + 1j * Rea_0_T) * ((S_base / pot) * ((V_nom / V_base_barras[barra_idx]) ** 2))
    z_pu_0 = z_pu_new + (3 * z_pu_new_t)
    return z_pu_0

def imp_lt_1(Res_1, Rea_1, V_nom, barra_idx):
    z_pu_1 = (Res_1 + 1j * Rea_1) * ((V_nom / V_base_barras[barra_idx]) ** 2)
    return z_pu_1

def adm_lt_pi_1(G_shunt, B_shunt, V_nom, barra_idx):
    admitancia_pu_1 = ((G_shunt + B_shunt * 1j) * ((V_base_barras[barra_idx] / V_nom) ** 2)) / 2
    return admitancia_pu_1

def imp_lt_0(Res_0, Rea_0, V_nom, barra_idx):
    z_pu_0 = (Res_0 + 1j * Rea_0) * ((V_nom / V_base_barras[barra_idx]) ** 2)
    return z_pu_0

def adm_lt_pi_0(G_shunt, B_shunt, V_nom, barra_idx):
    admitancia_pu_0 = ((G_shunt + B_shunt * 1j) * ((V_base_barras[barra_idx] / V_nom) ** 2)) / 2
    return admitancia_pu_0

def imp_m_1(Res_1, Rea_1, pot, V_nom, barra_idx):
    z_pu_1 = (Res_1 + 1j * Rea_1) * ((S_base / pot) * ((V_nom / V_base_barras[barra_idx]) ** 2))
    return z_pu_1

def imp_m_0(Res_0, Rea_0, Res_0_T, Rea_0_T, pot, V_nom, barra_idx):
    z_pu_new = (Res_0 + 1j * Rea_0) * ((S_base / pot) * ((V_nom / V_base_barras[barra_idx]) ** 2))
    z_pu_new_t = (Res_0_T + 1j * Rea_0_T) * ((S_base / pot) * ((V_nom / V_base_barras[barra_idx]) ** 2))
    z_pu_0 = z_pu_new + (3 * z_pu_new_t)
    return z_pu_0

def imp_s_1(P, Q, V_nom, S_base):
    z_ohm = (V_nom ** 2) / (P + 1j * Q)
    Z_base = (V_nom ** 2) / S_base  # Impedância base
    z_pu_1 = z_ohm / Z_base  # Impedância em p.u.
    return z_pu_1

def imp_s_0(P, Q, V_nom, S_base):
    z_ohm = (V_nom ** 2) / (P + 1j * Q)
    Z_base = (V_nom ** 2) / S_base  # Impedância base
    z_pu_0 = z_ohm / Z_base  # Impedância em p.u.
    return z_pu_0

################################################################################

"Função para configurar a impedância de sequência zero para um trafo e descrição"

def configurar_impedancia_sequencia_zero(conect_P, conect_S, zt_0, k, m):
    descricao = ""  # Inicializa descricao para evitar qualquer erro de variável indefinida
    if conect_P == 1 and conect_S == 1:  # Estrela-Estrela
        zt_0 = 0
        descricao = "entre as barras"
    elif conect_P == 1 and conect_S == 2:  # Estrela-Delta
        zt_0 = 0
        descricao = "entre as barras"
    elif conect_P == 1 and conect_S == 3:  # Estrela-Estrela Aterrada
        zt_0 = 0
        descricao = "entre as barras"
    elif conect_P == 2 and conect_S == 1:  # Delta-Estrela
        zt_0 = 0
        descricao = "entre as barras"
    elif conect_P == 2 and conect_S == 2:  # Delta-Delta
        zt_0 = 0
        descricao = "entre as barras"
    elif conect_P == 2 and conect_S == 3:  # Delta-Estrela Aterrada
        descricao = f"somente conectado à barra {m + 1}"
    elif conect_P == 3 and conect_S == 1:  # Estrela Aterrada-Estrela
        zt_0 = 0
        descricao = "entre as barras"
    elif conect_P == 3 and conect_S == 2:  # Estrela Aterrada-Delta
        descricao = f"somente conectado à barra {k + 1}"
    elif conect_P == 3 and conect_S == 3:  # Estrela Aterrada-Estrela Aterrada
        descricao = "entre as barras"
    return zt_0, descricao

################################################################################

"Função que garante a captura dos elementos do Loop abaixo"

def confirmar_insercao():
    while True:
        confirmacao = input("Deseja confirmar a inserção dos dados? (S/N): ").strip().lower()
        if confirmacao == "s":
            return True
        elif confirmacao == "n":
            return False
        else:
            print("Opção inválida. Digite 'S' para sim ou 'N' para não.")


################################################################################

"Loop para perguntar ao usuário se deseja adicionar elementos"
while True:
    elemento = input(
        "\nDeseja adicionar um elemento? (transformador = T  \ gerador = G \ linha = L \nmotor = M \ shunt = S \ nenhum = N): ").strip().lower()
    if elemento == "t":
        T, k, m, tap, conect_P, conect_S, defasamento, Multi_def = configurar_matriz_T(
            barras)  # Obtém T, índices e tensões nominais
        pot, V_k, V_m, Res_1, Rea_1, Res_0, Rea_0, Res_0_Tp, Rea_0_Tp, Res_0_Ts, Rea_0_Ts = capturar_dados_transformador()
        T0 = configurar_matriz_T_0(conect_P, conect_S)
        if confirmar_insercao():
            try:
                zt_1 = imp_t_1(Res_1, Rea_1, pot, V_k, k)
                zt_0, descricao = configurar_impedancia_sequencia_zero(conect_P, conect_S,
                                            imp_t_0(Res_0, Rea_0, pot, V_k, V_m, k, m, Res_0_Tp, Rea_0_Tp, Res_0_Ts, Rea_0_Ts),k, m)
                # Armazenando nas listas
                lista_imp_t_1.append(
                    {'bk': k + 1, 'bm': m + 1, 'zt_1': zt_1})  # Armazena as barras e impedância
                lista_imp_t_0.append(
                    {'bk': k + 1, 'bm': m + 1, 'zt_0': zt_0,
                     'descricao': descricao})  # Armazena as barras e impedância
                Y_t = calcular_Y_t(T, Res_1, Rea_1, pot, V_k, k)  # Sequência Positiva
                Y_t0 = calcular_Y_t0(T0, Res_0, Rea_0, pot, V_k, V_m, k, m, Res_0_Tp, Rea_0_Tp, Res_0_Ts,
                                     Rea_0_Ts)  # Sequência Zero
                lista_Y_t.append(Y_t)
                lista_Y_t0.append(Y_t0)  # Armazena a matriz de sequência zero
                # Calcula as impedâncias
            except ValueError as e:
                print(e)
        else:
            print("Dados do transformador descartados.")

    elif elemento == "g":
        G, k = configurar_matriz_G(barras)  # Obtém G e o índice da barra k
        pot, V_nom, Res_1, Rea_1, Res_0, Rea_0, conect, Res_0_T, Rea_0_T = capturar_dados_gerador()
        G0 = configurar_matriz_G_0(conect)
        if confirmar_insercao():
            zg_1 = imp_g_1(Res_1, Rea_1, pot, V_nom, k)
            zg_0 = imp_g_0(Res_0, Rea_0, Res_0_T, Rea_0_T, pot, V_nom, k)
            # Armazenando nas listas
            lista_imp_g_1.append({'bk': k + 1, 'zg_1': zg_1})  # Armazena a barra e impedância
            lista_imp_g_0.append({'bk': k + 1, 'zg_0': zg_0})  # Armazena a barra e impedância
            Y_g = calcular_Y_g(G, Res_1, Rea_1, pot, V_nom, k)
            Y_g0 = calcular_Y_g0(G0, Res_0, Rea_0, Res_0_T, Rea_0_T, pot, V_nom, k)
            lista_Y_g.append(Y_g)
            lista_Y_g0.append(Y_g0)
        else:
            print("Dados do gerador descartados.")

    elif elemento == "l":
        LT, k, m = configurar_matriz_LT(barras)
        V_nom, Res_1, Rea_1, Res_0, Rea_0, G_shunt, B_shunt = capturar_dados_linha()
        LT_PI = configurar_PI_LT()
        # Não necessita L0 pois modelo da linha se mantém
        if confirmar_insercao():
            zlt_1 = imp_lt_1(Res_1, Rea_1, V_nom, k)
            zlt_0 = imp_lt_0(Res_0, Rea_0, V_nom, k)
            adm_lt_1 = adm_lt_pi_1(G_shunt, B_shunt, V_nom, k)
            adm_lt_0 = adm_lt_pi_0(G_shunt, B_shunt, V_nom, k)
            # Armazenando nas listas
            lista_imp_lt_1.append(
                {'bk': k + 1, 'bm': m + 1, 'zlt_1': zlt_1})  # Armazena as barras e impedância
            lista_imp_lt_0.append(
                {'bk': k + 1, 'bm': m + 1, 'zlt_0': zlt_0})  # Armazena as barras e impedância
            lista_adm_lt_1.append({'bk': k + 1, 'bm': m + 1, 'adm_lt_1': adm_lt_1})
            lista_adm_lt_0.append({'bk': k + 1, 'bm': m + 1, 'adm_lt_0': adm_lt_0})
            # Formando a matriz do elemento
            Y_lt_base = calcular_Y_lt(LT, Res_1, Rea_1, V_nom, k)  # Admitância base seq positiva
            Y_lt_PI = calcular_Y_lt_PI(LT_PI, G_shunt, B_shunt, V_nom, k)  # Admitância shunt seq positiva
            Y_lt0_base = calcular_Y_lt0(LT, Res_0, Rea_0, V_nom, k)
            Y_lt_PI_0 = calcular_Y_lt_PI_0(LT_PI, G_shunt, B_shunt, V_nom, k)  # Admitância shunt seq zero

            # Soma das admitâncias base e shunt
            Y_lt = Y_lt_base + Y_lt_PI
            Y_lt0 = Y_lt0_base + Y_lt_PI_0

            lista_Y_lt.append(Y_lt)
            lista_Y_lt0.append(Y_lt0)
        else:
            print("Dados da linha descartados.")

    # Caso para Motores
    elif elemento == "m":
        M, k = configurar_matriz_M(barras)
        pot, V_nom, Res_1, Rea_1, Res_0, Rea_0, conect, Res_0_T, Rea_0_T = capturar_dados_motor()
        M0 = configurar_matriz_M_0(conect)
        if confirmar_insercao():
            zm_1 = imp_m_1(Res_1, Rea_1, pot, V_nom, k)
            zm_0 = imp_m_0(Res_0, Rea_0, Res_0_T, Rea_0_T, pot, V_nom, k)
            lista_imp_m_1.append({'bk': k + 1, 'zm_1': zm_1})
            lista_imp_m_0.append({'bk': k + 1, 'zm_0': zm_0})
            Y_m = calcular_Y_m(M, Res_1, Rea_1, pot, V_nom, k)
            Y_m0 = calcular_Y_m0(M0, Res_0, Rea_0, Res_0_T, Rea_0_T, pot, V_nom, k)
            lista_Y_m.append(Y_m)
            lista_Y_m0.append(Y_m0)
        else:
            print("Dados do motor descartados.")

    # Caso para Shunts
    elif elemento == "s":
        S, k = configurar_matriz_S(barras)
        tipo, P, Q = capturar_dados_shunt()
        if confirmar_insercao():
            zs_1 = imp_s_1(P, Q, V_base_barras[k], S_base)
            zs_0 = imp_s_0(P, Q, V_base_barras[k], S_base)
            lista_imp_s_1.append({'bk': k + 1, 'zs_1': zs_1, 'tipo_shunt': tipo})
            lista_imp_s_0.append({'bk': k + 1, 'zs_0': zs_0, 'tipo_shunt': tipo})
            Y_s = calcular_Y_s(S, P, Q, V_base_barras[k], S_base)
            Y_s0 = calcular_Y_s0(S, P, Q, V_base_barras[k], S_base)
            lista_Y_s.append(Y_s)
            lista_Y_s0.append(Y_s0)
        else:
            print("Dados do shunt descartados.")

    elif elemento == "n":
        break
    else:
        print("Opção inválida. Tente novamente.")

################################################################################

"Impedâncias do diagrama de sequências"
print("\n\n***Sequência postiva/negativa***")
# Exibe transformadores, apenas se existirem
if lista_imp_t_1:
    print("\n-> Impedâncias de Transformadores:")
    for imp in lista_imp_t_1:
        print(f"  Barra {imp['bk']} <-> Barra {imp['bm']}: ZT_1 = {imp['zt_1']}")
# Exibe geradores, apenas se existirem
if lista_imp_g_1:
    print("\n-> Impedâncias de Geradores:")
    for imp in lista_imp_g_1:
        print(f"  Barra {imp['bk']}: ZG_1 = {imp['zg_1']}")
# Exibe linhas de transmissão, apenas se existirem
if lista_imp_lt_1:
    print("\n-> Impedâncias de Linhas de Transmissão:")
    for imp in lista_imp_lt_1:
        print(f"  Barra {imp['bk']} <-> Barra {imp['bm']}: ZLT_1 = {imp['zlt_1']}")
    for adm in lista_adm_lt_1:
        if adm['adm_lt_1'] != 0:
            print("\n-> Admitâncias Shunt de Linhas de Transmissão:")
            print(f"  Barra {adm['bk']} e Barra {adm['bm']}: YLT_1 = {adm['adm_lt_1']}")
# Exibe motores, apenas se existirem
if lista_imp_m_1:
    print("\n-> Impedâncias de Motores:")
    for imp in lista_imp_m_1:
        print(f"  Barra {imp['bk']}: ZM_1 = {imp['zm_1']}")
# Exibe shunts, apenas se existirem
if lista_imp_s_1:
    print("\n-> Impedâncias de Shunts:")
    for imp in lista_imp_s_1:
        print(f"  Barra {imp['bk']}: ZS_1 = {imp['zs_1']} ({imp['tipo_shunt']})")  # Incluindo o tipo de shunt

print("\n***Sequência zero***")
# Exibe transformadores, apenas se existirem
if lista_imp_t_0:
    print("-\n> Impedâncias de Transformadores:")
    for imp in lista_imp_t_0:
        print(f"  Barra {imp['bk']} <-> Barra {imp['bm']}: ZT_0 = {imp['zt_0']} ({imp['descricao']})")
# Exibe geradores, apenas se existirem
if lista_imp_g_0:
    print("\n-> Impedâncias de Geradores:")
    for imp in lista_imp_g_0:
        print(f"  Barra {imp['bk']}: ZG_0 = {imp['zg_0']}")
# Exibe linhas de transmissão, apenas se existirem
if lista_imp_lt_0:
    print("\n-> Impedâncias de Linhas de Transmissão:")
    for imp in lista_imp_lt_0:
        print(f"  Barra {imp['bk']} <-> Barra {imp['bm']}: ZLT_0 = {imp['zlt_0']}")
    for adm in lista_adm_lt_0:
        if adm['adm_lt_0'] != 0:
            print("\n-> Admitâncias Shunt de Linhas de Transmissão:")
            print(f"  Barra {adm['bk']} e Barra {adm['bm']}: YLT_1 = {adm['adm_lt_0']}")
# Exibe motores, apenas se existirem
if lista_imp_m_0:
    print("\n-> Impedâncias de Motores:")
    for imp in lista_imp_m_0:
        print(f"  Barra {imp['bk']}: ZM_0 = {imp['zm_0']}")
# Exibe shunts, apenas se existirem
if lista_imp_s_0:
    print("\n-> Impedâncias de Shunts:")
    for imp in lista_imp_s_0:
        print(f"  Barra {imp['bk']}: ZS_0 = {imp['zs_0']} ({imp['tipo_shunt']})")  # Incluindo o tipo de shunt

################################################################################

"Exibição das Submatrizes do Sistema"
while True:
    try:
        # Solicita a entrada do usuário para exibir ou não as submatrizes
        print_submatrizes = input("\nDeseja conferir as submatrizes criadas? (S/N): ").strip().upper()

        if print_submatrizes not in ["S", "N"]:
            print("Opção inválida! Por favor, insira 'S' para sim ou 'N' para não.")
            continue

        if print_submatrizes == "S":
            print("\nExibição de todas as submatrizes armazenadas")

            # Sequência positiva/negativa
            if lista_Y_t:
                print("\n-> Todas as matrizes Y_t calculadas:")
                for i, Y in enumerate(lista_Y_t, start=1):
                    print(f"Y_t{i}:")
                    print(Y)
            if lista_Y_g:
                print("\n-> Todas as matrizes Y_g calculadas:")
                for i, Y in enumerate(lista_Y_g, start=1):
                    print(f"Y_g{i}:")
                    print(Y)
            if lista_Y_lt:
                print("\n-> Todas as matrizes Y_lt calculadas:")
                for i, Y in enumerate(lista_Y_lt, start=1):
                    print(f"Y_lt{i}:")
                    print(Y)
            if lista_Y_m:
                print("\n-> Todas as matrizes Y_m calculadas (Motores):")
                for i, Y in enumerate(lista_Y_m, start=1):
                    print(f"Y_m{i}:")
                    print(Y)
            if lista_Y_s:
                print("\n-> Todas as matrizes Y_s calculadas (Shunts):")
                for i, Y in enumerate(lista_Y_s, start=1):
                    print(f"Y_s{i}:")
                    print(Y)
            # Sequência zero
            if lista_Y_t0:
                print("\n-> Todas as matrizes Y_t0 calculadas:")
                for i, Y in enumerate(lista_Y_t0, start=1):
                    print(f"Y_t0{i}:")
                    print(Y)
            if lista_Y_g0:
                print("\n-> Todas as matrizes Y_g0 calculadas:")
                for i, Y in enumerate(lista_Y_g0, start=1):
                    print(f"Y_g0{i}:")
                    print(Y)
            if lista_Y_lt0:
                print("\n-> Todas as matrizes Y_lt0 calculadas:")
                for i, Y in enumerate(lista_Y_lt0, start=1):
                    print(f"Y_lt0{i}:")
                    print(Y)
            if lista_Y_m0:
                print("\n-> Todas as matrizes Y_m0 calculadas (Motores):")
                for i, Y in enumerate(lista_Y_m0, start=1):
                    print(f"Y_m0{i}:")
                    print(Y)
            if lista_Y_s0:
                print("\n-> Todas as matrizes Y_s0 calculadas (Shunts):")
                for i, Y in enumerate(lista_Y_s0, start=1):
                    print(f"Y_s0{i}:")
                    print(Y)
            if not any([lista_Y_t, lista_Y_g, lista_Y_lt, lista_Y_m, lista_Y_s,
                        lista_Y_t0, lista_Y_g0, lista_Y_lt0, lista_Y_m0, lista_Y_s0]):
                print("\nNenhuma submatriz foi criada.")
        else:
            print("\nExibição das submatrizes foi ignorada.")
        # Saia do loop após entrada válida
        break
    except Exception as e:
        print(f"Ocorreu um erro: {e}. Tente novamente.")

################################################################################

"Lógica de soma de todas as submatrizes para formar a Ybarra final"

# Função para somar todas as matrizes
def somar_matrizes(lista_matrizes):
    matriz_soma = np.zeros_like(lista_matrizes[0])
    for matriz in lista_matrizes:
        matriz_soma += matriz
    return matriz_soma


# Calcula a soma total de todas as matrizes
if lista_Y_t:
    soma_Y_t = somar_matrizes(lista_Y_t)
else:
    soma_Y_t = np.zeros_like(matriz_base)
if lista_Y_t0:
    soma_Y_t0 = somar_matrizes(lista_Y_t0)
else:
    soma_Y_t0 = np.zeros_like(matriz_base)

if lista_Y_g:
    soma_Y_g = somar_matrizes(lista_Y_g)
else:
    soma_Y_g = np.zeros_like(matriz_base)
if lista_Y_g0:
    soma_Y_g0 = somar_matrizes(lista_Y_g0)
else:
    soma_Y_g0 = np.zeros_like(matriz_base)

if lista_Y_lt:
    soma_Y_lt = somar_matrizes(lista_Y_lt)
else:
    soma_Y_lt = np.zeros_like(matriz_base)
if lista_Y_lt0:
    soma_Y_lt0 = somar_matrizes(lista_Y_lt0)
else:
    soma_Y_lt0 = np.zeros_like(matriz_base)

if lista_Y_m:
    soma_Y_m = somar_matrizes(lista_Y_m)
else:
    soma_Y_m = np.zeros_like(matriz_base)
if lista_Y_m0:
    soma_Y_m0 = somar_matrizes(lista_Y_m0)
else:
    soma_Y_m0 = np.zeros_like(matriz_base)

if lista_Y_s:
    soma_Y_s = somar_matrizes(lista_Y_s)
else:
    soma_Y_s = np.zeros_like(matriz_base)
if lista_Y_s0:
    soma_Y_s0 = somar_matrizes(lista_Y_s0)
else:
    soma_Y_s0 = np.zeros_like(matriz_base)

# Formação da Ybarra final
Y_barra1 = soma_Y_t + soma_Y_g + soma_Y_lt + soma_Y_m + soma_Y_s  # Sequência positiva/negativa
Y_barra0 = soma_Y_t0 + soma_Y_g0 + soma_Y_lt0 + soma_Y_m0 + soma_Y_s0  # Sequência zero

# Exibição da soma final
print("\n\n-> Matrizes Ybarra finais:")
print("\n. Y barra de sequência + e -:")
print(Y_barra1)
print("\n. Y barra de sequência 0:")
print(Y_barra0)

################################################################################

"Calculando as matrizes Zbarra através da inversa das Ybarra"
# Tentativa de inversão da matriz Y_barra1
try:
    Z_barra_pos = np.linalg.inv(Y_barra1)
    print("\n\n-> Matrizes impedância de barra")
    print("\n. Z barra de sequência + e -:")
    print(Z_barra_pos)
except np.linalg.LinAlgError:
    print("**** ERRO: A matriz Y_barra1 não é inversível (singular). ****")
    print("Por favor, verifique os dados inseridos e execute o programa novamente.")
    exit()  # Encerra o programa

# Tentativa de inversão da matriz Y_barra0
try:
    Z_barra_0 = np.linalg.inv(Y_barra0)
    print("\n. Z barra de sequência 0:")
    print(Z_barra_0)
except np.linalg.LinAlgError:
    print("**** ERRO: A matriz Y_barra0 não é inversível (singular). ****")
    print("Por favor, verifique os dados inseridos e execute o programa novamente.")
    exit()  # Encerra o programa

################################################################################

"######## Criando  conceito de áreas ##########"
# transformadores = [] lá em cima
def define_areas(matriz_admitancia, transformadores):
    num_barras = len(matriz_admitancia)

    # Inicializa um vetor para armazenar a área de cada barra (-1 indica que ainda não foi definida)
    areas = [-1] * num_barras
    area_atual = 0

    def dfs(barra, area):
        """Função recursiva para realizar a busca em profundidade (DFS)"""
        areas[barra] = area  # Marca a barra com a área atual
        for prox_barra in range(num_barras):
            # Verifica se existe admitância não nula e não há transformador entre as barras
            if (matriz_admitancia[barra][prox_barra] != 0 and
                    prox_barra != barra and
                    (barra, prox_barra) not in transformadores and
                    (prox_barra, barra) not in transformadores and
                    areas[prox_barra] == -1):  # Só visita se ainda não foi visitada
                dfs(prox_barra, area)

    # Faz a busca por todas as barras
    for barra in range(num_barras):
        if areas[barra] == -1:  # Se a barra ainda não foi marcada com uma área
            dfs(barra, area_atual)
            area_atual += 1  # Incrementa a área para a próxima busca

    return areas

# Definindo as áreas
areas = define_areas(Y_barra1, transformadores)

def criar_listas_areas(areas):
    # Cria um dicionário para armazenar as barras em cada área
    listas_areas = {}

    # Agrupa as barras de acordo com suas áreas
    for barra, area in enumerate(areas):
        if area not in listas_areas:
            listas_areas[area] = []  # Cria uma nova lista para a área se não existir
        listas_areas[area].append(barra + 1)  # Adiciona a barra (1-indexed) à lista da área
    return listas_areas  # Retorna o dicionário

# Armazenando o retorno de criar_listas_areas em listas_areas
listas_areas = criar_listas_areas(areas)

# Definindo nomes para as áreas (Podem ser criadas quantos nomes forem necessários
nomes_areas = ["areaA", "areaB", "a\reaC", "areaD", "areaE",
               "areaF", "areaG", "areaH", "areaI", "areaJ", "areaK",
               "areaL", "areaM", "areaN","areaO",
               "areaP", "areaQ", "areaR", "areaS", "areaT", "areaU",
               "areaV", "areaW", "areaX", "areaY", "areaZ"]

# Criando e printando as listas de áreas
#print("\n\n-> Listas de barras em cada área:")
for i, (area, barras) in enumerate(listas_areas.items()):
    nome_variavel = nomes_areas[i]
    globals()[nome_variavel] = barras  # Cria a variável global dinamicamente com o nome e lista de barras
    #print(f"{nome_variavel} = {globals()[nome_variavel]}")  # Valida e exibe o conteúdo criado

#Criando a lista de áreas por barra
areas_por_barra = [-1] * sum(len(barras) for barras in listas_areas.values())  # Inicializa com -1
# Preenche a lista areas_por_barra com as áreas correspondentes
for area, barras in listas_areas.items():
    for barra in barras:
        areas_por_barra[barra - 1] = area  # Subtrai 1 para ajustar ao índice 0

################################################################################

"Tratamento da matriz Multi_def"
# Início do tratamento
# Dicionário para armazenar as posições de cada grupo de área
posicoes_por_grupo_area = {}

# Agrupa as posições das linhas que têm a mesma área
for idx, grupo_area in enumerate(areas_por_barra):
    if grupo_area not in posicoes_por_grupo_area:
        posicoes_por_grupo_area[grupo_area] = []
    posicoes_por_grupo_area[grupo_area].append(idx)

# Replica valores não triviais entre linhas com o mesmo grupo de área
for grupo_area, indices in posicoes_por_grupo_area.items():
    if len(indices) > 1:  # grupo de área com mais de uma barra
        # Percorre todas as colunas
        for col in range(Multi_def.shape[1]):  # percorrendo cada coluna
            # Encontra o valor não trivial para essa coluna entre as linhas do mesmo grupo de área
            valores_na_coluna = [Multi_def[i][col] for i in indices if Multi_def[i][col] != 0]
            if valores_na_coluna:
                valor_nao_trivial = valores_na_coluna[0]  # Usa o primeiro valor não trivial encontrado
                # Define esse valor para todas as linhas do mesmo grupo de área na coluna atual
                for i in indices:
                    Multi_def[i][col] = valor_nao_trivial

# Realiza o segundo tratamento para replicar o conjugado dos valores não triviais em posições simétricas
# Itera sobre todas as posições da matriz, incluindo a parte inferior e superior
for i in range(Multi_def.shape[0]):
    for j in range(Multi_def.shape[1]):
        if i != j and Multi_def[i][j] != 0:  # Se o valor é não trivial e i != j
            # Atribui o valor em [i][j] para a posição simétrica [j][i] com o sinal invertido
            Multi_def[j][i] = -Multi_def[i][j]

# Iniciando terceiro tratamento
# Criando o dicionário phase_areas automaticamente

phase_areas = {}
for (barra1, barra2) in transformadores:
    area1 = areas_por_barra[barra1]
    area2 = areas_por_barra[barra2]

    if area1 != area2:
        defasagem = Multi_def[barra1, barra2]
        phase_areas[(area1, area2)] = defasagem
        phase_areas[(area2, area1)] = -defasagem

# Função para identificar o caminho direto entre duas barras e retornar as áreas do caminho
def identificar_caminho_entre_areas(barras_inicial, barra_destino, lista_imp_lt_1, lista_imp_t_1, areas_por_barra):
    visitadas = set()
    fila = [(barras_inicial - 1, [])]

    while fila:
        barra_atual, caminho = fila.pop(0)
        area_atual = areas_por_barra[barra_atual]
        if area_atual not in caminho:
            caminho.append(area_atual)

        if barra_atual == barra_destino - 1:
            return caminho

        visitadas.add(barra_atual)

        for imp in lista_imp_lt_1 + lista_imp_t_1:
            bk, bm = imp['bk'] - 1, imp['bm'] - 1
            proxima_barra = None

            if bk == barra_atual and bm not in visitadas:
                proxima_barra = bm
            elif bm == barra_atual and bk not in visitadas:
                proxima_barra = bk

            if proxima_barra is not None:
                fila.append((proxima_barra, caminho.copy()))

    return []

# Função para atualizar Multi_def usando phase_areas e os caminhos diretos
def atualizar_multi_def(Multi_def, areas_por_barra, lista_imp_lt_1, lista_imp_t_1, phase_areas):
    num_barras = len(Multi_def)
    for i in range(num_barras):
        for j in range(num_barras):
            if i != j and areas_por_barra[i] != areas_por_barra[j] and Multi_def[i][j] == 0:
                caminho_areas = identificar_caminho_entre_areas(i + 1, j + 1, lista_imp_lt_1, lista_imp_t_1,
                                                                areas_por_barra)
                if caminho_areas:
                    defasagem_total = 0
                    for k in range(len(caminho_areas) - 1):
                        area_atual, area_proxima = caminho_areas[k], caminho_areas[k + 1]
                        defasagem_total += phase_areas.get((area_atual, area_proxima), 0)

                    Multi_def[i][j] = defasagem_total
                    Multi_def[j][i] = -defasagem_total  # Define o valor oposto para a posição simétrica

    return Multi_def

# Atualizando a matriz Multi_def com base nos caminhos diretos e nas defasagens entre áreas
Multi_def_atualizada = atualizar_multi_def(Multi_def, areas_por_barra, lista_imp_lt_1, lista_imp_t_1, phase_areas)

# Exibindo o resultado final da matriz Multi_def
mostrar_m_def = input("\nDeseja verificar a matriz de defasagem entre as barras? (S/N): ").strip().upper()    # if mostrar_m_def
if mostrar_m_def == "S":
    print("\nMatriz de defasagens entre as barras:\n")
    print(Multi_def_atualizada)
    print("Obs: Defasagem da posição coluna em relação à posição linha!")

################################################################################

while True:

    "Aplicando o curto em um barra específica"
    z = int(input("\n\nQual barra está em curto? ")) - 1
    V_base_curto = V_base_barras[z]
    I_base_curto = I_base_barras[z]

    matriz_Zbarra_seqpos = Z_barra_pos
    matriz_Zbarra_seqneg = matriz_Zbarra_seqpos
    matriz_Zbarra_seqzero = Z_barra_0

    # Impedância de Thévennin a partir da barra de curto
    zkk_0 = matriz_Zbarra_seqzero[int(z)][int(z)]
    zkk_1 = matriz_Zbarra_seqpos[int(z)][int(z)]
    zkk_2 = matriz_Zbarra_seqneg[int(z)][int(z)]

    def obter_impedancia_de_falta():
        while True:  # Loop até o usuário fornecer uma entrada válida
            existe_zf = input('Existe impedância de falta? (S para sim / N para não): ').upper()

            if existe_zf == 'S':
                try:
                    # Se sim, pede um valor numérico ao usuário
                    real = float(input('Digite a parte real da impedância de falta (p.u): '))
                    imag = float(input('Digite a parte imaginária da impedância de falta (p.u): '))
                    zf = complex(real, imag)  # Atribui o valor de zf com parte real e imaginária
                    return zf  # Retorna o valor correto de zf
                except ValueError:
                    # Se der erro ao inserir os números, retorna uma mensagem de erro
                    print("Erro! Por favor, insira valores numéricos válidos.")
                    continue  # Recomeça a pergunta

            elif existe_zf == 'N':
                return 0 + 0j  # Atribui 0+j0 se não houver impedância

            else:
                # Se a opção for inválida, avisa e recomeça o loop
                print("Opção inválida. Por favor, insira S para Sim ou N para Não.")
                continue  # Recomeça a pergunta

    # Chama a função e captura o valor de zf
    zf = obter_impedancia_de_falta()

    ################################################################################

    "Fórmulas gerais para todos os curtos"

    def if_a(ifa_0, ifa_1, ifa_2):
        return ifa_0 + ifa_1 + ifa_2

    def if_b(ifa_0, ifa_1, ifa_2):
        return ifa_0 + (ifa_1 * a ** 2) + (ifa_2 * a)

    def if_c(ifa_0, ifa_1, ifa_2):
        return ifa_0 + (ifa_1 * a) + (ifa_2 * a ** 2)

    def Zjk_0(Vj):
        return matriz_Zbarra_seqzero[Vj - 1][int(z)]

    def Zjk_1(Vj):
        return matriz_Zbarra_seqpos[Vj - 1][int(z)]

    def Zjk_2(Vj):
        return matriz_Zbarra_seqneg[Vj - 1][int(z)]

    def Vja_0(Zjk_0, ifa_0):
        return (0 + 0j) - (Zjk_0) * (ifa_0)

    def Vja_1(Vf, Zjk_1, ifa_1):
        return Vf - (Zjk_1) * (ifa_1)

    def Vja_2(Zjk_2, ifa_2):
        return (0 + 0j) - (Zjk_2) * (ifa_2)

    def V_a(V_0, V_1, V_2):
        return V_0 + V_1 + V_2

    def V_b(V_0, V_1, V_2):
        return V_0 + (V_1 * a ** 2) + (V_2 * a)

    def V_c(V_0, V_1, V_2):
        return V_0 + (V_1 * a) + (V_2 * a ** 2)

    def I_a(I_0, I_1, I_2):
        return I_0 + I_1 + I_2

    def I_b(I_0, I_1, I_2):
        return I_0 + (I_1 * a ** 2) + (I_2 * a)

    def I_c(I_0, I_1, I_2):
        return I_0 + (I_1 * a) + (I_2 * a ** 2)

    # Tensão pré-falta
    Vf = 1
    # Deslocamento angular de Sequências (a = 1∠-120°)
    a = cmath.rect(1, math.radians(120))

    ################################################################################

    "Definindo o tipo de curto escolhido"
    curto = input('Opções de curto-circuito:\n'
                  'M para Monofásico na fase A;\n'
                  'B para Bifásico nas fases B-C;\n'
                  'BT para Bifásico-Terra nas fases B-C;\n'
                  'T para Trifásico.\n'
                  'Qual curto desejado? ').upper()

    while curto not in ["M", "B", "BT", "T"]:
        print("Opção inválida. Tente novamente.")
        curto = input('Qual curto desejado? ').upper()

    ################################################################################

    "Determinando os valores de corrente de defeito em cada fase"


    def print_defeitos(tipo_curto, z, if_a, if_b, if_c, I_base_curto):
        I_base_curto_rounded = round(I_base_curto, 4)

        print('Para o curto', tipo_curto, f'na barra {z + 1}:')
        print('--> Correntes de defeito:\n')

        print(f"ifa (0) = {ifa_0.real:.4f} {'+' if ifa_0.imag >= 0 else '-'} {abs(ifa_0.imag):.4f}j p.u  "
              f"= {abs(ifa_0):.4f} ∠ {np.angle(ifa_0, deg=True):.2f}° p.u  "
              f">-- x {I_base_curto:.4f} kA --> {abs(ifa_0 * I_base_curto):.4f} ∠ {np.angle(ifa_0, deg=True):.2f}° kA")
        print(f"ifa (1) = {ifa_1.real:.4f} {'+' if ifa_1.imag >= 0 else '-'} {abs(ifa_1.imag):.4f}j p.u  "
              f"= {abs(ifa_1):.4f} ∠ {np.angle(ifa_1, deg=True):.2f}° p.u  "
              f">-- x {I_base_curto:.4f} kA --> {abs(ifa_1 * I_base_curto):.4f} ∠ {np.angle(ifa_1, deg=True):.2f}° kA")
        print(f"ifa (2) = {ifa_2.real:.4f} {'+' if ifa_2.imag >= 0 else '-'} {abs(ifa_2.imag):.4f}j p.u  "
              f"= {abs(ifa_2):.4f} ∠ {np.angle(ifa_2, deg=True):.2f}° p.u  "
              f">-- x {I_base_curto:.4f} kA --> {abs(ifa_2 * I_base_curto):.4f} ∠ {np.angle(ifa_2, deg=True):.2f}° kA\n")

        print(f'if (A) = {if_a.real:.4f} {"+" if if_a.imag >= 0 else "-"} {abs(if_a.imag):.4f}j p.u  '
              f"= {abs(if_a):.4f} ∠ {np.angle(if_a, deg=True):.2f}° p.u  "
              f'>-- x {I_base_curto_rounded} kA --> {abs(if_a * I_base_curto):.4f} ∠ {np.angle(if_a, deg=True):.2f}° kA')
        print(f'if (B) = {if_b.real:.4f} {"+" if if_b.imag >= 0 else "-"} {abs(if_b.imag):.4f}j p.u  '
              f"= {abs(if_b):.4f} ∠ {np.angle(if_b, deg=True):.2f}° p.u  "
              f'>-- x {I_base_curto_rounded} kA --> {abs(if_b * I_base_curto):.4f} ∠ {np.angle(if_b, deg=True):.2f}° kA')
        print(f'if (C) = {if_c.real:.4f} {"+" if if_c.imag >= 0 else "-"} {abs(if_c.imag):.4f}j p.u  '
              f"= {abs(if_c):.4f} ∠ {np.angle(if_c, deg=True):.2f}° p.u  "
              f'>-- x {I_base_curto_rounded} kA --> {abs(if_c * I_base_curto):.4f} ∠ {np.angle(if_c, deg=True):.2f}° kA')

    # Monofásico
    if curto == "M":
        print('\n')
        print('*' * 10, 'Curto Monofásico', '*' * 10)
        tipo_curto = "monofásico"
        ifa_0 = (Vf / (zkk_0 + zkk_1 + zkk_2 + (3 * zf)))
        ifa_1 = ifa_0
        ifa_2 = ifa_0

        if_a = if_a(ifa_0, ifa_1, ifa_2)
        if_b = if_b(ifa_0, ifa_1, ifa_2)
        if_c = if_c(ifa_0, ifa_1, ifa_2)

        print_defeitos(tipo_curto, z, if_a, if_b, if_c, I_base_curto)

    # Bifásico
    elif curto == "B":
        print('\n')
        print('*' * 15, 'Curto Bifásico', '*' * 15)
        tipo_curto = "bifásico"
        ifa_1 = Vf / (zkk_1 + zkk_2 + zf)
        ifa_2 = -ifa_1
        ifa_0 = 0 + 0j

        if_a = if_a(ifa_0, ifa_1, ifa_2)
        if_b = if_b(ifa_0, ifa_1, ifa_2)
        if_c = if_c(ifa_0, ifa_1, ifa_2)

        print_defeitos(tipo_curto, z, if_a, if_b, if_c, I_base_curto)

    # Bifásico-Terra
    elif curto == "BT":
        print('\n')
        print('*' * 15, 'Curto Bifásico-Terra', '*' * 15)
        tipo_curto = "bifásico-terra"
        ifa_1 = Vf / (zkk_1 + ((zkk_2 * (zkk_0 + 3 * zf)) / (zkk_2 + zkk_0 + 3 * zf)))
        ifa_2 = (-ifa_1) * ((zkk_0 + 3 * zf) / (zkk_0 + zkk_2 + 3 * zf))
        ifa_0 = (-ifa_1) * (zkk_2 / (zkk_0 + zkk_2 + 3 * zf))

        if_a = if_a(ifa_0, ifa_1, ifa_2)
        if_b = if_b(ifa_0, ifa_1, ifa_2)
        if_c = if_c(ifa_0, ifa_1, ifa_2)

        print_defeitos(tipo_curto, z, if_a, if_b, if_c, I_base_curto)

    # Trifásico
    elif curto == "T":
        print('\n')
        print('*' * 15, 'Curto Trifásico', '*' * 15)
        tipo_curto = "trifásico"
        ifa_1 = Vf / (zkk_1 + zf)
        ifa_2 = 0
        ifa_0 = 0

        if_a = Vf / zkk_1
        if_b = if_a * (a ** 2)
        if_c = if_a * a

        print_defeitos(tipo_curto, z, if_a, if_b, if_c, I_base_curto)

    # Verificação de entrada inválida
    else:
        print('Opção inválida, rode o código novamente!')

    ################################################################################

    "Calculando todas as tensões de sequência NÃO CORRIGIDAS em todas as barras"

    def calcular_tensoes_barras(z, Vf, ifa_0, ifa_1, ifa_2):
        tensoes = {}
        # Inicializa listas para armazenar os resultados
        Vja_0_lista = [0j] * len(V_base_barras)  # Inicializa com zeros para facilitar
        Vja_1_lista = [0j] * len(V_base_barras)  # Inicializa com zeros para facilitar
        Vja_2_lista = [0j] * len(V_base_barras)  # Inicializa com zeros para facilitar

        for barra in range(len(V_base_barras)):
            # Calcula as tensões de sequência para a barra em questão
            Zjk_0 = matriz_Zbarra_seqzero[barra][z]  # Z0 entre a barra atual e a barra em curto
            Zjk_1 = matriz_Zbarra_seqpos[barra][z]  # Z1 entre a barra atual e a barra em curto
            Zjk_2 = matriz_Zbarra_seqneg[barra][z]  # Z2 entre a barra atual e a barra em curto

            # Calcula as tensões de sequência
            Vja_0_resultado = Vja_0(Zjk_0, ifa_0)
            Vja_1_resultado = Vja_1(Vf, Zjk_1, ifa_1)
            Vja_2_resultado = Vja_2(Zjk_2, ifa_2)

            # Armazena os resultados nas listas na posição correta
            Vja_0_lista[barra] = Vja_0_resultado
            Vja_1_lista[barra] = Vja_1_resultado
            Vja_2_lista[barra] = Vja_2_resultado

            # Armazena os resultados
            tensoes[barra] = {
                f'V{barra}a (0)': Vja_0_resultado,
                f'V{barra}a (1)': Vja_1_resultado,
                f'V{barra}a (2)': Vja_2_resultado}

        return tensoes, Vja_0_lista, Vja_1_lista, Vja_2_lista

    # Chamada da função para calcular as tensões
    tensoes_barras, Vja_0_lista, Vja_1_lista, Vja_2_lista = calcular_tensoes_barras(z, Vf, ifa_0, ifa_1, ifa_2)

    def print_tensoes(tensoes_barras, V_base_barras):
        for barra, tensao in tensoes_barras.items():
            V_base = V_base_barras[barra]  # Obtém a tensão base para essa barra
            print(f'Tensões na barra {barra + 1}:')

            # Exibindo tensões de sequência com valor polar em p.u. e valor multiplicado em kV
            V_0 = tensao[f'V{barra}a (0)']
            print(f'V{barra + 1}a (0): {abs(V_0):.4f} ∠ {np.angle(V_0, deg=True):.2f}° p.u = '
                  f'{V_0.real:.4f} {"+" if V_0.imag >= 0 else "-"} {abs(V_0.imag):.4f}j p.u  '
                  f'>-- x {V_base:.4f} kV --> {abs(V_0 * V_base):.4f} ∠ {np.angle(V_0 * V_base, deg=True):.2f}° kV')

            V_1 = tensao[f'V{barra}a (1)']
            print(f'V{barra + 1}a (1): {abs(V_1):.4f} ∠ {np.angle(V_1, deg=True):.2f}° p.u = '
                  f'{V_1.real:.4f} {"+" if V_1.imag >= 0 else "-"} {abs(V_1.imag):.4f}j p.u  '
                  f'>-- x {V_base:.4f} kV --> {abs(V_1 * V_base):.4f} ∠ {np.angle(V_1 * V_base, deg=True):.2f}° kV')

            V_2 = tensao[f'V{barra}a (2)']
            print(f'V{barra + 1}a (2): {abs(V_2):.4f} ∠ {np.angle(V_2, deg=True):.2f}° p.u = '
                  f'{V_2.real:.4f} {"+" if V_2.imag >= 0 else "-"} {abs(V_2.imag):.4f}j p.u  '
                  f'>-- x {V_base:.4f} kV --> {abs(V_2 * V_base):.4f} ∠ {np.angle(V_2 * V_base, deg=True):.2f}° kV\n')


    # Chamada da função para exibir tensões no formato desejado
    print("\n\n-> Tensões de sequência não corrigidas\n")
    print_tensoes(tensoes_barras, V_base_barras)

    ################################################################################

    "Calculando todas as correntes de sequência NÃO CORRIGIDAS"

    # Cálculo das correntes de sequência positiva não corrigidas
    def calcular_correntes_sequencia_positiva(Vja_1, lista_imp_g_1, lista_imp_lt_1, lista_imp_m_1, lista_imp_s_1):
        Vf = 1  # Tensão de referência para o gerador
        correntes = []  # Lista para armazenar as correntes calculadas
        print("\n> Correntes de sequência positiva (não corrigidas):")

        # Calculo da corrente para geradores
        for gerador in lista_imp_g_1:
            bk, zg_1 = gerador['bk'], gerador['zg_1']
            corrente = (Vf - Vja_1[bk - 1]) / zg_1
            correntes.append({'tipo': 'gerador', 'bk': bk, 'corrente': corrente})

        # Calculo da corrente para linhas de transmissão
        for linha in lista_imp_lt_1:
            bk, bm, zlt_1 = linha['bk'], linha['bm'], linha['zlt_1']
            corrente = (Vja_1[bk - 1] - Vja_1[bm - 1]) / zlt_1
            correntes.append({'tipo': 'linha_transmissao', 'bk': bk, 'bm': bm, 'corrente': corrente})

        # Calculo da corrente para motores
        for motor in lista_imp_m_1:
            bk, zm_1 = motor['bk'], motor['zm_1']
            corrente = (Vf - Vja_1[bk - 1]) / zm_1
            correntes.append({'tipo': 'motor', 'bk': bk, 'corrente': corrente})

        # Calculo da corrente para shunts
        for shunt in lista_imp_s_1:
            bk, zs_1, tipo_shunt = shunt['bk'], shunt['zs_1'], shunt['tipo_shunt']
            corrente = Vja_1[bk - 1] / zs_1  # corrente em direção à carga
            correntes.append({'tipo': 'shunt', 'tipo_shunt': tipo_shunt, 'bk': bk, 'corrente': corrente})

        # Imprimir resultados formatados apenas para os elementos existentes
        if any(c['tipo'] == 'gerador' for c in correntes):
            print("\nCorrentes provenientes de Geradores:")
            for corrente in correntes:
                if corrente['tipo'] == 'gerador':
                    valor_corrente = corrente['corrente']
                    print(
                        f"Ig_{corrente['bk']} (1) = {valor_corrente.real:.4f} {'+' if valor_corrente.imag >= 0 else '-'} {abs(valor_corrente.imag):.4f}j "
                        f"= {abs(valor_corrente):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° p.u")

        if any(c['tipo'] == 'linha_transmissao' for c in correntes):
            print("\nCorrentes entre barras de Linhas de Transmissão:")
            for corrente in correntes:
                if corrente['tipo'] == 'linha_transmissao':
                    valor_corrente = corrente['corrente']
                    print(
                        f"Ilt_{corrente['bk']}-{corrente['bm']} (1) = {valor_corrente.real:.4f} {'+' if valor_corrente.imag >= 0 else '-'} {abs(valor_corrente.imag):.4f}j "
                        f"= {abs(valor_corrente):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° p.u")

        if any(c['tipo'] == 'motor' for c in correntes):
            print("\nCorrentes provenientes de Motores:")
            for corrente in correntes:
                if corrente['tipo'] == 'motor':
                    valor_corrente = corrente['corrente']
                    print(
                        f"Im_{corrente['bk']} (1) = {valor_corrente.real:.4f} {'+' if valor_corrente.imag >= 0 else '-'} {abs(valor_corrente.imag):.4f}j "
                        f"= {abs(valor_corrente):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° p.u")

        if any(c['tipo'] == 'shunt' for c in correntes):
            print("\nCorrentes nos Shunts:")
            tipos_shunt = {1: "Carga", 2: "Capacitor", 3: "Reator"}
            for tipo_shunt, nome_tipo in tipos_shunt.items():
                print(f"\nCorrentes nos Shunts tipo {nome_tipo}:")
                for corrente in correntes:
                    if 'tipo_shunt' in corrente and corrente['tipo_shunt'] == tipo_shunt:
                        valor_corrente = corrente['corrente']
                        print(
                            f"Is_{corrente['bk']} (1) = {valor_corrente.real:.4f} {'+' if valor_corrente.imag >= 0 else '-'} {abs(valor_corrente.imag):.4f}j "
                            f"= {abs(valor_corrente):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° p.u")

        return correntes  # Retorna a lista após a impressão

    # Cálculo das correntes de sequência negativa não corrigidas
    def calcular_correntes_sequencia_negativa(Vja_2, lista_imp_g_1, lista_imp_lt_1, lista_imp_m_1, lista_imp_s_1):
        correntes = []  # Lista para armazenar as correntes calculadas
        print("\n-> Correntes de sequência negativa (não corrigidas):")

        # Calculo da corrente para geradores
        for gerador in lista_imp_g_1:
            bk, zg_1 = gerador['bk'], gerador['zg_1']
            corrente = -Vja_2[bk - 1] / zg_1
            correntes.append({'tipo': 'gerador', 'bk': bk, 'corrente': corrente})

        # Calculo da corrente para linhas de transmissão
        for linha in lista_imp_lt_1:
            bk, bm, zlt_1 = linha['bk'], linha['bm'], linha['zlt_1']
            corrente = (Vja_2[bk - 1] - Vja_2[bm - 1]) / zlt_1
            correntes.append({'tipo': 'linha_transmissao', 'bk': bk, 'bm': bm, 'corrente': corrente})

        # Calculo da corrente para motores
        for motor in lista_imp_m_1:
            bk, zm_1 = motor['bk'], motor['zm_1']
            corrente = -Vja_2[bk - 1] / zm_1
            correntes.append({'tipo': 'motor', 'bk': bk, 'corrente': corrente})

        # Calculo da corrente para shunts
        for shunt in lista_imp_s_1:
            bk, zs_1, tipo_shunt = shunt['bk'], shunt['zs_1'], shunt['tipo_shunt']
            corrente = Vja_2[bk - 1] / zs_1
            correntes.append({'tipo': 'shunt', 'tipo_shunt': tipo_shunt, 'bk': bk, 'corrente': corrente})

        # Imprimir resultados formatados apenas para os elementos existentes
        if any(c['tipo'] == 'gerador' for c in correntes):
            print("\nCorrentes provenientes de Geradores:")
            for corrente in correntes:
                if corrente['tipo'] == 'gerador':
                    valor_corrente = corrente['corrente']
                    print(
                        f"Ig_{corrente['bk']} (2) = {valor_corrente.real:.4f} {'+' if valor_corrente.imag >= 0 else '-'} {abs(valor_corrente.imag):.4f}j "
                        f"= {abs(valor_corrente):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° p.u")

        if any(c['tipo'] == 'linha_transmissao' for c in correntes):
            print("\nCorrentes entre barras de Linhas de Transmissão:")
            for corrente in correntes:
                if corrente['tipo'] == 'linha_transmissao':
                    valor_corrente = corrente['corrente']
                    print(
                        f"Ilt_{corrente['bk']}-{corrente['bm']} (2) = {valor_corrente.real:.4f} {'+' if valor_corrente.imag >= 0 else '-'} {abs(valor_corrente.imag):.4f}j "
                        f"= {abs(valor_corrente):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° p.u")

        if any(c['tipo'] == 'motor' for c in correntes):
            print("\nCorrentes provenientes de Motores:")
            for corrente in correntes:
                if corrente['tipo'] == 'motor':
                    valor_corrente = corrente['corrente']
                    print(
                        f"Im_{corrente['bk']} (2) = {valor_corrente.real:.4f} {'+' if valor_corrente.imag >= 0 else '-'} {abs(valor_corrente.imag):.4f}j "
                        f"= {abs(valor_corrente):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° p.u")

        if any(c['tipo'] == 'shunt' for c in correntes):
            print("\nCorrentes nos Shunts:")
            tipos_shunt = {1: "Carga", 2: "Capacitor", 3: "Reator"}
            for tipo_shunt, nome_tipo in tipos_shunt.items():
                print(f"\nCorrentes nos Shunts tipo {nome_tipo}:")
                for corrente in correntes:
                    if 'tipo_shunt' in corrente and corrente['tipo_shunt'] == tipo_shunt:
                        valor_corrente = corrente['corrente']
                        print(
                            f"Is_{corrente['bk']} (2) = {valor_corrente.real:.4f} {'+' if valor_corrente.imag >= 0 else '-'} {abs(valor_corrente.imag):.4f}j "
                            f"= {abs(valor_corrente):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° p.u")

        return correntes  # Retorna a lista após a impressão

    # Cálculo das correntes de sequência zero não corrigidas
    def calcular_correntes_sequencia_zero(Vja_0, lista_imp_g_0, lista_imp_lt_0, lista_imp_m_0, lista_imp_s_0):
        correntes = []  # Lista para armazenar as correntes calculadas
        print("\n-> Correntes de sequência zero (não corrigidas):")

        # Calculo da corrente para geradores (sequência zero)
        for gerador in lista_imp_g_0:
            bk, zg_0 = gerador['bk'], gerador['zg_0']
            corrente = -Vja_0[bk - 1] / zg_0
            correntes.append({'tipo': 'gerador', 'bk': bk, 'corrente': corrente})

        # Calculo da corrente para linhas de transmissão (sequência zero)
        for linha in lista_imp_lt_0:
            bk, bm, zlt_0 = linha['bk'], linha['bm'], linha['zlt_0']
            corrente = (Vja_0[bk - 1] - Vja_0[bm - 1]) / zlt_0
            correntes.append({'tipo': 'linha_transmissao', 'bk': bk, 'bm': bm, 'corrente': corrente})

        # Calculo da corrente para motores (sequência zero)
        for motor in lista_imp_m_0:
            bk, zm_0 = motor['bk'], motor['zm_0']
            corrente = -Vja_0[bk - 1] / zm_0
            correntes.append({'tipo': 'motor', 'bk': bk, 'corrente': corrente})

        # Calculo da corrente para shunts (sequência zero)
        for shunt in lista_imp_s_0:
            bk, zs_0, tipo_shunt = shunt['bk'], shunt['zs_0'], shunt['tipo_shunt']
            corrente = Vja_0[bk - 1] / zs_0
            correntes.append({'tipo': 'shunt', 'tipo_shunt': tipo_shunt, 'bk': bk, 'corrente': corrente})

        # Imprimir resultados formatados apenas para os elementos existentes
        if any(c['tipo'] == 'gerador' for c in correntes):
            print("\nCorrentes provenientes de Geradores:")
            for corrente in correntes:
                if corrente['tipo'] == 'gerador':
                    valor_corrente = corrente['corrente']
                    print(
                        f"Ig_{corrente['bk']} (0) = {valor_corrente.real:.4f} {'+' if valor_corrente.imag >= 0 else '-'} {abs(valor_corrente.imag):.4f}j "
                        f"= {abs(valor_corrente):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° p.u")

        if any(c['tipo'] == 'linha_transmissao' for c in correntes):
            print("\nCorrentes entre barras de Linhas de Transmissão:")
            for corrente in correntes:
                if corrente['tipo'] == 'linha_transmissao':
                    valor_corrente = corrente['corrente']
                    print(
                        f"Ilt_{corrente['bk']}-{corrente['bm']} (0) = {valor_corrente.real:.4f} {'+' if valor_corrente.imag >= 0 else '-'} {abs(valor_corrente.imag):.4f}j "
                        f"= {abs(valor_corrente):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° p.u")

        if any(c['tipo'] == 'motor' for c in correntes):
            print("\nCorrentes provenientes de Motores:")
            for corrente in correntes:
                if corrente['tipo'] == 'motor':
                    valor_corrente = corrente['corrente']
                    print(
                        f"Im_{corrente['bk']} (0) = {valor_corrente.real:.4f} {'+' if valor_corrente.imag >= 0 else '-'} {abs(valor_corrente.imag):.4f}j "
                        f"= {abs(valor_corrente):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° p.u")

        if any(c['tipo'] == 'shunt' for c in correntes):
            print("\nCorrentes nos Shunts:")
            tipos_shunt = {1: "Carga", 2: "Capacitor", 3: "Reator"}
            for tipo_shunt, nome_tipo in tipos_shunt.items():
                print(f"\nCorrentes nos Shunts tipo {nome_tipo}:")
                for corrente in correntes:
                    if 'tipo_shunt' in corrente and corrente['tipo_shunt'] == tipo_shunt:
                        valor_corrente = corrente['corrente']
                        print(
                            f"Is_{corrente['bk']} (0) = {valor_corrente.real:.4f} {'+' if valor_corrente.imag >= 0 else '-'} {abs(valor_corrente.imag):.4f}j "
                            f"= {abs(valor_corrente):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° p.u")

        return correntes  # Retorna a lista após a impressão

    # Chamada das funções para exibir as correntes no formato desejado
    correntes_calculadas_sequencia_positiva = calcular_correntes_sequencia_positiva(Vja_1_lista, lista_imp_g_1,
                                                                                    lista_imp_lt_1, lista_imp_m_1, lista_imp_s_1)
    correntes_calculadas_sequencia_negativa = calcular_correntes_sequencia_negativa(Vja_2_lista, lista_imp_g_1,
                                                                                    lista_imp_lt_1, lista_imp_m_1, lista_imp_s_1)
    correntes_calculadas_sequencia_zero = calcular_correntes_sequencia_zero(Vja_0_lista, lista_imp_g_0,
                                                                                    lista_imp_lt_0, lista_imp_m_0, lista_imp_s_0)

    ################################################################################

    "Calculando todas as tensões de sequência CORRIGIDAS para cada barra"

    def calcular_tensoes_barras_corrigidas(z, ifa_0, ifa_1, ifa_2):
        tensoes = {}
        # Inicializa listas para armazenar os resultados
        Vja_0_lista = [0j] * len(V_base_barras)  # Inicializa com zeros para facilitar
        Vja_1_lista = [0j] * len(V_base_barras)  # Inicializa com zeros para facilitar
        Vja_2_lista = [0j] * len(V_base_barras)  # Inicializa com zeros para facilitar

        for barra in range(len(V_base_barras)):
            # Calcula as tensões de sequência para a barra em questão
            Zjk_0 = matriz_Zbarra_seqzero[barra][z]  # Z0 entre a barra atual e a barra em curto
            Zjk_1 = matriz_Zbarra_seqpos[barra][z]  # Z1 entre a barra atual e a barra em curto
            Zjk_2 = matriz_Zbarra_seqneg[barra][z]  # Z2 entre a barra atual e a barra em curto

            # Calcula as tensões de sequência multiplicadas pela defasagem
            Vja_0_resultado = Vja_0(Zjk_0, ifa_0)
            Vja_1_resultado = Vja_1(Vf, Zjk_1, ifa_1) * cmath.rect(1, math.radians(Multi_def[z][barra]))
            Vja_2_resultado = Vja_2(Zjk_2, ifa_2) * cmath.rect(1, math.radians(Multi_def[barra][z]))

            # Armazena os resultados nas listas na posição correta
            Vja_0_lista[barra] = Vja_0_resultado
            Vja_1_lista[barra] = Vja_1_resultado
            Vja_2_lista[barra] = Vja_2_resultado

            # Armazena os resultados
            tensoes[barra] = {
                f'V{barra}a (0)': Vja_0_resultado,
                f'V{barra}a (1)': Vja_1_resultado,
                f'V{barra}a (2)': Vja_2_resultado}

        return tensoes, Vja_0_lista, Vja_1_lista, Vja_2_lista

    # Chamada da função para calcular as tensões
    tensoes_barras_corrigidas, Vja_0_lista_corrigida, Vja_1_lista_corrigida, Vja_2_lista_corrigida = calcular_tensoes_barras_corrigidas(
        z, ifa_0, ifa_1, ifa_2)

    print("\n ->Tensões de sequência corrigidas")
    # Chamada da função para exibir tensões no formato desejado
    print_tensoes(tensoes_barras_corrigidas, V_base_barras)

    ################################################################################

    "Calculando todas as correntes de sequência CORRIGIDAS"

    # Cálculo das correntes corrigidas de Seq +
    def calcular_correntes_sequencia_positiva_corrigidas(Vja_1, lista_imp_g_1, lista_imp_lt_1, lista_imp_m_1,
                                                         lista_imp_s_1, z):
        Vf = 1  # Tensão de referência para o gerador
        correntes_corrigidas = []  # Lista para armazenar as correntes corrigidas

        # Calculo da corrente para geradores
        for gerador in lista_imp_g_1:
            bk, zg_1 = gerador['bk'], gerador['zg_1']
            corrente = ((Vf - Vja_1[bk - 1]) / zg_1) * cmath.rect(1, math.radians(Multi_def[z][bk - 1]))
            correntes_corrigidas.append({'tipo': 'gerador', 'bk': bk, 'corrente': corrente})

        # Calculo da corrente para linhas de transmissão
        for linha in lista_imp_lt_1:
            bk, bm, zlt_1 = linha['bk'], linha['bm'], linha['zlt_1']
            corrente = ((Vja_1[bk - 1] - Vja_1[bm - 1]) / zlt_1) * cmath.rect(1, math.radians(Multi_def[z][bk - 1]))
            correntes_corrigidas.append({'tipo': 'linha_transmissao', 'bk': bk, 'bm': bm, 'corrente': corrente})

            # Calculo da corrente para motores
        for motor in lista_imp_m_1:
            bk, zm_1 = motor['bk'], motor['zm_1']
            corrente = ((Vf - Vja_1[bk - 1]) / zm_1) * cmath.rect(1, math.radians(Multi_def[z][bk - 1]))
            correntes_corrigidas.append({'tipo': 'motor', 'bk': bk, 'corrente': corrente})

        # Calculo da corrente para shunts
        for shunt in lista_imp_s_1:
            bk, zs_1, tipo_shunt = shunt['bk'], shunt['zs_1'], shunt['tipo_shunt']
            corrente = (Vja_1[bk - 1] / zs_1) * cmath.rect(1, math.radians(Multi_def[z][bk - 1]))
            correntes_corrigidas.append({'tipo': 'shunt', 'tipo_shunt': tipo_shunt, 'bk': bk, 'corrente': corrente})

        return correntes_corrigidas

    # Cálculo das correntes de sequência negativa corrigidas
    def calcular_correntes_sequencia_negativa_corrigidas(Vja_2, lista_imp_g_1, lista_imp_lt_1, lista_imp_m_1,
                                                         lista_imp_s_1, z):
        correntes_corrigidas = []  # Lista para armazenar as correntes corrigidas

        # Calculo da corrente para geradores
        for gerador in lista_imp_g_1:
            bk, zg_1 = gerador['bk'], gerador['zg_1']
            corrente = -Vja_2[bk - 1] / zg_1
            # Aplica a defasagem se o gerador não está na barra do curto nem na mesma área
            if areas_por_barra[bk - 1] != areas[z] and bk - 1 != z:
                corrente *= cmath.rect(1, math.radians(Multi_def[bk - 1][z]))
            correntes_corrigidas.append({'tipo': 'gerador', 'bk': bk, 'corrente': corrente})

        # Calculo da corrente para linhas de transmissão
        for linha in lista_imp_lt_1:
            bk, bm, zlt_1 = linha['bk'], linha['bm'], linha['zlt_1']
            corrente = (Vja_2[bk - 1] - Vja_2[bm - 1]) / zlt_1
            # Aplica a defasagem se as barras não estão na mesma área nem são a barra do curto
            if areas_por_barra[bk - 1] != areas[z] and areas_por_barra[bm - 1] != areas[
                z] and bk - 1 != z and bm - 1 != z:
                corrente *= cmath.rect(1, math.radians(Multi_def[bk - 1][z]))
            correntes_corrigidas.append({'tipo': 'linha_transmissao', 'bk': bk, 'bm': bm, 'corrente': corrente})

        # Calculo da corrente para motores
        for motor in lista_imp_m_1:
            bk, zm_1 = motor['bk'], motor['zm_1']
            corrente = (-Vja_2[bk - 1] / zm_1) * cmath.rect(1, math.radians(Multi_def[bk - 1][z]))
            correntes_corrigidas.append({'tipo': 'motor', 'bk': bk, 'corrente': corrente})

        # Calculo da corrente para shunts
        for shunt in lista_imp_s_1:
            bk, zs_1, tipo_shunt = shunt['bk'], shunt['zs_1'], shunt['tipo_shunt']
            corrente = (Vja_2[bk - 1] / zs_1) * cmath.rect(1, math.radians(Multi_def[bk - 1][z]))
            correntes_corrigidas.append({'tipo': 'shunt', 'tipo_shunt': tipo_shunt, 'bk': bk, 'corrente': corrente})

        return correntes_corrigidas

    # Cálculo das correntes corrigidas de Seq 0
    def calcular_correntes_sequencia_zero_corrigidas(Vja_0, lista_imp_g_0, lista_imp_lt_0, lista_imp_m_0,
                                                     lista_imp_s_0):
        correntes_corrigidas = []  # Lista para armazenar as correntes corrigidas

        # Calculo da corrente para geradores (sequência zero)
        for gerador in lista_imp_g_0:
            bk, zg_0 = gerador['bk'], gerador['zg_0']
            corrente = -Vja_0[bk - 1] / zg_0
            correntes_corrigidas.append({'tipo': 'gerador', 'bk': bk, 'corrente': corrente})

        # Calculo da corrente para linhas de transmissão (sequência zero)
        for linha in lista_imp_lt_0:
            bk, bm, zlt_0 = linha['bk'], linha['bm'], linha['zlt_0']
            corrente = (Vja_0[bk - 1] - Vja_0[bm - 1]) / zlt_0
            correntes_corrigidas.append({'tipo': 'linha_transmissao', 'bk': bk, 'bm': bm, 'corrente': corrente})

        # Calculo da corrente para motores
        for motor in lista_imp_m_0:
            bk, zm_0 = motor['bk'], motor['zm_0']
            corrente = -Vja_0[bk - 1] / zm_0
            correntes_corrigidas.append({'tipo': 'motor', 'bk': bk, 'corrente': corrente})

        # Calculo da corrente para shunts
        for shunt in lista_imp_s_0:
            bk, zs_0, tipo_shunt = shunt['bk'], shunt['zs_0'], shunt['tipo_shunt']
            corrente = Vja_0[bk - 1] / zs_0
            correntes_corrigidas.append({'tipo': 'shunt', 'tipo_shunt': tipo_shunt, 'bk': bk, 'corrente': corrente})

        return correntes_corrigidas


    correntes_calculadas_sequencia_positiva_corrigidas = calcular_correntes_sequencia_positiva_corrigidas(Vja_1_lista, lista_imp_g_1,
                                                                                                        lista_imp_lt_1, lista_imp_m_1, lista_imp_s_1, z)
    correntes_calculadas_sequencia_negativa_corrigidas = calcular_correntes_sequencia_negativa_corrigidas(Vja_2_lista, lista_imp_g_1,
                                                                                                        lista_imp_lt_1, lista_imp_m_1, lista_imp_s_1, z)
    correntes_calculadas_sequencia_zero_corrigidas = calcular_correntes_sequencia_zero_corrigidas(Vja_0_lista, lista_imp_g_0,
                                                                                                        lista_imp_lt_0, lista_imp_m_0, lista_imp_s_0)

    def print_correntes(correntes, I_base_barras):
        for corrente in correntes:
            tipo = corrente['tipo']
            bk = corrente['bk']
            valor_corrente = corrente['corrente']
            # Determina o I_base correto
            I_base = I_base_barras[bk - 1]  # Subtrai 1 porque as barras são indexadas a partir de 0
            I_base_rounded = round(I_base, 4)

            if tipo == 'gerador':
                print(
                    f"Ig_{bk} = {valor_corrente.real:.4f} {'+' if valor_corrente.imag >= 0 else '-'} {abs(valor_corrente.imag):.4f}j p.u "
                    f"= {abs(valor_corrente):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° p.u "
                    f">-- x {I_base_rounded} kA --> {abs(valor_corrente * I_base):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° kA")

            elif tipo == 'linha_transmissao':
                bm = corrente['bm']
                print(
                    f"Ilt_{bk}-{bm} = {valor_corrente.real:.4f} {'+' if valor_corrente.imag >= 0 else '-'} {abs(valor_corrente.imag):.4f}j p.u "
                    f"= {abs(valor_corrente):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° p.u "
                    f">-- x {I_base_rounded} kA --> {abs(valor_corrente * I_base):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° kA")

            elif tipo == 'motor':
                print(
                    f"Im_{bk} = {valor_corrente.real:.4f} {'+' if valor_corrente.imag >= 0 else '-'} {abs(valor_corrente.imag):.4f}j p.u "
                    f"= {abs(valor_corrente):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° p.u "
                    f">-- x {I_base_rounded} kA --> {abs(valor_corrente * I_base):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° kA")

            elif 'tipo_shunt' in corrente:  # Para shunts
                tipo_shunt = corrente['tipo_shunt']
                tipos_shunt = {1: "Carga", 2: "Capacitor", 3: "Reator"}
                nome_tipo = tipos_shunt[tipo_shunt]  # Como `tipo_shunt` sempre é válido, não há fallback
                print(
                    f"Is_{bk} ({nome_tipo}) = {valor_corrente.real:.4f} {'+' if valor_corrente.imag >= 0 else '-'} {abs(valor_corrente.imag):.4f}j p.u "
                    f"= {abs(valor_corrente):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° p.u "
                    f">-- x {I_base_rounded} kA --> {abs(valor_corrente * I_base):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° kA")

    print("\n-> Correntes de sequência positiva corrigidas:")
    print_correntes(correntes_calculadas_sequencia_positiva_corrigidas, I_base_barras)

    print("\n-> Correntes de sequência negativa corrigidas:")
    print_correntes(correntes_calculadas_sequencia_negativa_corrigidas, I_base_barras)

    print("\n-> Correntes de sequência zero corrigidas:")
    print_correntes(correntes_calculadas_sequencia_zero_corrigidas, I_base_barras)

    ################################################################################

    "Cálculo das tensões das barras em cada fase"
    # Cálculo das tensões de fase corrigidas
    def calcular_tensoes_fase(Vja_0_lista_corrigida, Vja_1_lista_corrigida, Vja_2_lista_corrigida):
        Vja, Vjb, Vjc = [], [], []

        for V0, V1, V2 in zip(Vja_0_lista_corrigida, Vja_1_lista_corrigida, Vja_2_lista_corrigida):
            Vja.append(V_a(V0, V1, V2))
            Vjb.append(V_b(V0, V1, V2))
            Vjc.append(V_c(V0, V1, V2))

        return Vja, Vjb, Vjc

    # Chamando a função para obter as listas de tensões corrigidas nas fases A, B e C
    Vja, Vjb, Vjc = calcular_tensoes_fase(Vja_0_lista_corrigida, Vja_1_lista_corrigida, Vja_2_lista_corrigida)

    def print_tensoes_fase(Vja, Vjb, Vjc, V_base_barras):
        print("\n\n-> Tensões de fase em cada barra:\n")
        for idx, (Va, Vb, Vc) in enumerate(zip(Vja, Vjb, Vjc), start=1):
            V_base = V_base_barras[idx - 1]  # Obtém a tensão base para essa barra
            print(f"Tensões na barra {idx}:")

            # Exibindo tensões de fase com valor polar antes do kV
            print(f"  V{idx} (A): {Va.real:.4f} {'+' if Va.imag >= 0 else '-'} {abs(Va.imag):.4f}j p.u  "
                  f"= {abs(Va):.4f} ∠ {np.angle(Va, deg=True):.2f}° p.u  "
                  f">-- x {V_base:.4f} kV --> {abs(Va * V_base):.4f} ∠ {np.angle(Va, deg=True):.2f}° kV")

            print(f"  V{idx} (B): {Vb.real:.4f} {'+' if Vb.imag >= 0 else '-'} {abs(Vb.imag):.4f}j p.u  "
                  f"= {abs(Vb):.4f} ∠ {np.angle(Vb, deg=True):.2f}° p.u  "
                  f">-- x {V_base:.4f} kV --> {abs(Vb * V_base):.4f} ∠ {np.angle(Vb, deg=True):.2f}° kV")

            print(f"  V{idx} (C): {Vc.real:.4f} {'+' if Vc.imag >= 0 else '-'} {abs(Vc.imag):.4f}j p.u  "
                  f"= {abs(Vc):.4f} ∠ {np.angle(Vc, deg=True):.2f}° p.u  "
                  f">-- x {V_base:.4f} kV --> {abs(Vc * V_base):.4f} ∠ {np.angle(Vc, deg=True):.2f}° kV\n")

    # Chamando a função para exibir as tensões de fase
    print_tensoes_fase(Vja, Vjb, Vjc, V_base_barras)

    ################################################################################

    "Cálculo das correntes referentes a cada fase"
    # Função principal para calcular as correntes nas fases A, B e C
    def calcular_correntes_fase(correntes_seq_pos, correntes_seq_neg, correntes_seq_zero):
        I_a_list, I_b_list, I_c_list = [], [], []

        # Cálculo da corrente para geradores (Fase A, B e C)
        for pos, neg, zero in zip(correntes_seq_pos, correntes_seq_neg, correntes_seq_zero):
            if pos['tipo'] == 'gerador' and neg['tipo'] == 'gerador' and zero['tipo'] == 'gerador':
                bk = pos['bk']
                I_a_val = I_a(zero['corrente'], pos['corrente'], neg['corrente'])
                I_b_val = I_b(zero['corrente'], pos['corrente'], neg['corrente'])
                I_c_val = I_c(zero['corrente'], pos['corrente'], neg['corrente'])
                I_a_list.append({'tipo': 'gerador', 'bk': bk, 'corrente': I_a_val})
                I_b_list.append({'tipo': 'gerador', 'bk': bk, 'corrente': I_b_val})
                I_c_list.append({'tipo': 'gerador', 'bk': bk, 'corrente': I_c_val})

            # Cálculo da corrente para linhas de transmissão (Fase A, B e C)
        for pos, neg, zero in zip(correntes_seq_pos, correntes_seq_neg, correntes_seq_zero):
            if pos['tipo'] == 'linha_transmissao' and neg['tipo'] == 'linha_transmissao' and zero[
                'tipo'] == 'linha_transmissao':
                bk, bm = pos['bk'], pos['bm']
                I_a_val = I_a(zero['corrente'], pos['corrente'], neg['corrente'])
                I_b_val = I_b(zero['corrente'], pos['corrente'], neg['corrente'])
                I_c_val = I_c(zero['corrente'], pos['corrente'], neg['corrente'])
                I_a_list.append({'tipo': 'linha_transmissao', 'bk': bk, 'bm': bm, 'corrente': I_a_val})
                I_b_list.append({'tipo': 'linha_transmissao', 'bk': bk, 'bm': bm, 'corrente': I_b_val})
                I_c_list.append({'tipo': 'linha_transmissao', 'bk': bk, 'bm': bm, 'corrente': I_c_val})

        # Cálculo da corrente para motores (Fase A, B e C)
        for pos, neg, zero in zip(correntes_seq_pos, correntes_seq_neg, correntes_seq_zero):
            if pos['tipo'] == 'motor' and neg['tipo'] == 'motor' and zero['tipo'] == 'motor':
                bk = pos['bk']
                I_a_val = I_a(zero['corrente'], pos['corrente'], neg['corrente'])
                I_b_val = I_b(zero['corrente'], pos['corrente'], neg['corrente'])
                I_c_val = I_c(zero['corrente'], pos['corrente'], neg['corrente'])
                I_a_list.append({'tipo': 'motor', 'bk': bk, 'corrente': I_a_val})
                I_b_list.append({'tipo': 'motor', 'bk': bk, 'corrente': I_b_val})
                I_c_list.append({'tipo': 'motor', 'bk': bk, 'corrente': I_c_val})

        # Cálculo da corrente para shunts (Fase A, B e C)
        for pos, neg, zero in zip(correntes_seq_pos, correntes_seq_neg, correntes_seq_zero):
            if pos['tipo'] == 'shunt' and neg['tipo'] == 'shunt' and zero['tipo'] == 'shunt':
                bk = pos['bk']
                tipo_shunt = pos['tipo_shunt']  # Tipo de shunt (1, 2 ou 3)
                I_a_val = I_a(zero['corrente'], pos['corrente'], neg['corrente'])
                I_b_val = I_b(zero['corrente'], pos['corrente'], neg['corrente'])
                I_c_val = I_c(zero['corrente'], pos['corrente'], neg['corrente'])
                I_a_list.append({'tipo': 'shunt', 'tipo_shunt': tipo_shunt, 'bk': bk, 'corrente': I_a_val})
                I_b_list.append({'tipo': 'shunt', 'tipo_shunt': tipo_shunt, 'bk': bk, 'corrente': I_b_val})
                I_c_list.append({'tipo': 'shunt', 'tipo_shunt': tipo_shunt, 'bk': bk, 'corrente': I_c_val})

        return I_a_list, I_b_list, I_c_list

    # Executa a função para calcular as correntes de fase A, B e C
    I_a, I_b, I_c = calcular_correntes_fase(correntes_calculadas_sequencia_positiva_corrigidas,
                                            correntes_calculadas_sequencia_negativa_corrigidas,
                                            correntes_calculadas_sequencia_zero_corrigidas)

    def print_correntes_fase(correntes, I_base_barras, fase):
        print(f"\n> Correntes na fase {fase}:")
        for corrente in correntes:
            tipo = corrente['tipo']
            bk = corrente['bk']
            valor_corrente = corrente['corrente']

            # Determina o I_base correto
            I_base = I_base_barras[bk - 1]  # Subtrai 1 porque as barras são indexadas a partir de 0
            I_base_rounded = round(I_base, 4)

            # Exibindo o valor em cartesiano e polar p.u., seguido pelo valor multiplicado pelo I_base em kA
            if tipo == 'gerador':
                print(f"Ig_{bk} ({fase}) = {valor_corrente.real:.4f} "
                      f"{'+' if valor_corrente.imag >= 0 else '-'} {abs(valor_corrente.imag):.4f}j p.u "
                      f"= {abs(valor_corrente):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° p.u "
                      f">-- x {I_base_rounded} kA --> {abs(valor_corrente * I_base):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° kA")

            elif tipo == 'linha_transmissao':
                bm = corrente['bm']
                print(f"Ilt_{bk}-{bm} ({fase}) = {valor_corrente.real:.4f} "
                      f"{'+' if valor_corrente.imag >= 0 else '-'} {abs(valor_corrente.imag):.4f}j p.u "
                      f"= {abs(valor_corrente):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° p.u "
                      f">-- x {I_base_rounded} kA --> {abs(valor_corrente * I_base):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° kA")

            elif tipo == 'motor':
                print(f"Im_{bk} ({fase}) = {valor_corrente.real:.4f} "
                      f"{'+' if valor_corrente.imag >= 0 else '-'} {abs(valor_corrente.imag):.4f}j p.u "
                      f"= {abs(valor_corrente):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° p.u "
                      f">-- x {I_base_rounded} kA --> {abs(valor_corrente * I_base):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° kA")

            elif 'tipo_shunt' in corrente:  # Para shunts
                tipo_shunt = corrente['tipo_shunt']  # 'tipo_shunt' sempre estará presente em correntes de shunt
                tipos_shunt = {1: "Carga", 2: "Capacitor", 3: "Reator"}
                nome_tipo = tipos_shunt[tipo_shunt]  # Como `tipo_shunt` é válido, não há fallback
                print(f"Is_{bk} ({nome_tipo} - {fase}) = {valor_corrente.real:.4f} "
                      f"{'+' if valor_corrente.imag >= 0 else '-'} {abs(valor_corrente.imag):.4f}j p.u "
                      f"= {abs(valor_corrente):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° p.u "
                      f">-- x {I_base_rounded} kA --> {abs(valor_corrente * I_base):.4f} ∠ {np.angle(valor_corrente, deg=True):.2f}° kA")

    # Executa a função para calcular e imprimir as correntes de fase A, B e C
    print_correntes_fase(I_a, I_base_barras, 'A')
    print_correntes_fase(I_b, I_base_barras, 'B')
    print_correntes_fase(I_c, I_base_barras, 'C')

    ################################################################################
    # Perguntar ao usuário se deseja verificar outra barra
    repetir = input("\n\nDeseja verificar o curto em outra barra? (S/N): ").upper()
    if repetir == 'N':
        print("Encerrando o programa. Obrigado!")
        break
    elif repetir != 'S':
        print("Opção inválida. Encerrando o programa por segurança.")
        break
