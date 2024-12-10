from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RedeemerPurpose(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REDEEMER_PURPOSE_UNSPECIFIED: _ClassVar[RedeemerPurpose]
    REDEEMER_PURPOSE_SPEND: _ClassVar[RedeemerPurpose]
    REDEEMER_PURPOSE_MINT: _ClassVar[RedeemerPurpose]
    REDEEMER_PURPOSE_CERT: _ClassVar[RedeemerPurpose]
    REDEEMER_PURPOSE_REWARD: _ClassVar[RedeemerPurpose]
    REDEEMER_PURPOSE_VOTE: _ClassVar[RedeemerPurpose]
    REDEEMER_PURPOSE_PROPOSE: _ClassVar[RedeemerPurpose]

class MirSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MIR_SOURCE_UNSPECIFIED: _ClassVar[MirSource]
    MIR_SOURCE_RESERVES: _ClassVar[MirSource]
    MIR_SOURCE_TREASURY: _ClassVar[MirSource]
REDEEMER_PURPOSE_UNSPECIFIED: RedeemerPurpose
REDEEMER_PURPOSE_SPEND: RedeemerPurpose
REDEEMER_PURPOSE_MINT: RedeemerPurpose
REDEEMER_PURPOSE_CERT: RedeemerPurpose
REDEEMER_PURPOSE_REWARD: RedeemerPurpose
REDEEMER_PURPOSE_VOTE: RedeemerPurpose
REDEEMER_PURPOSE_PROPOSE: RedeemerPurpose
MIR_SOURCE_UNSPECIFIED: MirSource
MIR_SOURCE_RESERVES: MirSource
MIR_SOURCE_TREASURY: MirSource

class Redeemer(_message.Message):
    __slots__ = ("purpose", "payload", "index", "ex_units")
    PURPOSE_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    EX_UNITS_FIELD_NUMBER: _ClassVar[int]
    purpose: RedeemerPurpose
    payload: PlutusData
    index: int
    ex_units: ExUnits
    def __init__(self, purpose: _Optional[_Union[RedeemerPurpose, str]] = ..., payload: _Optional[_Union[PlutusData, _Mapping]] = ..., index: _Optional[int] = ..., ex_units: _Optional[_Union[ExUnits, _Mapping]] = ...) -> None: ...

class TxInput(_message.Message):
    __slots__ = ("tx_hash", "output_index", "as_output", "redeemer")
    TX_HASH_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_INDEX_FIELD_NUMBER: _ClassVar[int]
    AS_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    REDEEMER_FIELD_NUMBER: _ClassVar[int]
    tx_hash: bytes
    output_index: int
    as_output: TxOutput
    redeemer: Redeemer
    def __init__(self, tx_hash: _Optional[bytes] = ..., output_index: _Optional[int] = ..., as_output: _Optional[_Union[TxOutput, _Mapping]] = ..., redeemer: _Optional[_Union[Redeemer, _Mapping]] = ...) -> None: ...

class TxOutput(_message.Message):
    __slots__ = ("address", "coin", "assets", "datum", "script")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    COIN_FIELD_NUMBER: _ClassVar[int]
    ASSETS_FIELD_NUMBER: _ClassVar[int]
    DATUM_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_FIELD_NUMBER: _ClassVar[int]
    address: bytes
    coin: int
    assets: _containers.RepeatedCompositeFieldContainer[Multiasset]
    datum: Datum
    script: Script
    def __init__(self, address: _Optional[bytes] = ..., coin: _Optional[int] = ..., assets: _Optional[_Iterable[_Union[Multiasset, _Mapping]]] = ..., datum: _Optional[_Union[Datum, _Mapping]] = ..., script: _Optional[_Union[Script, _Mapping]] = ...) -> None: ...

class Datum(_message.Message):
    __slots__ = ("hash", "payload", "original_cbor")
    HASH_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_CBOR_FIELD_NUMBER: _ClassVar[int]
    hash: bytes
    payload: PlutusData
    original_cbor: bytes
    def __init__(self, hash: _Optional[bytes] = ..., payload: _Optional[_Union[PlutusData, _Mapping]] = ..., original_cbor: _Optional[bytes] = ...) -> None: ...

class Asset(_message.Message):
    __slots__ = ("name", "output_coin", "mint_coin")
    NAME_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_COIN_FIELD_NUMBER: _ClassVar[int]
    MINT_COIN_FIELD_NUMBER: _ClassVar[int]
    name: bytes
    output_coin: int
    mint_coin: int
    def __init__(self, name: _Optional[bytes] = ..., output_coin: _Optional[int] = ..., mint_coin: _Optional[int] = ...) -> None: ...

class Multiasset(_message.Message):
    __slots__ = ("policy_id", "assets", "redeemer")
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    ASSETS_FIELD_NUMBER: _ClassVar[int]
    REDEEMER_FIELD_NUMBER: _ClassVar[int]
    policy_id: bytes
    assets: _containers.RepeatedCompositeFieldContainer[Asset]
    redeemer: Redeemer
    def __init__(self, policy_id: _Optional[bytes] = ..., assets: _Optional[_Iterable[_Union[Asset, _Mapping]]] = ..., redeemer: _Optional[_Union[Redeemer, _Mapping]] = ...) -> None: ...

class TxValidity(_message.Message):
    __slots__ = ("start", "ttl")
    START_FIELD_NUMBER: _ClassVar[int]
    TTL_FIELD_NUMBER: _ClassVar[int]
    start: int
    ttl: int
    def __init__(self, start: _Optional[int] = ..., ttl: _Optional[int] = ...) -> None: ...

class Collateral(_message.Message):
    __slots__ = ("collateral", "collateral_return", "total_collateral")
    COLLATERAL_FIELD_NUMBER: _ClassVar[int]
    COLLATERAL_RETURN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COLLATERAL_FIELD_NUMBER: _ClassVar[int]
    collateral: _containers.RepeatedCompositeFieldContainer[TxInput]
    collateral_return: TxOutput
    total_collateral: int
    def __init__(self, collateral: _Optional[_Iterable[_Union[TxInput, _Mapping]]] = ..., collateral_return: _Optional[_Union[TxOutput, _Mapping]] = ..., total_collateral: _Optional[int] = ...) -> None: ...

class Withdrawal(_message.Message):
    __slots__ = ("reward_account", "coin", "redeemer")
    REWARD_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    COIN_FIELD_NUMBER: _ClassVar[int]
    REDEEMER_FIELD_NUMBER: _ClassVar[int]
    reward_account: bytes
    coin: int
    redeemer: Redeemer
    def __init__(self, reward_account: _Optional[bytes] = ..., coin: _Optional[int] = ..., redeemer: _Optional[_Union[Redeemer, _Mapping]] = ...) -> None: ...

class WitnessSet(_message.Message):
    __slots__ = ("vkeywitness", "script", "plutus_datums")
    VKEYWITNESS_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_FIELD_NUMBER: _ClassVar[int]
    PLUTUS_DATUMS_FIELD_NUMBER: _ClassVar[int]
    vkeywitness: _containers.RepeatedCompositeFieldContainer[VKeyWitness]
    script: _containers.RepeatedCompositeFieldContainer[Script]
    plutus_datums: _containers.RepeatedCompositeFieldContainer[PlutusData]
    def __init__(self, vkeywitness: _Optional[_Iterable[_Union[VKeyWitness, _Mapping]]] = ..., script: _Optional[_Iterable[_Union[Script, _Mapping]]] = ..., plutus_datums: _Optional[_Iterable[_Union[PlutusData, _Mapping]]] = ...) -> None: ...

class AuxData(_message.Message):
    __slots__ = ("metadata", "scripts")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SCRIPTS_FIELD_NUMBER: _ClassVar[int]
    metadata: _containers.RepeatedCompositeFieldContainer[Metadata]
    scripts: _containers.RepeatedCompositeFieldContainer[Script]
    def __init__(self, metadata: _Optional[_Iterable[_Union[Metadata, _Mapping]]] = ..., scripts: _Optional[_Iterable[_Union[Script, _Mapping]]] = ...) -> None: ...

class Tx(_message.Message):
    __slots__ = ("inputs", "outputs", "certificates", "withdrawals", "mint", "reference_inputs", "witnesses", "collateral", "fee", "validity", "successful", "auxiliary", "hash")
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    CERTIFICATES_FIELD_NUMBER: _ClassVar[int]
    WITHDRAWALS_FIELD_NUMBER: _ClassVar[int]
    MINT_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_INPUTS_FIELD_NUMBER: _ClassVar[int]
    WITNESSES_FIELD_NUMBER: _ClassVar[int]
    COLLATERAL_FIELD_NUMBER: _ClassVar[int]
    FEE_FIELD_NUMBER: _ClassVar[int]
    VALIDITY_FIELD_NUMBER: _ClassVar[int]
    SUCCESSFUL_FIELD_NUMBER: _ClassVar[int]
    AUXILIARY_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    inputs: _containers.RepeatedCompositeFieldContainer[TxInput]
    outputs: _containers.RepeatedCompositeFieldContainer[TxOutput]
    certificates: _containers.RepeatedCompositeFieldContainer[Certificate]
    withdrawals: _containers.RepeatedCompositeFieldContainer[Withdrawal]
    mint: _containers.RepeatedCompositeFieldContainer[Multiasset]
    reference_inputs: _containers.RepeatedCompositeFieldContainer[TxInput]
    witnesses: WitnessSet
    collateral: Collateral
    fee: int
    validity: TxValidity
    successful: bool
    auxiliary: AuxData
    hash: bytes
    def __init__(self, inputs: _Optional[_Iterable[_Union[TxInput, _Mapping]]] = ..., outputs: _Optional[_Iterable[_Union[TxOutput, _Mapping]]] = ..., certificates: _Optional[_Iterable[_Union[Certificate, _Mapping]]] = ..., withdrawals: _Optional[_Iterable[_Union[Withdrawal, _Mapping]]] = ..., mint: _Optional[_Iterable[_Union[Multiasset, _Mapping]]] = ..., reference_inputs: _Optional[_Iterable[_Union[TxInput, _Mapping]]] = ..., witnesses: _Optional[_Union[WitnessSet, _Mapping]] = ..., collateral: _Optional[_Union[Collateral, _Mapping]] = ..., fee: _Optional[int] = ..., validity: _Optional[_Union[TxValidity, _Mapping]] = ..., successful: bool = ..., auxiliary: _Optional[_Union[AuxData, _Mapping]] = ..., hash: _Optional[bytes] = ...) -> None: ...

class BlockHeader(_message.Message):
    __slots__ = ("slot", "hash", "height")
    SLOT_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    slot: int
    hash: bytes
    height: int
    def __init__(self, slot: _Optional[int] = ..., hash: _Optional[bytes] = ..., height: _Optional[int] = ...) -> None: ...

class BlockBody(_message.Message):
    __slots__ = ("tx",)
    TX_FIELD_NUMBER: _ClassVar[int]
    tx: _containers.RepeatedCompositeFieldContainer[Tx]
    def __init__(self, tx: _Optional[_Iterable[_Union[Tx, _Mapping]]] = ...) -> None: ...

class Block(_message.Message):
    __slots__ = ("header", "body")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    header: BlockHeader
    body: BlockBody
    def __init__(self, header: _Optional[_Union[BlockHeader, _Mapping]] = ..., body: _Optional[_Union[BlockBody, _Mapping]] = ...) -> None: ...

class VKeyWitness(_message.Message):
    __slots__ = ("vkey", "signature")
    VKEY_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    vkey: bytes
    signature: bytes
    def __init__(self, vkey: _Optional[bytes] = ..., signature: _Optional[bytes] = ...) -> None: ...

class NativeScript(_message.Message):
    __slots__ = ("script_pubkey", "script_all", "script_any", "script_n_of_k", "invalid_before", "invalid_hereafter")
    SCRIPT_PUBKEY_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_ALL_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_ANY_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_N_OF_K_FIELD_NUMBER: _ClassVar[int]
    INVALID_BEFORE_FIELD_NUMBER: _ClassVar[int]
    INVALID_HEREAFTER_FIELD_NUMBER: _ClassVar[int]
    script_pubkey: bytes
    script_all: NativeScriptList
    script_any: NativeScriptList
    script_n_of_k: ScriptNOfK
    invalid_before: int
    invalid_hereafter: int
    def __init__(self, script_pubkey: _Optional[bytes] = ..., script_all: _Optional[_Union[NativeScriptList, _Mapping]] = ..., script_any: _Optional[_Union[NativeScriptList, _Mapping]] = ..., script_n_of_k: _Optional[_Union[ScriptNOfK, _Mapping]] = ..., invalid_before: _Optional[int] = ..., invalid_hereafter: _Optional[int] = ...) -> None: ...

class NativeScriptList(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[NativeScript]
    def __init__(self, items: _Optional[_Iterable[_Union[NativeScript, _Mapping]]] = ...) -> None: ...

class ScriptNOfK(_message.Message):
    __slots__ = ("k", "scripts")
    K_FIELD_NUMBER: _ClassVar[int]
    SCRIPTS_FIELD_NUMBER: _ClassVar[int]
    k: int
    scripts: _containers.RepeatedCompositeFieldContainer[NativeScript]
    def __init__(self, k: _Optional[int] = ..., scripts: _Optional[_Iterable[_Union[NativeScript, _Mapping]]] = ...) -> None: ...

class Constr(_message.Message):
    __slots__ = ("tag", "any_constructor", "fields")
    TAG_FIELD_NUMBER: _ClassVar[int]
    ANY_CONSTRUCTOR_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    tag: int
    any_constructor: int
    fields: _containers.RepeatedCompositeFieldContainer[PlutusData]
    def __init__(self, tag: _Optional[int] = ..., any_constructor: _Optional[int] = ..., fields: _Optional[_Iterable[_Union[PlutusData, _Mapping]]] = ...) -> None: ...

class BigInt(_message.Message):
    __slots__ = ("int", "big_u_int", "big_n_int")
    INT_FIELD_NUMBER: _ClassVar[int]
    BIG_U_INT_FIELD_NUMBER: _ClassVar[int]
    BIG_N_INT_FIELD_NUMBER: _ClassVar[int]
    int: int
    big_u_int: bytes
    big_n_int: bytes
    def __init__(self, int: _Optional[int] = ..., big_u_int: _Optional[bytes] = ..., big_n_int: _Optional[bytes] = ...) -> None: ...

class PlutusDataPair(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: PlutusData
    value: PlutusData
    def __init__(self, key: _Optional[_Union[PlutusData, _Mapping]] = ..., value: _Optional[_Union[PlutusData, _Mapping]] = ...) -> None: ...

class PlutusData(_message.Message):
    __slots__ = ("constr", "map", "big_int", "bounded_bytes", "array")
    CONSTR_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    BIG_INT_FIELD_NUMBER: _ClassVar[int]
    BOUNDED_BYTES_FIELD_NUMBER: _ClassVar[int]
    ARRAY_FIELD_NUMBER: _ClassVar[int]
    constr: Constr
    map: PlutusDataMap
    big_int: BigInt
    bounded_bytes: bytes
    array: PlutusDataArray
    def __init__(self, constr: _Optional[_Union[Constr, _Mapping]] = ..., map: _Optional[_Union[PlutusDataMap, _Mapping]] = ..., big_int: _Optional[_Union[BigInt, _Mapping]] = ..., bounded_bytes: _Optional[bytes] = ..., array: _Optional[_Union[PlutusDataArray, _Mapping]] = ...) -> None: ...

class PlutusDataMap(_message.Message):
    __slots__ = ("pairs",)
    PAIRS_FIELD_NUMBER: _ClassVar[int]
    pairs: _containers.RepeatedCompositeFieldContainer[PlutusDataPair]
    def __init__(self, pairs: _Optional[_Iterable[_Union[PlutusDataPair, _Mapping]]] = ...) -> None: ...

class PlutusDataArray(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[PlutusData]
    def __init__(self, items: _Optional[_Iterable[_Union[PlutusData, _Mapping]]] = ...) -> None: ...

class Script(_message.Message):
    __slots__ = ("native", "plutus_v1", "plutus_v2", "plutus_v3")
    NATIVE_FIELD_NUMBER: _ClassVar[int]
    PLUTUS_V1_FIELD_NUMBER: _ClassVar[int]
    PLUTUS_V2_FIELD_NUMBER: _ClassVar[int]
    PLUTUS_V3_FIELD_NUMBER: _ClassVar[int]
    native: NativeScript
    plutus_v1: bytes
    plutus_v2: bytes
    plutus_v3: bytes
    def __init__(self, native: _Optional[_Union[NativeScript, _Mapping]] = ..., plutus_v1: _Optional[bytes] = ..., plutus_v2: _Optional[bytes] = ..., plutus_v3: _Optional[bytes] = ...) -> None: ...

class Metadatum(_message.Message):
    __slots__ = ("int", "bytes", "text", "array", "map")
    INT_FIELD_NUMBER: _ClassVar[int]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    ARRAY_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    int: int
    bytes: bytes
    text: str
    array: MetadatumArray
    map: MetadatumMap
    def __init__(self, int: _Optional[int] = ..., bytes: _Optional[bytes] = ..., text: _Optional[str] = ..., array: _Optional[_Union[MetadatumArray, _Mapping]] = ..., map: _Optional[_Union[MetadatumMap, _Mapping]] = ...) -> None: ...

class MetadatumArray(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[Metadatum]
    def __init__(self, items: _Optional[_Iterable[_Union[Metadatum, _Mapping]]] = ...) -> None: ...

class MetadatumMap(_message.Message):
    __slots__ = ("pairs",)
    PAIRS_FIELD_NUMBER: _ClassVar[int]
    pairs: _containers.RepeatedCompositeFieldContainer[MetadatumPair]
    def __init__(self, pairs: _Optional[_Iterable[_Union[MetadatumPair, _Mapping]]] = ...) -> None: ...

class MetadatumPair(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: Metadatum
    value: Metadatum
    def __init__(self, key: _Optional[_Union[Metadatum, _Mapping]] = ..., value: _Optional[_Union[Metadatum, _Mapping]] = ...) -> None: ...

class Metadata(_message.Message):
    __slots__ = ("label", "value")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    label: int
    value: Metadatum
    def __init__(self, label: _Optional[int] = ..., value: _Optional[_Union[Metadatum, _Mapping]] = ...) -> None: ...

class StakeCredential(_message.Message):
    __slots__ = ("addr_key_hash", "script_hash")
    ADDR_KEY_HASH_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_HASH_FIELD_NUMBER: _ClassVar[int]
    addr_key_hash: bytes
    script_hash: bytes
    def __init__(self, addr_key_hash: _Optional[bytes] = ..., script_hash: _Optional[bytes] = ...) -> None: ...

class RationalNumber(_message.Message):
    __slots__ = ("numerator", "denominator")
    NUMERATOR_FIELD_NUMBER: _ClassVar[int]
    DENOMINATOR_FIELD_NUMBER: _ClassVar[int]
    numerator: int
    denominator: int
    def __init__(self, numerator: _Optional[int] = ..., denominator: _Optional[int] = ...) -> None: ...

class Relay(_message.Message):
    __slots__ = ("ip_v4", "ip_v6", "dns_name", "port")
    IP_V4_FIELD_NUMBER: _ClassVar[int]
    IP_V6_FIELD_NUMBER: _ClassVar[int]
    DNS_NAME_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    ip_v4: bytes
    ip_v6: bytes
    dns_name: str
    port: int
    def __init__(self, ip_v4: _Optional[bytes] = ..., ip_v6: _Optional[bytes] = ..., dns_name: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...

class PoolMetadata(_message.Message):
    __slots__ = ("url", "hash")
    URL_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    url: str
    hash: bytes
    def __init__(self, url: _Optional[str] = ..., hash: _Optional[bytes] = ...) -> None: ...

class Certificate(_message.Message):
    __slots__ = ("stake_registration", "stake_deregistration", "stake_delegation", "pool_registration", "pool_retirement", "genesis_key_delegation", "mir_cert", "reg_cert", "unreg_cert", "vote_deleg_cert", "stake_vote_deleg_cert", "stake_reg_deleg_cert", "vote_reg_deleg_cert", "stake_vote_reg_deleg_cert", "auth_committee_hot_cert", "resign_committee_cold_cert", "reg_drep_cert", "unreg_drep_cert", "update_drep_cert", "redeemer")
    STAKE_REGISTRATION_FIELD_NUMBER: _ClassVar[int]
    STAKE_DEREGISTRATION_FIELD_NUMBER: _ClassVar[int]
    STAKE_DELEGATION_FIELD_NUMBER: _ClassVar[int]
    POOL_REGISTRATION_FIELD_NUMBER: _ClassVar[int]
    POOL_RETIREMENT_FIELD_NUMBER: _ClassVar[int]
    GENESIS_KEY_DELEGATION_FIELD_NUMBER: _ClassVar[int]
    MIR_CERT_FIELD_NUMBER: _ClassVar[int]
    REG_CERT_FIELD_NUMBER: _ClassVar[int]
    UNREG_CERT_FIELD_NUMBER: _ClassVar[int]
    VOTE_DELEG_CERT_FIELD_NUMBER: _ClassVar[int]
    STAKE_VOTE_DELEG_CERT_FIELD_NUMBER: _ClassVar[int]
    STAKE_REG_DELEG_CERT_FIELD_NUMBER: _ClassVar[int]
    VOTE_REG_DELEG_CERT_FIELD_NUMBER: _ClassVar[int]
    STAKE_VOTE_REG_DELEG_CERT_FIELD_NUMBER: _ClassVar[int]
    AUTH_COMMITTEE_HOT_CERT_FIELD_NUMBER: _ClassVar[int]
    RESIGN_COMMITTEE_COLD_CERT_FIELD_NUMBER: _ClassVar[int]
    REG_DREP_CERT_FIELD_NUMBER: _ClassVar[int]
    UNREG_DREP_CERT_FIELD_NUMBER: _ClassVar[int]
    UPDATE_DREP_CERT_FIELD_NUMBER: _ClassVar[int]
    REDEEMER_FIELD_NUMBER: _ClassVar[int]
    stake_registration: StakeCredential
    stake_deregistration: StakeCredential
    stake_delegation: StakeDelegationCert
    pool_registration: PoolRegistrationCert
    pool_retirement: PoolRetirementCert
    genesis_key_delegation: GenesisKeyDelegationCert
    mir_cert: MirCert
    reg_cert: RegCert
    unreg_cert: UnRegCert
    vote_deleg_cert: VoteDelegCert
    stake_vote_deleg_cert: StakeVoteDelegCert
    stake_reg_deleg_cert: StakeRegDelegCert
    vote_reg_deleg_cert: VoteRegDelegCert
    stake_vote_reg_deleg_cert: StakeVoteRegDelegCert
    auth_committee_hot_cert: AuthCommitteeHotCert
    resign_committee_cold_cert: ResignCommitteeColdCert
    reg_drep_cert: RegDRepCert
    unreg_drep_cert: UnRegDRepCert
    update_drep_cert: UpdateDRepCert
    redeemer: Redeemer
    def __init__(self, stake_registration: _Optional[_Union[StakeCredential, _Mapping]] = ..., stake_deregistration: _Optional[_Union[StakeCredential, _Mapping]] = ..., stake_delegation: _Optional[_Union[StakeDelegationCert, _Mapping]] = ..., pool_registration: _Optional[_Union[PoolRegistrationCert, _Mapping]] = ..., pool_retirement: _Optional[_Union[PoolRetirementCert, _Mapping]] = ..., genesis_key_delegation: _Optional[_Union[GenesisKeyDelegationCert, _Mapping]] = ..., mir_cert: _Optional[_Union[MirCert, _Mapping]] = ..., reg_cert: _Optional[_Union[RegCert, _Mapping]] = ..., unreg_cert: _Optional[_Union[UnRegCert, _Mapping]] = ..., vote_deleg_cert: _Optional[_Union[VoteDelegCert, _Mapping]] = ..., stake_vote_deleg_cert: _Optional[_Union[StakeVoteDelegCert, _Mapping]] = ..., stake_reg_deleg_cert: _Optional[_Union[StakeRegDelegCert, _Mapping]] = ..., vote_reg_deleg_cert: _Optional[_Union[VoteRegDelegCert, _Mapping]] = ..., stake_vote_reg_deleg_cert: _Optional[_Union[StakeVoteRegDelegCert, _Mapping]] = ..., auth_committee_hot_cert: _Optional[_Union[AuthCommitteeHotCert, _Mapping]] = ..., resign_committee_cold_cert: _Optional[_Union[ResignCommitteeColdCert, _Mapping]] = ..., reg_drep_cert: _Optional[_Union[RegDRepCert, _Mapping]] = ..., unreg_drep_cert: _Optional[_Union[UnRegDRepCert, _Mapping]] = ..., update_drep_cert: _Optional[_Union[UpdateDRepCert, _Mapping]] = ..., redeemer: _Optional[_Union[Redeemer, _Mapping]] = ...) -> None: ...

class StakeDelegationCert(_message.Message):
    __slots__ = ("stake_credential", "pool_keyhash")
    STAKE_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    POOL_KEYHASH_FIELD_NUMBER: _ClassVar[int]
    stake_credential: StakeCredential
    pool_keyhash: bytes
    def __init__(self, stake_credential: _Optional[_Union[StakeCredential, _Mapping]] = ..., pool_keyhash: _Optional[bytes] = ...) -> None: ...

class PoolRegistrationCert(_message.Message):
    __slots__ = ("operator", "vrf_keyhash", "pledge", "cost", "margin", "reward_account", "pool_owners", "relays", "pool_metadata")
    OPERATOR_FIELD_NUMBER: _ClassVar[int]
    VRF_KEYHASH_FIELD_NUMBER: _ClassVar[int]
    PLEDGE_FIELD_NUMBER: _ClassVar[int]
    COST_FIELD_NUMBER: _ClassVar[int]
    MARGIN_FIELD_NUMBER: _ClassVar[int]
    REWARD_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    POOL_OWNERS_FIELD_NUMBER: _ClassVar[int]
    RELAYS_FIELD_NUMBER: _ClassVar[int]
    POOL_METADATA_FIELD_NUMBER: _ClassVar[int]
    operator: bytes
    vrf_keyhash: bytes
    pledge: int
    cost: int
    margin: RationalNumber
    reward_account: bytes
    pool_owners: _containers.RepeatedScalarFieldContainer[bytes]
    relays: _containers.RepeatedCompositeFieldContainer[Relay]
    pool_metadata: PoolMetadata
    def __init__(self, operator: _Optional[bytes] = ..., vrf_keyhash: _Optional[bytes] = ..., pledge: _Optional[int] = ..., cost: _Optional[int] = ..., margin: _Optional[_Union[RationalNumber, _Mapping]] = ..., reward_account: _Optional[bytes] = ..., pool_owners: _Optional[_Iterable[bytes]] = ..., relays: _Optional[_Iterable[_Union[Relay, _Mapping]]] = ..., pool_metadata: _Optional[_Union[PoolMetadata, _Mapping]] = ...) -> None: ...

class PoolRetirementCert(_message.Message):
    __slots__ = ("pool_keyhash", "epoch")
    POOL_KEYHASH_FIELD_NUMBER: _ClassVar[int]
    EPOCH_FIELD_NUMBER: _ClassVar[int]
    pool_keyhash: bytes
    epoch: int
    def __init__(self, pool_keyhash: _Optional[bytes] = ..., epoch: _Optional[int] = ...) -> None: ...

class GenesisKeyDelegationCert(_message.Message):
    __slots__ = ("genesis_hash", "genesis_delegate_hash", "vrf_keyhash")
    GENESIS_HASH_FIELD_NUMBER: _ClassVar[int]
    GENESIS_DELEGATE_HASH_FIELD_NUMBER: _ClassVar[int]
    VRF_KEYHASH_FIELD_NUMBER: _ClassVar[int]
    genesis_hash: bytes
    genesis_delegate_hash: bytes
    vrf_keyhash: bytes
    def __init__(self, genesis_hash: _Optional[bytes] = ..., genesis_delegate_hash: _Optional[bytes] = ..., vrf_keyhash: _Optional[bytes] = ...) -> None: ...

class MirTarget(_message.Message):
    __slots__ = ("stake_credential", "delta_coin")
    STAKE_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    DELTA_COIN_FIELD_NUMBER: _ClassVar[int]
    stake_credential: StakeCredential
    delta_coin: int
    def __init__(self, stake_credential: _Optional[_Union[StakeCredential, _Mapping]] = ..., delta_coin: _Optional[int] = ...) -> None: ...

class MirCert(_message.Message):
    __slots__ = ("to", "other_pot")
    FROM_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    OTHER_POT_FIELD_NUMBER: _ClassVar[int]
    to: _containers.RepeatedCompositeFieldContainer[MirTarget]
    other_pot: int
    def __init__(self, to: _Optional[_Iterable[_Union[MirTarget, _Mapping]]] = ..., other_pot: _Optional[int] = ..., **kwargs) -> None: ...

class RegCert(_message.Message):
    __slots__ = ("stake_credential", "coin")
    STAKE_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    COIN_FIELD_NUMBER: _ClassVar[int]
    stake_credential: StakeCredential
    coin: int
    def __init__(self, stake_credential: _Optional[_Union[StakeCredential, _Mapping]] = ..., coin: _Optional[int] = ...) -> None: ...

class UnRegCert(_message.Message):
    __slots__ = ("stake_credential", "coin")
    STAKE_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    COIN_FIELD_NUMBER: _ClassVar[int]
    stake_credential: StakeCredential
    coin: int
    def __init__(self, stake_credential: _Optional[_Union[StakeCredential, _Mapping]] = ..., coin: _Optional[int] = ...) -> None: ...

class DRep(_message.Message):
    __slots__ = ("addr_key_hash", "script_hash", "abstain", "no_confidence")
    ADDR_KEY_HASH_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_HASH_FIELD_NUMBER: _ClassVar[int]
    ABSTAIN_FIELD_NUMBER: _ClassVar[int]
    NO_CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    addr_key_hash: bytes
    script_hash: bytes
    abstain: bool
    no_confidence: bool
    def __init__(self, addr_key_hash: _Optional[bytes] = ..., script_hash: _Optional[bytes] = ..., abstain: bool = ..., no_confidence: bool = ...) -> None: ...

class VoteDelegCert(_message.Message):
    __slots__ = ("stake_credential", "drep")
    STAKE_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    DREP_FIELD_NUMBER: _ClassVar[int]
    stake_credential: StakeCredential
    drep: DRep
    def __init__(self, stake_credential: _Optional[_Union[StakeCredential, _Mapping]] = ..., drep: _Optional[_Union[DRep, _Mapping]] = ...) -> None: ...

class StakeVoteDelegCert(_message.Message):
    __slots__ = ("stake_credential", "pool_keyhash", "drep")
    STAKE_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    POOL_KEYHASH_FIELD_NUMBER: _ClassVar[int]
    DREP_FIELD_NUMBER: _ClassVar[int]
    stake_credential: StakeCredential
    pool_keyhash: bytes
    drep: DRep
    def __init__(self, stake_credential: _Optional[_Union[StakeCredential, _Mapping]] = ..., pool_keyhash: _Optional[bytes] = ..., drep: _Optional[_Union[DRep, _Mapping]] = ...) -> None: ...

class StakeRegDelegCert(_message.Message):
    __slots__ = ("stake_credential", "pool_keyhash", "coin")
    STAKE_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    POOL_KEYHASH_FIELD_NUMBER: _ClassVar[int]
    COIN_FIELD_NUMBER: _ClassVar[int]
    stake_credential: StakeCredential
    pool_keyhash: bytes
    coin: int
    def __init__(self, stake_credential: _Optional[_Union[StakeCredential, _Mapping]] = ..., pool_keyhash: _Optional[bytes] = ..., coin: _Optional[int] = ...) -> None: ...

class VoteRegDelegCert(_message.Message):
    __slots__ = ("stake_credential", "drep", "coin")
    STAKE_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    DREP_FIELD_NUMBER: _ClassVar[int]
    COIN_FIELD_NUMBER: _ClassVar[int]
    stake_credential: StakeCredential
    drep: DRep
    coin: int
    def __init__(self, stake_credential: _Optional[_Union[StakeCredential, _Mapping]] = ..., drep: _Optional[_Union[DRep, _Mapping]] = ..., coin: _Optional[int] = ...) -> None: ...

class StakeVoteRegDelegCert(_message.Message):
    __slots__ = ("stake_credential", "pool_keyhash", "drep", "coin")
    STAKE_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    POOL_KEYHASH_FIELD_NUMBER: _ClassVar[int]
    DREP_FIELD_NUMBER: _ClassVar[int]
    COIN_FIELD_NUMBER: _ClassVar[int]
    stake_credential: StakeCredential
    pool_keyhash: bytes
    drep: DRep
    coin: int
    def __init__(self, stake_credential: _Optional[_Union[StakeCredential, _Mapping]] = ..., pool_keyhash: _Optional[bytes] = ..., drep: _Optional[_Union[DRep, _Mapping]] = ..., coin: _Optional[int] = ...) -> None: ...

class AuthCommitteeHotCert(_message.Message):
    __slots__ = ("committee_cold_credential", "committee_hot_credential")
    COMMITTEE_COLD_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    COMMITTEE_HOT_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    committee_cold_credential: StakeCredential
    committee_hot_credential: StakeCredential
    def __init__(self, committee_cold_credential: _Optional[_Union[StakeCredential, _Mapping]] = ..., committee_hot_credential: _Optional[_Union[StakeCredential, _Mapping]] = ...) -> None: ...

class Anchor(_message.Message):
    __slots__ = ("url", "content_hash")
    URL_FIELD_NUMBER: _ClassVar[int]
    CONTENT_HASH_FIELD_NUMBER: _ClassVar[int]
    url: str
    content_hash: bytes
    def __init__(self, url: _Optional[str] = ..., content_hash: _Optional[bytes] = ...) -> None: ...

class ResignCommitteeColdCert(_message.Message):
    __slots__ = ("committee_cold_credential", "anchor")
    COMMITTEE_COLD_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    ANCHOR_FIELD_NUMBER: _ClassVar[int]
    committee_cold_credential: StakeCredential
    anchor: Anchor
    def __init__(self, committee_cold_credential: _Optional[_Union[StakeCredential, _Mapping]] = ..., anchor: _Optional[_Union[Anchor, _Mapping]] = ...) -> None: ...

class RegDRepCert(_message.Message):
    __slots__ = ("drep_credential", "coin", "anchor")
    DREP_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    COIN_FIELD_NUMBER: _ClassVar[int]
    ANCHOR_FIELD_NUMBER: _ClassVar[int]
    drep_credential: StakeCredential
    coin: int
    anchor: Anchor
    def __init__(self, drep_credential: _Optional[_Union[StakeCredential, _Mapping]] = ..., coin: _Optional[int] = ..., anchor: _Optional[_Union[Anchor, _Mapping]] = ...) -> None: ...

class UnRegDRepCert(_message.Message):
    __slots__ = ("drep_credential", "coin")
    DREP_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    COIN_FIELD_NUMBER: _ClassVar[int]
    drep_credential: StakeCredential
    coin: int
    def __init__(self, drep_credential: _Optional[_Union[StakeCredential, _Mapping]] = ..., coin: _Optional[int] = ...) -> None: ...

class UpdateDRepCert(_message.Message):
    __slots__ = ("drep_credential", "anchor")
    DREP_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    ANCHOR_FIELD_NUMBER: _ClassVar[int]
    drep_credential: StakeCredential
    anchor: Anchor
    def __init__(self, drep_credential: _Optional[_Union[StakeCredential, _Mapping]] = ..., anchor: _Optional[_Union[Anchor, _Mapping]] = ...) -> None: ...

class AddressPattern(_message.Message):
    __slots__ = ("exact_address", "payment_part", "delegation_part")
    EXACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_PART_FIELD_NUMBER: _ClassVar[int]
    DELEGATION_PART_FIELD_NUMBER: _ClassVar[int]
    exact_address: bytes
    payment_part: bytes
    delegation_part: bytes
    def __init__(self, exact_address: _Optional[bytes] = ..., payment_part: _Optional[bytes] = ..., delegation_part: _Optional[bytes] = ...) -> None: ...

class AssetPattern(_message.Message):
    __slots__ = ("policy_id", "asset_name")
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    ASSET_NAME_FIELD_NUMBER: _ClassVar[int]
    policy_id: bytes
    asset_name: bytes
    def __init__(self, policy_id: _Optional[bytes] = ..., asset_name: _Optional[bytes] = ...) -> None: ...

class TxOutputPattern(_message.Message):
    __slots__ = ("address", "asset")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ASSET_FIELD_NUMBER: _ClassVar[int]
    address: AddressPattern
    asset: AssetPattern
    def __init__(self, address: _Optional[_Union[AddressPattern, _Mapping]] = ..., asset: _Optional[_Union[AssetPattern, _Mapping]] = ...) -> None: ...

class TxPattern(_message.Message):
    __slots__ = ("consumes", "produces", "has_address", "moves_asset", "mints_asset")
    CONSUMES_FIELD_NUMBER: _ClassVar[int]
    PRODUCES_FIELD_NUMBER: _ClassVar[int]
    HAS_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    MOVES_ASSET_FIELD_NUMBER: _ClassVar[int]
    MINTS_ASSET_FIELD_NUMBER: _ClassVar[int]
    consumes: TxOutputPattern
    produces: TxOutputPattern
    has_address: AddressPattern
    moves_asset: AssetPattern
    mints_asset: AssetPattern
    def __init__(self, consumes: _Optional[_Union[TxOutputPattern, _Mapping]] = ..., produces: _Optional[_Union[TxOutputPattern, _Mapping]] = ..., has_address: _Optional[_Union[AddressPattern, _Mapping]] = ..., moves_asset: _Optional[_Union[AssetPattern, _Mapping]] = ..., mints_asset: _Optional[_Union[AssetPattern, _Mapping]] = ...) -> None: ...

class ExUnits(_message.Message):
    __slots__ = ("steps", "memory")
    STEPS_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    steps: int
    memory: int
    def __init__(self, steps: _Optional[int] = ..., memory: _Optional[int] = ...) -> None: ...

class ExPrices(_message.Message):
    __slots__ = ("steps", "memory")
    STEPS_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    steps: RationalNumber
    memory: RationalNumber
    def __init__(self, steps: _Optional[_Union[RationalNumber, _Mapping]] = ..., memory: _Optional[_Union[RationalNumber, _Mapping]] = ...) -> None: ...

class ProtocolVersion(_message.Message):
    __slots__ = ("major", "minor")
    MAJOR_FIELD_NUMBER: _ClassVar[int]
    MINOR_FIELD_NUMBER: _ClassVar[int]
    major: int
    minor: int
    def __init__(self, major: _Optional[int] = ..., minor: _Optional[int] = ...) -> None: ...

class CostModel(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, values: _Optional[_Iterable[int]] = ...) -> None: ...

class CostModels(_message.Message):
    __slots__ = ("plutus_v1", "plutus_v2", "plutus_v3")
    PLUTUS_V1_FIELD_NUMBER: _ClassVar[int]
    PLUTUS_V2_FIELD_NUMBER: _ClassVar[int]
    PLUTUS_V3_FIELD_NUMBER: _ClassVar[int]
    plutus_v1: CostModel
    plutus_v2: CostModel
    plutus_v3: CostModel
    def __init__(self, plutus_v1: _Optional[_Union[CostModel, _Mapping]] = ..., plutus_v2: _Optional[_Union[CostModel, _Mapping]] = ..., plutus_v3: _Optional[_Union[CostModel, _Mapping]] = ...) -> None: ...

class PParams(_message.Message):
    __slots__ = ("coins_per_utxo_byte", "max_tx_size", "min_fee_coefficient", "min_fee_constant", "max_block_body_size", "max_block_header_size", "stake_key_deposit", "pool_deposit", "pool_retirement_epoch_bound", "desired_number_of_pools", "pool_influence", "monetary_expansion", "treasury_expansion", "min_pool_cost", "protocol_version", "max_value_size", "collateral_percentage", "max_collateral_inputs", "cost_models", "prices", "max_execution_units_per_transaction", "max_execution_units_per_block")
    COINS_PER_UTXO_BYTE_FIELD_NUMBER: _ClassVar[int]
    MAX_TX_SIZE_FIELD_NUMBER: _ClassVar[int]
    MIN_FEE_COEFFICIENT_FIELD_NUMBER: _ClassVar[int]
    MIN_FEE_CONSTANT_FIELD_NUMBER: _ClassVar[int]
    MAX_BLOCK_BODY_SIZE_FIELD_NUMBER: _ClassVar[int]
    MAX_BLOCK_HEADER_SIZE_FIELD_NUMBER: _ClassVar[int]
    STAKE_KEY_DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    POOL_DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    POOL_RETIREMENT_EPOCH_BOUND_FIELD_NUMBER: _ClassVar[int]
    DESIRED_NUMBER_OF_POOLS_FIELD_NUMBER: _ClassVar[int]
    POOL_INFLUENCE_FIELD_NUMBER: _ClassVar[int]
    MONETARY_EXPANSION_FIELD_NUMBER: _ClassVar[int]
    TREASURY_EXPANSION_FIELD_NUMBER: _ClassVar[int]
    MIN_POOL_COST_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_VERSION_FIELD_NUMBER: _ClassVar[int]
    MAX_VALUE_SIZE_FIELD_NUMBER: _ClassVar[int]
    COLLATERAL_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    MAX_COLLATERAL_INPUTS_FIELD_NUMBER: _ClassVar[int]
    COST_MODELS_FIELD_NUMBER: _ClassVar[int]
    PRICES_FIELD_NUMBER: _ClassVar[int]
    MAX_EXECUTION_UNITS_PER_TRANSACTION_FIELD_NUMBER: _ClassVar[int]
    MAX_EXECUTION_UNITS_PER_BLOCK_FIELD_NUMBER: _ClassVar[int]
    coins_per_utxo_byte: int
    max_tx_size: int
    min_fee_coefficient: int
    min_fee_constant: int
    max_block_body_size: int
    max_block_header_size: int
    stake_key_deposit: int
    pool_deposit: int
    pool_retirement_epoch_bound: int
    desired_number_of_pools: int
    pool_influence: RationalNumber
    monetary_expansion: RationalNumber
    treasury_expansion: RationalNumber
    min_pool_cost: int
    protocol_version: ProtocolVersion
    max_value_size: int
    collateral_percentage: int
    max_collateral_inputs: int
    cost_models: CostModels
    prices: ExPrices
    max_execution_units_per_transaction: ExUnits
    max_execution_units_per_block: ExUnits
    def __init__(self, coins_per_utxo_byte: _Optional[int] = ..., max_tx_size: _Optional[int] = ..., min_fee_coefficient: _Optional[int] = ..., min_fee_constant: _Optional[int] = ..., max_block_body_size: _Optional[int] = ..., max_block_header_size: _Optional[int] = ..., stake_key_deposit: _Optional[int] = ..., pool_deposit: _Optional[int] = ..., pool_retirement_epoch_bound: _Optional[int] = ..., desired_number_of_pools: _Optional[int] = ..., pool_influence: _Optional[_Union[RationalNumber, _Mapping]] = ..., monetary_expansion: _Optional[_Union[RationalNumber, _Mapping]] = ..., treasury_expansion: _Optional[_Union[RationalNumber, _Mapping]] = ..., min_pool_cost: _Optional[int] = ..., protocol_version: _Optional[_Union[ProtocolVersion, _Mapping]] = ..., max_value_size: _Optional[int] = ..., collateral_percentage: _Optional[int] = ..., max_collateral_inputs: _Optional[int] = ..., cost_models: _Optional[_Union[CostModels, _Mapping]] = ..., prices: _Optional[_Union[ExPrices, _Mapping]] = ..., max_execution_units_per_transaction: _Optional[_Union[ExUnits, _Mapping]] = ..., max_execution_units_per_block: _Optional[_Union[ExUnits, _Mapping]] = ...) -> None: ...

class EvalError(_message.Message):
    __slots__ = ("msg",)
    MSG_FIELD_NUMBER: _ClassVar[int]
    msg: str
    def __init__(self, msg: _Optional[str] = ...) -> None: ...

class EvalTrace(_message.Message):
    __slots__ = ("msg",)
    MSG_FIELD_NUMBER: _ClassVar[int]
    msg: str
    def __init__(self, msg: _Optional[str] = ...) -> None: ...

class TxEval(_message.Message):
    __slots__ = ("fee", "ex_units", "errors", "traces", "redeemers")
    FEE_FIELD_NUMBER: _ClassVar[int]
    EX_UNITS_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    TRACES_FIELD_NUMBER: _ClassVar[int]
    REDEEMERS_FIELD_NUMBER: _ClassVar[int]
    fee: int
    ex_units: ExUnits
    errors: _containers.RepeatedCompositeFieldContainer[EvalError]
    traces: _containers.RepeatedCompositeFieldContainer[EvalTrace]
    redeemers: _containers.RepeatedCompositeFieldContainer[Redeemer]
    def __init__(self, fee: _Optional[int] = ..., ex_units: _Optional[_Union[ExUnits, _Mapping]] = ..., errors: _Optional[_Iterable[_Union[EvalError, _Mapping]]] = ..., traces: _Optional[_Iterable[_Union[EvalTrace, _Mapping]]] = ..., redeemers: _Optional[_Iterable[_Union[Redeemer, _Mapping]]] = ...) -> None: ...
