"""
在应用的models.py文件中，通过一个内嵌类class Meta给model定义元数据，类似于
class Foo(models.Model)
    bar = models.CharField(max_length=30)

    class Meta:
        ...
        ...
Model元数据就是’不是一个字段的任何数据‘--比如排序选项，admin选项等等
下面是所有可能用到的Meta选项，没有一个选项是必须的，是否添加class Meta到model完全是可选的

1.app_label:只在一种情况下使用，就是你的模型类不在默认的应用程序包下的models.py文件中，这时候需要指定这个模型
类是哪个应用程序的，比如在其他地方写了一个模型类，而这个模型类是属于myapp的，那么这时需要指定为：
app_label = 'myapp'

2.db_table:用于指定自定义数据库表名。Django有一套默认的按照一定规则生成数据模型对应的数据库表名，如果想使用自定
义的表名，就通过这个属性指定：table_name = 'my_owner_table'
若不提供该参数，Django会使用app_lable+'_'+module_name作为表的名字
若表的名字是一个SQL保留字，或包含python变量名不允许的字符--特别是连字符，Django会自动在幕后将列名字和表名字用
引号引起来

3.db_tablespace:有些数据库有数据表空间，如Oracle。可以通过db_talbespace来指定这个模型对应的数据库表放在哪个
数据表空间

4.get_latest_by:由于Django的管理方法中有个lastest()方法，就是得到最近一行记录。如果数据模型中有DateField
或DateTimeField类型的字段，可以通过这个选项来指定lastest()是按照哪个字段进行选取的
一个DateField或DateTimeField字段的名字，若提供该选项，该模块将拥有一个get_lastest()函数以得到最新的对象：
get_latest_by = 'order_date'

5.managed:由于Django会自动根据模型类生成映射的数据库表，如果不希望Django这么做，可以把managed的值设置为False
managed默认值为True时Django可以对数据库表进行迁移、删除等操作

6.order_with_respect_to:这个选项一般用于多对多关系中，它指向一个关联对象。关联对象找到这个对象后它是经过排序的
指定这个属性后会得到一个get_xxx_order()和set_xxx_order()的方法，通过他们可以设置或者回去排序的对象
例如，一个PizzaTopping关联到一个Pizza对象，这样做：
order_with_respect_to = 'pizza'
就允许toppings依照相关的pizza来排序

7.ordering：告诉Django模型对象返回的记录结果集是按照哪个字段排序的，比如下面的代码：
# 按订单升序排序
ordering = ['order_date']
# 按订单降序排序，- 表示降序
ordering = ['-order_date']
# 随机排序，？表示随机
ordering = ['?order_date']
# 对pub_date降序，然后对author升序
ordering = ['-pub_date', 'author']
需要注意的是，不论使用了多少字段排序，admin只使用第一个字段

8.permissions:在Django Admin管理模块下使用的。如果设置了这个属性可以让指定的方法权限描述更清晰可读。要创建
一个对象所需要的额外的权限，如果一个对象有admin设置，则每个对象的添加、删除和改变权限会依据该选项自动创建，下面
这个例子指定了一个附加权限：can_deliver_pizzas:
permissions = (('can_deliver_pizzas', 'Can deliver pizzas'),)
这是一个2元素tuple的tuple或列表，其中2元素tuple的格式为:(permissions_code, human_readable_permissi
on_name)

9.unique_together:需要通过两个字段保持唯一性时使用。这会在Django admin层和数据库层同时做出限制（也就是相关
的UNIQUE语句会被包括在CREATE TABLE语句中）。比如，一个Person的Firstname和lastname两者的组合必须是唯一的，
那么需要这样设置：
unique_together = (('first_anme', 'last_name'),)

10.verbose_name:给模型类起一个更可读的名字
verbose_name = 'pizza'
若未提供该选项，Django则会用一个类名字的munged版本来代替：CamelCase becomes camel case

11.verbose_name_plural:指定模型的复数形式是什么，如：
verbose_name_plural = 'sotries'
若未提供该选项，Django会使用verbose_name + 'S'
"""