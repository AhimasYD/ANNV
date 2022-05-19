from weakref import ref


class WeakMethod:
    def __init__(self, obj, fun):
        self.obj = ref(obj)
        self.fun = fun

    def __call__(self, *arg):
        if self.obj() is None:
            print('No more object')
            return
        params = (self.obj(),) + arg
        self.fun(*params)
