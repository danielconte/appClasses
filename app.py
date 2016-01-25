#!-*- encoding: utf8 -*-
from nltk.corpus import floresta
from collections import defaultdict

def contarPalavras(textoP):
    total = 0
    gramatica = 0
    uml = 0
    for frase in textoP:
        novaFrase = []
        aux = ""
        for palavra in frase:
            total = total + 1
            if palavra[1] !='0':
                gramatica = gramatica + 1
            if palavra[2] !='':
                uml = uml + 1
    print("|Total:" + str(total))
    print("|Gramática:" + str(gramatica) + " (" + str(gramatica * 100 / total) + "%)")
    print("|UML:" + str(uml) + " (" + str(uml * 100 / total) + "%)")   

def simplificar(t):
    if "+" in t:
        return t[t.index("+")+1:]
    else:
        return t
        
palavrasM = floresta.tagged_words()
palavrasM = [(palavra.lower(),simplificar(classificacao)) for (palavra,classificacao) in palavrasM]

def classificarPalavra(palavra):
    tipos = [];
    for par in palavrasM:
        if par[0]==palavra.decode('utf-8'):
            tipos.append(par[1])
    if len(tipos) > 0:
        d = defaultdict(int)
        for i in tipos:
            d[i] += 1
        classe = max(d.iteritems(), key=lambda x: x[1])
        return(classe[0])
    else:
        return("0")
        
def carregarArquivo(nome):
    texto = open(nome);
    texto = texto.read().replace("\n",".").replace(";",".").replace(","," ").replace("  "," ")
    texto = texto.replace("..",".").replace("  "," ").replace("..",".").replace(". ",".")
    texto = texto.replace("(","").replace(")","")
    frase = texto.split(".")
    textoSeparado = []
    for parte in frase:
        textoSeparado.append(parte.split(" "))
    return textoSeparado  

def classificarFrase(frase):   
    fraseClassificada = []      
    for palavra in frase:        
        fraseClassificada.append([palavra,classificarPalavra(palavra),""])
    return fraseClassificada    

def classificarTexto():
    texto = carregarArquivo("texto.txt")
    textoClassificado = []
    for frase in texto:
        textoClassificado.append(classificarFrase(frase))
    return textoClassificado
 
def regra1(textoP): #nomes viram classes	
    texto = []
    for frase in textoP:
        novaFrase = []
        for palavra in frase:
            if palavra[1]=="n":
                elemento = "C"
            else:
                elemento = palavra[2]
            novaFrase.append([palavra[0],palavra[1],elemento])
        texto.append(novaFrase)	
    return texto	
	
def regra2(textoP): #nomes seguidos viram atributos
    texto = []
    for frase in textoP:
        novaFrase = []
        aux = ""
        for palavra in frase:
            if palavra[2]=="C" and aux =="":
                aux = "C"
            else:
                if palavra[2]=="C" and (aux=="C" or aux=="A"):
                    aux = "A"
                else:
                    aux = ""
            novaFrase.append([palavra[0],palavra[1],aux])
        texto.append(novaFrase)	
    return texto
        
def regra3(textoP): #nomes especicias não são classes
    texto = []
    excecoes = ["registro","sistema","informação","histórico","relatório","organização"]   
    for frase in textoP:
        novaFrase = []
        aux = ""
        for palavra in frase:
            if palavra[0] in excecoes:
                aux = "3"
            else:              
                aux = palavra[2]
            novaFrase.append([palavra[0],palavra[1],aux])
        texto.append(novaFrase)	
    return texto    
    
def regra4(textoP): #nomes próprios são desconsiderados
    texto = [] 
    for frase in textoP:
        novaFrase = []
        palavra = frase[0]
        novaFrase.append([palavra[0],palavra[1],palavra[2]])
        aux = ""
        frase.pop(0)
        for palavra in frase:
            if palavra[0].istitle():
                aux = "4"
            else:
                aux = palavra[2]
            novaFrase.append([palavra[0],palavra[1],aux])
        texto.append(novaFrase)	
    return texto  
    
def regra5(textoP): #verbos são operações
    texto = [] 
    for frase in textoP:
        novaFrase = []
        for palavra in frase:
            if palavra[1][0] == "v" and palavra[2] == "" :
                aux = "O"
            else:
                aux = palavra[2]
            novaFrase.append([palavra[0],palavra[1],aux])
        texto.append(novaFrase)	
    return texto        

def regra6(textoP): #adjetivos são atributos
    texto = [] 
    for frase in textoP:
        novaFrase = []
        for palavra in frase:
            if palavra[1] == "adj" :
                aux = "A"
            else:
                aux = palavra[2]
            novaFrase.append([palavra[0],palavra[1],aux])
        texto.append(novaFrase)	
    return texto     
    
def regra7(textoP): #verbos de ligação são desconsiderados
    texto = []       
    verbos = open("verbos.txt");
    verbos = verbos.read()
    verbos = verbos.split(", ") 
    for frase in textoP:
        novaFrase = []
        aux = ""
        for palavra in frase:
            if palavra[0] in verbos and palavra[1][0] == 'v':
                aux = "5"
            else:              
                aux = palavra[2]
            novaFrase.append([palavra[0],palavra[1],aux])
        texto.append(novaFrase)	
    return texto  
    
def regra8(textoP): #atributos compostos/complexos
    texto  = []
    for frase in textoP:
        novaFrase = []
        excecoes = ["número","data","identificador","tipo","nome","números","datas","identificadores","tipos","nomes","telefone","RG","CPF"]
        aux = ""
        auxC = ""
        for palavra in frase:
            if aux == "" and palavra[0] not in excecoes:  
                novaFrase.append([palavra[0],palavra[1],palavra[2]])
            elif palavra[0] in excecoes:
                if aux != "":                    
                    novaFrase.append([aux,"8","A"])
                aux = palavra[0]
            elif aux != "":
                if palavra[1] == "adj":
                    novaFrase.append([aux + " " + palavra[0],palavra[1],"A"])
                    aux = ""
                elif palavra[1] == "prp":
                    aux = aux + " " + palavra[0]
                    auxC = "prp"
                elif palavra[1] == "n" and auxC == "prp":
                    novaFrase.append([aux + " " + palavra[0],palavra[1],"A"])
                    aux = ""
                else: 
                    novaFrase.append([palavra[0],palavra[1],palavra[2]])
                    novaFrase.append([aux,"8","A"])
                    aux = ""                        
        texto.append(novaFrase)
    return texto         
   
    
def organizarClasses(textoP): #identifica as classes e as separa, remove plurais regra9
    lista = [] 
    for frase in textoP:
        for palavra in frase:
            if palavra[2] == "C" and palavra[0] not in lista:
                if palavra[0] + "s" not in lista and palavra[0]:  
                    if palavra[0] + "s" in lista:
                        lista.remove(palavra[0] + "s")
                        lista.append(palavra[0])                  
                    else:                        
                        auxP = palavra[0][:-1]
                        if auxP not in lista:
                            lista.append(palavra[0])
    for classe in lista:
        classesP.append(classe)        
        
def prepararTexto(textoP):
    texto = []
    novaFrase = []        
    for frase in textoP:
        for palavra in frase:
            if palavra[0] != "":
                if palavra[2] == "C":
                    texto.append(novaFrase)
                    novaFrase = []
                novaFrase.append([palavra[0],palavra[1],palavra[2]])
    return texto            
     
   
def vincularAtributos(textoP):    #regra10
    for classeP in classesP:
        atributosP = []
        operacoesP = []
        for frase in textoP:            
            fraseP = frase
            aux = "N"
            for palavra in frase:
                if (classeP == palavra[0]) or (classeP + "s" == palavra[0]):
                    aux = "S"                            
                if aux == "S":                
                    if palavra[2] == "A" and palavra[0] not in atributosP:
                        atributosP.append(palavra[0])
                    if palavra[2] == "O" and palavra[0] not in operacoesP:
                        operacoesP.append(palavra[0])
        classes.append([classeP,atributosP,operacoesP])   

def imprimirClasses():
    print("Classes----------------------------------")
    for classe in classes:    
        
        if classe[1] or classe[2]:
            print(classe[0])
 
        

classesP = []
classes = [] #[nomeClasse,[atributos],[operações]]
  
textoFinal = classificarTexto()

textoFinal = regra1(textoFinal)
textoFinal = regra2(textoFinal)
textoFinal = regra3(textoFinal)
textoFinal = regra4(textoFinal)
textoFinal = regra5(textoFinal)
textoFinal = regra6(textoFinal)
textoFinal = regra7(textoFinal)
textoFinal = regra8(textoFinal)


#textoFinal = prepararTexto(textoFinal)
organizarClasses(textoFinal)
vincularAtributos(textoFinal)

imprimirClasses()

#print("Contagem__________________________________")
contarPalavras(textoFinal)