print("test")

i=int(input("请输入"))
if i ==1 :
    print(1)
    while i!=5 :
        i=i+1
        print("while OK 数值",i)
        if i==2 :
            continue
        print("while OK 数值 continue",i)
    print("while 数值",i)

elif i==2 :
    print("2")
    for i in range(i) :
        print(i)
else :
    for j in range(i) :
        print("!=1,数值为",j)
        if j==7 :
            break
            print("break")