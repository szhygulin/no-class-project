import sys
import copy

def input(file):
    # reads file and provide input data in corresponding datastructures
    labels = []
    adj_matrix = []
    for x in file.readlines():
        line = x.split('\t')
        label = line[0]
        row = line[1]
        row = row.split(',')
        matrix_row = []
        for y in row:
            if int(y) >= 0:
                matrix_row.append(int(y))
            else:
                raise ValueError("weight values cannot be less than 0")
        labels.append(label)
        adj_matrix.append(matrix_row)
    return labels, adj_matrix

# L1 distance for computing stopping condition
def l1Distance(a, b):
    result = 0
    for i in range(len(a)):
        result += abs(b[i] - a[i])
    return result

def pageRank(A, nodes, d, epsilon):
    n = len(nodes)
    iterations = 0
    # compute outbound links for every page
    outbound_links = []
    for x in A:
        links = 0
        for y in x:
            links += y
        outbound_links.append(links)
    # initialize page ranks
    page_rank = [1/n] * n
    # initialize previous step page ranks for calculations of the next step
    prev_page_rank = [0] * n
    while l1Distance(page_rank, prev_page_rank) >= epsilon:
        iterations += 1
        # shallow copy will lead to having always prev_page_rank == page_rank
        prev_page_rank = copy.deepcopy(page_rank)
        # calculate next step page ranks
        for i in range(n):
            sum_factor = 0.0
            for j in range(n):
                # counting only pages that have link to i, otherwise A[j][i] = 0
                sum_factor += A[j][i] * prev_page_rank[j] / outbound_links[j]
            page_rank[i] = (1 - d) / n + d * sum_factor
        print(f'iteration {iterations} has L1 distance {l1Distance(page_rank, prev_page_rank)}')
    return iterations, page_rank

def output(file_name, iterations, nodes):
    with open(file_name, 'w') as f:
        f.write(f'number of iterations: {iterations}\n')
        f.write('rankings: ')
        for n, x in enumerate(nodes):
            if n < len(nodes) - 1:
                f.write(f'{x["label"]} ({x["page_rank"]}), ')
            else:
                f.write(f'{x["label"]} ({x["page_rank"]}).\n')

if __name__ == '__main__':
    try:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        d = float(sys.argv[3])
        epsilon = float(sys.argv[4])
    except:
        raise ValueError('Not enough input parameters or incorrect type')
    try:
        with open(input_file, 'r') as f:
            labels, adj_matrix = input(f)
    except:
        raise ValueError('Input file has not correct format or is not a file')
    # check d and epsilon ranges
    if not (0 < epsilon < 1):
        raise ValueError("Epsilon out of ranges")
    if not (0 < d < 1):
        raise ValueError("d out of ranges")
    # keep track of vertices' indexes in adjacency matrix
    nodes = []
    for x in labels:
        node = {'label': x, 'row_index': labels.index(x)}
        nodes.append(node)
    iterations, page_rank = pageRank(adj_matrix, nodes, d, epsilon)
    # assign nodes corresponding page rank and sort them based on derived value
    for x in nodes:
        x['page_rank'] = page_rank[x['row_index']]
    nodes = sorted(nodes, key=lambda k: k['page_rank'], reverse=True)
    output(output_file, iterations, nodes)