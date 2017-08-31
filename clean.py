import sys, os, re

def chunks(l, n):
	n = max(1, n)
	return (l[i:i+n] for i in range(0, len(l), n))

def clean(target, destination, regex):
	with open(target, "r") as f:
		target = f.read()
	with open(regex, "r") as f:
		rxs = list(chunks(f.read().split("\n"), 2))
	for pair in rxs:
		print(".......")
		pattern = re.compile(pair[0], re.M)
		target = re.sub(pattern, pair[1], target)
		print(pair)
	with open(destination, "w") as f:
		f.write(target)


if __name__ == "__main__":
	clean(sys.argv[1], sys.argv[2], sys.argv[3])