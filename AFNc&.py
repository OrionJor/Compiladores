def operadores(char):
    TodosOperadores = '+*.'
    for i in range(0, len(TodosOperadores)):
        if char == TodosOperadores[i]:
            valor = True
            return True
        else:
            valor = False
    return (valor)

class Automato(object):

    def __init__(self):
        self.alfabeto = None
        self.estados = Estados()
        self.estados = []
        self.qtEstados = None
        self.Transicoes = []
        self.estadoInicial = None
        self.estadosFinal = None

class Estados(object):

    def __init__(self):
        self.nome = 0

def baseF(simbolo):
    base = Automato()
    base.alfabeto = simbolo
    base.qtEstados = 2
    base.estados = [Estados()] * base.qtEstados
    base.estados[0] = Estados()
    base.estados[1] = Estados()
    base.estados[0].nome = 0
    base.estados[1].nome = 1
    base.Transicoes.append([simbolo, base.estados[0], base.estados[1]])
    base.estadoInicial = base.estados[0]
    base.estadosFinal = base.estados[1]
    return base

def uneAlfabetos(a, b):
    return a + b

def distibuiChars(lista, lista2):
    for i in range(0, len(lista)):
        lista2.append(lista[i])
    return lista2

def concatenacao(A, B):
    novo = Automato()
    novo.alfabeto = uneAlfabetos(A.alfabeto, B.alfabeto)
    novo.qtEstados = A.qtEstados + B.qtEstados

    for j in range(0, len(A.Transicoes)):
        novo.Transicoes.append([A.Transicoes[j][0], A.Transicoes[j][1], A.Transicoes[j][2]])

    for j in range(0, len(A.estados)):
        novo.estados.append(A.estados[j])

    novo.Transicoes.append(["&", A.estadosFinal, B.estadoInicial])

    for j in range(0, len(B.Transicoes)):
        novo.Transicoes.append([B.Transicoes[j][0], B.Transicoes[j][1], B.Transicoes[j][2]])

    for j in range(0, len(B.estados)):
        novo.estados.append(B.estados[j])


    novo.estadoInicial = novo.estados[0]
    novo.estadosFinal = novo.estados[-1]

    for i in range(0, len(novo.estados)):
        novo.estados[i].nome = i

    return novo

def uniao(A, B):
    novo = Automato()
    novo.alfabeto = uneAlfabetos(A.alfabeto, B.alfabeto)
    novo.qtEstados = A.qtEstados + B.qtEstados + 2
    newEstadoI = Estados()
    newEstadoF = Estados()

    novo.estados.append(newEstadoI)

    for j in range(0, len(A.Transicoes)):
        novo.Transicoes.append([A.Transicoes[j][0], A.Transicoes[j][1], A.Transicoes[j][2]])

    for j in range(0, len(A.estados)):
        novo.estados.append(A.estados[j])

    for j in range(0, len(B.Transicoes)):
        novo.Transicoes.append([B.Transicoes[j][0], B.Transicoes[j][1], B.Transicoes[j][2]])

    for j in range(0, len(B.estados)):
        novo.estados.append(B.estados[j])

    novo.estados.append(newEstadoF)
    novo.Transicoes.append(["&", novo.estados[0], A.estadoInicial])
    novo.Transicoes.append(["&", novo.estados[0], B.estadoInicial])
    novo.Transicoes.append(["&", A.estadosFinal, novo.estados[-1]])
    novo.Transicoes.append(["&", B.estadosFinal, novo.estados[-1]])
    novo.estadoInicial = novo.estados[0]
    novo.estadosFinal = novo.estados[-1]

    for i in range(0, len(novo.estados)):
        novo.estados[i].nome = i

    return novo

def fechoDeKleene(Ak):
    novo = Automato()
    novo.alfabeto = uneAlfabetos(Ak.alfabeto, "")
    novo.qtEstados = Ak.qtEstados + 2
    newEstadoI = Estados()
    newEstadoF = Estados()

    novo.estados.append(newEstadoI)

    for j in range(0, len(Ak.Transicoes)):
        novo.Transicoes.append([Ak.Transicoes[j][0], Ak.Transicoes[j][1], Ak.Transicoes[j][2]])

    for j in range(0, len(Ak.estados)):
        novo.estados.append(Ak.estados[j])

    novo.estados.append(newEstadoF)

    novo.Transicoes.append(["&", novo.estados[0], Ak.estadoInicial])
    novo.Transicoes.append(["&", novo.estados[0], novo.estados[-1]])
    novo.Transicoes.append(["&", Ak.estadoInicial, Ak.estadosFinal])
    novo.Transicoes.append(["&", Ak.estadosFinal, novo.estados[-1]])

    novo.estadoInicial = novo.estados[0]
    novo.estadosFinal = novo.estados[-1]

    for i in range(0, len(novo.estados)):
        novo.estados[i].nome = i

    return novo

def percorreExpressao(expressao):
    pilha = []
    for i in range(0, len(expressao)):
        if not operadores(expressao[i]):
            pilha.append(baseF(expressao[i]))
        elif operadores(expressao[i]):
            if (expressao[i] == "*"):
                op1 = pilha.pop(-1)
                pilha.append(fechoDeKleene(op1))
            else:
                op2 = pilha.pop(-1)
                if pilha:
                    op1 = pilha.pop(-1)
                    if expressao[i] == ".":
                        pilha.append(concatenacao(op1, op2))
                    elif expressao[i] == "+":
                        pilha.append(uniao(op1, op2))
    return pilha

def olhaPilha(pilha):
    final = "\n-######## AUTOMATO FINITO NAO DETERMINISTICO COM MOV. & ########\n"
    for i in range(0, len(pilha[0].Transicoes)):
        final = final + str(pilha[0].Transicoes[i][0]) + "---------------------------->      " + str(
            pilha[0].Transicoes[i][1].nome) + "q<->q" + str(pilha[0].Transicoes[i][2].nome) + "\n"
    return final



from notacaoposfixa import infixaParaPosfixa
expressao = infixaParaPosfixa("a+b")
print(olhaPilha(percorreExpressao(expressao)))


pilha = percorreExpressao(expressao)

print("\n####################AUTOMATO FINITO NAO DETERMINISTICO COM MOV. &###########################\n")
for b in range(len(pilha[0].Transicoes)):
    if pilha[0].estados[b].nome == 0:
        print("(->q", pilha[0].estados[b].nome, ",", pilha[0].Transicoes[b][0], ")" "= {q",
              pilha[0].Transicoes[b][2].nome, "}")
    else:
        print("(q", pilha[0].estados[b].nome, ",", pilha[0].Transicoes[b][0], ")" "= {q",
              pilha[0].Transicoes[b][2].nome, "}")