import os
from pprint import pprint


if __name__ == "__main__":
    results = {}
    with open("datanode_1/logs/time.txt") as f:
        results["datanode_1"] = float(f.read().strip("\n"))
    with open("datanode_1/logs/time_opt.txt") as f:
        results["datanode_1_opt"] = float(f.read().strip("\n"))
    with open("datanode_3/logs/time.txt") as f:
        results["datanode_3"] = float(f.read().strip("\n"))
    with open("datanode_3/logs/time_opt.txt") as f:
        results["datanode_3_opt"] = float(f.read().strip("\n"))

    pprint(results)
    print()
    os.remove("datanode_1/logs/time.txt")
    os.remove("datanode_1/logs/time_opt.txt")
    os.remove("datanode_3/logs/time.txt")
    os.remove("datanode_3/logs/time_opt.txt")

    