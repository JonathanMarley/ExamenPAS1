import threading

#vamos a utilizar las variales de entorno que seria la global en este caso vamos gregar
x = 0

#objeto lock
lock = threading.Lock()

def incremento():
    global x
    with lock:
        x += 1

def TareaThread():
    for _ in range(100000):
        incremento()

def TareaPrin():
    global x
    x = 10
    for i in range(10):
        incremento()
        print("Iteraccion {0}: x = {1}".format(i, x))

if __name__ == "__main__":
    for i in range(10):
        TareaPrin()
