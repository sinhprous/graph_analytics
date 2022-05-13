"""
Copyright 2020 Twitter, Inc.
SPDX-License-Identifier: Apache-2.0
"""
import torch
from torch import Tensor
from torch_geometric.typing import Adj, OptTensor

from utils import get_symmetrically_normalized_adjacency


class FeaturePropagation(torch.nn.Module):
    def __init__(self, num_iterations: int):
        super(FeaturePropagation, self).__init__()
        self.num_iterations = num_iterations

    def propagate(self, x: Tensor, edge_index: Adj, mask: Tensor, edge_weight: OptTensor = None) -> Tensor:
        # out is inizialized to 0 for missing values. However, its initialization does not matter for the final
        # value at convergence
        out = x
        if mask is not None:
            out = torch.zeros_like(x)
            out[mask] = x[mask]

        n_nodes = x.shape[0]
        adj = self.get_propagation_matrix(out, edge_index, edge_weight, n_nodes)
        for _ in range(self.num_iterations):
            # Diffuse current features
            out = torch.sparse.mm(adj, out)
            # Reset original known features
            out[mask] = x[mask]

        return out

    def get_propagation_matrix(self, x, edge_index, edge_weight, n_nodes):
        # Initialize all edge weights to ones if the graph is unweighted)
        edge_weight = edge_weight if edge_weight else torch.ones(edge_index.shape[1]).to(edge_index.device)
        edge_index, edge_weight = get_symmetrically_normalized_adjacency(edge_index, n_nodes=n_nodes)
        # import pdb; pdb.set_trace()
        adj = torch.sparse.FloatTensor(edge_index, values=edge_weight).to(edge_index.device)

        return adj
