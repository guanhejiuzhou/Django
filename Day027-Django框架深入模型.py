"""
一、配置关系型数据库MySQL：
1.修改项目的配置文件setting.py：在配置ENGINE属性时，常用的可选值包括：
django.db.backends.sqlite3:SQLite嵌入式数据库
django.db.backends.postgresql:BSD许可证下发行的开源关系型数据库产品
django.db.backends.mysql:甲骨文公司的经济高效的数据库产品
django.db.backends.oracle:甲骨文公司的关系型数据库旗舰产品

2.python操作MySQL的依赖库PyMySQL，如果使用python3需要修改项目目录下的__init__.py文件并加入如下所示的
代码，避免Django找不到连接MySQL的客户端工具，代码为：
pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()

3.为应用程序创建数据库，创建名为oa的数据库：create database oa default charset utf8;

4.Django框架自身有自带的数据模型，后面会用到，为此先做一次迁移操作。所谓迁移，就是根据模型自动生成关系数据库中
的二维表，命令为：python manage.py migrate

5.为应用创建数据模型：定义模型使用字段类及其属性，IntegerField对应数据库中的integer类型，CharField对应
数据库的varchar类型，DecimalField对应数据库的decimal类型，ForeignKey用来建立多对一外键关联。字段属性
primary_key用于设置主键，max_length用来设置字段的最大长度，db_column用来设置数据库中与字段对应的列，
verbose_name则设置了Django后台管理系统中该字段显示的名称。

6.再次执行迁移操作，先通过模型生成迁移文件，再执行迁移创建二维表，代码：python manage.py makemigrations hrs
 python manage.py migrate
"""
'''
Django模型最佳实践：
1.正确的为模型和关系字段命名
2.设置适当的related_name属性
3.用OneToOneField代替ForeignKeyField(unique=True)
4.通过迁移操作（migrate）来添加模型
5.用NoSQL来应对需要降低范式级别的场景
6.如果布尔类型可以为空要使用NullBooleanField
7.在模型中放置业务逻辑
8.用<ModelName>.DoesNotExists取代ObjectDoesNotExists
9.在数据库中不要出现无效数据
10.不要对QuerySet调用len()函数
11.将QuerySet的exists()方法的返回值用于if条件
12.用DecimalField来存储货币相关数据而不是FloatField
13.定义__str__方法
14.不要将数据文件放在同一个目录中

'''

'''
模型定义参考
对字段名称的限制：字段名不能是python的保留字，否则会导致语法错误；字段名不能有多个连续下划线，否则影响ORM查询

Django模型字段类：
字段类                 说明
AutoField             自增ID字段
BigIntegerField       64位有符号整数
BinaryField           存储二进制数据的字段，对应python的bytes类型
BooleanField          存储True或False
CharField             长度较小的字符串
DateField             存储日期，有auto_now和auto_now_add属性
DateTimeField         存储日期和日期，两个附加属性同上
DecimalField          存储固定精度小数，有max_digits(有效位数)和decimal_places(小数点后面)两个必要的参数
DurationField         存储时间跨度
EmailField            与CharField相同，可以用EmailValidator验证
FileField             文件上传字段
FloatField            存储浮点数
ImageField            其他同FileField，要验证上传的是不是有效图像
IntegerField          存储32位有符号整数
GenericlPAddressField 存储IPV4或IPV6地址
NullBooleanField      存储True、false或null值
PositiveIntegerField  存储无符号整数（只能存储整数）
SluqField             存储Slug（简短标注）
SmallIntegerField     存储16位有符号整数
TextField             存储数据量较大的文本
TimeField             存储时间
URLField              存储URL的CharField
UUIDField             存储全局唯一标识符


字段属性：
属性                   说明
null                  数据库中对应的字段是否允许为null，默认为false
blank                 后台模型管理验证数据时，是否允许为null，默认为false
choices               设定字段的选项，各元组中的第一个值是设置在模型上的值，第二个值是人类可读的值
db_column             字段对应到数据库表中的列名，未指定时直接使用字段的名称
db_index              设置为True时将在该字段创建索引
db_tablespace         为有索引的字段设置使用的表空间，默认为DEFAULT_INDEX_TABLESPACE
default               字段的默认值
editable              字段在后台模型管理或ModelForm中是否显示，默认为True
error_messages        设定字段抛出异常时的默认消息的字典，其中的键包括null/blank/invalid/invalid_choice;unique/unique_for_date
help_text             表单小组件旁边显示的额外的帮助文本
primary_key           将字段指定为模型的主键，未指定时会自动添加AutoField用于主键，只读
unique                设置为True时，表中字段的值必须是唯一的
verbose_name          字段在后台模型管理显示的名称，未指定时使用字段的名称

ForeignKey属性：
1.limit_choices_to:值是一个Q对象或返回一个Q对象，用于限制后台显示哪些对象
2.related_name:用于获取关联对象的关联管理器对象（反向查询），如果不允许反向，该属性应该被设置为'+'或者以'+"结尾
3.to_field：指定关联的字段，默认关联对象的主键字段
4.db_constraint:是否为外键创建约束，默认值为True
5.on_delete:外键关联的对象被删除时对应的动作，可取的值包括django.db.models中定义的
    CASCADE:级联删除
    PROTECT：抛出ProtectedError异常，阻止删除引用的对象
    SET_NULL:把外键设置为null，当null属性被设置为True时才能这么做
    SET_DEFAULT：把外键设置为默认值，提供了默认值才能这么做
    
ManyToManyField属性：
1.symmetrical:是否建立对称的多对的关系
2.through:指定维持多对多关系的中间表的Django模型
3.throughfields:定义了中间模型时可以指定建立多对多关系的字段
4.db_table:指定维持多对多关系的中间表的表名
'''

'''
模型单元数据选项：
选项                  说明
abstract             设置为True时模型是抽象父类
app_label            如果定义模型的应用不在INSTALLED_APPS中可以用该属性指定
db_table             模型使用的数据表名称
db_tablespace        模型使用的数据表空间
default_related_name 关联对象回指这个模型时默认使用的名称，默认为<model_name>_set
get_latest_by        模型中可排序字段的名称
managed              设置为True时，Django在迁移中创建数据表并在执行flush管理命令时把表移除
order_with_respect_to   标记对象为可排序的
ordering             对象的默认排序
permissions          创建对象时写入权限表的额外权限
default_permissions  默认为('add', 'change', 'delete')
unique_together      设定组合在一起时必须独一无二的字段名
index_together       设定一起建立索引的多个字段名
verbose_name         为对象设定人类可读的名称
verbose_name_plural  设定对象的复数名称
'''

'''
按字段查找可以用的条件：
1.exact/iexact：精确匹配/忽略大小写的精确匹配查询
2.contains/icontains/startswith/istartwith/endwith/iendswith:基于like的模糊查询
3.in：集合运算
4.gt/gte/It/Ite:大于/大于等于/小于/小于等于关系运算
5.range：指定范围查询（SQL中的between...and...）
6.year/month/day/week_day/hour/minute/second:查询时间日期
7.isnull：查询空值（True）或非空值（False）
8.search：基于全文索引的全文检索
9.regex/iregex:基于正则表达式的模糊查询
'''