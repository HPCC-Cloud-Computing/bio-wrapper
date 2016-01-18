cm = "clustalw -infile={input_file[0]} -type=protein -matrix=pam -outfile={output_file} -outorder=input"\
    .format(input_file=['abcdef'], output_file='sdfjkas')

print(cm)