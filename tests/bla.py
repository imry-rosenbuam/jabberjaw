import sys
from julia import Main

Main.xs = [1, 2, 3]

Main.eval("sin.(xs)")

print(sys.version_info)