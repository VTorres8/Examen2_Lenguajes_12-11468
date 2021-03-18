from manejadorTipos import *
import unittest
from io import StringIO
from unittest.mock import patch


class Test_Manejador_Tipos(unittest.TestCase):

    #Probar funcion "crear_tipo_atomico", verificamos si el atomico creado es
    #una instancia de TipoAtomico
    def test__prueba1_crear1_tipo_atomico(self):
        accion = "ATOMICO bool 1 2"
        accion = accion.split(" ")
        crear_tipo_atomico(accion)
        self.assertIsInstance(t_atomicos["bool"], TipoAtomico)

    #Probar funcion "crear_tipo_atomico", en un caso donde el tipo ya existe
    def test__prueba2_crear1_tipo_atomico_error(self):
        accion = "ATOMICO bool 1 2"
        accion = accion.split(" ")
        no_lo_crea = crear_tipo_atomico(accion)
        self.assertFalse(no_lo_crea)

    #Probar funcion "crear_reg_o_reg_var", verificamos si el struct creado es
    #una instancia de Registro
    def test__prueba3_crear2_reg_o_reg_var_1(self):
        accion = "STRUCT struct bool"
        accion = accion.split(" ")
        crear_reg_o_reg_var(accion)
        self.assertIsInstance(reg_structs["struct"], Registro)

    #Probar funcion "crear_reg_o_reg_var", verificamos si el union creado es
    #una instancia de RegistroVariante
    def test__prueba4_crear3_reg_o_reg_var_2(self):
        accion = "UNION union bool"
        accion = accion.split(" ")
        crear_reg_o_reg_var(accion)
        self.assertIsInstance(reg_var_unions["union"], RegistroVariante)

    #Probar funcion "crear_reg_o_reg_var" para un caso donde el el struct que vamos a
    #crear tiene un tipo atomico que no fue definido
    def test__prueba5_crear3_reg_o_reg_var_3_error(self):
        accion = "STRUCT struct1 bool int"
        accion = accion.split(" ")
        no_lo_crea = crear_reg_o_reg_var(accion)
        self.assertFalse(no_lo_crea)

    #Probar funcion "definido", para verificar si un tipo atomico fue previamente definido
    #En este caso si lo fue y debe retornar True la funcion
    def test__prueba6_definido(self):
        accion = "ATOMICO bool 1 2"
        accion = accion.split(" ")
        si_definido = definido(accion)
        self.assertTrue(si_definido)

    #Probar funcion "definido", para verificar si un tipo atomico fue previamente definido
    #En este caso no lo fue y debe retornar False la funcion
    def test__prueba7_definido_error(self):
        accion = "ATOMICO jojo1 4"
        accion = accion.split(" ")
        no_definido = definido(accion)
        self.assertFalse(no_definido)
    
    #Probamos funcion describir un tipo atomico previamente creado
    def test__prueba8_describir1_tipo_atomico(self):
        accion = "ATOMICO char 2 2"
        accion = accion.split(" ")
        crear_tipo_atomico(accion)
        describir_tipo_atomico =  describir("char")
        self.assertEqual(describir_tipo_atomico, "Tipo Atomico: char; Representacion: 2 bytes; Alineacion: 2 bytes.")

    #Probamos describir un tipo atomico que no fue previamente creado
    def test__prueba9_describir2_tipo_atomico_error(self):
        describir_tipo_atomico_no_existente =  describir("jojo")
        self.assertNotEqual(describir_tipo_atomico_no_existente, "Tipo Atomico: int; Representacion: 4 bytes; Alineacion: 4 bytes.")

    #Probamos describir un struct no definido
    def test__prueba10_describir3_struct1(self):
        accion_bool = "ATOMICO bool 1 2"
        accion_bool = accion_bool.split(" ")
        crear_tipo_atomico(accion_bool)

        accion = "STRUCT struct6 bool"
        accion = accion.split(" ")
        crear_reg_o_reg_var(accion)
       
       #Con patch tomamos la salida tras describir el struct antes definido (STRUCT struct bool)
        with patch('sys.stdout', new=StringIO()) as mocked_stdout:
            describir("struct6")
            output = mocked_stdout.getvalue() 

        #Para cada caso las salidas esperadas son:
        empaquetado = "| bool |"
        sin_empaquetar =  "| bool |"
        optimizado = "| bool |"

        self.assertTrue(empaquetado in output and sin_empaquetar in output and optimizado in output) 

    #Probamos describir un union definido
    def test__prueba11_describir3_union(self):

        crear_reg_o_reg_var("UNION union2 bool".split(" "))

        with patch('sys.stdout', new=StringIO()) as mocked_stdout:
            describir("union2")
            output = mocked_stdout.getvalue()  
        
        esperado = "| bool |"
        self.assertTrue(esperado in output)
    
    #Probamos la funcion anidamiento para detectar que un struct no tiene nivel de anidamiento mayor a 1
    def test__prueba12_anidamiento(self):
        accion = "ATOMICO bool 1 2"
        accion = accion.split(" ")
        crear_tipo_atomico(accion)

        accion1 = "STRUCT s1 bool"
        accion1 = accion1.split(" ")
        crear_reg_o_reg_var(accion1)

        accion2 = "STRUCT s2 s1 bool"
        accion2 = accion2.split(" ")
        crear_reg_o_reg_var(accion2) 
        
        esperado = anidamiento(accion2)
        self.assertFalse(esperado)

    #Probamos la funcion anidamiento para detectar que un struct tiene nivel de anidamiento mayor a 1
    def test_prueba13_anidamiento_error(self):
        accion_bool = "ATOMICO bool 1 2"
        accion_bool = accion_bool.split(" ")
        crear_tipo_atomico(accion_bool)

        accion_char = "ATOMICO char 2 2"
        accion_char = accion_char.split(" ")
        crear_tipo_atomico(accion_char)

        accion_union = "UNION unioncita bool char"
        accion_union = accion_union.split(" ")
        crear_reg_o_reg_var(accion_union)

        accion1 = "STRUCT s3 bool"
        accion1 = accion1.split(" ")
        crear_reg_o_reg_var(accion1)

        accion2 = "STRUCT s4 s3 char"
        accion2 = accion2.split(" ")
        crear_reg_o_reg_var(accion2) 
        
        esperado = anidamiento(accion2)

        accion3 = "STRUCT s5 s4 unioncita"
        accion3 = accion3.split(" ")  
        
        esperado = anidamiento(accion3)
        self.assertTrue(esperado)

    #Probamos la funcion para calcular la representacion de una union
    def test__prueba14_union_representacion(self):
        accion = "ATOMICO char 2 2"
        accion = accion.split(" ")
        crear_tipo_atomico(accion)

        accion1 = "UNION union1 bool char"
        accion1 = accion1.split(" ")
        crear_reg_o_reg_var(accion1)
        
        r_variable = reg_var_unions[accion1[1]]
        representacion = union_representacion(r_variable.lista_tipos)
        esperado = 2
        self.assertEqual(representacion,esperado)

    #Probamos la funcion para calcular la alineacion de una union
    def test__prueba15_union_representacion(self):
        crear_tipo_atomico("ATOMICO random 2 3".split(" "))
        crear_reg_o_reg_var("UNION prueba3 random prueba prueba2".split(" "))
        accion_int = "ATOMICO int 4 4"
        accion_int = accion_int.split(" ")
        crear_tipo_atomico(accion_int)

        accion = "ATOMICO char 2 2"
        accion = accion.split(" ")
        crear_tipo_atomico(accion)

        accion1 = "UNION union2 bool char int"
        accion1 = accion1.split(" ")
        crear_reg_o_reg_var(accion1)
        
        r_variable = reg_var_unions[accion1[1]]
        alineacion = union_alineacion(r_variable.lista_tipos)
        esperado = 2
        self.assertEqual(alineacion,esperado)
    
    #Probamos la funcion mcm, para calcular el minimo comun multiplo de una lista de numeros
    def test_prueba16_mcm(self):

        #alineacioones de bool, char e int
        alineaciones = [1,2,4]

        minimo_comun_multiplo = mcm(alineaciones)
        esperado = 4

        self.assertEqual(minimo_comun_multiplo,esperado)

    #Probamos la funcion print_registro_struct
    def test_prueba17_print_registro_struct(self):
        crear_tipo_atomico("ATOMICO float 8 8".split(" "))
        crear_tipo_atomico("ATOMICO bool 1 2".split(" "))
        crear_reg_o_reg_var("UNION prueba float bool".split(" "))
        with patch('sys.stdout', new=StringIO()) as mocked_stdout:
            describir("prueba")
            output = mocked_stdout.getvalue()
        #Resultados esperados
        expected_output = "Tipos del registro variante:"
        self.assertTrue(expected_output in output)

    def test_prueba18(self):
        crear_reg_o_reg_var("STRUCT prueba2 bool prueba".split(" "))
        with patch('sys.stdout', new=StringIO()) as mocked_stdout:
            describir("prueba2")
            output = mocked_stdout.getvalue()
        print(output)
            
        #Resultados esperados
        empaquetado = "Registro (Struct) Empaquetado"
        no_empaquetado =  "Registro (Struct) Sin Empaquetar"
        optimizado = "Registro (Struct) Optimizado"
        #Verificamos que el output contenga los strings de los resultados esperados
        self.assertFalse(empaquetado in output and no_empaquetado in output and optimizado in output)

    #Crearemos ahora un union con otro union dentro y otro struct. En este caso veremos que ocurre si el struct esta empaquetado
    #No empaquetado y optimizado
    def test_prueba19(self):
        crear_tipo_atomico("ATOMICO random 2 3".split(" "))
        crear_reg_o_reg_var("UNION prueba3 random prueba2".split(" "))
        with patch('sys.stdout', new=StringIO()) as mocked_stdout:
            describir("prueba3")
            output = mocked_stdout.getvalue()
        print(output)
        
        #Resultados esperados
        esperado1 = "Registro Variante (Union)"
        esperado2 =  "Tipos del registro variante:"
        esperado3 = "Registro Variante (Union) Interno"
        esperado4 = "Registro (Struct) Interno,"
        esperado5 = "Representacion grafica del Struct Interno:"
        #Verificamos que el output contenga los strings de los resultados esperados
        self.assertFalse(esperado1 in output and esperado2 in output and esperado3 in output and esperado4 in output and esperado5 in output)
    
    def test_prueba20(self):
        crear_tipo_atomico("ATOMICO jota 5 7".split(" "))
        crear_tipo_atomico("UNION uni jota int".split(" "))
        crear_reg_o_reg_var("STRUCT prueba4 jota int".split(" "))
        with patch('sys.stdout', new=StringIO()) as mocked_stdout:
            describir("prueba4")
            output = mocked_stdout.getvalue()

        empaquetado = "Registro (Struct) Empaquetado"
        no_empaquetado =  "Registro (Struct) Sin Empaquetar"
        optimizado = "Registro (Struct) Optimizado"
        print(output)
        #Verificamos que el output contenga los strings de los resultados esperados
        self.assertFalse(empaquetado in output and no_empaquetado in output and optimizado in output)

    def test_prueba21(self):
        crear_reg_o_reg_var("STRUCT prueba5 prueba4 jota random".split(" "))
        with patch('sys.stdout', new=StringIO()) as mocked_stdout:
            describir("prueba5")
            output = mocked_stdout.getvalue()

        empaquetado = "Registro (Struct) Empaquetado"
        no_empaquetado =  "Registro (Struct) Sin Empaquetar"
        optimizado = "Registro (Struct) Optimizado"
        print(output)
        
        self.assertFalse(empaquetado in output and no_empaquetado in output and optimizado in output)  

if __name__ == '__main__':
    unittest.main()
