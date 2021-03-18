//Clase para definir el nodo del arbol.
class Nodo {

    public valor: number;
    public izquierdo: Nodo;
    public derecho: Nodo;

    constructor(valor) {
        this.valor = valor;
        this.izquierdo = null;
        this.derecho = null;
    }
}

//Clase para definir el arbol binario
class ArbolBinario {
    raiz: Nodo;

    constructor() {
        this.raiz = null;
    }

    //funcion de la clase ArbolBinario que verifica si el arbol es un
    //Arbol Binario de Busqueda (BST: Binary Search Tree) y retorna true si lo es
    //y false si no lo es.
    esDeBusqueda(nodo, min = null, max = null) {

        //Verificamos si hemos llegado al final del recorrido y de ser asi entonces las condiciones para ser
        //un arbol de busqueda binario se cumplieron y podemos regresar "true".
        if (!nodo) return true;

        //En este punto verificamos si el nodo del arbol en el que nos encontramos cumple con las condiciones
        //establecidas para ser un BST. Si entramos en el if, entonces el nodo no cumple esas condiciones por
        //lo tanto retornamos false. 
        if ((max !== null && nodo.valor >= max) || (min !== null && nodo.valor <= min)) {
            return false;
        }

        //verificamos para el hijo izquierdo y para el hijo derecho si son BST
        const hijoIzquierdo = this.esDeBusqueda(nodo.izquierdo, min, nodo.valor);
        const hijoDerecho = this.esDeBusqueda(nodo.derecho, nodo.valor, max);

        //Al final retornamos true si tanto el hijo derecho como el izquierdo cumplen que son BST, de lo contrario
        //retornaremos false
        return hijoIzquierdo && hijoDerecho;
    }
}

//Prueba con un arbol que no es BST
const t = new Nodo(10);
t.izquierdo = new Nodo(0);
t.izquierdo.izquierdo = new Nodo(7);
t.izquierdo.derecho = new Nodo(4);
t.derecho = new Nodo(12);
const t1 = new ArbolBinario();
t1.raiz = t;
console.log(t1.esDeBusqueda(t)); // Nos retornara false.

//Prueba con un arbol que si es BST
const v = new Nodo(10);
v.izquierdo = new Nodo(4);
v.izquierdo.izquierdo = new Nodo(0);
v.izquierdo.derecho = new Nodo(7);
v.derecho = new Nodo(12);
const t2 = new ArbolBinario();
t2.raiz = v;
console.log(t2.esDeBusqueda(v)); //Nos retornara true.