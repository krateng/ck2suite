def deepadd(dictionary,nodes,value):
	*nodes,lastnode = nodes

	res = dictionary
	for n in nodes:
		res = res.setdefault(n,{})

	res.setdefault(lastnode,[])

	res[lastnode] = list(set(res[lastnode] + [value]))
