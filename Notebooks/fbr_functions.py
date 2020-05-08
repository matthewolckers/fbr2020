import numpy as np
import pandas as pd
import networkx as nx
import itertools

# Author: Matthew Olckers www.matthewolckers.com
# Date: 7 May 2020

def InformationMeasure(g, include_self_comparisons=True):
    '''
    Takes a social network graph, represented by edgeList, into
    a matrix of comparisons where element ij = 1 if some agent s
    is friends with both i and j or ij are friends, and zero otherwise.

    The information measure is the density of the resulting comparison
    network.

    g: networkx graph

    Return: Float between zero and one
    '''
    G = nx.to_numpy_matrix(g, dtype=int, weight=None)
    H = np.linalg.matrix_power(G, 2)
    if include_self_comparisons:
        H = G + H
    np.fill_diagonal(H, 0)
    H[H > 1] = 1
    n = nx.number_of_nodes(g)
    return H.sum()/(n*(n-1))



def removeUnsupportedEdges(g):
    '''
    On the social network graph g, remove any edge ij for which
    there does not exist a path (i,k,j) where k is the support
    or shared friend of the pair (i,j).

    Return: networkx graph
    '''
    G = nx.to_numpy_matrix(g, dtype=int, weight=None)
    G_2 = np.linalg.matrix_power(G, 2)
    G_2[G_2 > 1] = 1
    G_supp = np.multiply(G,G_2)
    return nx.from_numpy_matrix(G_supp)


def remove_within_group_edges(g, A):
    '''
    Take a graph g and a set of nodes A
    and remove edges within the group A
    and within the complement of A.

    Return: networkx graph
    '''
    bipartite = g.copy()
    x = nx.subgraph(g,nbunch=A)
    if len(x.edges())>0:
        bipartite.remove_edges_from(x.edges())
    B = g.nodes - A
    y = nx.subgraph(g,nbunch=B)
    if len(y.edges())>0:
        bipartite.remove_edges_from(y.edges())
    return bipartite

def max_bi_information(g):
    '''
    Greedy algorithm to determine the maximum strategy proof
    information on a network g. The network becomes strategy
    proof by partitioning the network into two groups and
    only allowing members of group A to rank members of group
    B and vice versa.

    Return: dict with maximum information (float between zero and one) and
            the list of nodes in the partition.
    '''
    nodes = list(g.nodes)
    max_info = 0
    max_info_nodes = list()
    for r in range(1,len(nodes)//2):
        splits = itertools.combinations(nodes, r)
        for s in splits:
            b = remove_within_group_edges(g, s)
            info = InformationMeasure(b, include_self_comparisons=False)
            if info > max_info:
                max_info = info
                max_info_nodes = list(s)
    return {'max_bi_info': max_info, 'max_bi_info_nodes':max_info_nodes}


def classifyComparisons(g):
    '''
    The social network, g, produces comparisons of different
    types that matter for incentive compatibilty. This
    method classifies comparisons into supported,
    transitive closure of supported, compared by three,
    and a residual.

    Return: Dictionary of edge classifications
    '''
    result = {}
    G = nx.to_numpy_matrix(g, dtype=int, weight=None)
    G_2 = np.linalg.matrix_power(G, 2)
    H = np.copy(G_2)
    H[H > 1] = 1
    np.fill_diagonal(H, 0)
    result["Total"] = np.sum(H)
    G_supp = np.multiply(G,H)
    result["Supported"] = np.sum(G_supp)
    G_supp_2 = np.linalg.matrix_power(G_supp, 2)
    G_supp_2[G_supp_2 > 1] = 1
    np.fill_diagonal(G_supp_2, 0)
    result["Transitive"] = np.sum(np.multiply(G_supp_2,1-G_supp))
    G_comp3 = np.copy(G_2)
    G_comp3[G_comp3 < 3] = 0
    G_comp3[G_comp3 >= 3] = 1
    np.fill_diagonal(G_comp3, 0)
    result["By three"] = np.sum(np.multiply(G_comp3,1-G_supp_2))
    return result


class NetStats:
    '''
    Version: 4 February 2020
    '''
    def __init__(self):
        self.ave_dist = []
        self.ave_clust = []
        self.num_edges = []
        self.ave_deg = []
        self.diameter = []
        self.density = []
        self.num_nodes = []

        self.info_total = []
        self.info_total_friend_only = []
        self.info_expostIC = []
        self.info_SP = []

        self.comp_total = []
        self.comp_supp = []
        self.comp_trans = []
        self.comp_by_three = []

        self.links_supported = []

        self.networks = {}
        self.key_list = []


    def extract(self, key, g, giant=True):
        '''
        Extract network statistics from a social network, g.
        '''
        if giant:
            g = g.subgraph(max(nx.connected_components(g), key=len)).copy()

        self.num_nodes.append(nx.number_of_nodes(g))

        self.key_list.append(key)

        n = nx.number_of_nodes(g)

        # Social network
        # Extract basic network stats
        self.num_edges.append(nx.number_of_edges(g))
        self.ave_deg.append(2*nx.number_of_edges(g)/n)
        self.density.append(nx.density(g))
        self.ave_clust.append(nx.average_clustering(g))

        # Calculate network stats that require G is connected.
        if nx.is_connected(g):
            self.ave_dist.append(nx.average_shortest_path_length(g))
            self.diameter.append(nx.diameter(g))
        else:
            self.ave_dist.append(np.nan)
            self.diameter.append(np.nan)

        # Network with only supported edges (ex-post IC)
        g_supp = removeUnsupportedEdges(g)

        self.links_supported.append(nx.number_of_edges(g_supp)/nx.number_of_edges(g))

        # Bipartite network to maximize strategyproof information
        # Just records the nodes

        if (n <= 20) & giant:
            g_bi = max_bi_information(g)
        else:
            g_bi = {'max_bi_info':np.nan , 'max_bi_info_nodes':{} }

        # Information measures
        self.info_total.append(InformationMeasure(g))
        self.info_total_friend_only.append(InformationMeasure(g, include_self_comparisons=False))
        self.info_expostIC.append(InformationMeasure(g_supp, include_self_comparisons=False))
        self.info_SP.append(g_bi['max_bi_info'])

        # Classify comparisons
        comp = classifyComparisons(g)
        self.comp_total.append(comp["Total"]/(n*(n-1)))
        self.comp_supp.append(comp["Supported"]/(n*(n-1)))
        self.comp_trans.append(comp["Transitive"]/(n*(n-1)))
        self.comp_by_three.append(comp["By three"]/(n*(n-1)))


        # Save the network in a dictionary so we can plot it later
        self.networks[str(key)] = {'g':g, 'g_supp': g_supp, 'g_bi': g_bi}

        print("Loading network #" + str(key), end="\r") # Counter to see progress on network extraction

    def collect(self, dict_of_networks, extract_from_giant=True):
        '''
        Collect the network statistics into a pandas dataframe.
        '''
        for key, network in dict_of_networks.items():
            self.extract(key, network, giant=extract_from_giant)

        network_data = list(zip(self.ave_dist, self.ave_clust, self.num_edges, self.ave_deg,
                                self.diameter,self.density, self.num_nodes,
                                self.info_total, self.info_total_friend_only, self.info_expostIC, self.info_SP,
                                self.links_supported,
                                self.comp_total,self.comp_supp,self.comp_trans,self.comp_by_three,
                                self.key_list))

        result = pd.DataFrame(data = network_data, columns=['ave_dist', 'ave_clust', 'num_edges', 'ave_deg',
                                                            'diameter','density','num_nodes',
                                                            'info_total','info_total_friend_only','info_expostIC','info_SP',
                                                            'links_supported',
                                                            'comp_total','comp_supp','comp_trans','comp_by_three',
                                                            'key'])

        return(result)
