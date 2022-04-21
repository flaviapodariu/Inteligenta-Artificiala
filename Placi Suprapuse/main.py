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
    NSOL = int(sys.argv[3])
    TIMEOUT = int(sys.argv[4])


lista_inputuri = os.listdir(input_folder)

for input_file in lista_inputuri:
    fout = open(output_folder + "/out_" + input_file, "w")
    g = Graph(input_folder + "/" + input_file)

    fout.write("Breadth First \n\n")
    g.breadth_first(time.time(), fout, NSOL, timeout=TIMEOUT)

    fout.write("Depth First \n\n")
    g.depth_first(time.time(), fout, NSOL, timeout=TIMEOUT)

    fout.write("A* -> euristica banala \n\n")
    g.a_star(time.time(), fout, "banala", NSOL, timeout=TIMEOUT)

    fout.write("A* -> euristica admisibila 1\n\n")
    g.a_star(time.time(), fout, "admisibila1", NSOL, timeout=TIMEOUT)

    fout.write("A* -> euristica neadmisibila\n\n")
    g.a_star(time.time(), fout, "neadmisibila", NSOL, timeout=TIMEOUT)

    fout.write("A* optimizat -> euristica banala\n\n")
    g.a_star_optimizat(time.time(), fout, "banala", timeout=TIMEOUT)

    fout.write("A* optimizat -> euristica admisibila 1\n\n")
    g.a_star_optimizat(time.time(), fout, "admisibila1", timeout=TIMEOUT)

    fout.write("A* optimizat -> euristica neadmisibila\n\n")
    g.a_star_optimizat(time.time(), fout, "neadmisibila", timeout=TIMEOUT)

    fout.write("DFI \n\n")
    g.depth_first_iterativ(time.time(), fout, NSOL, timeout=TIMEOUT)

    fout.write("IDA* -> euristica banala \n\n")
    g.ida_star(time.time(), fout, "banala", NSOL, timeout=TIMEOUT)

    fout.write("IDA* -> euristica admisibila 1\n\n")
    g.ida_star(time.time(), fout, "admisibila1", NSOL, timeout=TIMEOUT)

    fout.write("IDA* -> euristica admisibila 2\n\n")
    g.ida_star(time.time(), fout, "admisibila2", NSOL, timeout=TIMEOUT)

