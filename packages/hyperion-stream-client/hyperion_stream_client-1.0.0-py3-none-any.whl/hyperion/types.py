from typing import Literal, Optional, TypedDict, NamedTuple, Union, List, Callable, Any


class SavedRequest(NamedTuple):
    type = str
    req = Union["StreamActionsRequest", "StreamDeltasRequest"]


class HyperionClientOptions(NamedTuple):
    """Client Options"""

    endpoint: str
    """ Hyperion endpoint URL"""

    chain_api: Optional[str] = None
    """ Chain API (optional) """

    debug: bool = False
    """ Debug flag """

    lib_stream: bool = False
    """ Libstream flag """


class StreamDeltasRequest(NamedTuple):
    """Stream Delta Request"""

    code: str
    """ Contract code """

    table: str
    """ Contract table """

    scope: str
    """ Token scope (symbol) """

    payer: str
    """ Payer account """

    start_from: Union[str, int]
    """ Starting block number or string identifier """

    read_until: Union[str, int]
    """ Block number or string identifier to read until """


class RequestFilter(TypedDict):
    """Request Filter"""

    field: str
    """ Field to filter on (e.g., '@transfer.to') """

    value: str
    """ The value to match for the field (e.g., 'eosio.ramfee') """


class StreamActionsRequest(TypedDict):
    """Stream Actions Request"""

    contract: str
    """ Contract name """

    account: str
    """ Account name """

    action: str
    """ Action name """

    start_from: Union[int, str]
    """ Starting block number or string identifier """

    read_until: Union[int, str]
    """ Block number or string identifier to read until """

    filters: List[RequestFilter] = []
    """ List of filters to apply """


class ActionContent:
    def __init__(self, **kwargs):
        self.timestamp = kwargs.get("@timestamp")
        self.global_sequence = kwargs.get("global_sequence")
        self.account_ram_deltas = kwargs.get("account_ram_deltas", [])
        self.act = kwargs.get("act", {})
        self.block_num = kwargs.get("block_num")
        self.action_ordinal = kwargs.get("action_ordinal")
        self.creator_action_ordinal = kwargs.get("creator_action_ordinal")
        self.cpu_usage_us = kwargs.get("cpu_usage_us")
        self.net_usage_words = kwargs.get("net_usage_words")
        self.code_sequence = kwargs.get("code_sequence")
        self.abi_sequence = kwargs.get("abi_sequence")
        self.trx_id = kwargs.get("trx_id")
        self.producer = kwargs.get("producer")
        self.notified = kwargs.get("notified")
        self.extra = {k: v for k, v in kwargs.items() if k not in self.__dict__}


class DeltaContent:
    def __init__(self, **kwargs):
        self.code = kwargs.get("code")
        self.table = kwargs.get("table")
        self.scope = kwargs.get("scope")
        self.payer = kwargs.get("payer")
        self.block_num = kwargs.get("block_num")
        self.data = kwargs.get("data")
        self.extra = {k: v for k, v in kwargs.items() if k not in self.__dict__}


class IncomingData(NamedTuple):
    """Stream Incoming Data"""

    type: Literal["action", "delta"]
    """ Incoming data type - Either 'action' or 'delta' """

    mode: Literal["live", "history"]
    """ Incoming Data mode - Either 'live' or 'history' """

    content: Union[ActionContent, DeltaContent]
    """ Content of the stream - Action or Delta based on the type """

    irreversible: bool
    """ Flag data is irreversible """


class LIBData(NamedTuple):
    """LIB data related to the blockchain"""

    chain_id: str
    """ Chain ID """

    block_num: int
    """ Block number """

    block_id: str
    """ Block ID """


class ForkData(NamedTuple):
    """Fork data related to the blockchain"""

    chain_id: str
    """ Chain ID """

    starting_block: int
    """ Starting block number of the fork """

    ending_block: int
    """ Ending block number of the fork """

    new_id: str
    """ New chain ID after the fork """



EventData = Union[IncomingData, LIBData, ForkData, None]
EventListener = Callable[[Optional[EventData]], None]
