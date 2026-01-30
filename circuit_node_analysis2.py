import numpy as np
import matplotlib.pyplot as plt

class CircuitModel:
    def __init__(self, nodes, resistors, current_sources):
        self.nodes = nodes
        self.resistors = resistors
        self.current_sources = current_sources

def build_y_matrix(circuit):
    N = circuit.nodes - 1
    Y = np.zeros((N, N))
    I = np.zeros(N)
    for n1, n2, R in circuit.resistors:
        g = 1 / R
        if n1 != 0: Y[n1-1, n1-1] += g
        if n2 != 0: Y[n2-1, n2-1] += g
        if n1 != 0 and n2 != 0:
            Y[n1-1, n2-1] -= g
            Y[n2-1, n1-1] -= g
    for n, I_val in circuit.current_sources:
        if n != 0: I[n-1] += I_val
    return Y, I

def solve_circuit(circuit):
    Y, I = build_y_matrix(circuit)
    V = np.linalg.solve(Y, I)
    return V

def calculate_branch_currents(circuit, V):
    branch_currents = []
    for n1, n2, R in circuit.resistors:
        v1 = 0 if n1 == 0 else V[n1-1]
        v2 = 0 if n2 == 0 else V[n2-1]
        I_branch = (v1 - v2)/R
        branch_currents.append(((n1, n2), I_branch))
    return branch_currents

def validate_kcl(circuit, V):
    kcl_results = []
    for i in range(len(V)):
        current_sum = 0
        for n1, n2, R in circuit.resistors:
            if n1 == i+1: v2 = 0 if n2 == 0 else V[n2-1]; current_sum += (V[i]-v2)/R
            if n2 == i+1: v1 = 0 if n1 == 0 else V[n1-1]; current_sum += (V[i]-v1)/R
        for n, I_val in circuit.current_sources:
            if n == i+1: current_sum -= I_val
        kcl_results.append(current_sum)
    return kcl_results

# -------- نمونه مدارهای تست --------
example_circuits = [
    {
        'name': 'مدار 1: دو گره + منبع جریان',
        'resistors': [(1,0,10),(1,2,5),(2,0,20)],
        'current_sources': [(1,2)],
        'nodes': 3
    },
    {
        'name': 'مدار 2: یک گره متصل به گره دیگر + منبع جریان',
        'resistors': [(1,0,15),(1,2,10)],
        'current_sources': [(1,1.5)],
        'nodes': 3
    },
    {
        'name': 'مدار 3: بدون منبع ولتاژ, فقط مقاومت و منبع جریان',
        'resistors': [(1,0,8),(1,2,12),(2,0,6)],
        'current_sources': [(1,2)],
        'nodes': 3
    }
]

for ex in example_circuits:
    print(f"\n================= {ex['name']} =================")
    circuit = CircuitModel(nodes=ex['nodes'], resistors=ex['resistors'], current_sources=ex['current_sources'])
    V = solve_circuit(circuit)
    print("ولتاژ گره‌ها:")
    for i,v in enumerate(V,1): print(f"V{i} = {v:.4f} ولت")
    branch_currents = calculate_branch_currents(circuit,V)
    print("\nجریان شاخه‌ها:")
    for idx,((n1,n2),I_branch) in enumerate(branch_currents,1): print(f"I_R{idx} ({n1}->{n2}) = {I_branch:.4f} آمپر")
    kcl_results = validate_kcl(circuit,V)
    print("\nKCL برای هر گره:")
    for i,val in enumerate(kcl_results,1): print(f"گره {i}: جمع جریان = {val:.6f} آمپر")
    # نمودار جمع جریان‌ها
    I_in = ex['current_sources'][0][1]
    plt.figure(figsize=(6,4))
    plt.bar([f"گره {i+1}" for i in range(len(kcl_results))], kcl_results, color='skyblue')
    plt.axhline(0,color='r',linestyle='--',label='I_in')
    plt.ylabel('جمع جریان ها (A)')
    plt.title(f'جمع جریان‌ها در هر گره ({ex["name"]})')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()
