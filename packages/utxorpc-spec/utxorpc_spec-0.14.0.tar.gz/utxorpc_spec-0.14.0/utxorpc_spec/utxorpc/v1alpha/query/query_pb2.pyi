from google.protobuf import field_mask_pb2 as _field_mask_pb2
from utxorpc.v1alpha.cardano import cardano_pb2 as _cardano_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChainPoint(_message.Message):
    __slots__ = ("slot", "hash")
    SLOT_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    slot: int
    hash: bytes
    def __init__(self, slot: _Optional[int] = ..., hash: _Optional[bytes] = ...) -> None: ...

class TxoRef(_message.Message):
    __slots__ = ("hash", "index")
    HASH_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    hash: bytes
    index: int
    def __init__(self, hash: _Optional[bytes] = ..., index: _Optional[int] = ...) -> None: ...

class ReadParamsRequest(_message.Message):
    __slots__ = ("field_mask",)
    FIELD_MASK_FIELD_NUMBER: _ClassVar[int]
    field_mask: _field_mask_pb2.FieldMask
    def __init__(self, field_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class AnyChainParams(_message.Message):
    __slots__ = ("cardano",)
    CARDANO_FIELD_NUMBER: _ClassVar[int]
    cardano: _cardano_pb2.PParams
    def __init__(self, cardano: _Optional[_Union[_cardano_pb2.PParams, _Mapping]] = ...) -> None: ...

class ReadParamsResponse(_message.Message):
    __slots__ = ("values", "ledger_tip")
    VALUES_FIELD_NUMBER: _ClassVar[int]
    LEDGER_TIP_FIELD_NUMBER: _ClassVar[int]
    values: AnyChainParams
    ledger_tip: ChainPoint
    def __init__(self, values: _Optional[_Union[AnyChainParams, _Mapping]] = ..., ledger_tip: _Optional[_Union[ChainPoint, _Mapping]] = ...) -> None: ...

class AnyUtxoPattern(_message.Message):
    __slots__ = ("cardano",)
    CARDANO_FIELD_NUMBER: _ClassVar[int]
    cardano: _cardano_pb2.TxOutputPattern
    def __init__(self, cardano: _Optional[_Union[_cardano_pb2.TxOutputPattern, _Mapping]] = ...) -> None: ...

class UtxoPredicate(_message.Message):
    __slots__ = ("match", "all_of", "any_of")
    MATCH_FIELD_NUMBER: _ClassVar[int]
    NOT_FIELD_NUMBER: _ClassVar[int]
    ALL_OF_FIELD_NUMBER: _ClassVar[int]
    ANY_OF_FIELD_NUMBER: _ClassVar[int]
    match: AnyUtxoPattern
    all_of: _containers.RepeatedCompositeFieldContainer[UtxoPredicate]
    any_of: _containers.RepeatedCompositeFieldContainer[UtxoPredicate]
    def __init__(self, match: _Optional[_Union[AnyUtxoPattern, _Mapping]] = ..., all_of: _Optional[_Iterable[_Union[UtxoPredicate, _Mapping]]] = ..., any_of: _Optional[_Iterable[_Union[UtxoPredicate, _Mapping]]] = ..., **kwargs) -> None: ...

class AnyUtxoData(_message.Message):
    __slots__ = ("native_bytes", "txo_ref", "cardano")
    NATIVE_BYTES_FIELD_NUMBER: _ClassVar[int]
    TXO_REF_FIELD_NUMBER: _ClassVar[int]
    CARDANO_FIELD_NUMBER: _ClassVar[int]
    native_bytes: bytes
    txo_ref: TxoRef
    cardano: _cardano_pb2.TxOutput
    def __init__(self, native_bytes: _Optional[bytes] = ..., txo_ref: _Optional[_Union[TxoRef, _Mapping]] = ..., cardano: _Optional[_Union[_cardano_pb2.TxOutput, _Mapping]] = ...) -> None: ...

class ReadUtxosRequest(_message.Message):
    __slots__ = ("keys", "field_mask")
    KEYS_FIELD_NUMBER: _ClassVar[int]
    FIELD_MASK_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedCompositeFieldContainer[TxoRef]
    field_mask: _field_mask_pb2.FieldMask
    def __init__(self, keys: _Optional[_Iterable[_Union[TxoRef, _Mapping]]] = ..., field_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class ReadUtxosResponse(_message.Message):
    __slots__ = ("items", "ledger_tip")
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    LEDGER_TIP_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[AnyUtxoData]
    ledger_tip: ChainPoint
    def __init__(self, items: _Optional[_Iterable[_Union[AnyUtxoData, _Mapping]]] = ..., ledger_tip: _Optional[_Union[ChainPoint, _Mapping]] = ...) -> None: ...

class SearchUtxosRequest(_message.Message):
    __slots__ = ("predicate", "field_mask", "max_items", "start_token")
    PREDICATE_FIELD_NUMBER: _ClassVar[int]
    FIELD_MASK_FIELD_NUMBER: _ClassVar[int]
    MAX_ITEMS_FIELD_NUMBER: _ClassVar[int]
    START_TOKEN_FIELD_NUMBER: _ClassVar[int]
    predicate: UtxoPredicate
    field_mask: _field_mask_pb2.FieldMask
    max_items: int
    start_token: str
    def __init__(self, predicate: _Optional[_Union[UtxoPredicate, _Mapping]] = ..., field_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ..., max_items: _Optional[int] = ..., start_token: _Optional[str] = ...) -> None: ...

class SearchUtxosResponse(_message.Message):
    __slots__ = ("items", "ledger_tip", "next_token")
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    LEDGER_TIP_FIELD_NUMBER: _ClassVar[int]
    NEXT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[AnyUtxoData]
    ledger_tip: ChainPoint
    next_token: str
    def __init__(self, items: _Optional[_Iterable[_Union[AnyUtxoData, _Mapping]]] = ..., ledger_tip: _Optional[_Union[ChainPoint, _Mapping]] = ..., next_token: _Optional[str] = ...) -> None: ...

class ReadDataRequest(_message.Message):
    __slots__ = ("keys", "field_mask")
    KEYS_FIELD_NUMBER: _ClassVar[int]
    FIELD_MASK_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedScalarFieldContainer[bytes]
    field_mask: _field_mask_pb2.FieldMask
    def __init__(self, keys: _Optional[_Iterable[bytes]] = ..., field_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class AnyChainDatum(_message.Message):
    __slots__ = ("native_bytes", "key", "cardano")
    NATIVE_BYTES_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    CARDANO_FIELD_NUMBER: _ClassVar[int]
    native_bytes: bytes
    key: bytes
    cardano: _cardano_pb2.PlutusData
    def __init__(self, native_bytes: _Optional[bytes] = ..., key: _Optional[bytes] = ..., cardano: _Optional[_Union[_cardano_pb2.PlutusData, _Mapping]] = ...) -> None: ...

class ReadDataResponse(_message.Message):
    __slots__ = ("values", "ledger_tip")
    VALUES_FIELD_NUMBER: _ClassVar[int]
    LEDGER_TIP_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[AnyChainDatum]
    ledger_tip: ChainPoint
    def __init__(self, values: _Optional[_Iterable[_Union[AnyChainDatum, _Mapping]]] = ..., ledger_tip: _Optional[_Union[ChainPoint, _Mapping]] = ...) -> None: ...
