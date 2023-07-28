from qiskit import Aer, QuantumCircuit, transpile, assemble
from qiskit import execute, ClassicalRegister, QuantumRegister
import numpy as np
'''This code is a demonstration of Goemans-Williamson Max-Cut Algorithm using Quantum Approximation Optimization algorithm.
This is one of the Generative Enchaned Optimization(GEO) algorithms which the application of Quantum Computing'''

# creating a graph
def create_max_cut_graph():
    # The graph with four nodes and the following edges: (0, 1), (0, 2), (1, 3), (2, 3).
    num_nodes = 4
    edges = [(0, 1), (0, 2), (1, 3), (2, 3)]
    graph = {
        'num_nodes': num_nodes,
        'edges': edges
    }
    return graph

# QAOA circuit 
def build_qaoa_circuit(graph, p):
    num_nodes = graph['num_nodes']
    edges = graph['edges']

    q = QuantumRegister(num_nodes, name='q')
    c = ClassicalRegister(num_nodes, name='c')
    qc = QuantumCircuit(q, c)

    qc.h(q)
    for _ in range(p):
        for edge in edges:
            qc.cx(q[edge[0]], q[edge[1]])
            qc.rz(np.pi, q[edge[1]])  
            qc.rz(np.pi, q[edge[0]])  
    qc.measure(q, c)
    
    return qc

if __name__ == "__main__":
    p = 1
    max_cut_graph = create_max_cut_graph()
    qaoa_circuit = build_qaoa_circuit(max_cut_graph, p)

    # Running QAOA circuit 
    backend = Aer.get_backend('qasm_simulator')
    shots = 1000
    qaoa_job = execute(qaoa_circuit, backend=backend, shots=shots)
    result = qaoa_job.result().get_counts(qaoa_circuit)
 
    # finding optimal solution
    max_cut_value = 0
    optimal_cut = ''
    for cut in result:
        if result[cut] > max_cut_value:
            max_cut_value = result[cut]
            optimal_cut = cut

    print(f"Optimal cut: {optimal_cut}, Max-Cut value: {max_cut_value / shots}")