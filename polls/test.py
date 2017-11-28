import functools
def print_hello(method):
    print 'aaa'
    @functools.wraps(method)
    def wrapera(*args, **kwargs): 
        print "hello"
        kwargs['name']='fly'
        return method(*args, **kwargs)
    return wrapera

def hello():
    print 'yes hello'

@print_hello
def sayHi(name):
    print "hi"+name
    
sayHi()

print_hello(hello)