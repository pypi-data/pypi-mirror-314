# Moy Nalog

Неофициальная асинхронная библиотека **moy_nalog** предоставляет API для автоматизации отчётности самозанятых на [lknpd.nalog.ru](https://npd.nalog.ru/web-app/).


Пример использования:

```python
import asyncio
from moy_nalog import MoyNalog

nalog = MoyNalog("1234567890", "MyStrongPassword")


async def main():
    await nalog.add_income(
        "Предоставление информационных услуг #970/2495", amount=1000, quantity=1
    )


asyncio.run(main())
```