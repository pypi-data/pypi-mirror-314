# Hyperion Stream Client

[![PyPi Version](https://img.shields.io/pypi/v/hyperion-stream-client)](https://pypi.org/project/hyperion-stream-client/)
![GitHub](https://img.shields.io/github/license/debugtitan/hyperion-stream-client)

### Installation

PyPI

```bash
pip install -U hyperion-stream-client
```

### Usage

```python
    from contextlib import suppress
    from hyperion.hyperion_stream_client import HyperionClientOptions, HyperionStreamClient, StreamActionsRequest
    import asyncio

    async def data_handler(data):
        print(data)

    async def main():
        options = HyperionClientOptions(
            endpoint="https://proton.eosusa.io", debug=True, lib_stream=False
        )
        client = HyperionStreamClient(options)

        # Set the custom handler
        client.async_data_handler = data_handler

        try:
            # Connect the client
            await client.connect()

            # Stream actions
            await client.stream_actions(
                StreamActionsRequest(
                    contract="swap.alcor",
                    account="swap.alcor",
                    action="logswap",
                    start_from="LIB",
                    read_until=0,
                )
            )
        except Exception as e:
            print(f"Error: {e}")

        while True:
            await asyncio.sleep(1)

    if __name__ == "__main__":
        with suppress(KeyboardInterrupt):
            asyncio.run(main())

```

## Class
```python
    from contextlib import suppress
    from hyperion.hyperion_stream_client import HyperionClientOptions,HyperionStreamClient,StreamActionsRequest
    import asyncio


    class EventListener(HyperionStreamClient):
        def __init__(self):
            options = HyperionClientOptions(
                endpoint="https://proton.eosusa.io", debug=True, lib_stream=False
            )
            super().__init__(options)
            self.async_data_handler = self.data_handler
            self.async_lib_data_handler = self.lib_data_handler

        async def start(self):
            # Make connection first
            try:
                await self.connect()

                # Stream Actions
                await self.stream_actions(
                    StreamActionsRequest(
                        contract="swap.alcor",
                        account="swap.alcor",
                        action="logswap",
                        start_from="LIB",
                        read_until=0,
                    )
                )
            except Exception as e:
                print(e)

            while True:
                await asyncio.sleep(1)

        async def data_handler(self, data):
            print(data)

        async def lib_data_handler(self, data):
            print(data)


    if __name__ == "__main__":
        with suppress(KeyboardInterrupt) as _err:
            asyncio.run(EventListener().start())
```



## License
[MIT](https://choosealicense.com/licenses/mit/)