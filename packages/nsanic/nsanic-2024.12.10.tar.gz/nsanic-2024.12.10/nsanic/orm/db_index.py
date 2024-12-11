from tortoise.indexes import Index


class VchpIndex(Index):
    """BTree类索引 模糊匹配仅支持xxx% varchar_pattern模式通配符 简单通配下配合limit offset使用达到最好性能"""
    INDEX_CREATE_TEMPLATE = (
        "CREATE{index_type}INDEX {index_name} ON {table_name} ({fields} varchar_pattern_ops){extra};")


class GistTrgmIndex(Index):
    """
    gist模糊匹配索引
    支持模糊匹配 %%全通配符 实测简单varchar char模式下十万百万级别的数据下性能更差 另外需要安装pg_trgm插件
    """

    INDEX_TYPE = 'GIST'
    INDEX_CREATE_TEMPLATE = (
        "CREATE INDEX {index_name} ON {table_name} USING {index_type}({fields} gist_trgm_ops){extra};")
