# smsocials

## setup

```bash
pip install smsocials
```

## example

```python
import asyncio

from smsocials import VKService


async def main():
    vk_service = VKService(
        "token"
    )

    user_info = await vk_service.get_user_info("123")
    print(user_info)


asyncio.run(main())

```
