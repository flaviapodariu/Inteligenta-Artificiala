import sys
import os
import time
from graph import Graph

# input, output, NSOL, timeout
if len(sys.argv) != 5:
    print("Numar de argumente gresit!")
    sys.exit(0)
else:
    input_folder = os.getcwd() + sys.argv[1]
    output_folder = os.getcwd() + sys.argv[2]
    NSOL = sys.argv[3]
    TIMEOUT = sys.argv[4]


lista_inputuri = os.listdir(input_folder)

for input_file in lista_inputuri:
    # print(input_file)
    # g = Graph(input_folder + "/" + input_file)
    g = Graph(os.path.join(input_folder, input_file))
    fout = open(os.path.join(output_folder, "out_" + input_file), "w")

    fout.write("Breadth First \n\n")
    g.breadth_first(time.time(), fout, 1, timeout=TIMEOUT)

    fout.write("Depth First \n\n")
    g.depth_first(time.time(), fout, 1, timeout=TIMEOUT)

    fout.write("A* -> euristica banala \n\n")
    g.a_star(time.time(), fout, "banala", timeout=TIMEOUT)

    fout.write("A* -> euristica admisibila 1\n\n")
    g.a_star(time.time(), fout, "admisibila1", timeout=TIMEOUT)

    fout.write("A* -> euristica neadmisibila\n\n")
    g.a_star(time.time(), fout, "neadmisibila", timeout=TIMEOUT)

    fout.write("A* optimizat -> euristica banala\n\n")
    g.a_star_optimizat(time.time(), fout, "banala", timeout=TIMEOUT)

    fout.write("A* optimizat -> euristica admisibila 1\n\n")
    g.a_star_optimizat(time.time(), fout, "admisibila1", timeout=TIMEOUT)

    fout.write("A* optimizat -> euristica neadmisibila\n\n")
    g.a_star_optimizat(time.time(), fout, "neadmisibila", timeout=TIMEOUT)

    fout.write("DFI \n\n")
    g.depth_first_iterativ(time.time(), fout, timeout=TIMEOUT)


g = Graph("inputs/no_ans.txt")
# l = g.start.genereaza_succesori()
# for nod in l:
#     print(nod)



# g.a_star("admisibila1", 1)
