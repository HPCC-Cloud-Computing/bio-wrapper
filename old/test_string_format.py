a = "sdfljkas%(output_file)sasdfhakj" % {'output_file':' ', 'djaf':'sdfku'}
print(a)
print('%(output_file)s' in a)
if '%(output_file)s' in a:

    print(True)
