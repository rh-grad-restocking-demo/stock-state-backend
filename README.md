# stock-state-backend




```shell
python -m stock.cli setup-db
python -m stock.cli register-shelve --product_sku="apples" --product_category="fresh" --shelve_restock_threshold=20 --shelve_stock_amount=100
python -m stock.cli retrieve-shelve --product_sku="apples"
python -m stock.cli deplete-shelve --product_sku="apples" --amount=5
python -m stock.cli restock-shelve --product_sku="apples" --amount=5
```
