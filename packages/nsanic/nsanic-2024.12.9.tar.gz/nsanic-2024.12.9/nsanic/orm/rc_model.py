from datetime import datetime, date
from typing import Union

from nsanic.libs.component import ConfMeta
from nsanic.libs.consts import GLOBAL_TZ
from nsanic.libs.tool import json_parse, json_encode
from nsanic.orm.db_model import DBModel


class RCModel(ConfMeta):
    """数据缓存redis模型"""

    db_model: DBModel = None
    '''数据模型'''
    expired_mode = 0
    '''缓存过期模式 0--hash类的固定缓存(无过期) 1--key value类的时效型缓存 带过期时间 默认12小时'''
    expired_sec = 43200
    '''key value类的时效型缓存的过期时间'''

    @classmethod
    def set_conf(cls, conf, db_model=None):
        cls.conf = conf
        if db_model:
            cls.db_model = db_model

    @classmethod
    async def fun_set_cache(cls, info: dict):
        """附加缓存设置"""
        pass

    @classmethod
    async def cache_by_pk(cls, pk_val: Union[bytes, int, str], split: Union[str, int, float, datetime, date] = None,
                          tz: str = GLOBAL_TZ):
        async def from_db():
            db_info = await cls.db_model.get_by_pk(pk_val, tz=tz)
            if db_info:
                if cls.expired_mode:
                    await cls.conf.rds.set_item(key, json_encode(db_info), ex_time=cls.expired_sec)
                else:
                    await cls.conf.rds.set_hash(tb_name, pk_val, json_encode(db_info))
                await cls.fun_set_cache(db_info)
                return db_info
            return

        if not cls.db_model:
            return
        tb_name = cls.db_model.sheet_name(split, tz=tz)
        if isinstance(pk_val, bytes):
            pk_val = pk_val.decode('utf-8')
        key = f"{tb_name}:{pk_val}"
        if cls.expired_mode:
            info = await cls.conf.rds.get_item(key)
        else:
            info = await cls.conf.rds.get_hash(tb_name, pk_val)
        if info:
            return json_parse(info, cls.logerr)
        p_info = await cls.conf.rds.locked(key, from_db)
        return p_info

    @classmethod
    async def cache_by_unique(cls, unique: dict, suffix: str, split: Union[str, int, float, datetime, date] = None,
                              tz: str = GLOBAL_TZ):
        async def from_db():
            info = await cls.db_model.get_by_dict(unique, limit=1, split=split, tz=tz)
            if info:
                pk_val = info.get(cls.db_model.pk_name())
                if cls.expired_mode:
                    await cls.conf.rds.set_item(key, pk_val, ex_time=cls.expired_sec)
                else:
                    await cls.conf.rds.set_hash(key_name, unique_val, pk_val)
                await cls.fun_set_cache(info)
                return info
            return

        if not cls.db_model:
            return
        key_name = f'{cls.db_model.sheet_name(split)}_{suffix}'
        unique_val = '_'.join([str(unique.get(k)) for k in sorted(unique)])
        key = f'{key_name}:{unique_val}'
        if cls.expired_mode:
            item_id = await cls.conf.rds.get_item(key)
        else:
            item_id = await cls.conf.rds.get_hash(key_name, unique_val)
        if item_id:
            return await cls.cache_by_pk(item_id, split=split, tz=tz)
        return await cls.conf.rds.locked(key, fun=from_db)

    # @classmethod
    # async def query_map(cls, is_super=False, field_name='name', groups: (list, tuple) = None, group_key='gid'):
    #     """"""
    #     async def from_db():
    #         data_list = await cls.db_model.get_by_dict()
    #         return [await cls.fun_set_cache(info) for n in data_list]
    #     if not groups:
    #         groups = []
    #     if not cls.db_model:
    #         return []
    #     pk_name = cls.db_model.pk_name()
    #     all_items = await cls.conf.rds.get_hash_val(cls.db_model.sheet_name())
    #     if not all_items:
    #         all_items = await cls.conf.rds.locked(cls.db_model.sheet_name(), fun=from_db, time_out=5)
    #     if (not is_super) and cls.db_model.check_field(group_key):
    #         new_list = []
    #         for item in all_items:
    #             info = json_parse(item, log_fun=cls.logerr)
    #             g_id = info.get(group_key)
    #             (g_id in groups) and new_list.append({
    #                 'label': info.get(field_name), 'value': info.get(pk_name), group_key: g_id})
    #         return new_list
    #     return [{'label': info.get(field_name), 'value': info.get(pk_name), group_key: info.get(group_key)}
    #             for item in all_items if (info := json_parse(item, cls.logerr))]

    @classmethod
    async def get_name(cls, pk_id: int or str, key_field='name', split: Union[str, int, float, datetime, date] = None,
                       tz: str = GLOBAL_TZ):
        if not pk_id:
            return '-'
        info = await cls.cache_by_pk(pk_id, split=split, tz=tz)
        return info.get(key_field) if info else '-'

    @classmethod
    async def get_map(cls, pk_id: int or str, key_list: list or tuple = None,
                      split: Union[str, int, float, datetime, date] = None, tz: str = GLOBAL_TZ):
        if not pk_id:
            return {}
        info = await cls.cache_by_pk(pk_id, split=split, tz=tz)
        return {name: info.get(name) for name in key_list} if info else {}
