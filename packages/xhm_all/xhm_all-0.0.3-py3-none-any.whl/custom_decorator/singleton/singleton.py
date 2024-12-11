def singleton(cls):
    instances = {}

    class SingletonWrapper(cls):
        def __new__(cls, *args, **kwargs):
            if cls not in instances:
                instances[cls] = super(SingletonWrapper, cls).__new__(cls)
                instances[cls].__init__(*args, **kwargs)
            return instances[cls]

    return SingletonWrapper
