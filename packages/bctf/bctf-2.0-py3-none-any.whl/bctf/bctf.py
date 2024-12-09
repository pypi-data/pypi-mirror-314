import pickle
import csv
def write(file,content,delimiters=","):
    ext = file.name.split(".")[-1].lower()
    if ext=="txt":
        file.write(str(content)+"\n")
    elif ext=="dat":
        pickle.dump(content,file)
    elif ext=="csv":
        cont=csv.writer(file,delimiter=delimiters)
        cont.writerow(content)
    else:
        print("Unsupported file")
def read(file,delimiters=",",bytes=""):
    ext = file.name.split(".")[-1].lower()
    if ext=="txt":
        cont=file.read()
    elif ext=="dat":
        cont=[]
        while True:
            try:
                cont.append(pickle.load(file))
            except EOFError:
                break
        return cont
    elif ext=="csv":
        cont=csv.reader(file,delimiter=delimiters)
        return list(cont)
    else:
        print("Unsupported file")
def append(file,content,delimiters=","):
    ext = file.name.split(".")[-1].lower()
    if ext=="txt":
        file.write(str(content)+"\n")
    elif ext=="dat":
        pickle.dump(content,file)
    elif ext=="csv":
        cont=csv.writer(file,delimiter=delimiters)
        cont.writerow(content)
    else:
        print("Unsupported file")
