import sys
import os
import time
from graph import Graph


# informatii despre un nod din arborele de parcurgere (nu din graful initial)


# input, output, NSOL, timeout
# if len(sys.argv) != 5:
#     print("Numar de argumente gresit!")
#     sys.exit(0)
# else:
#     input_folder = os.getcwd() + sys.argv[1]
#     output_folder = os.getcwd() + sys.argv[2]
#     NSOL = sys.argv[3]
#     timeout = sys.argv[4]


# lista_inputuri = os.listdir(input_folder)
#
# for input_file in lista_inputuri:
#     # print(input_file)
#     g = Graph(input_folder + "/" + input_file)

g = Graph("inputs/no_ans.txt")
print(g.start)
l = g.start.genereaza_succesori()
for nod in l:
    print(nod)
# g.depth_first()
# g.bf()
# g.dfi()
