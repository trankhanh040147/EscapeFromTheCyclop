def randMap():
    import random
    f = open("./assets/data/MAP/map1.txt", 'w')
    string = ''
    for i in range(0, 50):
        x = random.randint(0, 29)
        y = random.randint(0, 16)
        string += str(f"{x} {y}.")
    string = string[:-1]
    f.write(string)
    f.close()

def addbox(pos):
    f = open('./assets/data/MAP/map1.txt', 'a')
    string = str(f".{pos[0]} {pos[1]}")
    f.write(string)
    f.close()
