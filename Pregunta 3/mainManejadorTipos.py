from manejadorTipos import *

#Main o menu del manejador de memoria
def menu():
    print("****************************************************")
    print("****************************************************")
    print("**************** MANEJADOR DE TIPOS ****************")
    print("****************************************************")
    print("****************************************************")
    
    accion = ""

    while True:
        print("Puede realizar alguna de las siguientes acciones:\n")

        print("* Con: ATOMICO <nombre> <representacion> <alineacion>, defina un nuevo tipo atomico.")
        print("* Con: STRUCT <nombre> [<tipo>], defina un nuevo registro (struct).")
        print("* Con: UNION <nombre> [<tipo>], defina un nuevo registro variante (union).")
        print("* Con: DESCRIBIR <nombre>, describa alguno de los tipos previamente definidos.")
        print()

        #String en el que guardaremos la accion ingresada por consola
        accion = input()

        #Procesamos el input, le quitamos posibles espacios en blanco al final y
        #hacemos split por el caracter " " para tener cada elemento de la acción ingresada. 
        accion = accion.strip()
        accion = accion.split(" ")

        #Si la instruccion pasada es "ATOMICO"
        if accion[0].lower() == "atomico":

            #Si la accion se escribio completa con sus 4 elementos (ATOMICO <nombre> <representacion> <alineacion>)
            if( len(accion) == 4 ):

                #Si la <representacion> y <alineacion> son numeros, entonces podemos crear el tipo atomico que se ingreso           
                if accion[2].isdigit() and accion[3].isdigit():
                    crear_tipo_atomico(accion)

                #De lo contratio se informa el error y recuerda que estos valores deben ser numericos
                else:
                    print("ERROR: Recuerde que la <representacion> y <alineacion> son numeros.")
            
            #De lo contrario la accion se paso en un formato invalido, entonces se informa el error y se recuerda el
            #formato valido para esta accion
            else:
                print("ERROR: Recuerde que para definir un tipo atomico debe ingresar")
                print("\t  ATOMICO <nombre> <representacion> <alineacion>")
        
        #Si la instruccion pasada es "STRUCT"
        elif accion[0].lower() == "struct":

            #Si la accion tiene menos de 3 elementos entonces esta incompleta, por lo cual se informa el error y recuerda
            #el formato valido para esta accion
            if len(accion) < 3:
               print("ERROR: Recuerde que para definir un registro (struct) debe ingresar")
               print("\t\tSTRUCT <nombre> [<tipo>]")

            #De lo contrario, creamos el registro (struct) ingresado
            else:
                crear_reg_o_reg_var(accion)

        #Si la instruccion pasada es "UNION"
        elif accion[0].lower() == "union":

            #Si la accion tiene menos de 3 elementos entonces esta incompleta, por lo cual se informa el error y recuerda
            #el formato valido para esta accion
            if len(accion) < 3:
               print("ERROR: Recuerde que para definir un registro variante debe ingresar")
               print("\t\tUNION <nombre> [<tipo>]")

            #De lo contrario, creamos el registro variante (union) ingresado
            else:
                crear_reg_o_reg_var(accion)

        #Si la instruccion pasada es "DESCRIBIR"
        elif accion[0].lower() == "describir":

            #Si la accion se escribio completa con sus dos elementos (DESCRIBIR <nombre>), entonces podemos  pasar a 
            #describir la accion 
            if (len(accion) == 2):
                describir(accion[1])
               
            #De lo contrario la accion se paso en un formato invalido, entonces se informa el error y se recuerda el
            #formato valido para esta accion
            else:
                print("ERROR: Recuerde que para describir algun tipo debe ingresar")
                print("\t\tDESCRIBIR <nombre>")

        #Si la instruccion pasada es "SALIR" nos salimos como sea >:3 muahaha
        elif accion[0].lower() == "salir":
            break

        #De lo contrario se muestra error y se pide ingresar una accion valida
        else:
            print("ERROR: Introduzca una accion valida.")

        print()
            

if __name__ == '__main__':
    menu()