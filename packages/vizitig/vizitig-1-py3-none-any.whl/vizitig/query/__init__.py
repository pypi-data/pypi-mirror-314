from functools import singledispatch

import networkdisk as nd

from vizitig.errors import InvalidKmerSize, MetaNotFound, NoIndex, QueryError
from vizitig.index import load_kmer_index
from vizitig.info import are_kmer_ingested, get_graph
from vizitig.query import query
from vizitig.query.query import Term, parse
from vizitig.types import DNA, Kmer


def search_kmer(graph_name, kmer) -> nd.sql.helper.IterableQuery:
    G = get_graph(graph_name)
    try:
        kmer_index = load_kmer_index(graph_name)
        nid = kmer_index.get(kmer)
        if nid is not None:
            return constant_to_iterable_query(G, nid)
        return empty_iterable_query(G)

    except NoIndex:
        if not are_kmer_ingested(graph_name):
            return G.find_all_nodes(sequence=lambda e: e.like(f"%{kmer}%"))
    return G.find_all_nodes(kmer)


def constant_to_iterable_query(
    G: nd.sqlite.DiGraph,
    nid: int,
) -> nd.sql.helper.IterableQuery:
    col = G.dialect.columns.ValueColumn(nid)
    query = G.dialect.queries.SelectQuery(columns=(col,))
    return G.dialect.helper.IterableQuery(G.helper, query).map(lambda e: e[0])


def empty_iterable_query(G: nd.sqlite.DiGraph) -> nd.sql.helper.IterableQuery:
    col = G.dialect.constants.Null
    cond = G.dialect.conditions.FalseCondition()
    query = G.dialect.queries.SelectQuery(columns=(col,), condition=cond)
    return G.dialect.helper.IterableQuery(G.helper, query).map(lambda e: e[0])


@singledispatch
def _search(T: Term, gname: str) -> nd.sql.helper.IterableQuery:
    raise NotImplementedError(T)


@_search.register(query.Meta)
def _(T, gname):
    G = get_graph(gname)
    if T.attrs:
        raise NotImplementedError
    try:
        if T.name is None:
            it = iter(G.metadata.vars_values[T.type].values())
            try:
                iq = G.find_all_nodes(next(it))
            except StopIteration:
                raise MetaNotFound(T.t)
            for meta in it:
                iq = iq.union(G.find_all_nodes(meta))
            return iq
        meta = G.metadata.vars_values[T.type][T.name]
    except KeyError:
        raise MetaNotFound(T)
    return G.find_all_nodes(meta)


@_search.register(query.Color)
def _(T, gname):
    G = get_graph(gname)
    try:
        color = G.metadata.vars_values["Color"][T.t]
    except KeyError:
        raise MetaNotFound(T.t)
    return G.find_all_nodes(color)


@_search.register(query.All)
def _(T, gname):
    G = get_graph(gname)
    return G.find_all_nodes()


@_search.register(query.Partial)
def _(T, gname):
    raise QueryError("Partial is only for Client-side")


@_search.register(query.Degree)
def _(T, gname):
    raise QueryError("Degree is only for Client-side")


@_search.register(query.Selection)
def _(T, gname):
    raise QueryError("Selection is only for Client-side")


@_search.register(query.Kmer)
def _(T, gname):
    G = get_graph(gname)
    if len(T.t) != G.metadata.k:
        raise InvalidKmerSize(f"{T.size} expected {G.metadata.k}")

    kmer = Kmer.from_dna(DNA(T.kmer)).canonical()
    return search_kmer(gname, kmer)


@_search.register(query.Seq)
def _(T, gname):
    G = get_graph(gname)
    if len(T.seq) < G.metadata.k:
        return G.find_all_nodes(sequence=lambda e: e.like(f"%{T.seq}%"))
    it = next(iter(DNA.from_str(T.seq))).enum_canonical_kmer(G.metadata.k)
    iq = search_kmer(gname, next(it))
    for kmer in it:
        iq = iq.union(search_kmer(gname, kmer))
    return iq


@_search.register(query.NodeId)
def _(T, gname):
    G = get_graph(gname)
    return G.nbunch_iter((T.t,))


@_search.register(query.And)
def _(T, gname):
    iqs = list(map(lambda t: _search(t, gname), T.t))
    return iqs[0].intersection(*iqs[1:])


@_search.register(query.Or)
def _(T, gname):
    iqs = list(map(lambda t: _search(t, gname), T.t))
    if iqs:
        return iqs[0].union(*iqs[1:])
    G = get_graph(gname)
    return empty_iterable_query(G)


@_search.register(query.Not)
def _(T, gname):
    G = get_graph(gname)
    return G.find_all_nodes().difference(_search(T.t, gname))


def search(name: str, q: str, limit=1000) -> list[int]:
    term = parse(q)
    iq = _search(term, name)
    if isinstance(
        iq.query,
        nd.sqlite.queries.SelectQuery,
    ):  # ugly because of nd limit broken on iq with union/intersection
        return list(iq.limit(limit))
    return [x for _, x in zip(range(limit), iq)]
