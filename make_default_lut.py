with open("default.txt","w") as deflut:
    for i in range(64):
        for j in range(1024):
            deflut.write(str(j) + "\n")
