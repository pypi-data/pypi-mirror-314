# -*- coding: utf-8 -*-
# even: stable; odd: develop


#!/usr/bin/env python

# wrapper for mysql.

import networkx as nx
import numpy as np
import logging
import hashlib


def encode_graph(g):
    return ",".join([line for line in nx.generate_edgelist(g, data=False)])


def decode_graph(s):
    return nx.parse_edgelist(s.split(","))


def matrix_sort(m):
    newm = []
    for row in m:
        n = 0
        for x in np.sort(row):  # sorted copy
            n = n * 10 + int(x)
        newm.append(n)
    return " ".join([str(x) for x in sorted(newm)])


def sorteddm(g):
    logger = logging.getLogger()
    result = hashlib.md5(
        matrix_sort(np.array(nx.floyd_warshall_numpy(g))).encode("utf-8")
    ).hexdigest()
    logger.debug(result)
    return result


# local, volatile set of graphs.
class GraphStat:
    def __init__(self):
        # lookup table
        self.graphhashes = dict()
        # storage
        self.graphs = []

    def query_id(self, a):
        assert nx.is_connected(a)
        self.lastgraph = a
        self.lasthash = sorteddm(a)
        if self.lasthash in self.graphhashes:
            for g_id in self.graphhashes[self.lasthash]:
                # 既存の構造の場合、isomorphismが必要になり30%処理が余分にかかる。
                # 実際にはこれまでconflictは一度も起きていないので、
                # 確認する必要はないかもしれないが、30%のコストで
                # 安全になるなら当面はこのままでいこう。
                if nx.is_isomorphic(self.graphs[g_id], a):
                    self.lastid = g_id
                    return g_id
        self.lastid = -1
        return -1

    def register(self):  # register the last queried graph.
        assert self.lastid == -1
        new_id = len(self.graphs)
        if self.lasthash in self.graphhashes:
            logging.getLogger().info("Collision")
            # sys.exit(0)
        else:
            self.graphhashes[self.lasthash] = []
        self.graphhashes[self.lasthash].append(new_id)
        self.graphs.append(self.lastgraph)
        return new_id

    def get(self, id):
        if len(self.graphs) <= id:
            return None
        return self.graphs[id]


def unittest(gdb):
    print("unit test.")
    g = nx.path_graph(5)
    print(encode_graph(decode_graph(encode_graph(g))))
    id = gdb.query_id(g)
    print(id)
    if id < 0:
        id = gdb.register()
        print(id)
    id = gdb.query_id(g)
    print(id)
    g = nx.path_graph(4)
    id = gdb.query_id(g)
    print(id)
    if id < 0:
        id = gdb.register()
        print(id)


if __name__ == "__main__":
    gdb = GraphStat()
    unittest(gdb)
