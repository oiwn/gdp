# GDP

Grab Data Pipeline - implementation of abstract data pipeline used to
filter, transform, validate and store data among various sources.

Designed to work with Grab Framework but could be used as a part of any other
data extraction framework.

## Notes

Desired API:

```python
class ItemStorage(AbstractStorage):
   schema = {'name': {'type': 'string', 'required': True}}

storage = ItemStorage()
data = {'name': 'item name'}
result = storage.persist(data)
assert result.status == 'ok'
print(result.as_dict())
# {'status': 'ok', 'op_type': 'inserted', 'step': 'save'}
```

### Workflow

- `pre-filter` check required fields: distributor code color size price title
- `transform` data transformation, cleanup and normalization
- `post-filter` filter by some criteria (category, size etc.)
- `validate` validate data accoiding to schema (check upper/lower case)
- `save` - item could be inserted/updated/skipped(not changed)

Save stage backend should be pluggable (for different storages: mongodb,
elasticsearch, influxdb)

During the `save` stage data could be passed to additional layers implementing
data persistence using different kind of databases:

- elasticsearch
- influxdb
- postgres
- other processing pipelines

Result of operations should be returned as `StorageResult` with fields defined
by schema attached as class attribute.


For example:

- `_id` inserted/updated record id/key available after `save` stage
- `err_msg` detailed description of error happened during item processing
- `status` [ok, error]
- `op_type` [inserted, updateed, skipped, filtered, failed]
- `step` pipeline step i.e. `pre_filter`, `save` etc.
- `layers` ordered list of results from additional layers [{}, {}, ..., {}]

Result class can store `layers` in 2 ways as a list of dicts to
preserve order and as a associative array for fast access by key. (???)

Reference to stored `_id`: item id or key should be available after save stage.


```python
class ItemStorage(AbstractStorage):
    schema = {
        'name': {'type': 'string', 'required': True},
        'price': {'type': 'number', 'required': True}
    }

class ItemPriceHistoryStorage(AbstractStorage):
    schema = {
        'item_id': {'type': 'string', 'required': True},
        'old_price': {'type': 'number', 'required': True},
        'new_price': {'type': 'number', 'required': True},
        'diff': {'type': 'number', 'required': True},
    }

storage = ItemStorage(results_class=SomeResults,
                      layers=[ItemPriceHistoryStorage(**params)])

item = {'name': 'item name', 'price': 5.30}
result = storage.persist(item)
assert result.success == result.types.success.TRUE == True
assert result.op == result.type.op.INSERTED == 'inserted'
assert result.step == 'save'
assert '_id' in result
assert result.layers == []  # not passed to ItemPriceHistoryStorage

item = {'name': 'item name', 'price': 4.80}
result = storage.persist(item)
assert result.success == True
assert result.op == 'updated'
print(result.layers.list())
# ['<ItemPriceHistoryStorage Result: {...}>']
print(result.layers.get_layer_for(ItemPriceHistoryStorage).result.as_dict())
# {'status': 'ok', 'op_type': 'inserted', 'step': 'save', '_id': 324}
```
