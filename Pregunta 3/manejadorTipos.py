import copy
from itertools import permutations
from functools import reduce
from math import gcd

#Clase que representa los tipos atomicos quienes poseen:
class TipoAtomico:
    def __init__(self,nombre, representacion, alineacion):
        self.nombre = nombre                    #Su nombre accion[0]
        self.representacion = representacion    #Su representacion (numero de bytes que ocupa)
        self.alineacion = alineacion            #Su alineacion (numero de bytes a los que debe estar alineado)

    #Metodo que representa como string un objeto TipoAtomico
    def __repr__(self):
        return "Tipo Atomico: {}; Representacion: {} bytes; Alineacion: {} bytes.".format(self.nombre,self.representacion, self.alineacion)

#Clase que representa los registros (structs), y estos poseen:
class Registro:
    def __init__(self, nombre, lista_tipos, representacion= None, alineacion = None, nro_bytes_desperdiciados = None, lista_tipos_aux = None):
        self.nombre = nombre                    #Su nombre
        self.lista_tipos = lista_tipos          #La lista de tipos atomicos y registros (structs o unions) que definen sus campos
        self.representacion = representacion    #Su representacion (numero de bytes que ocupa)
        self.alineacion = alineacion            #Su alineacion (numero de bytes a los que debe estar alineado)
        self.nro_bytes_desperdiciados = nro_bytes_desperdiciados #El numero de bytes que se desperdician en su interior (si es que se desperdicia alguno)
        self.lista_tipos_aux = lista_tipos_aux  #Una conveniente lista auxiliar de sus tipos y registros que usaremos para guardar
                                                #la configuración en la que se guardan estos en los casos "empaquetado", "sin empaquetar" y "optimizado"
                                                                

#Clase representa los registros variantes (unions) y estos poseen:
class RegistroVariante:
    def __init__(self, nombre, lista_tipos, representacion = None, alineacion = None):
        self.nombre = nombre                     #Su nombre
        self.lista_tipos = lista_tipos           #La lista de tipos atomicos y registros (structs o unions) que definen sus campos
        self.representacion = representacion     #Su representacion (numero de bytes que ocupa)
        self.alineacion = alineacion             #Su alineacion (numero de bytes a los que debe estar alineado)

#Diccionario en el que tendremos todos los tipos atomicos que se ingresen/definan en en manejador
t_atomicos = dict()

#Diccionario en el que tendremos todos los registros (structs) que se ingresen/definan en en manejador
reg_structs = dict()

#Diccionario en el que tendremos todos los registros variantes (unions) que se ingresen/definan en en manejador
reg_var_unions = dict()

#Funcion con la que verificamos si el nombre del tipo atomico o registro (struct o union) que se quiere ingresar ya ha sido previamente
#definido en el manejador (y por lo tanto se encuentra en alguno de los diccionarios antes definidos) y se informa el error.
def definido(accion):
    if(accion[1] in t_atomicos.keys()):
        print("ERROR: El nombre que intenta usar ya pertenece a un tipo atomico definido.")
        return True
    if(accion[1] in reg_structs.keys()):
        print("ERROR: El nombre que intenta usar ya pertenece a un registro (struct) definido.")
        return True
    if(accion[1] in reg_var_unions.keys()):
        print("ERROR: El nombre que intenta usar ya pertenece a un registro variante (union) definido.")
        return True
    return False

#Funcion para ingresar el tipo atomico que se esta creando/definiendo en el diccionario correspondiente (t_atomicos).
#La clave sera el "<nombre>" y el valor sera el objeto "TipoAtomico" correspondiente.
def crear_tipo_atomico(accion): 

    #Si el nombre del tipo a definir no se encuentra en el manejador (no se definio ya antes)
    if not(definido(accion)):   
        #Procedemos a insertar el nuevo tipo atomico     
        t_atomicos[accion[1]] = TipoAtomico(accion[1],accion[2], accion[3])
    else:
        return False

#Funcion para ingresar registros o registros variantes, que se estan creando/definiendo, en sus respectivos diccionarios (reg_structs y reg_var_unions).
#La clave sera, de la lista [<tipo>], el "<tipo>" (especificamente el "<nombre del tipo>" correspondiente al <tipo> en cuestion).
#Y el valor sera:
#Para los registros (struct), el objeto "Registro" correspondiente.
#Para los registros variantes (unions), el objeto "RegistroVariante" correspondiente.
def crear_reg_o_reg_var(accion):
    
    #Si el nombre del registro (struct o union) a definir no se encuentra en el manejador (no se definio ya antes) 
    if not(definido(accion)):

        #Para cada tipo de la lista de tipos que define los campos del registro
        for tipo in accion[2:]: 

            #Si el tipo no se encuentra ni en el diccionario de tipos atomicos, ni en el de registros, ni en el de registros variantes
            #entonces se ha introducido un tipo que no existe.
            if tipo not in t_atomicos.keys() and tipo not in reg_structs.keys() and tipo not in reg_var_unions.keys():
                print(f"ERROR: El tipo <{tipo}> que se introdujo en el {accion[0]}, no existe", end="\n")
                return False
        
        #Verificamos el nivel de anidamiento de los registros :'v
        if (anidamiento(accion)):
            return print("ERROR (Vamo' a calmano'): Se excedio el nivel maximo de anidamiento que podemos manejar (u.u).")
        
        #Arreglo en el que tendremos los objetos TipoAtomico, Registro o RegistroVariante que corresponden a los tipos en
        #la lista de tipos del registro en cuestion
        lista_tipos_objetos = [] 

        #Para cada tipo en la lista de tipos que define los campos del registro 
        for tipo in accion[2:]:

            #Si el tipo se encuentra en el diccionario de tipos atomicos entonces
            if(tipo in t_atomicos.keys()):

                #Ingresamos en "lista_tipos_objetos", el objeto TipoAtomico correspondiente a ese tipo
                lista_tipos_objetos.append(t_atomicos[tipo])

            #Sino, si el tipo se encuentra en el diccionario de registros (structs) entonces
            elif(tipo in reg_structs.keys()):

                #Ingresamos en "lista_tipos_objetos", el objeto Registro correspondiente a ese tipo
                lista_tipos_objetos.append(reg_structs[tipo])

            #De lo contrario, si el tipo se encuentra en el diccionario de registros variantes (unions) entonces
            else:

                #Ingresamos en "lista_tipos_objetos", el objeto RegistroVariante correspondiente a ese tipo
                lista_tipos_objetos.append(reg_var_unions[tipo])

        #Si la accion que realizamos es STRUCT
        if(accion[0] == "struct"):

            #Creamos el objeto Registro del nuevo Struct que estamos creando/definiendo
            registro = Registro(accion[1], lista_tipos_objetos)
            
            #Ingresamos al diccionario de registros al nuevo registro. 
            reg_structs[accion[1]] = registro

        #Si la accion que realizamos es UNION
        else:
            #Creamos el objeto RegistroVariante del nuevo Union que estamos creando/definiendo
            nuevo_registro = RegistroVariante(accion[1], lista_tipos_objetos)

            #Ingresamos al diccionario de registros variantes al nuevo registro variante. 
            reg_var_unions[accion[1]] = nuevo_registro

#Funcion para verificar que el nivel de anidamiento de registros (structs y unions) es el que podemos
#manejar de momento :'v    
def anidamiento(accion):
    
    #Para cada tipo en la lista de tipos que define los campos del registro 
    for tipo in accion[2:]:

        #Si el tipo se encuentra en el diccionario de tipos atomicos entonces
        if(tipo in t_atomicos.keys()):
            
            #Tomamos el objeto TipoAtomico para ese tipo (del diccionario)
            objeto = t_atomicos[tipo]

        #Sino, si el tipo se encuentra en el diccionario de registros (structs) entonces
        elif(tipo in reg_structs.keys()):

            #Tomamos el objeto Registro para ese tipo (del diccionario)
            objeto = reg_structs[tipo]

        #De lo contrario, si el tipo se encuentra en el diccionario de registros variantes (unions) entonces
        else:
            objeto = reg_var_unions[tipo]
        
        #Si el objeto es del tipo Registro (struct) o del tipo RegistroVariante (union)
        if type(objeto) is Registro or type(objeto) is RegistroVariante:

            #Si verificamos y dentro de el registro en cuestion encontramos que, en su lista de tipos tiene algun otro "struct" o "union"
            if(tiene_registro_struct(objeto.lista_tipos) or tiene_reg_var_union(objeto.lista_tipos)):

                #retornamos true porque entonces hay mas de 1 nivel de anidamiento de registros
                return True

    #Si no hay mas de 1 nivel de anidamiento retornamos false (si :'v de momento solo funciono con 1 nivel de anidamiento)
    return False

#Funcion que verifica si en la lista de tipos de un registro (struct o union) hay algun otro struct
#Y retorna un arreglo con todos los structs que tiene el registro en su lista de tipos
def tiene_registro_struct(lista_tipos):
    structs = []
    
    #Recorremos todos los tipos en la lista de tipos
    for tipo in lista_tipos:

        #Si el tipo se encuentra en el diccionario de registros (structs)
        if tipo.nombre in reg_structs.keys():

            #Agregamos ese tipo en el arreglo de structs
            structs.append(tipo)

    return structs

#Funcion que verifica si en la lista de tipos de un registro (struct o union) hay algun otro union
#Y retorna un arreglo con todos los unions que tiene el registro en su lista de tipos
def tiene_reg_var_union(lista_tipos):
    unions = []

    #Recorremos todos los tipos en la lista de tipos
    for tipo in lista_tipos:

        #Si el tipo se encuentra en el diccionario de registros variantes (unions)
        if tipo.nombre in reg_var_unions.keys():

            #Agregamos ese tipo en el arreglo de unions
            unions.append(tipo)

    return unions

#Funcion que organiza los registros, en general, de forma empaquetada (no importa la alineacion)
#y retorna una lista con los tipos en ese orden (registro_empaquetado)
def empaquetado(lista_tipos):
    registro_empaquetado = []

    #Volteamos la lista de tipos por conveniencia
    lista_tipos = lista_tipos[::-1]

    #Mientras que tengamos tipos en la lista
    while lista_tipos:

        #Hacemos pop() para sacar el ultimo tipo de la lista (por esta razon la volteamos antes, ya que
        #ahora al hacer pop estaremos sacando los tipos de la lista en el orden en el que fueron ingresados
        #cuando se creo el registro)
        tipo = lista_tipos.pop()

        #Guardamos en esta variable la representacion del tipo que acabamos de extraer de la lista de tipos
        representacion = int(tipo.representacion)

        #Tambien tomamos el nombre de dicho tipo
        nombre = tipo.nombre

        #Utilizando el nombre del tipo y verificamos:
        #Si es un tipo atomico o un registro variante (union)
        if nombre in t_atomicos.keys() or nombre in reg_var_unions.keys():

            #Utilizamos la representacion del tipo para introducirlo en la lista "registro_empaquetado"
            #tantas veces como lo indica su representacion.
            while representacion:
                registro_empaquetado.append(tipo)
                representacion -= 1

        #De lo contrario, si el tipo es un struct, entonces vamos a insertar una tupla con el tipo y su
        #lista auxiliar de tipos "(tipo, lista_tipos_aux)"" definida para los objetos "Registros".

        #Se menciono al crear la clase Registro que esta lista auxiliar guardara la configuracion de los campos
        #del registro (definidos por la lista de tipos) segun el caso en el que nos encontraramos. Asi que, como
        #este es el caso empaquetado esta lista guardara la lista de tipos con la configuracion "empaquetada", es decir
        #todos los tipos se guardan uno al lado del otro sin respetar las alineaciones.
        else:             
            registro_empaquetado.append((tipo,tipo.lista_tipos_aux))
          
    return registro_empaquetado
  
#Funcion que organiza los registros, en general, para el caso sin empaquetar (aqui si importa la alineacion)
#y retorna una lista con los tipos en ese orden (registro_sin_empaquetar)
def sin_empaquetar(lista_tipos):
    registro_sin_empaquetar = []

    #Volteamos la lista de tipos por conveniencia tal y como hicimos en el caso "empaquetado"
    lista_tipos = lista_tipos[::-1]
    
    #Mientras que tengamos tipos en la lista
    while lista_tipos:

        #Hacemos pop() para sacar el ultimo tipo de la lista (como hicimos en el caso empaquetado) aprovechado
        #que como volteamos la lista de tipos, estaremos sacando los tipos de la lista en el orden en el que fueron ingresados
        #cuando se creo el registro
        tipo = lista_tipos.pop()

        #Guardamos en esta variable la representacion del tipo
        representacion = int(tipo.representacion)

        #Tambien guardamos su alineacion (ya que esta vez si hay que considerarla)
        alineacion = int(tipo.alineacion)

        #Y tambien tomamos en esta variable su nombre
        nombre = tipo.nombre 

        #Si la longitud de la lista "registro_sin_empaquetar" modulo la alineacion del tipo que quiero insertar, es 0
        #(es decir que la longitud del registro sin empaquetar que estamos construyendo, es multiplo de la alineacion del tipo
        #que le queremos introducir), esto significa que la posicion en el registro en la que voy a colocar al tipo es valida
        #ya que respeta la alineacion de dicho tipo
        if len(registro_sin_empaquetar) % alineacion == 0:

            #Entonces utilizando el nombre del tipo
            #Si este es un tipo atomico o un registro variante (union)
            if nombre in t_atomicos.keys() or nombre in reg_var_unions.keys():

                #Utilizamos la representacion del tipo para introducirlo en la lista "registro_sin_empaquetar"
                #tantas veces como lo indica su representacion.
                while representacion:
                    registro_sin_empaquetar.append(tipo)
                    representacion -= 1
            
            #De lo contrario, si el tipo es un struct, entonces vamos a insertar una tupla con el tipo y su
            #lista auxiliar de tipos "(tipo, lista_tipos_aux)" definida para los objetos "Registros".

            #Tal y como hicimos en el caso empaquetado, usaremos la lista auxiliar del registro que, en este caso
            #guardaremos la lista de tipos con la configuracion "sin empaquetar", es decir que todos los campos del
            #registro se definen con los tipos que seran guardados respetando las alineaciones.
            else:
                registro_sin_empaquetar.append((tipo,tipo.lista_tipos_aux))

        #En caso de que no se cumpla la condicion del modulo, esto significa que tendre posiciones vacias en el registro
        #(bytes desperdiciados) hasta que llegue a una posicion dentro de este que cumpla con la alineacion del tipo y
        #donde entonces pueda colocarlo
        else:
            #De manera que procedemos a rellenar con 0 (con el que representaremos esos espacios desperdiciados)
            #hasta que la longitud del registro, y por ende la posicion en la que introducire al tipo, sea el adecuado
            #segun la alineacion correspondiente
            while len(registro_sin_empaquetar) % alineacion != 0 :
                registro_sin_empaquetar.append(0)

            #Cuando tengamos la posicion adecuada segun la alineacion, tras rellenar con 0
            ##Si el tipo es un tipo atomico o un registro variante (union)
            if nombre in t_atomicos.keys() or nombre in reg_var_unions.keys():

                #Utilizamos la representacion del tipo para introducirlo en el "registro_sin_empaquetar"
                #tantas veces como lo indica su representacion.
                while representacion:
                    registro_sin_empaquetar.append(tipo)
                    representacion -= 1
            else:
             
                #De lo contrario, si el tipo es un struct, entonces vamos a insertar una tupla con el tipo y su
                #lista auxiliar de tipos "(tipo, lista_tipos_aux)"" definida para los objetos "Registros" y que
                #contendra la configuracion de los campos del registro definida por los tipos en el orden que
                #cumple con la alineacion (caso sin empaquetar).
                registro_sin_empaquetar.append((tipo,tipo.lista_tipos_aux))
                      
    return registro_sin_empaquetar

#Funcion que genera todas las permutaciones posibles de los campos de los registros y busca el mejor caso, es decir,
#aquella configuracion de los tipos en el registro que respete sus alineaciones pero que minimice la memoria, en otras
#palabras, que desperdicie la menor cantidad de bytes posible
#bytes posible
def optimizado(nombre):
    permutaciones_sin_empaquetar = []

    #Si el tipo se encuentra en el diccionario de registros (structs)
    if nombre in reg_structs.keys():

        #Copiamos la lista de tipos del tipo en cuestion
        lista_tipos_copia = copy.deepcopy(reg_structs[nombre].lista_tipos)

        #Obtenemos la lista de todas las permutaciones posibles de los tipos en el registro al hacer "list(perumations(lista_tipos_copia))"
        #Es decir, tenemos todas las posibles configuraciones en las que se le pudieron haber pasado al registro los tipos que definen sus campos.
        #(tipos que se encuentran en su lista_tipos particular) Y entonces recorremos cada una de estas.
        for permutacion in list(permutations(lista_tipos_copia)):
            
            #Por cada permutacion, creamos su variante "sin empaquetar" que cumple con las alineaciones de los tipos segun el orden en el que
            #fueron ingresados en el registro en dicha permutacion e insertamos esta variante sin empaquetar de la permutacion en una lista
            #(permutaciones_sin_empaquetar), por lo cual tendremos una lista de listas (lista de permutaciones sin empaquetar)
            permutaciones_sin_empaquetar.append(sin_empaquetar(list(permutacion)))

        #Utilizamos la funcion "desperdicio_representacion_reg" para obtener la representacion de la primera permutacion sin empaquetar del registro
        #que estamos procesando en busqueda de su configuracion optima y a su vez obtenemos la cantidad de bytes desperdiciados en la misma
        representacion_optima, minimo_bytes_desperdiciados = desperdicio_representacion_reg(permutaciones_sin_empaquetar[0])
        
        #A su vez en esta variable guardamos esa misma primera permutacion sin empaquetar como la optima
        permutacion_optima = permutaciones_sin_empaquetar[0]

        #Para cada permutacion sin empaquetar, del registro, en la lista
        for permutacion in permutaciones_sin_empaquetar:

            #Obtenemos su representacion y la cantidad de bytes que desperdicia     
            representacion, bytes_desperdiciados = desperdicio_representacion_reg(permutacion)

            #Si los bytes desperdiciados en la permutacion son menos que los de la permutacion que teniamos antes como "optima", entonces
            if(bytes_desperdiciados < minimo_bytes_desperdiciados):

                #La menor cantidad de bytes desperdiciados pasa a ser la de la permutacion actual
                minimo_bytes_desperdiciados = bytes_desperdiciados

                #La permutacion optima cambia a la que tenemos actualmente
                permutacion_optima = permutacion

                #La representacion de la permutacion optima cambia a la que tenemos actualmente
                representacion_optima = representacion

        #print("representacion optima: ",representacion_optima)
        #print("longitud de permutacion optima: ",len(permutacion_optima))

        #Retornamos la permutacion optima y su representacion
        return permutacion_optima, representacion_optima

#Funcion que se encarga de tomar los campos del registro definidos por sus tipos, toma todos los registros internos que pueda tener
#el registro en sus respectivos campos y procede a calcular cuantos bytes se estan desperdiciando en el registro (sumando el desperdicio de los
# registros internos con el desperdicio que tenga el externo) y tambien calcula la representacion del registro sumando su representacion inicial
#con la de los registros internos y restando 1 por cada registro interno que posee (ya que en el registro externo estos se representan en un solo
#campo con su nombre y por lo tanto debemos restar esas apariciones para tener la representacion verdadera del registro en cuestion)
def desperdicio_representacion_reg(registro):

    #Variable donde guardamos la cantidad de 0 que tiene el registro que estamos procesando
    #Es decir, la cantidad de bytes desperdiciados
    bytes_desperdiciados = registro.count(0)

    #Variable en la que guardaremos la representacion final del registro que estamos procesando
    representacion_final = 0

    #Variable donde guardaremos el nro de registros internos que posee el registro que estamos procesando
    nro_registros_internos = 0

    #Variable donde guardamos la longitud que tiene el registro que procesamos inicialmente.
    #Esta sera parte de su representación (que obtendremos luego de procesar sus structs internos)
    longitud_registro = len(registro)
    
    #Lista que contiene todos los registros que tiene dentro el registro que procesamos
    registros_internos = [reg_interno for reg_interno in registro if type(reg_interno) is tuple]

    #Recorremos cada registro interno del registro que estamos procesando de la lista que creamos antes
    for reg_interno in registros_internos:

        #Aumentamos en uno el contador de registros internos
        nro_registros_internos += 1

        #A la longitud del registro le sumamos la longitud del registro interno, actualizando de esa manera la
        #longitud del registro que estamos procesando
        longitud_registro += len(reg_interno[1])

        #Actualizamos la cantidad de bytes desperdiciados en el registro que estamos procesando, sumándole
        #la cantidad de bytes que se desperdician en el registro interno que procesamos en la iteración actual
        bytes_desperdiciados += reg_interno[1].count(0)

    #Al salir del ciclo podremos obtener la representacion real del registro que estuvimos procesando, restando la longitud
    #del registro actual (luego del procesamiento que le hicimos con el ciclo) menos el numero de registros internos que tenía
    #el que procesamos
    representacion_final = longitud_registro - nro_registros_internos

    #Retornamos la representacion final del registro y los bytes desperdiciados
    return  representacion_final, bytes_desperdiciados

#Funcion utilizada para describir un tipo atomico, registro o registro variante, indicando su tamano, alineacion
#y cantidad de bytes desperdiciados para los casos "empaquetado", "sin empaquetar" y "optimizado".

#Notese que lista_tipos_aux es un atributo que contiene su representacion dependiendo de cada caso,
#Es decir, empaquetado, no empaquetado y optimizado previamente (reordenado)
def describir(nombre):

    #Si lo que se paso para describir es un tipo atomico, entonces simplemente imprimimos su informacion
    if nombre in t_atomicos.keys():
        print(t_atomicos[nombre])
        return repr(t_atomicos[nombre])

    #Si lo que se paso para describir es un registro (struct) entonces:
    elif nombre in reg_structs.keys():
       
        #En esta variable tomamos la lista de tipos que definen los campos del registro
        lista_tipos_reg = reg_structs[nombre].lista_tipos  

        #Chequeamos si tiene registros (structs) internos y los guardamos en esta variable     
        structs_internos = tiene_registro_struct(lista_tipos_reg)

        #Chequeamos si tiene registros variantes (unions) internos y los guardamos en esta variable
        unions_internos = tiene_reg_var_union(lista_tipos_reg)
        
        print("********************************************************************************************************")
        print("************************************ CASO REGISTRO (STRUCT) EMPAQUETADO ********************************")
        print("********************************************************************************************************")
        print()

        #Si en efecto el registro tiene registros (structs) internos
        if(structs_internos):

            #Por cada registro struct en la lista de registros internos
            for struct in structs_internos:

                #Como este es el caso empaquetado, tomamos la lista de tipos del struct interno y con la funcion
                #"empaquetado" ordenamos sus campos sin hacer caso a las alineaciones de los tipos para proceder a guardar
                #la configuracion "empaquetada" del registro en la lista auxiliar del struct interno (recordemos que en esta siempre
                #tendremos los tipos del registro en la configuracion del caso, en este caso en la forma empaquetada)
                struct.lista_tipos_aux = empaquetado(struct.lista_tipos) 

                #Calculamos la representacion del struct interno y la guardamos en su respectivo atributo
                struct.representacion = len(struct.lista_tipos_aux)

        #Si en efecto el registro tiene registros variantes (unionss) internos
        if(unions_internos):

            #Por cada registro variante union en la lista de registros internos
            for union in unions_internos:

                #Le calculamos su representacion y la guardamos en el atributo correspondiente a la misma para este union
                union.representacion = union_representacion(union.lista_tipos)
        
        #Luego de procesar los registros (structs) y registros variantes (unions) del registro (claro, si es que tenia alguno)
        #procedemos a procesar el registro en cuestion (es decir, este registro externo que contiene a los antes procesados)
        #Utilizaremos la misma funcion "empaquetado" para obtener la configuracion "empaquetada" del registro (donde no importan
        #las alineaciones de los tipos) y asi colocarla en su lista auxiliar como hemos hecho en otras ocasiones.
        reg_structs[nombre].lista_tipos_aux = empaquetado(lista_tipos_reg)
        
        #Procedemos entonces a imprimir el registro
        print_registro_struct(reg_structs[nombre].lista_tipos_aux)

        #Luego calculamos la representacion y el desperdicio del mismo
        reg_structs[nombre].representacion, reg_structs[nombre].nro_bytes_desperdiciados = desperdicio_representacion_reg(reg_structs[nombre].lista_tipos_aux)
        
        #Y los imprimimos
        print(f"\nRegistro (Struct) Empaquetado, Ocupacion: {reg_structs[nombre].representacion} bytes; Desperdicio: 0 bytes.")
        print()

        print("********************************************************************************************************")
        print("********************************** CASO REGISTRO (STRUCT) SIN EMPAQUETAR *******************************")
        print("********************************************************************************************************")
        
        #Si en efecto el registro tiene registros (structs) internos
        if(structs_internos):

            #Por cada registro struct en la lista de registros internos
            for struct in structs_internos:
                
                #Como este es el caso sin empaquetar, tomamos la lista de tipos del struct interno y con la funcion
                #"sin_empaquetar" ordenamos sus campos, ahora si, tomando en cuenta las alineaciones de los tipos para proceder a guardar
                #la configuracion "sin empaquetar" del registro en la lista auxiliar del struct interno (recordemos que en esta siempre
                #tendremos los tipos del registro en la configuracion del caso, en este caso en la forma sin empaquetar.
                struct.lista_tipos_aux  = sin_empaquetar(struct.lista_tipos) 

                #Calculamos la representacion del struct interno y la guardamos en su respectivo atributo
                struct.representacion = len(struct.lista_tipos_aux)

                #Tambien calculamos su alineacion y para este caso esta corresponde a la alineacion que tenga su primer tipo, entonces
                #tomamos la alineacion del primer tipo en su lista de tipos asociada
                struct.alineacion = struct.lista_tipos[0].alineacion

        #Si en efecto el registro tiene registros variantes (unionss) internos
        if(unions_internos):

            #Por cada registro variante union en la lista de registros internos
            for union in unions_internos:

                #Le calculamos su representacion y la guardamos en el atributo correspondiente a la misma para este union
                union.representacion = union_representacion(union.lista_tipos)

                #Tambien le calculamos su alineacion y la guardamos en el atributo correspondiente a la misma para este union
                union.alineacion = union_alineacion(union.lista_tipos)

        #Luego de procesar los registros (structs) y registros variantes (unions) del registro (si es que tenia alguno)
        #procedemos a procesar el registro en cuestion (es decir, este registro externo que contiene a los antes procesados)
        #Utilizaremos la misma funcion "sin_empaquetar" para obtener la configuracion "no empaquetada" del registro (donde ahora
        #si importan las alineaciones de los tipos) y asi colocarla en su lista auxiliar como hemos hecho en otras ocasiones.
        reg_structs[nombre].lista_tipos_aux = sin_empaquetar(lista_tipos_reg)
        
        #Luego de hacer esto, procedemos a obtener la representacion del registro
        #reg_structs[nombre].representacion = len(reg_structs[nombre].lista_tipos_aux)

        #Procedemos entonces a imprimir el registro
        print_registro_struct(reg_structs[nombre].lista_tipos_aux)

        #Luego calculamos la representacion y el desperdicio del mismo
        reg_structs[nombre].representacion, reg_structs[nombre].nro_bytes_desperdiciados = desperdicio_representacion_reg(reg_structs[nombre].lista_tipos_aux)
        
        #Y lo imprimimos
        print(f"\nRegistro (Struct) Sin Empaquetar, Ocupacion: {reg_structs[nombre].representacion} bytes; Desperdicio: {reg_structs[nombre].nro_bytes_desperdiciados} bytes.")
        print()
        
        print("********************************************************************************************************")
        print("************************************ CASO REGISTRO (STRUCT) OPTIMIZADO *********************************")
        print("********************************************************************************************************")
        
        #Si en efecto el registro tiene registros (structs) internos
        if(structs_internos):

            #Por cada registro struct en la lista de registros internos
            for struct in structs_internos:

                #Buscamos su configuracion optimizada utilizando la funcion "optimizado" y tambien obtenemos su representacion
                struct.lista_tipos_aux,struct.representacion  = optimizado(struct.nombre) 
                
                #Calculamos la alineacion del struct y en este caso esta sera la alineacion del primer tipo de su configuracion optima          
                struct.alineacion = struct.lista_tipos_aux[0].alineacion

        #Si en efecto el registro tiene registros variantes (unions) internos
        if(unions_internos):

            #Por cada registro variante union en la lista de registros variantes internos
            for union in unions_internos:

                #Le calculamos su representacion y la guardamos en el atributo correspondiente a la misma para este union
                union.representacion = union_representacion(union.lista_tipos)

                #Tambien le calculamos su alineacion y la guardamos en el atributo correspondiente a la misma para este union
                union.alineacion = union_alineacion(union.lista_tipos)

        #Luego de procesar los registros (structs) y registros variantes (unions) del registro (si tenia alguno)
        #procedemos a procesar el registro en cuestion (es decir, este registro externo que contiene a los antes procesados)
        #Utilizaremos la misma funcion "optimizar" para obtener la configuracion "optima" del registro (recordamos que en esta
        #tambien importan las alineaciones de los tipos) y asi colocarla en su lista auxiliar como hemos hecho en otras ocasiones.
        reg_structs[nombre].lista_tipos_aux, reg_structs[nombre].representacion = optimizado(nombre)
        
        #Procedemos entonces a imprimir el registro
        print_registro_struct(reg_structs[nombre].lista_tipos_aux)

        #Luego calculamos la representacion y el desperdicio del mismo
        reg_structs[nombre].representacion, reg_structs[nombre].nro_bytes_desperdiciados = desperdicio_representacion_reg(reg_structs[nombre].lista_tipos_aux)
        
        #Y lo imprimimos
        print(f"\nRegistro (Struct) Optimizado, Ocupacion: {reg_structs[nombre].representacion} bytes; Desperdicio: {reg_structs[nombre].nro_bytes_desperdiciados} bytes.")
        print()

    #Si lo que se paso para describir es un registro variante (union) entonces:
    elif nombre in reg_var_unions.keys():

        #En esta variable tomamos la lista de tipos que definen los campos del registro
        lista_tipos_reg_var = reg_var_unions[nombre].lista_tipos

        #Chequeamos si tiene registros (structs) internos y los guardamos en esta variable     
        structs_internos = tiene_registro_struct(lista_tipos_reg_var)

        #Chequeamos si tiene registros variantes (unions) internos y los guardamos en esta variable
        unions_internos = tiene_reg_var_union(lista_tipos_reg_var)
        
        #Si en efecto el registro variante tiene registros variantes (unions) internos
        if(unions_internos):

            #Por cada registro variante union en la lista de registros variantes internos
            for union in unions_internos:

                #Le calculamos su representacion y la guardamos en el atributo correspondiente a la misma para este union
                union.representacion = union_representacion(union.lista_tipos)

                #Tambien le calculamos su alineacion y la guardamos en el atributo correspondiente a la misma para este union
                union.alineacion = union_alineacion(union.lista_tipos)
        
        #Sin no hay structs internos entonces
        if(not(structs_internos)):

            #Obtenemos su representacion y la asignamos a su atrobuto correspondiente
            reg_var_unions[nombre].representacion = union_representacion(reg_var_unions[nombre].lista_tipos)
            
            #Obtenemos su alineacion y la asignamos a su atributo correspondiente
            reg_var_unions[nombre].alineacion = union_alineacion(reg_var_unions[nombre].lista_tipos)
            
            #E imprimimos el registro variante con su informacion basica
            print_registros_variantes(reg_var_unions[nombre])
        
        #De lo contrario, si en efecto el registro variante tiene registros (structs) internos entonces
        #habra que presentar para cada caso del struct (empaquetado, sin empaquetar y optimizado) como
        #varia el registro variante (union)
        else:

            #Por cada struct en la lista de registros struct internos
            for struct in structs_internos:

                #Obtenemos su configuracion "empaquetada" utilizando la funcion "empaquetado" y la guardamos en su lista
                #auxiliar como hemos hecho en otras ocasiones
                struct.lista_tipos_aux = empaquetado(struct.lista_tipos) 

                #Calculamos su representacion
                struct.representacion = len(struct.lista_tipos_aux)

            print("********************************************************************************************************")
            print("******************************** CASO REGISTRO VARIANTE (UNION) EMPAQUETADO ****************************")
            print("********************************************************************************************************")
        
            print("\n")

            #Calculamos la representacion del registro variante que contiene los structs           
            reg_var_unions[nombre].representacion = union_representacion(reg_var_unions[nombre].lista_tipos)
            
            #Y procedemos a imprimir el registro variante en cuestion
            print_registros_variantes(reg_var_unions[nombre])
            print("\n")

            print("********************************************************************************************************")
            print("****************************** CASO REGISTRO VARIANTE (UNION) SIN EMPAQUETAR ***************************")
            print("********************************************************************************************************")
        
            print("\n")

            #Por cada struct en la lista de registros struct internos
            for struct in structs_internos:

                #Obtenemos su configuracion "sin empaquetar" utilizando la funcion "sin_empaquetar" y la guardamos en su lista
                #auxiliar como hemos hecho en otras ocasiones
                struct.lista_tipos_aux  = sin_empaquetar(struct.lista_tipos)  

                #Calculamos su representacion
                struct.representacion = len(struct.lista_tipos_aux)

                #Tambien calculamos su alineacion       
                struct.alineacion = struct.lista_tipos[0].alineacion

            #Calculamos la representacion del registro variante que contiene los structs           
            reg_var_unions[nombre].representacion = union_representacion(reg_var_unions[nombre].lista_tipos)

            #Tambien calculamos su alineacion          
            reg_var_unions[nombre].alineacion = union_alineacion(reg_var_unions[nombre].lista_tipos)

            #Y procedemos a imprimir el registro variante en cuestion 
            print_registros_variantes(reg_var_unions[nombre])
            print("\n")

            print("********************************************************************************************************")
            print("********************************* CASO REGISTRO VARIANTE (UNION) OPTIMIZADO ****************************")
            print("********************************************************************************************************")
        
            print("\n")

            #Por cada struct en la lista de registros struct internos
            for struct in structs_internos:

                #Obtenemos su configuracion "optimizada" utilizando la funcion "optimizado" y la guardamos en su lista
                #auxiliar como hemos hecho en otras ocasiones. Tambien obtenemos su representacion.
                struct.lista_tipos_aux,struct.representacion  = optimizado(struct.nombre)              
                
                #Obtenemos su alineacion correspondiente tambiem segun el primer elemento de su configuracion optima
                struct.alineacion = struct.lista_tipos_aux[0].alineacion

            #Calculamos la representacion del registro variante que contiene los structs
            reg_var_unions[nombre].representacion = union_representacion(reg_var_unions[nombre].lista_tipos)

            #Tambien calculamos su alineacion 
            reg_var_unions[nombre].alineacion = union_alineacion(reg_var_unions[nombre].lista_tipos)
            
            #Y procedemos a imprimir el registro variante en cuestion
            print_registros_variantes(reg_var_unions[nombre])
    
    #De lo contrario, el nombre que se paso no se corresponde con alguno de los tipos anteriores
    #Entonces se informa error y que ese nombre no esta definido.
    else:
        print(f"ERROR: El nombre <{nombre}>, no es de un tipo previamente definido.")

#Funcion que calcula la representacion de un registro variante (union)
def union_representacion(lista_tipos):

    representaciones = []

    #Para cada tipo en la lista de tipos del registro variante (union)
    for tipo in lista_tipos:

        #Tomamos su representacion y la colocamos en la lista de representaciones
        representaciones.append(int(tipo.representacion))

    #Al final retornamos la representacion mas grande de entre los tipos, ya que esa sera la representacion
    #del registro variante
    return max(representaciones)

#Funcion utilizada por los union, basicamente busca entre las alineaciones de todos sus posibles lista_tipos
#Y retorna el minimo comun multiplo entre todos ellos

#Funcion que calcula la alineacion de un registro variante (union)
def union_alineacion(lista_tipos):

    alineaciones = []

    #Para cada tipo en la lista de tipos del registro variante (union)
    for tipo in lista_tipos:

        #Tomamos su alineacion y la colocamos en la lista de alineaciones
        alineaciones.append(int(tipo.alineacion))

    #Al final retornamos el minimo comun multiplo de entre las alineaciones de todos los tipos, ya que esa
    #sera la alineacion del registro variante
    return mcm(alineaciones)

#Funcion que calcula el minimo comun multiplo (mcm) de una lista de enteros
def mcm(alineaciones):
    return reduce(lambda x, y: x*y // gcd(x,y), alineaciones)

#Funcion para imprimir registros (structs) y mostrar toda su informacion asociada
def print_registro_struct(lista_tipos_aux):

    indice = 0

    #Recorremos la lista auxiliar del registro en donde tenemos la configuracion de sus campos segun el caso en el
    #que estemos (empaquetado, sin empaquetar u optimizado)
    while indice < len(lista_tipos_aux):

        #Cada vez que nos consigamos un 0 (es decir, un byte desperdiciado) aumentamos el indice en 1 y continuamos el recorrido.
        if (lista_tipos_aux[indice] == 0):
            indice +=1
            continue


        #Si el elemento en la lista auxiliar es una tupla, eso significa que al print esta llegando un registro que previamente paso
        #por la funcion "sin_empaquetar" (donde hacemos caso a las alineaciones de los tipos del registro) y en esta, se determino que
        #este tipo era un registro interno "struct" por lo cual se guardo en la lista de tipos como una tupla con el tipo en cuestion y su
        #lista auxiliar de tipos, es decir, como: "(tipo, lista_tipos_aux)" .
        if(type(lista_tipos_aux[indice]) is tuple):

            #Procedemos entonces a imprimir el registro interno pasandole a la funcion correspondiente la lista auxilia del struct interno en
            #la que tenemos la configuracion de sus campos para el caso que nos piden (lista_tipos_aux[indice][1], que es lo que esta en la 
            #posicion 1 de la tupla), el objeto como tal del tipo struct (lista_tipos_aux[indice][0], que es lo que esta en la posicion 0 de la tupla)
            #y el indice en el que nos encontramos que sera la posicion del registro desde la que empieza el struct interno
            print_struct_interno(lista_tipos_aux[indice][1], lista_tipos_aux[indice][0] ,indice)
            indice += 1
        
        #Sino, si el elemento es un tipo atomico entonces
        elif lista_tipos_aux[indice].nombre in t_atomicos.keys():

            #Imprimimos el tipo y aumentamos el indice la cantidad de su representacion para poder pasar a imprimir el siguiente tipo en la
            #proxima iteracion
            print(f"En Posicion [{indice}], {lista_tipos_aux[indice]}", end="\n")
            indice += int(lista_tipos_aux[indice].representacion)

        #Sino, si el elemento  es un registro variable (union)
        elif lista_tipos_aux[indice].nombre in reg_var_unions.keys():

            lista_tipos_sin_repetidos = []

            #Recorremos los tipos del registro y armamos la lista "lista_tipos_sin_repetidos" para, como su nombre lo indica, tener
            #los tipos del registro variante sin repeticiones
            for tipo in lista_tipos_aux[indice].lista_tipos:
                if tipo not in lista_tipos_sin_repetidos:
                    lista_tipos_sin_repetidos.append(tipo)

            #Imprimimos el registro variante con su respectiva informacion
            print(f"En Posicion [{indice}], Registro Variante (Union); Representacion: {lista_tipos_aux[indice].representacion} bytes; Alineacion: {lista_tipos_aux[indice].alineacion} bytes.", end="\n")
            print("Tipos del registro variante:")
            print("-----------------------------------------------------")
            print_registro_union_grafico(lista_tipos_sin_repetidos)
            print("-----------------------------------------------------")
            indice += int(lista_tipos_aux[indice].representacion)
    
    #Finalmente procedemos a imprimir la representacion grafica del registro
    print("\nRepresentacion grafica del Registro (Struct): ")
    print("\n-----------------------------------------------------")
    print_registro_struct_grafico(lista_tipos_aux)
    print("\n-----------------------------------------------------")
    

#Funcion para imprimir registros (structs) internos
def print_struct_interno(lista_aux, struct_interno, indice_inicial):

    indice = 0

    print(f"En Posicion [{indice_inicial}], Registro (Struct) Interno:", end="\n")
    
    #Imprimimos "graficamente" el struct interno
    print("\n\tRepresentacion grafica del Registro (Struct) Interno: ")
    print("\n\t-----------------------------------------------------")
    print_registro_struct_grafico(struct_interno.lista_tipos_aux)
    print("\n\t-----------------------------------------------------")

    #Recorremos los campos del registro (definidos en su lista de tipos auxiliar como se ha explicado en otras ocasiones) 
    while indice < len(lista_aux):

        #Si nos conseguimos un 0 (byte desperdiciado), aumentamos en 1 el indice y continuamos el recorrido.
        if(lista_aux[indice] == 0):
            indice += 1
            continue

        #Imprimimos el tipo en el campo correspondiente
        print(f"\tEn su Posicion [{indice}]: {lista_aux[indice]}", end="\n")
        
        #Sumamos al indice la representacion del tipo (dentro del struct interno) que acabamos de imprimir para que
        #entonces en la siguiente iteracion podamos pasar a imprimir el siguiente tipo
        indice += int(lista_aux[indice].representacion)
    print("\n")

#Funcion para imprimir un registro (struct) en forma grafica como la cajita vista en clase
#con 4 bytes por fila
def print_registro_struct_grafico(lista_tipos_aux):
    
    #Recorremos la lista auxiliar de tipos del registro
    for i in range(len(lista_tipos_aux)):

        #Con este if cuidamos que la impresion se haga cada 4 elementos para tener una
        #cajita como la del ejemplo en clase con cambos de 4 bytes y que cada 4 elemento se cierre la cajita
        #Cuando i es 0 no imprimimos el cierre de cajita.
        if i % 4 == 0 :
            if i == 0: print()
            else: print("|")

        #Si el tipo es un tipo atomico o un registro (struct) o un registro variante (union)
        if type(lista_tipos_aux[i]) is TipoAtomico or type(lista_tipos_aux[i]) is Registro or type(lista_tipos_aux[i]) is RegistroVariante:

            #Entonces imprimimos nu nombre solamente
            print("| " + lista_tipos_aux[i].nombre, end=" ")

        #Sino, si el tipo en la lista esta guardado como tupla, entonces es un struct
        elif type(lista_tipos_aux[i]) is tuple:

            #Entones imprimimos su nombre (tomandolo del objeto Registro que guardamos en la primera posicion de la tupla)
            print("| " + str(lista_tipos_aux[i][0].nombre), end =" ")
        
        #De lo contrario, si es un 0, lo imprimimos como string
        else:
            print("| " + str(lista_tipos_aux[i]), end =" ")

        #Si ya llegamos al final de la lista cerramos la ultima fila de la cajita
        if i == len(lista_tipos_aux) - 1: print("|")

#Funcion para imprimir registros variantes (unions)
def print_registros_variantes(reg_variante):

    lista_tipos_sin_repetidos = []

    #Recorremos los tipos del registro y armamos la lista "lista_tipos_sin_repetidos" para, como su nombre lo indica, tener
    #los tipos del registro variante sin repeticiones
    for tipo in reg_variante.lista_tipos:
        if tipo not in lista_tipos_sin_repetidos:
            lista_tipos_sin_repetidos.append(tipo)

    #Imprimimos su informacion basica y la representacion grafica del mismo
    print(f"Registro Variante (Union), Representacion: {reg_variante.representacion} bytes; Alineacion: {reg_variante.alineacion} bytes.", end="\n")
    print("Tipos del registro variante:")
    print("\n-----------------------------------------------------")
    print_registro_union_grafico(lista_tipos_sin_repetidos)
    print("\n-----------------------------------------------------")

    #Recorremos cada tipo en la lista de tipos del registro variante para inprimir la informacion
    #basica de sus tipos
    for tipo in lista_tipos_sin_repetidos:

        #Si el tipo es un tipo atomico imprimimos su informacion correspondiente
        if type(tipo) is TipoAtomico:
            print("\t"+str(tipo), end="\n")

        #Si el tipo es un registro variante (Union), imprimimos su informacion correspondiente
        elif type(tipo) is RegistroVariante:
            print(f"\tRegistro Variante (Union) Interno, Representacion: {tipo.representacion} bytes; Alineacion: {tipo.alineacion}.", end="\n")
            print("\tTipos del registro variante:")
            print("\n\t-----------------------------------------------------")
            print_registro_union_grafico(lista_tipos_sin_repetidos)
            print("\n\t-----------------------------------------------------")
            print("\n")
        
        #Si el tipo es un registro (struct)
        elif type(tipo) is Registro:
            print(f"\tRegistro (Struct) Interno, Representacion: {tipo.representacion} bytes; Alineacion: {tipo.alineacion} bytes; Desperdicio: {tipo.lista_tipos_aux.count(0)} bytes.", end="\n")
            print("\t Representacion grafica del Struct Interno:")
            print("\n\t-----------------------------------------------------")
            print_registro_struct_grafico(tipo.lista_tipos_aux)
            print("\n\t-----------------------------------------------------")

#Funcion para imprimir graficamente los tipos de un registro variante
def print_registro_union_grafico(lista_tipos_sin_repetidos):
    
    #Recorremos la lista de los tipos del registro variante
    for i in range(len(lista_tipos_sin_repetidos)):

        #Si el tipo es un tipo atomico o un registro (struct) o un registro variante (union)
        if type(lista_tipos_sin_repetidos[i]) is TipoAtomico or type(lista_tipos_sin_repetidos[i]) is Registro or type(lista_tipos_sin_repetidos[i]) is RegistroVariante:

            #Entonces imprimimos su nombre solamente
            print("| " + lista_tipos_sin_repetidos[i].nombre, end=" ")

        #Si ya llegamos al final de la lista cerramos con |
        if i == len(lista_tipos_sin_repetidos) - 1: print("|")
