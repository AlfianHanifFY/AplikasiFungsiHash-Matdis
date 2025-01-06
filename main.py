import time

def readFile(filePath):
    try:
        with open(filePath, 'r') as file:
            words = file.read().splitlines()  
        return words
    except FileNotFoundError:
        print("\033[1;31mFile tidak ditemukan.\033[0m")
        return []


def hash(word, datasetSize):
    ascii_sum = sum(ord(char) for char in word)
    return ascii_sum % datasetSize


def addHashChaining(hashDataset, word, datasetSize):
    index = hash(word, datasetSize)
    
    if hashDataset[index] == []:
        hashDataset[index] = [word]
    else:
        hashDataset[index].append(word)
        
def createHashDataset(words, datasetSize):
    hashDataset = [[] for _ in range(datasetSize)] 
    collisions = 0
    
    for word in words:
        index = hash(word, datasetSize)
        if hashDataset[index]:
            collisions += 1
        addHashChaining(hashDataset, word, datasetSize)
    
    return hashDataset, collisions


def searchHash(hashDataset, target,datasetSize):
    index = hash(target, datasetSize)
    comparisons = 0  
    
    if hashDataset[index] != []:
        for word in hashDataset[index]:
            comparisons += 1
            if word == target:
                return True, comparisons 
    return False, comparisons  


def linearSearch(words, target):
    comparisons = 0
    for word in words:
        comparisons += 1
        if word == target:
            return True, comparisons
    return False, comparisons





datasetSize = 14557  
filePath = "data.txt" 
words = readFile(filePath)
if words:
    print("\n\033[1;32mProses dataset dengan " + str(len(words)) + " kata...\033[0m\n")
    print("\033[1;33mHash Chaining:\033[0m")
    hashDataset, collisions = createHashDataset(words, datasetSize)
    print(f"\033[1;32mTotal Collisions : {collisions}\033[0m\n")
    
    while True:
        print("\n\033[1;34mMasukkan Kata yang ingin dicari (atau '\033[1;31mexit\033[1;34m' untuk keluar): \033[0m")
        word_to_search = input().strip()
        if word_to_search.lower() == "exit":
            print("\033[1;31mProgram selesai.\033[0m")
            break

        if not word_to_search:
            print("\033[1;31mInput tidak boleh kosong.\033[0m")
            continue
        
        startTime = time.time()
        found, comparisons = searchHash(hashDataset, word_to_search,datasetSize)
        elapsedTime = time.time() - startTime
        simple_search_time = elapsedTime * 1000
        
        startTime = time.time()
        found_conv, comparisons_conv = linearSearch(words, word_to_search)
        elapsedTime = time.time() - startTime
        linearSearch_time = elapsedTime * 1000

        print(f"\n\033[1;33mHasil Pencarian Kata: {word_to_search}\033[0m")
        print("+----+-------------------+----------------+-------------------+-------------------+")
        print("| No |  Fungsi           | Ketemu         | Perbandingan (n)  | Waktu (ms)        |")
        print("+----+-------------------+----------------+-------------------+-------------------+")
        print(f"| 1  | Hash              | {'\033[1;32m✔\033[0m' if found else '\033[1;31m✘\033[0m'}              | {comparisons:<17} | {simple_search_time:.6f}          |")
        print(f"| 2  | Linear Search     | {'\033[1;32m✔\033[0m' if found else '\033[1;31m✘\033[0m'}              | {comparisons_conv:<17} | {linearSearch_time:.6f}          |")
        print("+----+-------------------+----------------+-------------------+-------------------+")

else:
    print("\033[1;31mTidak ada kata yang dibaca dari file.\033[0m")
