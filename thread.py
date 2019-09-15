import time
from threading import Thread
from random import uniform


def myfunc(name):
    for i in range(50):
        time.sleep(uniform(0.5, 0))
    print(name)


def corrida():
    t1 = Thread(target=myfunc, args=("Coelho",))
    t2 = Thread(target=myfunc, args=("Vaca",))
    t3 = Thread(target=myfunc, args=("Cachorro",))
    t4 = Thread(target=myfunc, args=("Elefante",))
    t5 = Thread(target=myfunc, args=("Gafanhoto",))

    t1.name = "Coelho"
    t2.name = "Vaca"
    t3.name = "Cachorro"
    t4.name = "Elefante"
    t5.name = "Gafanhoto"

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

corrida()

"""
class CustomThread(Thread):
    def run(self):
        print('Custom thread function.\n')

for i in range(3):
    t = CustomThread()
"""