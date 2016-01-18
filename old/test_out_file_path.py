import os
import shutil

# filename = "foo/bar/baz.txt"
filename = "a"
os.makedirs(filename, exist_ok=True)
# os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, "w") as f:
    f.write("FOOBAR")


# with open('b', 'w') as f:
#     f.write('dsfkjhaskfjas')

# shutil.rmtree('foo', True)