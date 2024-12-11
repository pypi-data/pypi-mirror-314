# nocodb-api

Python client for NocoDB API v2


## Install

Install from [pypi](https://pypi.org/project/nocodb-client/):

```shell
pip install nocodb-client
```

Install from Github:

```shell
pip install "nocodb-api@git+https://github.com/liuli01/nocodb-api"
```
## Quickstart
```python
#%%
import json
import os
from nocodb import NocoDB
from nocodb.Column import Column
import logging

logging.basicConfig()
logging.getLogger('nocodb').setLevel(level=logging.DEBUG)

CONFIG = {
    "NOCO_URL": "https://app.nocodb.com",
    "NOCO_API_KEY": "",
    "NOCO_BASE_ID": "",
    "TIMEOUT": "30"
}


try:
    with open("test_config.json") as config_file:
        CONFIG.update(json.load(config_file))

except FileNotFoundError:
    for s in CONFIG:
        if s in os.environ:
            CONFIG[s] = os.environ[s]

noco = NocoDB(url=CONFIG["NOCO_URL"],
                        api_key=CONFIG["NOCO_API_KEY"])
base = noco.get_base(base_id=CONFIG["NOCO_BASE_ID"])

[t.delete() for t in base.get_tables()]

#%%
"""
数据新增操作
"""
#%% 创建表
base.create_table("test_01")
#%% 获取表对象
table=base.get_table_by_title("test_01")
#%% 增加一条记录
table.create_record(Title="First Record")
# %% 创建多条记录
table.create_records([{"Title": "Second Record"}, {"Title": "Third Record"}])
#%% 新增列
table.create_column("Update", "Update", Column.DataType.SingleLineText)


"""
数据修改操作
"""
# %% 更新1条记录
table.update_record(Id="1",Update="First Record Updated")
# %% 更新多条记录
table.update_records([{"Id":"2","Update": "Second Record Updated"},{"Id":"3","Update": "Third Record Updated"}])

"""
数据查询操作
"""
# 数据查询操作
#%% 根据id查看一条记录
record_1=table.get_record(1).metadata
#%% 根据Id查看记录的某个字段
value_1=table.get_record(1).get_value("Title")
#%% 根据字段值筛选获取记录
field_records=table.get_records_by_field_value("Title","First Record")
[print(r.metadata) for r in field_records]
# %% 根据自定义条件获取记录
condition_records=table.get_records(params={"where": f"(Title,eq,First Record)"})
[print(r.metadata) for r in condition_records]
# %% 获取所有记录元数据
records=table.get_records()
[print(r.metadata) for r in table.get_records()]
# %% 获取所有记录数量
print(table.get_number_of_records())
"""
数据删除操作
"""
# %% 删除一条记录
table.delete_record(1)
#%% 
table.delete_records([2,3])
# %%

```


Get debug log:

```python
import logging
from nocodb import NocoDB

logging.basicConfig()
logging.getLogger('nocodb').setLevel(logging.DEBUG)
# Now every log is visible.

# Limit to submodules:
logging.getLogger('nocodb.Base').setLevel(logging.DEBUG)
```


## Development

```shell
python -m venv .venv
. ./.venv/bin/activate
```

### Tests in Docker

Create a file `test_config.json` with the parameters, or change the Environment Variables in `tests/Dockerfile`, than run:

```shell
docker run --rm -it $(docker build -q -f tests/Dockerfile .)
```

### Official docs

- https://meta-apis-v2.nocodb.com
- https://data-apis-v2.nocodb.com
- https://docs.nocodb.com

### Documentation with [pdoc](https://pdoc.dev)

*TODO*

```shell
pip install -e ".[doc]"
pdoc -d google nocodb
```
