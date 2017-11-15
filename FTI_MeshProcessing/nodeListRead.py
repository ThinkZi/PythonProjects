#This code the reads the node coordinates in old nastran format
#and generates a dictionary called node.
#Node is a dictionary with the key being the integer node id
#and the value being a list of float coordinates {nodeID:[x,y,z]}
def GetNodeCoordinates(content):
    nodalCoordinateFileName='node_coordinates.dat'
    node={}
    node_ext={}
    for line in content.splitlines():
        l=line.split()
        if len(l) == 0: continue
        # node id

        if l[0].startswith("GRID*"):
            nid=int(l[1])
            node[nid]=[float(l[2]),float(l[3])]
            node_ext[l[-1]]=nid

        elif l[0].startswith("*"):

                if len(l) == 0: continue
                connector=l[0].replace("*","")
                if connector in node_ext.keys():
                    node_number=node_ext[connector]
                    node[node_number].append(float(l[1]))
        else:
            pass

    return node
