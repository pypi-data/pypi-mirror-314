from typing import Literal, TypeAlias

from lark import Lark, Transformer
from lark import exceptions as larkexceptions
from pydantic.dataclasses import dataclass

from vizitig.errors import ParseError


class Base:
    @property
    def t(self):
        keys = self.__dataclass_fields__.values()
        key = next(iter(keys))
        return getattr(self, key.name)


@dataclass(frozen=True)
class All(Base):
    all: None = None


@dataclass(frozen=True)
class Partial(Base):
    partial: None = None


@dataclass(frozen=True)
class Selection(Base):
    selection: None = None


@dataclass(frozen=True)
class NodeId(Base):
    id: int


@dataclass(frozen=True)
class Attr:
    key: str
    value: str | int
    op: Literal["=", "<", ">"]


@dataclass(frozen=True)
class Meta(Base):
    type: str
    name: str | None = None
    attrs: tuple[Attr, ...] = ()


@dataclass(frozen=True)
class Color(Base):
    color: str


@dataclass(frozen=True)
class Kmer(Base):
    kmer: str


@dataclass(frozen=True)
class Degree(Base):
    degree: int


@dataclass(frozen=True)
class Seq(Base):
    seq: str


@dataclass(frozen=True)
class PseudoMapping(Base):
    psdomap: str


@dataclass(frozen=True)
class And(Base):
    land: list["Term"]


@dataclass(frozen=True)
class Or(Base):
    lor: list["Term"]


@dataclass(frozen=True)
class Not(Base):
    lnot: "Term"


Term: TypeAlias = (
    NodeId
    | Meta
    | Color
    | And
    | Or
    | Not
    | Kmer
    | str
    | Seq
    | All
    | Partial
    | Selection
    | Degree
)


Grammar = r"""
?formula: lor_infix  
        | lor_prefix
        | land 
        | lnot 
        | par  
        | literal

_LEFTPAR  : /\s*\(\s*/ 
_RIGHTPAR : /\s*\)\s*/
?par      : _LEFTPAR formula _RIGHTPAR 
_SEP      : /\s*,\s*/
lor_infix : formula "or"i (_SPACES formula | par) 
lor_prefix: "or"i _LEFTPAR (formula ( _SEP formula )*)? _RIGHTPAR
land      : formula "and"i (_SPACES formula | par)
lnot      : "not"i (_SPACES formula | par)
_SPACES   : /\s+/
        
?literal: nodeid 
        | kmer 
        | color
        | psdomap
        | meta
        | seq
        | all
        | partial
        | selection 
        | degree 
    
selection.1: "selection"i ((_LEFTPAR _RIGHTPAR) |)
partial.1  : "Partial"i ((_LEFTPAR _RIGHTPAR) |)
all.1      : "All"i ((_LEFTPAR _RIGHTPAR) |)
nodeid.1   : "NodeId"i _LEFTPAR  integer _RIGHTPAR
color.1    : "Color"i _LEFTPAR  ident  _RIGHTPAR
degree.1   : "Degree"i _LEFTPAR integer _RIGHTPAR
meta.0     : ident _LEFTPAR (arg ( _SEP  arg )* | ) _RIGHTPAR
?arg       : ident | attr

kmer.2     : "Kmer"i _LEFTPAR acgt  _RIGHTPAR
attr       : ident op (ident | integer)
seq.1      : "Seq"i _LEFTPAR acgt _RIGHTPAR
psdomap.1  : ("PseudoMapping"i | "PM"i ) _LEFTPAR acgt _RIGHTPAR
op         : EQUAL | LT | GT

EQUAL      : "="
LT         : "<"
GT         : ">"

acgt       : /[ACGT]+/i 
integer    : INT
ident      : /[a-zA-Z_][\w\.\-\_]*/i
    
%import common.CNAME
%import common.INT
%import common.WS 
%ignore WS
"""


class QueryEval(Transformer):
    def kmer(self, e):
        return Kmer(e[0])

    def degree(self, e):
        return Degree(e[0])

    def seq(self, e):
        return Seq(e[0])

    def all(self, *args):
        return All()

    def partial(self, *args):
        return Partial()

    def selection(self, *args):
        return Selection()

    def acgt(self, e):
        # return next(DNA.from_str(e[0]))
        return e[0]

    def psdomap(self, e):
        return PseudoMapping(e[0])

    def integer(self, e):
        return int(e[0])

    def ident(self, e):
        return str(e[0])

    def color(self, e):
        return Color(e[0])

    def attr(self, e):
        return Attr(key=e[0], op=e[1], value=e[2])

    def op(self, e):
        return str(e[0])

    def meta(self, args):
        type = args[0]
        name = None
        attrs = []
        for arg in args[1:]:
            if isinstance(arg, Attr):
                attrs.append(arg)
                continue
            assert name is None
            name = arg
        return Meta(type=type, name=name, attrs=attrs)

    def nodeid(self, e):
        return NodeId(e[0])

    def land(self, e):
        return And(list(filter(bool, e)))

    def lor(self, e):
        return Or(list(filter(bool, e)))

    lor_prefix = lor
    lor_infix = lor

    def lnot(self, e):
        k = next(filter(bool, e))
        return Not(k)


parser = Lark(Grammar, start="formula")


def parse(query: str) -> Term:
    try:
        tree = parser.parse(query)
    except larkexceptions.LarkError as E:
        raise ParseError(E)
    return QueryEval().transform(tree)
