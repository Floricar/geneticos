import random
def crearpoblacioninicial(p, dom_d, dom_h, l_cromosoma):
    muestra = []
    for i in range(0,p):
        r = random.randint(dom_d ,dom_h) #Extraccion de muestra aleatoria
        r = bin(r)  #Conversion a binario
        r = r.split('0b')[1]    
        if (len(r)<l_cromosoma):
            a = l_cromosoma - len(r)
            r = '0'* a + r
        muestra.append(r)
    return muestra

def funcionobjetivo(r):
    r = int(r, 2)
    f = (float(r)/1073741823)**2 #Funcion objetivo harcodeada (se debe editar segun el problema en particular)
    return f

def seleccionruleta(fitness):
    giros = len(fitness)
    s = []
    ruleta = []
    maximo = 0
    maximo_i = 0
    y = 0
    for i in range(len(fitness)):   #Por cada cromosoma ajusto su fitness y armo la ruleta
        aux = round(fitness[i],2) 
        aux = aux*100   #redondeo y lo paso a un numero entero entre 0 y 100
        aux = int(aux)
        for j in range(0,aux):
            ruleta.append(i)
        if (maximo<aux): 
            maximo = aux
            maximo_i = i
    if(len(ruleta)<100): #Ajusto la ruleta para que no quede menor a 100 por el redondeo
        y = 100-len(ruleta)
        for k in range(0,y):
            ruleta.append(maximo_i)
    for i in range(0,giros): #Giro la ruleta
        r = random.randint(0,99)
        s.append(ruleta[r])
    return s

def cruzar_1p(p1, p2, rango):
    pos = random.randint(0,rango-1)
    p1 = str(p1)    #Mediante auxiliares corto en dos las cadenas de los padres
    p1_aux1 = p1[0:pos]
    p1_aux2 = p1[pos:]
    p2 = str(p2)
    p2_aux1 = p2[0:pos]
    p2_aux2 = p2[pos:]
    p1 = p1_aux1 + p2_aux2 #y las cambio entre ellas segun una posicion (pos) random
    p2 = p2_aux1 + p1_aux2
    res = []
    res.append(p1)
    res.append(p2)
    return res

def mutar_invertida(hijo_m, rango):
    hijo_m = str(hijo_m)
    pos = random.randint(0,rango-1) #Se identifica si hay que cambniar un 0 o un 1 en la posicion random
    if (hijo_m[pos]=="0"):
        hijo_m_aux1 = hijo_m[0:pos] #Se guarda desde el inicio hasta la pos random
        hijo_m_aux2 = hijo_m[pos+1:] #Se guarda desde una posicion +1 hasta el final
        hijo_m = hijo_m_aux1 + "1" + hijo_m_aux2 #Se suma aux1, se agrega el 1 y el aux2
    elif (hijo_m[pos]=="1"):
        hijo_m_aux1 = hijo_m[0:pos] #Mismo procedimiento que el anterior
        hijo_m_aux2 = hijo_m[pos+1:]
        hijo_m = hijo_m_aux1 + "0" + hijo_m_aux2
    return hijo_m

def ordenar_asc(array1, array2):
    #array1 = fobj; array2 = pob
    length = len(array1) - 1
    sorted = False

    while not sorted:
        sorted = True
        for i in range(length):
            if array1[i] < array1[i+1]:
                sorted = False
                array1[i], array1[i+1] = array1[i+1], array1[i]
                array2[i], array2[i+1] = array2[i+1], array2[i]
    
    return array1, array2


def main():
    #INICIALIZO LOS VALORES DE LOS PARAMETROS
    dom_desde = 0 # Dominio desde
    dom_hasta = 1073741823 #Dominio hasta
    l_crom = 30 #Longitud de los cromosomas
    pobi = 10 #Poblacion inicial (solo numeros pares)
    cr = 0.75 #Probabilidad de crossover
    mu = 0.05 #Probabilidad de mutacion
    ciclos = 20 #Cantidad de ciclos del programa
    m_selec = "ruleta" #Metodo de seleccion
    m_cr = "1punto" #Metodo de crossover
    m_mu = "invertida" #Metodo de mutacion
    elit = True #Bandera de si se realiza elitismo o no
    r_elit = 3  #Cantidad de cromosomas en el grupo elite

    #CREO PRIMER POBLACION
    pob = crearpoblacioninicial(p = pobi, dom_d=dom_desde, dom_h=dom_hasta, l_cromosoma=l_crom)
    
    #CREO REPOSITORIO .csv PARA EL GUARDADO DE LOS RESULTADOS INTERMEDIOS -> UTILIZADO PARA EL INFORME FINAL
    saveFile = open('resultados.csv','a')
    saveFile.write("Generacion")
    saveFile.write(',')
    saveFile.write("Maximo")
    saveFile.write(',')
    saveFile.write("Minimo")
    saveFile.write(',')
    saveFile.write("Sumatoria")
    saveFile.write(',')
    saveFile.write("Promedio")
    saveFile.write('\n')
    saveFile.close
    
    #COMIENZAN LOS CICLOS
    for c in range(0, ciclos):
        fobj = []
        suma = 0
        for i in range(pobi): 
            #Calculo de la funcion objetivo
            f = funcionobjetivo(pob[i]) 
            fobj.append(f)
            suma = suma + f
        maximo = max(fobj)
        minimo = min(fobj)
        promedio = suma/pobi
        saveFile = open('resultados.csv','a')
        saveFile.write(str(c+1))
        saveFile.write(',')
        saveFile.write(str(maximo))
        saveFile.write(',')
        saveFile.write(str(minimo))
        saveFile.write(',')
        saveFile.write(str(suma))
        saveFile.write(',')
        saveFile.write(str(promedio))
        saveFile.write('\n')
        saveFile.close
        
        if(c==ciclos-1):
            print max(fobj)
            break
        if elit:
            fobj, pob = ordenar_asc(fobj, pob)
            elite = []
            for i in range(r_elit):
                elite.append(pob[i])
            if c == 0:
                pobi = pobi - r_elit

        #Calculo fitness
        fobj_fitnes = [] 
        x = 0   
        for i in range(pobi):
            x = fobj[i]/suma
            fobj_fitnes.append(x)
                
        #Hacemos la seleccion
        if (m_selec == "ruleta"):
            seleccionados = seleccionruleta(fitness=fobj_fitnes)
        
        #Reproduccion
        actos = len(seleccionados)/2
        hijos = []
        
        #Crossover
        for i in range(0,actos):           
            h = []
            r_cr = random.random()
            if (r_cr <= cr):
                if(m_cr == "1punto"):
                    h = cruzar_1p(p1=pob[int(seleccionados[i])], p2=pob[int(seleccionados[i+actos])], rango=l_crom)
            else:
                h.append(pob[int(seleccionados[i])])
                h.append(pob[int(seleccionados[i+actos])])
            hijos.append(h[0])
            hijos.append(h[1])
        
        #Mutacion
        for i in range(len(hijos)):
            r_mu = random.random()
            if(r_mu <= mu):
                if(m_mu == "invertida"):
                    hijos[i] = mutar_invertida(hijo_m = hijos[i], rango=l_crom)
        
        #Siguiente generacion
        if elit:
            pob = hijos + elite
        else:
            pob = hijos
        
            

if __name__ == '__main__':
    main()