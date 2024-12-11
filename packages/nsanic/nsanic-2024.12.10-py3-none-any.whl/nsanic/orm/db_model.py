import asyncio
from datetime import datetime, date
from enum import Enum
from typing import Union
from uuid import UUID

from tortoise import Model, fields, connections, transactions
from tortoise.converters import encoders
from tortoise.expressions import Q

from nsanic.libs import tool_dt

GeneratorClass = None


class DBModel(Model):
    _SPLIT_TABLES = set()
    '''当前分表集合'''
    _SPLIT_SUFFIX = {1: 'str', 2: 'y%Y', 3: 'y%Ym%m', 4: 'y%Yw%w', 5: 'y%Ym%md%d'}
    '''表名后缀类型映射 1--自定义标记 2--按日期年标记 3--按日期年月标记 4--按日期年周标记 5--按日期年月日标记'''
    _SPLIT_TYPE = 0
    '''分表模式 0--不分表 1--自定义标记分表 2--按年分表 3--按月分表 4--按周分表 5--按日分表'''
    _SPLIT_FIELD = 'created'
    '''分表字段或标记字符串'''

    created = fields.BigIntField(null=True, index=True, default=0, description='创建时间')

    class Meta:
        abstract = True

    @classmethod
    def sheet_name(cls, suffix: Union[str, int, float, datetime, date] = None, tz: str = None):
        """
        数据表名 
        :param suffix: 当前待设置的后缀或后缀数据
        :param tz: 指定按日期分表数据的时区
        """
        tb_name = cls._meta.db_table or cls.__name__.lower()
        if cls._SPLIT_TYPE:
            if cls._SPLIT_TYPE not in cls._SPLIT_SUFFIX:
                raise Exception('Invalid split table type.')
            if (cls._SPLIT_TYPE == 1) or (isinstance(suffix, str)):
                tb_name = f"{tb_name}_{suffix}"
            else:
                fmt = cls._SPLIT_SUFFIX.get(cls._SPLIT_TYPE)
                tb_name = f"{tb_name}_{tool_dt.dt_str(suffix, fmt=fmt, tz=tz)}"
        return tb_name

    @classmethod
    def pk_name(cls):
        return cls._meta.db_pk_column

    @classmethod
    def check_field(cls, field: str):
        return field in cls._meta.db_fields

    @classmethod
    def out_fields(cls, forbids: Union[list, tuple, set] = None):
        """禁止部分字段输出"""
        return [name for name in cls._meta.db_fields if name not in forbids] if forbids else cls._meta.db_fields

    @staticmethod
    def check_val(val, field, model):
        if val is not None:
            if isinstance(val, UUID):
                val = str(val)
            elif isinstance(val, Enum):
                val = val.val if hasattr(val, 'val') else val.value
            return encoders.get(type(val))(val)
        column = model._meta.fields_map.get(field)
        if not column:
            raise Exception(f'数据模型{model.__name__}不包含指定的字段{field}')
        vdft = column.default
        if vdft is not None:
            if isinstance(vdft, UUID):
                vdft = str(vdft)
            elif isinstance(vdft, Enum):
                vdft = vdft.val if hasattr(vdft, 'val') else vdft.value
            return encoders.get(type(vdft))(vdft)
        return "NULL"

    @classmethod
    def get_meta_db(cls, db_key: str = None):
        if (not db_key) or (db_key == 'default'):
            return cls._meta.db
        else:
            conn = connections.get(db_key)
            if not conn:
                raise Exception(f'Can not found {db_key} db config, please confirm the config is exist.')
        if type(conn).__name__ == 'TransactionWrapper':
            return conn._parent
        return conn

    @classmethod
    def __check_orders(cls, orders: Union[str, list, tuple]):
        if orders:
            if isinstance(orders, str):
                orders = [orders]
            new_order = []
            for key in orders:
                key_str = key[1:] if key[0] in ('-', '+') else key
                (key_str in cls._meta.db_fields) and new_order.append(key)
            return new_order
        return []

    @classmethod
    def __fetch_generator_class(cls):
        global GeneratorClass
        if GeneratorClass:
            return GeneratorClass
        dialect = cls._meta.db.schema_generator.DIALECT
        if dialect == 'postgres':
            from nsanic.orm.pgsql_generator import PgSqlGenerator
            GeneratorClass = PgSqlGenerator
        elif dialect == 'mysql':
            from nsanic.orm.mysql_generator import MySqlGenerator
            GeneratorClass = MySqlGenerator
        elif dialect == 'mssql':
            from nsanic.orm.mssql_generator import MsSqlGenerator
            GeneratorClass = MsSqlGenerator
        return GeneratorClass

    @classmethod
    def get_sheet_name(cls, tb_suffix: str = None):
        or_name = cls._meta.db_table or cls.__name__.lower()
        return f"{or_name}_{tb_suffix}" if tb_suffix else or_name, or_name

    @classmethod
    def get_split_suffix(cls, split: Union[str, int, float, datetime, date], param: dict, tz: str = None):
        """
        获取字典参数的分表后缀
        :param split: 分表标记或标记位数据
        :param param: 查询参数
        :param tz: 按日期分表数据的时区
        """
        if not cls._SPLIT_TYPE:
            return ''
        if cls._SPLIT_TYPE not in cls._SPLIT_SUFFIX:
            raise Exception('Invalid split table type.')
        if cls._SPLIT_TYPE == 1:
            return f'{split}'
        if not split:
            split = cls._SPLIT_FIELD
        kval = (param.get(split) or param.get(f'{split}__gte') or param.get(f'{split}__lte')
                or param.get(f'{split}__gt') or param.get(f'{split}__lt')) or tool_dt.cur_time()
        return f'{tool_dt.dt_str(kval, fmt=cls._SPLIT_SUFFIX.get(cls._SPLIT_TYPE), tz=tz)}'

    @classmethod
    async def exec_sql(cls, sql: str, db_key='default', query=False, for_one=False):
        db = cls.get_meta_db(db_key)
        if query:
            sta = await db.execute_query(sql)
        else:
            await db.execute_script(sql)
            sta = [1, 1]
        if (not sta) or (not sta[0]):
            if query:
                return []
            error = f'执行sql失败--{sta}: {sql}'
            raise Exception(error)
        return (sta[1] if not for_one else sta[1][0]) if sta and (len(sta) > 1) else True

    @classmethod
    async def exec_query(cls, sql: str, retry=1, db_key='default'):
        for i in range(retry):
            sta = await cls.exec_sql(sql, query=True, db_key=db_key)
            if not sta:
                await asyncio.sleep(0.2)
            return sta
        return None

    @classmethod
    async def exec_insert(cls, sql_list: list[str], use_transaction=False, db_key='default'):
        db = cls.get_meta_db(db_key)
        if not use_transaction:
            for sql in sql_list:
                sta = await db.execute_query(sql)
                if (not sta) or (not sta[0]):
                    error = f'执行sql失败--{sta}: {sql}'
                    raise Exception(error)
        else:
            async with transactions.in_transaction(db_key or 'default'):
                for sql in sql_list:
                    sta = await db.execute_query(sql)
                    if (not sta) or (not sta[0]):
                        error = f'执行sql失败--{sta}: {sql}'
                        raise Exception(error)
        return True

    @classmethod
    def gen_simple_query(
            cls,
            param: dict = None,
            field: Union[tuple, list, set] = None,
            exclude: Union[tuple, list, set] = None,
            groups: Union[str, list, tuple] = None,
            orders: Union[str, list, tuple] = None,
            offset=0,
            limit=0,
            with_del=False,
            with_field=False,
            db_key: str = None):
        if db_key and (db_key != 'default'):
            db = cls.get_meta_db(db_key)
            q_set = cls.filter(sta_del=False).using_db(db) if (hasattr(cls, 'sta_del')) and (not with_del) else cls.all(using_db=db)
        else:
            q_set = cls.filter(sta_del=False) if (hasattr(cls, 'sta_del')) and (not with_del) else cls.all()
        if param:
            q_set = q_set.filter(Q(**param))
        if groups:
            if isinstance(groups, str):
                groups = [groups]
            q_set = q_set.group_by(*groups)
        orders = cls.__check_orders(orders)
        if orders:
            q_set = q_set.order_by(*orders)
        if limit:
            q_set = q_set.limit(limit)
        if offset:
            q_set = q_set.offset(offset)
        if with_field:
            out_field = [f for f in field if f in cls._meta.db_fields] if field else (
                [v for v in cls._meta.db_fields if v not in exclude] if exclude else [])
            return q_set, out_field
        return q_set

    @classmethod
    async def check_table(cls, suffix: str = None, db_key: str = None):
        tb_name, or_name = cls.get_sheet_name(suffix)
        if tb_name not in cls._SPLIT_TABLES:
            cls._meta.db_table = cls._meta.basetable._table_name = tb_name
            _creator = cls.__fetch_generator_class()
            if not _creator:
                cls._meta.db_table = or_name
                raise Exception(f'未定义的表创建模式：{cls._meta.db.schema_generator.DIALECT}')
            db = cls.get_meta_db(db_key)
            _sql_dict = _creator(db).get_table_sql_new(cls)
            cls._meta.db_table = or_name
            if not _sql_dict:
                raise Exception(f'无法生成建表模型：{_sql_dict}')
            sql = _sql_dict.get('table_creation_string')
            if not sql:
                raise Exception(f'无法生成创建表SQL：{_sql_dict}')
            await cls._meta.db.execute_script(sql)
            cls._SPLIT_TABLES.add(tb_name)

    @classmethod
    async def fetch_on_page(
            cls,
            param: dict = None,
            page=1,
            size=20,
            field: Union[tuple, list, set] = None,
            exclude: Union[tuple, list, set] = None,
            groups: Union[str, list, tuple] = None,
            orders: Union[str, list, tuple] = '-created',
            split: Union[str, int, float, datetime, date] = None,
            with_del=False,
            with_count: int = 1,
            db_key: str = None,
            tz: str = None):
        """
        简单分页查询
        :param param:字典形式的查询参数, __lte __gte 等可自行通过key构造
        :param page: 页数
        :param size: 分页大小
        :param field: 指定输出的字段（优先）
        :param exclude: 指定不输出的字段
        :param groups: 分组字段
        :param orders: 排序字段
        :param split: 分表标记 设置分表类型为1时生效，
        :param with_count: 是否进行数量查询 0-否 1-精确数量 2-模糊数量(针对大表)
        :param with_del: 是否包含逻辑删除数据
        :param db_key: 采用的数据库配置
        :param tz: 指定按日期分表采用的时区
        """
        if page < 1:
            page = 1
        offset = (page - 1) * size
        total = 0
        q_set, out_field = cls.gen_simple_query(
            param=param, field=field, exclude=exclude, groups=groups, orders=orders, limit=size, offset=offset,
            with_del=with_del, with_field=True, db_key=db_key)
        suffix = cls.get_split_suffix(split, param, tz=tz)
        if suffix:
            cls._meta.basetable._table_name, _ = cls.get_sheet_name(suffix)
        if with_count:
            total = await q_set.count()
        data_list = await q_set.values(*out_field)
        return data_list, total

    @classmethod
    async def get_by_pk(
            cls,
            val: Union[int, str],
            field: Union[tuple, list] = None,
            exclude: Union[tuple, list] = None,
            split: Union[str, int, float, datetime, date] = None,
            db_key: str = None,
            tz: str = None):
        """
        通过唯一主键查询
        :param val: 主键值
        :param field: 指定输出的字段
        :param exclude: 指定排除的字段
        :param split: 分表标记 设置分表类型为1时生效，
        :param db_key: 指定数据库配置名
        :param tz: 按日期分表时指定的时区
        """
        if not cls._meta.db_pk_column:
            raise Exception(f'Current sheet {cls.sheet_name()} has no set primary key')
        param = {cls.pk_name(): val}
        query_model, f_list = cls.gen_simple_query(
            param, field=field, exclude=exclude, limit=1, with_field=True, db_key=db_key)
        suffix = cls.get_split_suffix(split, param, tz=tz)
        if suffix:
            cls._meta.basetable._table_name, _ = cls.get_sheet_name(suffix)
        info = await query_model.values(*f_list)
        return info[0] if info else None

    @classmethod
    async def get_by_dict(
            cls,
            param: dict = None,
            field: Union[tuple, list, set] = None,
            exclude: Union[tuple, list, set] = None,
            groups: Union[str, list, tuple] = None,
            orders: Union[str, list, tuple] = '-created',
            split: Union[str, int, float, datetime, date] = None,
            limit=0,
            offset=0,
            with_del=False,
            db_key: str = None,
            tz: str = None):
        query_model, out_filed = cls.gen_simple_query(
            param=param, field=field, exclude=exclude, groups=groups, orders=orders, limit=limit, offset=offset,
            with_del=with_del, with_field=True, db_key=db_key)
        suffix = cls.get_split_suffix(split, param, tz=tz)
        if suffix:
            cls._meta.basetable._table_name, _ = cls.get_sheet_name(suffix)
        dlist = await query_model.values(*out_filed)
        if limit == 1:
            return dlist[0] if dlist else None
        return dlist

    @classmethod
    async def get_count(
            cls,
            param: dict = None,
            with_del=False,
            split: Union[str, int, float, datetime, date] = None,
            db_key: str = None,
            tz: str = None):
        q_set = cls.gen_simple_query(param=param, with_del=with_del, db_key=db_key)
        suffix = cls.get_split_suffix(split, param, tz=tz)
        if suffix:
            cls._meta.basetable._table_name, _ = cls.get_sheet_name(suffix)
        return await q_set.count()

    @classmethod
    async def add_one(cls, param: dict, fun_success=None, db_key: str = None):
        """
        自动分表模式创建
        公共 新增或更新 值为None采用默认值

        :param param: 字典数据模型
        :param fun_success: 执行成功后的补充处理函数 协程函数 参数为生成的Model模型
        :param db_key: 指定数据库配置
        """
        if cls._SPLIT_TYPE:
            raise Exception('分表模型不能使用该方式添加数据')
        cur_time = tool_dt.cur_time()
        param['created'] = cur_time
        ('updated' in cls._meta.db_fields) and param.update({'updated': cur_time})
        new_dict = {field: val for field, val in param.items() if (field in cls._meta.db_fields) and (val is not None)}
        if not new_dict:
            return None
        if (not db_key) or (db_key == 'default'):
            row = await cls.create(**new_dict)
        else:
            db = cls.get_meta_db(db_key)
            row = await cls.create(using_db=db, **new_dict)
        if row:
            callable(fun_success) and await fun_success(row)
            return row
        return None

    @classmethod
    async def update_by_pk(
            cls,
            pk_val: Union[int, str],
            param: dict,
            old_data: dict = None,
            fun_success=None,
            split: Union[str, int, float, datetime, date] = None,
            db_key: str = None,
            tz: str = None):
        if not cls._meta.db_pk_column:
            raise Exception(f'Current sheet {cls.sheet_name()} has no set primary key')
        if not old_data:
            if fun_success:
                raise Exception(f'Must be get [old_data] param for execute the function')
            new_dict = {k: v for k, v in param.items() if (k in cls._meta.db_fields) and (v is not None)}
            split_param = {cls._SPLIT_FIELD: split} if (cls._SPLIT_FIELD not in param) else param
            suffix = cls.get_split_suffix(split, split_param, tz=tz)
        else:
            new_dict = {k: v for k, v in param.items() if (
                    (k in cls._meta.db_fields) and (v is not None)) and (old_data.get(k) != v)}
            split_param = {cls._SPLIT_FIELD: split} if (cls._SPLIT_FIELD not in old_data) else old_data
            suffix = cls.get_split_suffix(split, split_param, tz=tz)
        ('created' in new_dict) and new_dict.pop('created')
        if new_dict:
            ('updated' in cls._meta.db_fields) and new_dict.update({'updated': tool_dt.cur_time()})
            if suffix:
                cls._meta.basetable._table_name, _ = cls.get_sheet_name(suffix)
            if (not db_key) or (db_key == 'default'):
                sta = await cls.filter(**{cls._meta.db_pk_column: pk_val}).limit(1).update(**new_dict)
            else:
                db = cls.get_meta_db(db_key)
                sta = await cls.filter(**{cls._meta.db_pk_column: pk_val}).using_db(db).limit(1).update(**new_dict)
            if sta:
                if callable(fun_success):
                    old_data.update(**new_dict)
                    await fun_success(old_data)
                return new_dict
            return False
        return None

    @classmethod
    async def update_by_cond(
            cls,
            param: dict,
            upinfo: dict,
            limit=1,
            split: Union[str, int, float, datetime, date] = None,
            fun_success=None,
            db_key: str = None,
            tz: str = None):
        new_dict = {k: v for k, v in upinfo.items() if (k in cls._meta.db_fields) and (v is not None)}
        created = ('created' in new_dict) and new_dict.pop('created')
        if new_dict:
            ('updated' in cls._meta.db_fields) and new_dict.update({'updated': tool_dt.cur_time()})
            query_model = cls.gen_simple_query(param, limit=limit, db_key=db_key)
            suffix = cls.get_split_suffix(split, param, tz=tz)
            if suffix:
                cls._meta.basetable._table_name, _ = cls.get_sheet_name(suffix)
            sta = await query_model.update(**new_dict)
            if sta:
                created and new_dict.update({'created': created})
                callable(fun_success) and await fun_success(new_dict)
                return new_dict
            return False
        return None

    @classmethod
    async def del_by_pk(
            cls,
            pk_val: Union[int, str],
            force=False,
            split: Union[str, int, float, datetime, date] = None,
            db_key: str = None,
            tz: str = None,
            fun_success=None,
            fun_ags: Union[list, tuple] = None):
        if not cls._meta.db_pk_column:
            raise Exception(f'Current sheet {cls.sheet_name()} has no set primary key')
        if fun_ags is None:
            fun_ags = ()
        suffix = cls.get_split_suffix(split, {cls._SPLIT_FIELD: split}, tz=tz)
        if suffix:
            cls._meta.basetable._table_name, _ = cls.get_sheet_name(suffix)
        param = {cls._meta.db_pk_column: pk_val}
        if (not hasattr(cls, 'sta_del')) or force:
            sta = await cls.gen_simple_query(param, limit=1, db_key=db_key).delete()
            if sta:
                callable(fun_success) and await fun_success(*fun_ags)
                return True
            return False
        sta = await cls.gen_simple_query(param, limit=1, db_key=db_key).update(sta_del=True)
        if sta:
            callable(fun_success) and await fun_success(*fun_ags)
            return True
        return False

    @classmethod
    async def del_by_cond(
            cls,
            param: dict,
            limit=1,
            force=False,
            split: Union[str, int, float, datetime, date] = None,
            db_key: str = None,
            tz: str = None,
            fun_success=None,
            fun_ags: Union[list, tuple] = None):
        if fun_ags is None:
            fun_ags = ()
        query_model = cls.gen_simple_query(param, limit=limit, with_del=force, with_field=False, db_key=db_key)
        if (not hasattr(cls, 'sta_del')) or force:
            suffix = cls.get_split_suffix(split, param, tz=tz)
            if suffix:
                cls._meta.basetable._table_name, _ = cls.get_sheet_name(suffix)
            sta = await query_model.delete()
            if sta:
                callable(fun_success) and await fun_success(*fun_ags)
                return True
            return False
        suffix = cls.get_split_suffix(split, param, tz=tz)
        if suffix:
            cls._meta.basetable._table_name, _ = cls.get_sheet_name(suffix)
        sta = await query_model.update(sta_del=True)
        if sta:
            callable(fun_success) and await fun_success(*fun_ags)
            return True
        return False

    @classmethod
    async def split_bulk_insert(
            cls,
            data: Union[list[dict], tuple[dict]],
            split: Union[str, int, float, datetime, date] = None,
            use_transaction=False,
            db_key: str = None,
            tz: str = None):
        if not cls._SPLIT_TYPE:
            raise Exception(f'当前数据模型未指定分表模式：{cls.__name__}')
        model_map = {}
        for item in data:
            if not isinstance(item, dict):
                raise Exception(f'检测到无效的数据结构: {item}, {type(item)}')
            (not item.get('created')) and item.update({'created': tool_dt.cur_time()})
            suffix = cls.get_split_suffix(split or cls._SPLIT_FIELD, item, tz=tz)
            model_map[suffix].append(item) if suffix in model_map else model_map.update({suffix: [item]})
        sql_list = []
        for k, v in model_map.items():
            await cls.check_table(k, db_key)
            sql, _, _ = cls.gen_insertup_sql(v, suffix=k)
            sql_list.append(sql)
        try:
            return await cls.exec_insert(sql_list, use_transaction=use_transaction, db_key=db_key)
        except Exception as err:
            raise Exception(f'分表批量写入数据失败：{err}')

    @classmethod
    async def split_add_one(
            cls,
            data: dict,
            split: Union[str, int, float, datetime, date] = None,
            fun_success=None,
            db_key: str = None,
            tz: str = None):
        if not cls._SPLIT_TYPE:
            raise Exception(f'当前数据模型未指定分表模式：{cls.__name__}')
        new_d = {field: val for field, val in data.items() if (field in cls._meta.db_fields) and (val is not None)}
        if not new_d:
            return None
        (not new_d.get('created')) and new_d.update({'created': tool_dt.cur_time()})
        suffix = cls.get_split_suffix(split or cls._SPLIT_FIELD, data, tz=tz)
        try:
            sql, pk_list, cond_list = cls.gen_insertup_sql([new_d], suffix=suffix)
            await cls.check_table(suffix, db_key)
            await cls.exec_sql(sql)
        except Exception as err:
            raise Exception(f'{cls.get_sheet_name(suffix)}分表写入数据失败：{err}')
        if callable(fun_success) and (pk_list or cond_list):
            data = (await fun_success(pk_list)) if pk_list else (await fun_success(cond_list))
            return data
        return 1

    @classmethod
    def gen_insertup_sql(
            cls,
            dlist: Union[list[dict], tuple[dict]],
            upfield: Union[list, tuple] = None,
            add_field: Union[list, tuple] = None,
            mult_field: Union[list, tuple] = None,
            suffix: str = None):
        """
        生成插入数据sql, 使用该写入方式的前提是确保数据库模型不为空的字段有值或存在默认值，否则将无法写入
        """
        if not dlist:
            raise Exception(f'没有可生成sql的数据: {cls.sheet_name(suffix=suffix)}')
        all_field = list(cls._meta.db_fields)
        v_list = []
        for item in dlist:
            if not isinstance(item, dict):
                raise Exception(f'读到不符合规范的数据结构：{item}')
            arr = [cls.check_val(item.get(k), k, cls) for k in all_field]
            v_list.append("({})".format(','.join(arr)))
        sql = F"INSERT INTO `{cls.sheet_name(suffix=suffix)}`({','.join([f'`{f}`' for f in all_field])}) VALUES "
        sql += ",".join(v_list)
        pk_list = []
        cond_list = []
        if upfield or add_field or mult_field:
            for item in dlist:
                pk_val = item.get(cls.pk_name())
                if pk_val:
                    pk_list.append(pk_val)
                    continue
                if not cls._meta.unique_together:
                    raise Exception('数据结构错误,更新必须指定数据模型的唯一键或唯一索引')
                cond = {k: item.get(k) for k in cls._meta.unique_together[0]}
                if not cond:
                    raise Exception('数据结构错误,更新必须指定包含数据唯一索引的值')
                cond_list.append(cond)
            if cls._meta.db.schema_generator.DIALECT == 'mysql':
                sql += "AS up_rows ON DUPLICATE KEY UPDATE "
                if upfield:
                    sql += ",".join(["{0}=up_rows.{0}".format(field) for field in upfield if field in all_field])
                if add_field:
                    sql += ",".join(['{0}={0}+up_rows.{0}'.format(field) for field in add_field if field in all_field])
                if mult_field:
                    sql += ",".join(['{0}={0}*up_rows.{0}'.format(field) for field in mult_field if field in all_field])
            elif cls._meta.db.schema_generator.DIALECT == 'postgres':
                if pk_list and cond_list:
                    raise Exception('pgsql更新模式下所有数据只能指定唯一键或唯一索引两者之一的方式')
                if pk_list:
                    up_keys = cls.pk_name()
                else:
                    up_keys = ','.join(list(cls._meta.unique_together[0]))
                sql += f"ON CONFLICT ({up_keys}) DO UPDATE SET "
                if upfield:
                    sql += ','.join([f"{filed}=EXCLUDED.{filed}" for filed in upfield])
        return sql, pk_list, cond_list
