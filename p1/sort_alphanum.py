output = ['0ZEB', 'BIL8', 'FK1M', 'RAUN', 'UG44']

def sort(lst):
    #lst = [str(i) for i in lst] 
    #lst.sort() 
    #lst = [int(i) if i.isdigit() else i for i in lst ] 
    #return lst
    print(lst[1][1])
    for i in range(len(lst)-1):
        #print(i[0])
        if lst[i][0].isdigit():
            print(lst[i])
            temp_String = lst[i]
            lst.pop(i)
            print(lst)
            lst.append(temp_String)
            print(lst)
            

sort(output)