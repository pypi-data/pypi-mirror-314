from google.protobuf import field_mask_pb2 as _field_mask_pb2
from utxorpc.v1alpha.cardano import cardano_pb2 as _cardano_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BlockRef(_message.Message):
    __slots__ = ("index", "hash")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    index: int
    hash: bytes
    def __init__(self, index: _Optional[int] = ..., hash: _Optional[bytes] = ...) -> None: ...

class AnyChainTxPattern(_message.Message):
    __slots__ = ("cardano",)
    CARDANO_FIELD_NUMBER: _ClassVar[int]
    cardano: _cardano_pb2.TxPattern
    def __init__(self, cardano: _Optional[_Union[_cardano_pb2.TxPattern, _Mapping]] = ...) -> None: ...

class TxPredicate(_message.Message):
    __slots__ = ("match", "all_of", "any_of")
    MATCH_FIELD_NUMBER: _ClassVar[int]
    NOT_FIELD_NUMBER: _ClassVar[int]
    ALL_OF_FIELD_NUMBER: _ClassVar[int]
    ANY_OF_FIELD_NUMBER: _ClassVar[int]
    match: AnyChainTxPattern
    all_of: _containers.RepeatedCompositeFieldContainer[TxPredicate]
    any_of: _containers.RepeatedCompositeFieldContainer[TxPredicate]
    def __init__(self, match: _Optional[_Union[AnyChainTxPattern, _Mapping]] = ..., all_of: _Optional[_Iterable[_Union[TxPredicate, _Mapping]]] = ..., any_of: _Optional[_Iterable[_Union[TxPredicate, _Mapping]]] = ..., **kwargs) -> None: ...

class WatchTxRequest(_message.Message):
    __slots__ = ("predicate", "field_mask", "intersect")
    PREDICATE_FIELD_NUMBER: _ClassVar[int]
    FIELD_MASK_FIELD_NUMBER: _ClassVar[int]
    INTERSECT_FIELD_NUMBER: _ClassVar[int]
    predicate: TxPredicate
    field_mask: _field_mask_pb2.FieldMask
    intersect: _containers.RepeatedCompositeFieldContainer[BlockRef]
    def __init__(self, predicate: _Optional[_Union[TxPredicate, _Mapping]] = ..., field_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ..., intersect: _Optional[_Iterable[_Union[BlockRef, _Mapping]]] = ...) -> None: ...

class AnyChainTx(_message.Message):
    __slots__ = ("cardano",)
    CARDANO_FIELD_NUMBER: _ClassVar[int]
    cardano: _cardano_pb2.Tx
    def __init__(self, cardano: _Optional[_Union[_cardano_pb2.Tx, _Mapping]] = ...) -> None: ...

class WatchTxResponse(_message.Message):
    __slots__ = ("apply", "undo")
    APPLY_FIELD_NUMBER: _ClassVar[int]
    UNDO_FIELD_NUMBER: _ClassVar[int]
    apply: AnyChainTx
    undo: AnyChainTx
    def __init__(self, apply: _Optional[_Union[AnyChainTx, _Mapping]] = ..., undo: _Optional[_Union[AnyChainTx, _Mapping]] = ...) -> None: ...
