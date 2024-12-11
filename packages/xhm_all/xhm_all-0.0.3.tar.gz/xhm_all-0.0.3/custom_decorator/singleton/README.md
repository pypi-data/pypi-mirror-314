### 使用说明
单例模式装饰器，使用示例：
~~~
@singleton
class MyClass:
    def __init__(self, x):
        self.x = x

# 创建实例
instance1 = MyClass(42)
instance2 = MyClass(24)

# 两个实例是同一个对象
print(instance1 is instance2)  # True
print(instance1.x)  # 42
print(instance2.x)  # 42
~~~