# print (int(2**15))
#包 必须含有__init__.py文件
#python程序由包(package)、模块(module)和函数组成。包是由一系列模块(文件，函数集合体)组成的集合。模块是处理某一类问题的函数和类的集合。
#包的作用是实现程序的重用。
#函数
print ("1")
def sort (s1,s2):
    if s1>s2 :
        print (s1) 
    elif s1==s2 :
        print ("=")
    else :
        print (s2,"big") 
s1=1
s2=2
sort(s1,s2)
print ("s1=",s1)

#类

class Fruit:
    #A 变量是一个类变量，它的值将在这个类的所有实例之间共享。你可以在内部类或外部类使用 Fruit.A 访问。
    A=100
    def __init__(self) :
       print ("Fruit _init")
    def grow(self):
    
       print ("Fruit grow2")

#对象 对象的三特效 即对象的句柄、属性和方法
# f1=Fruit()
# f1.grow()
# python使用函数"staticmethod()"或"@ staticmethod"指令的方法把普通的函数转换为静态方法。静态方法相当于全局函数。
#6 python的构造函数名为__init__，析构函数名为__del__
# self 代表类的实例，self 在定义类的方法时是必须有的，虽然在调用时不必传入相应的参数。 self代表类的实例，而非类
#self 代表的是类的实例，代表当前对象的地址，而 self.__class__ 则指向类。 self 不是关键字
#继承
# 1、如果在子类中需要父类的构造方法就需要显式的调用父类的构造方法，或者不重写父类的构造方法。详细说明可查看： python 子类继承父类构造函数说明。
# 2、在调用基类的方法时，需要加上基类的类名前缀，且需要带上 self 参数变量。区别在于类中调用普通函数时并不需要带上 self 参数
# 3、Python 总是首先查找对应类型的方法，如果它不能在派生类中找到对应的方法，它才开始到基类中逐个查找。（先在本类中查找调用的方法，找不到才去基类中找）。
class Apple(Fruit):
   A=200 
   B=300
   def __init__(self) :
       print ("Apple _init")
   def grow(self) :
       print ("Fruit apple")
f2=Fruit()
f2.grow()
print (Fruit.A)
print (Apple.A)
print (Apple.B)
print (f2.A)
f3=Apple()
f3.grow()


#实例对象属性修改
# getattr(obj, name[, default]) : 访问对象的属性。
# hasattr(obj,name) : 检查是否存在一个属性。
# setattr(obj,name,value) : 设置一个属性。如果属性不存在，会创建一个新属性。
# delattr(obj, name) : 删除属性。
# Print (f2.age)
#增加
print (hasattr(f2,'age'))
f2.age=10
print (hasattr(f2,'age'))
print (f2.age)
#修改
f2.age=20
print (f2.age)
#查看当前对象类型
print (type(1))
#删除
del f2.age
print (hasattr(f2,'age'))
# print (f2.age)

