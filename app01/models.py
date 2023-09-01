from django.db import models


class Admin(models.Model):
    """ 管理员 """
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    def __str__(self):
        return self.username


class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name="部门表", max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    deposit = models.DecimalField(verbose_name="存款", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name="入职时间")

    # 无约束
    # depart_id = models.IntegerField(verbose_name='部门ID')
    # 1. 有约束
    #     - to, 与哪张表关联
    #     - to_field, 与表中哪一列关联
    # 2. Django
    #     - 写的depart
    #     - 生成的数据列depart_id
    # 3. 如果部门表被删除
    # #### 3.1 级联删除
    # depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)
    # #### 3.2 depart_id列置空
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id",
                               null=True, blank=True, on_delete=models.SET_NULL)

    # 在Django中做的约束
    gender_choices = (
        (1, "male"),
        (2, "female"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class PrettyNum(models.Model):
    """ 靓号表 """
    mobile = models.CharField(verbose_name="手机号", max_length=32)
    price = models.IntegerField(verbose_name="价格", default=0)

    level_choices = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)

    status_choices = (
        (1, "已占用"),
        (2, "未使用"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)


class Order(models.Model):
    """ 订单 """
    order_id = models.CharField(verbose_name="order number", max_length=64)
    product = models.CharField(verbose_name="product", max_length=64)
    price = models.IntegerField(verbose_name="price")

    status_choices = (
        (1, "Pending"),
        (2, "Ordered"),
    )
    status = models.SmallIntegerField(verbose_name="status", choices=status_choices, default=1)
    customer = models.ForeignKey(verbose_name="name", to="Admin", on_delete=models.CASCADE)
