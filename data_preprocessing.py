# This is a data preprocessing script. It transforms raw transaction data to adjacency matrix.

import sys
from io import StringIO
import csv

class AddressesNetwork():
    '''
    stores addresses' indexes and weighted adjacency matrix
    '''

    def __init__(self):
        self.addresses = {}                 # index of the address
        self.A = []                         # adjacency matrix
        self.n = 0                          # amount of known addresses

    def add_address(self, address):
        '''
        adds new address to the network
        :param address: address to be added
        :return: null
        '''
        self.addresses[address] = self.n
        self.n += 1
        for (n, x) in enumerate(self.A):
            self.A[n].append(0)
        self.A.append([0] * self.n)

    def add_weight(self, _from, _to, value):
        '''
        adds up to edge weight corresponding to transaction's value
        :param _from: address who sends transaction
        :param _to: transaction recipient
        :param value: value of the transaction
        :return: null
        '''
        self.A[self.addresses[_from]][self.addresses[_to]] += value

    def normalize_matrix(self):
        """
        Normilizes matrix's rows to 1
        :return: null
        """
        for (n, x) in enumerate(self.A):
            weight_sum = sum(x);
            for i in range(len(x)):
                self.A[n][i] = float(self.A[n][i]) / weight_sum

    def dump_to_file(self, file):
        '''
        stores network in the format required by pagerank algorithm
        :param file: file object
        :return: null
        '''
        print(f"Amount of unique addresses is {self.n}")
        for n in range(self.n):
            file.write(f"{n}\t")
            file.write(','.join(map(str, self.A[n])))
            file.write('\n')



if __name__ == '__main__':
    try:
        input_folder = sys.argv[1]
        i = int(sys.argv[2])
    except:
        raise ValueError('Not enough input parameters')
    network = AddressesNetwork()
    # Numeration of files in folders must be consecutive
    with open(f"{input_folder}/{i}.csv", 'r') as f:
        x = f.read()
        y = StringIO(x)
        reader = csv.reader(y, delimiter=',')
        # omitting first row
        fields = next(reader)
        for (m, row) in enumerate(reader):
            _from = row[fields.index("from")]
            _to = row[fields.index("to")]
            value = row[fields.index("value")]
            # check if "from" or "to" address appears first time
            if _from not in network.addresses:
                network.add_address(_from)
            if _to not in network.addresses:
                network.add_address(_to)
            network.add_weight(_from, _to, int(value))
            if m % 100000 == 0:
                print(f"file {i}, {m} rows processed")
    with open("network.txt", "w") as f:
        network.dump_to_file(f)


