Dataset is stored in the csv folder.

Run data preprocessing unit with command:

python3 data_preprocessing.py csv 0

where:
csv - represents the folder with dataset
0 - represent the number of the file

The program will output network.txt file, which is input to the AddressRank algorithm.

Run main algorithm with the command:

python3 main.py network.txt output.txt 0.9 0.0000001

where:
network.txt - path to the input data
output.txt - path to the output file for result being stored
0.9 - d - dump factor (float)
0.0000001 - epsilon - convergence parameter (float).


Program will report 2 lines:
amount of iterations needed for the program to converge, and sequence of addresses with their ranks sorted in descending order.

address_extractor.py is used to get addresses for nodes reported as top 10.
