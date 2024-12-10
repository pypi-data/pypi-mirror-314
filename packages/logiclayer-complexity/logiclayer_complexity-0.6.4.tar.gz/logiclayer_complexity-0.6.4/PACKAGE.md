<p>
<a href="https://github.com/Datawheel/logiclayer-complexity/releases"><img src="https://flat.badgen.net/github/release/Datawheel/logiclayer-complexity" /></a>
<a href="https://github.com/Datawheel/logiclayer-complexity/blob/master/LICENSE"><img src="https://flat.badgen.net/github/license/Datawheel/logiclayer-complexity" /></a>
<a href="https://github.com/Datawheel/logiclayer-complexity/"><img src="https://flat.badgen.net/github/checks/Datawheel/logiclayer-complexity" /></a>
<a href="https://github.com/Datawheel/logiclayer-complexity/issues"><img src="https://flat.badgen.net/github/issues/Datawheel/logiclayer-complexity" /></a>
</p>

## Getting started

This module must be used with [LogicLayer](https://pypi.org/project/logiclayer). An instance of `OlapServer` from the `tesseract_olap` package is also required to retrieve the data.

```python
# app.py

from logiclayer import LogicLayer
from logiclayer_complexity import EconomicComplexityModule
from tesseract_olap import OlapServer
from tesseract_olap.logiclayer import TesseractModule

layer = LogicLayer()
olap = OlapServer(backend="clickhouse://...", schema="./schema/")

cmplx = EconomicComplexityModule(olap)
layer.add_module("/complexity", cmplx)

# You can reuse the `olap` object with an instace of `TesseractModule`
tsrc = TesseractModule(olap)
layer.add_module("/tesseract", tsrc)
```

Is not officially supported, but you can also use the module directly with a FastAPI instance:

```python
cmplx = EconomicComplexityModule(olap)

app = FastAPI()
app.include_router(cmplx.router, prefix="/complexity")
```

---
&copy; 2022 [Datawheel, LLC.](https://www.datawheel.us/)  
This project is licensed under [MIT](./LICENSE).
