from django.test import TestCase

# Create your tests here.

# metaclass是类的模板，所以必须从`type`类型派生：
class ListMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['add'] = lambda self, value: self.append(value)
        attrs['hello'] = lambda : print('hello')
        return type.__new__(cls, name, bases, attrs)


class MyList(list, metaclass=ListMetaclass):
    @classmethod
    def hello2(cls):
        print('hello2')


MyList.hello()
MyList.hello2()

class MyEncoder(simplejson.JSONEncoder):
    """ 继承自simplejson的编码基类，用于处理复杂类型的编码
    """

    def default(self, obj):
        if isinstance(obj, QuerySet):
            """ Queryset实例
            直接使用Django内置的序列化工具进行序列化
            但是如果直接返回serialize('json',obj)
            则在simplejson序列化时会被从当成字符串处理
            则会多出前后的双引号
            因此这里先获得序列化后的对象
            然后再用simplejson反序列化一次
            得到一个标准的字典（dict）对象
            """
            return simplejson.loads(serialize('json', obj))
        if isinstance(obj, models.Model):
            """
            如果传入的是单个对象，区别于QuerySet的就是
            Django不支持序列化单个对象
            因此，首先用单个对象来构造一个只有一个对象的数组
            这是就可以看做是QuerySet对象
            然后此时再用Django来进行序列化
            就如同处理QuerySet一样
            但是由于序列化QuerySet会被'[]'所包围
            因此使用string[1:-1]来去除
            由于序列化QuerySet而带入的'[]'
            """
            return simplejson.loads(serialize('json', [obj])[1:-1])
        if hasattr(obj, 'isoformat'):
            # 处理日期类型
            return obj.isoformat()
        return simplejson.JSONEncoder.default(self, obj)

def toJSON(obj):
   if isinstance(obj, QuerySet):
       return simplejson.dumps(obj, cls=DjangoJSONEncoder)
   if isinstance(obj, models.Model):
       #do the same as above by making it a queryset first
       set_obj = [obj]
       set_str = simplejson.dumps(simplejson.loads(serialize('json', set_obj)))
       #eliminate brackets in the beginning and the end
       str_obj = set_str[1:len(set_str)-2]
   return str_obj

def getJson(**args):
    """    使用MyEncoder这个自定义的规则类来序列化对象
    """
    result = dict(args)
    return simplejson.dumps(result, cls=MyEncoder)


def account(request):
    accounts = WxAccounts.objects.filter(nickname="Aaaaaaaaaaayou")
    for obj in accounts:
        print (obj)
    # return JsonResponse(list(accounts), encoder=MyEncoder, safe=False)
    # return JsonResponse(data, safe=False)
