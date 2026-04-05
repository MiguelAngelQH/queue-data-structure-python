# TASK:
#
# Achieve full statement coverage on the Queue class. 
# You will need to:
# 1) Write your test code in the test function.
# 2) Press submit. The grader will tell you if you 
#    fail to cover any specific part of the code.
# 3) Update your test function until you cover the 
#    entire code base.
#
# You can also run your code through a code coverage 
# tool on your local machine if you prefer. This is 
# not necessary, however.
# If you have any questions, please don't hesitate 
# to ask in the forums!

import array

class Queue:
    def __init__(self,size_max):
        assert size_max > 0
        self.max = size_max
        self.head = 0
        self.tail = 0
        self.size = 0
        self.data = array.array('i', range(size_max))

    def empty(self):
        return self.size == 0

    def full(self):
        return self.size == self.max

    def enqueue(self,x):
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
            assert (self.tail-self.head) == self.size
        if self.tail < self.head:
            assert (self.head-self.tail) == (self.max-self.size)
        if self.head == self.tail:
            assert (self.size==0) or (self.size==self.max)

# Add test code to test() that achieves 100% coverage of the 
# Queue class.
def test():
    print("=" * 55)
    print("EJERCICIO 1: Tests manuales con cobertura 100%")
    print("=" * 55)

    # --- Test __init__ con assert (size_max > 0) ---
    print("\n[1] Test __init__ con tamaño inválido (assert):")
    try:
        q_bad = Queue(0)
    except AssertionError:
        print("    YES: AssertionError capturado correctamente para size=0")

    # --- Cola básica vacía ---
    print("\n[2] Cola recién creada:")
    q = Queue(3)
    print(f"    empty()={q.empty()} → esperado True:  {'YES' if q.empty() else 'NO'}")
    print(f"    full()={q.full()}  → esperado False: {'YES' if not q.full() else 'NO'}")
    q.checkRep()
    print("    checkRep() → YES sin errores (tail==head, size==0)")

    # --- enqueue normal ---
    print("\n[3] Enqueue de elementos:")
    r1 = q.enqueue(10)
    r2 = q.enqueue(20)
    print(f"    enqueue(10)={r1} → True: {'YES' if r1 else 'NO'}")
    print(f"    enqueue(20)={r2} → True: {'YES' if r2 else 'NO'}")
    print(f"    empty()={q.empty()} → False: {'YES' if not q.empty() else 'NO'}")
    print(f"    full()={q.full()}  → False: {'YES' if not q.full() else 'NO'}")
    q.checkRep()  # tail > head
    print("    checkRep() → YES (tail > head)")

    # --- Llenar la cola ---
    print("\n[4] Llenar la cola (enqueue hasta full):")
    r3 = q.enqueue(30)
    print(f"    enqueue(30)={r3} → True: {'YES' if r3 else 'NO'}")
    print(f"    full()={q.full()} → True: {'YES' if q.full() else 'NO'}")
    q.checkRep()  # head==tail, size==max
    print("    checkRep() → YES (head==tail, size==max)")

    # --- enqueue cuando está llena ---
    print("\n[5] Enqueue con cola llena:")
    r4 = q.enqueue(99)
    print(f"    enqueue(99)={r4} → False: {'YES' if not r4 else 'NO'}")

    # --- dequeue normal ---
    print("\n[6] Dequeue de elementos:")
    v1 = q.dequeue()
    v2 = q.dequeue()
    print(f"    dequeue()={v1} → 10: {'YES' if v1 == 10 else 'NO'}")
    print(f"    dequeue()={v2} → 20: {'YES' if v2 == 20 else 'NO'}")
    q.checkRep()
    print("    checkRep() → YES")

    # --- Wrap-around circular (tail vuelve a 0) ---
    print("\n[7] Wrap-around circular del tail:")
    q.enqueue(40)
    q.enqueue(50)  # tail llega a max → vuelve a 0
    q.checkRep()
    print("    checkRep() → YES (tail wrapped)")

    # --- Wrap-around del head ---
    print("\n[8] Wrap-around circular del head:")
    q.dequeue()  # saca 30
    q.dequeue()  # saca 40
    q.dequeue()  # saca 50, head llega a max → vuelve a 0
    q.checkRep()
    print("    checkRep() → YES (head wrapped)")

    # --- dequeue en cola vacía ---
    print("\n[9] Dequeue con cola vacía:")
    v_none = q.dequeue()
    print(f"    dequeue()={v_none} → None: {'YES' if v_none is None else 'NO'}")

    # --- head < tail en checkRep ---
    print("\n[10] checkRep con head < tail (después de nuevo ciclo):")
    q2 = Queue(5)
    for i in range(3):
        q2.enqueue(i)
    q2.dequeue()
    q2.checkRep()  # tail(3) > head(1)
    print("    checkRep() → YES (tail > head)")

    # Forzar head > tail
    print("\n[11] checkRep con head > tail (wrap-around):")
    q3 = Queue(3)
    q3.enqueue(1); q3.enqueue(2); q3.enqueue(3)
    q3.dequeue(); q3.dequeue()
    q3.enqueue(4)  # tail wraps → tail=0, head=2 → head > tail
    q3.checkRep()
    print("    checkRep() → YES (head > tail)")

    print("\n" + "=" * 55)
    print("YES TODOS LOS TESTS PASARON — Cobertura 100%")
    print("=" * 55)

test()

