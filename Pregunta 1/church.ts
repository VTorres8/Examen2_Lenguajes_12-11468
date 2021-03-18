//Vamos a definir church aprovechando las funciones tipo lambda

//Definimos el cero como la funcion identidad segun la definicion de
//los numeros de church
let cero = (f => x => x);

// Definimos "Successor" para aplicar la funcion una vez mas sobre cualquier church n
//Por ejemplo si el numero de church es 0, su sucesor sera 1 y asi sucesivamente como
//indica la definicion de estos numeros.
let succ = (n => f => x => f(n(f)(x)));

// Para poder mostrar los numeros de church como enteros concretos creamos "suma1"
//que lo que hara sera literalmente sumar un 1 y luego con "churchAInt" nos encargaremos
//de que suma 1 sea pasada y realizada en las distintas llamadas a la funcion para que vaya
//actualizando x con el valor del numero de church que iremos construyendo mediante reptidas llamadas
//a "sucesor"
let suma1 = x => x + 1;
let churchAInt = n => n(suma1)(0);

//Funcion para tener la opcion de convertir un numero entero a un numeral de church
function intAChurch(i) {
  if (i === 0) {
    return cero;
  }
  else {
    return succ(intAChurch(i - 1));
  }
}

//Definimos la suma para los numeros de church
let suma = m => n => f => x => n(f)(m(f)(x));

//Definimos la multiplicacion para dos numeros de church
let mult = m => n => f => x => n(m(f))(x);


//Algunas pruebas pa- ve qlq

//Mostramos los primeros 3 numeros de church (partiendo del 0)
console.log("El numero " + churchAInt(cero) + " de church.");
let uno = succ(cero);
console.log("El numero " + churchAInt(uno) + " de church." );
let dos = succ(uno);
console.log("El numero " + churchAInt(dos) + " de church." );


//Probamos que si le pasamos un engtero a nuestra funcion "intAChurch", esta crea el church que
//corresponde y luego cuando se lo pasamos a nuestra funcion "churchAInt" entonces nos da en
//efecto ese valor.
console.log(churchAInt(intAChurch(42)));

//Sumamos 1 y 2 de church
let sumo_1_2 =suma(uno)(dos);
console.log("1 + 2 = " + churchAInt(sumo_1_2));

//Creamos el 11 y 31 de church y los sumamos
let once = intAChurch(11);
let treintaYuno = intAChurch(31);
let sumo_11_31 = suma(once)(treintaYuno);
console.log("11 + 31 = " + churchAInt(sumo_11_31));

//Multiplicamos 2 y 3
let tres = succ(dos);
let mult_2_3 = mult(dos)(tres);
console.log("2 * 3 = " + churchAInt(mult_2_3));

//Multiplicamos 11 y 2
let mult_11_2 = mult(once)(dos);
console.log("11 * 2 = " + churchAInt(mult_11_2));