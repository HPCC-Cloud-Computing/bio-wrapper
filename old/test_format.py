cm = "clustalw -infile={input_file[0]} -type=protein -matrix=pam -outfile=ksfslfk -outorder=input"\
    .format(input_file=['abcdef'], output_file='sdfjkas')

print(cm)