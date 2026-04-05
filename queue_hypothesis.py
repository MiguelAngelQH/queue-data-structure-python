"""
EJERCICIO 2: Generación AUTOMÁTICA de test cases con Hypothesis
================================================================
Hypothesis es una librería de Property-Based Testing:
en lugar de escribir valores fijos, le dices QUÉ PROPIEDADES
debe cumplir tu código y Hypothesis genera cientos de casos
aleatorios para intentar romperlo (incluye casos extremos).
"""

import array
from hypothesis import given, settings, assume
from hypothesis import strategies as st

# Clase Queue es la misma que el ejercicio 1
class Queue:
    def __init__(self, size_max):
        assert size_max > 0
        self.max = size_max
        self.head = 0
        self.tail = 0
        self.size = 0
        self.data = array.array('i', range(size_max))

    def empty(self):  return self.size == 0
    def full(self):   return self.size == self.max

    def enqueue(self, x):
        if self.size == self.max:
            return False
        self.data[self.tail] = x
        self.size += 1
        self.tail += 1
        if self.tail == self.max:
            self.tail = 0
        return True

    def dequeue(self):
        if self.size == 0:
            return None
        x = self.data[self.head]
        self.size -= 1
        self.head += 1
        if self.head == self.max:
            self.head = 0
        return x

    def checkRep(self):
        assert self.tail >= 0
        assert self.tail < self.max
        assert self.head >= 0
        assert self.head < self.max
        if self.tail > self.head:
            assert (self.tail - self.head) == self.size
        if self.tail < self.head:
            assert (self.head - self.tail) == (self.max - self.size)
        if self.head == self.tail:
            assert (self.size == 0) or (self.size == self.max)


# TESTS AUTOMÁTICOS CON HYPOTHESIS

print("=" * 60)
print("EJERCICIO 2: Tests automáticos con Hypothesis")
print("=" * 60)

# TEST 1: La cola vacía siempre cumple sus invariantes
@given(size=st.integers(min_value=1, max_value=50))
def test_nueva_cola_vacia(size):
    """Hypothesis prueba decenas de tamaños distintos automáticamente."""
    q = Queue(size)
    assert q.empty() == True
    assert q.full()  == False
    assert q.size    == 0
    q.checkRep()

test_nueva_cola_vacia()
print("\nYES TEST 1: Cola vacía — Hypothesis probó múltiples tamaños automáticamente")

# TEST 2: Enqueue + Dequeue conserva el orden FIFO
@given(
    size=st.integers(min_value=1, max_value=20),
    items=st.lists(st.integers(min_value=-(2**30), max_value=2**30-1),
                   min_size=0, max_size=20)
)
def test_fifo_order(size, items):
    """La propiedad FIFO: lo que entra primero, sale primero."""
    q = Queue(size)
    inserted = []
    for item in items:
        if q.enqueue(item):
            inserted.append(item)
    retrieved = []
    while not q.empty():
        retrieved.append(q.dequeue())
    assert inserted == retrieved   # ← PROPIEDAD FUNDAMENTAL

test_fifo_order()
print("YES TEST 2: Orden FIFO — Hypothesis generó listas aleatorias automáticamente")

# TEST 3: size nunca supera max
@given(
    size=st.integers(min_value=1, max_value=10),
    ops=st.lists(st.booleans(), min_size=0, max_size=30)
)
def test_size_nunca_supera_max(size, ops):
    """True=enqueue, False=dequeue — secuencia aleatoria de operaciones."""
    q = Queue(size)
    for enq in ops:
        if enq:
            q.enqueue(42)
        else:
            q.dequeue()
        assert 0 <= q.size <= q.max
        q.checkRep()

test_size_nunca_supera_max()
print("YES TEST 3: size ∈ [0, max] — Hypothesis generó secuencias aleatorias de ops")

# TEST 4: enqueue devuelve False solo cuando está llena
@given(size=st.integers(min_value=1, max_value=15))
def test_enqueue_llena(size):
    """Al llenar la cola, el siguiente enqueue DEBE retornar False."""
    q = Queue(size)
    for i in range(size):
        result = q.enqueue(i)
        assert result == True
    assert q.full()
    assert q.enqueue(999) == False

test_enqueue_llena()
print("YES TEST 4: enqueue→False cuando llena — probado con múltiples tamaños")

# TEST 5: dequeue devuelve None en cola vacía
@given(size=st.integers(min_value=1, max_value=10))
def test_dequeue_vacia(size):
    """Una cola vacía siempre retorna None al hacer dequeue."""
    q = Queue(size)
    assert q.dequeue() is None

test_dequeue_vacia()
print("YES TEST 5: dequeue→None cuando vacía — verificado automáticamente")

# TEST 6: Wrap-around circular funciona correctamente
@given(
    size=st.integers(min_value=2, max_value=10),
    rounds=st.integers(min_value=1, max_value=5)
)
def test_wrap_around(size, rounds):
    """Llena y vacía la cola múltiples veces para forzar el wrap-around."""
    q = Queue(size)
    for _ in range(rounds):
        for i in range(size):
            q.enqueue(i)
        q.checkRep()
        for _ in range(size):
            q.dequeue()
        q.checkRep()
    assert q.empty()

test_wrap_around()
print("YES TEST 6: Wrap-around circular — Hypothesis probó múltiples ciclos")

print("\n" + "=" * 60)
print("YES TODOS LOS TESTS AUTOMÁTICOS PASARON")
print("   Hypothesis generó cientos de casos de prueba automáticamente,")
print("   incluyendo valores extremos, negativos y secuencias inesperadas.")
print("=" * 60)
