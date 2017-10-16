from random import shuffle

if __name__ == "__main__":
    idList = []
    for i in  range(20):
        idList.append(i)
    print(idList)
    shuffle(idList)
    print(idList)