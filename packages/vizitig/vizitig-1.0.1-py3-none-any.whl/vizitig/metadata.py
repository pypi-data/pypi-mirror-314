from typing import Iterable, List, MutableMapping, Tuple, Any

import networkdisk as nd
from pydantic import BaseModel

from vizitig import compatible_versions, version
from vizitig.errors import IncompatibleViziGraph, NotAViziGraphError
from vizitig.types import (
    AvailableKmerTypes,
    Color,
    ESign,
    SubseqData,
    ViziKey,
    Zero,
    encode_kmer,
    decode_kmer,
)
from vizitig.utils import cantor_pairing, inverse_cantor_pairing


class NodeDesc(BaseModel):
    seq: str
    metadatas: List[Color | SubseqData]
    neighbors: dict[int, ESign | None] = {}


class GraphMetadata(BaseModel):
    k: int
    size: int
    name: str
    edge_size: int  # number of edges
    gid: str  # a uniq global identifier of the graph generated once
    types_list: List[str] = list()
    vars_names: MutableMapping[str, List[str]] = dict()
    vars_values: MutableMapping[str, MutableMapping[str, Color | SubseqData]] = dict()
    filter_list: MutableMapping[str, str] = dict()
    vizitig_version: str = version

    def model_post_init(self, __context):
        nd.utils.serialize.encoderFunctions[self.key_type] = (
            self.encoder,
            self.decoder,
        )

    @property
    def key_type(self):
        return f"vizi_{self.gid}".upper()

    def encoder(self, to_encode: ViziKey | Zero) -> int | float | bytes:
        if isinstance(to_encode, float):
            return to_encode
        if isinstance(to_encode, (Color, SubseqData)):
            if (
                to_encode.offset is None
            ):  # Hacky but it helps recognizing the metadata that were
                # already ingested
                if to_encode == self.vars_values[to_encode.type][to_encode.id]:
                    to_encode = self.vars_values[to_encode.type][to_encode.id]

            assert to_encode.type in self.types_list
            assert to_encode.offset is not None
            return -cantor_pairing(
                to_encode.offset,
                self.types_list.index(to_encode.type) + 4,
            )
        if isinstance(to_encode, AvailableKmerTypes):
            return encode_kmer(to_encode, self.k)
        if to_encode == "sequence":
            return -1
        if to_encode == "occurence":
            return -2

        if "Kmer" in str(type(to_encode)):
            raise TypeError(f"""your Kmer Class ({type(to_encode)})is locally unknown. 
                            Avoid if this error occurs during tests.""")
        if isinstance(to_encode, Zero):
            return 0
        raise NotImplementedError(f"to_encode is of incorrect type {type(to_encode)}")

    def add_filter(self, fname: str, filter: str):
        assert isinstance(filter, str)
        self.filter_list[fname] = filter

    def get_filters(self) -> Iterable[tuple[str, str]]:
        return self.filter_list.items()

    def remove_filter(self, fname: str):
        assert fname in self.filter_list
        self.filter_list.pop(fname)

    def decoder(self, to_decode):
        if isinstance(to_decode, bytes) or (
            isinstance(to_decode, int) and to_decode >= 0
        ):
            return decode_kmer(to_decode, self.k)
        if isinstance(to_decode, float):
            return to_decode
        if to_decode == -1:
            return "sequence"
        if to_decode == -2:
            return "occurence"
        if to_decode <= -3:
            num1, num2 = inverse_cantor_pairing(-to_decode)
            type_to_decode = self.types_list[num2 - 4]
            return self.vars_values[type_to_decode][
                self.vars_names[type_to_decode][num1]
            ]

        raise NotImplementedError(
            f"to_decode is of incorrect type or value {to_decode, type(to_decode)}",
        )

    def add_iterative_metadatas(
        self,
        iterator: Iterable[Tuple[SubseqData | Color, Any]],
    ) -> Iterable[Tuple[SubseqData | Color, Any]]:
        for metadata, val in iterator:
            setup_metadata = self.add_metadata(metadata)
            yield (setup_metadata, val)

    def add_metadata(self, m: Color | SubseqData) -> Color | SubseqData:
        assert isinstance(m, (Color, SubseqData))
        if m.type not in self.vars_names:
            self.vars_names[m.type] = []
            self.vars_values[m.type] = {}
            self.types_list.append(m.type)

        if m.id not in self.vars_names[m.type]:
            self.vars_names[m.type].append(m.id)
        m.set_offset(len(self.vars_names[m.type]) - 1)
        self.vars_values[m.type][m.id] = m
        return m

    def set_all_offsets(self):
        for type_name in self.types_list:
            for i, name in enumerate(self.vars_names[type_name]):
                self.vars_values[type_name][name].set_offset(i)

    def commit_to_graph(self, G: nd.sqlite.DiGraph | nd.sqlite.Graph):
        G.graph = self.model_dump()

    @classmethod
    def set_metadata(
        cls,
        G: nd.sqlite.DiGraph | nd.sqlite.Graph,
        check_compatibility: bool = True,
        name: str | None = None,
    ):
        d = G.graph.fold()
        d.setdefault("name", name)
        if "vizitig_version" not in d:
            raise NotAViziGraphError()
        if check_compatibility and d["vizitig_version"] not in compatible_versions:
            raise IncompatibleViziGraph(d["vizitig_version"])
        GM = cls(**d)
        assert GM.gid
        G.metadata = GM

    def to_nodedesc(
        self,
        d: dict[ViziKey, None],
        neighbors: dict[int, ESign | None],
    ) -> NodeDesc:
        metadatas = list()
        for k in d:
            if isinstance(k, (Color, SubseqData)):
                metadatas.append(k)
        return NodeDesc(
            seq=str(d["sequence"]),
            metadatas=metadatas,
            neighbors=neighbors,
        )
