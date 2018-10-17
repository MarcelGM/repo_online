import sys
import os

text_file_name = sys.argv[1] #"kk.txt"
out_file_name = sys.argv[2] #"out_kk.txt"

text_file = open( text_file_name, 'r')
out = open( out_file_name, 'w')

for line in text_file:
    line_words = line.split("\n")[0].split(" ")
    for word in line_words:
        str_to_print = word + "\tO\tO\tO\n"
        out.write(str_to_print)
    out.write("\n")

out.close()
text_file.close()

#Delete last \n
with open(out_file_name, 'rb+') as filehandle:
    filehandle.seek(-1, os.SEEK_END)
    filehandle.truncate()
