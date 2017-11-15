#This code reads the element connectivity information together with the nodal values
#It stores the elements in a dictionary called element together with the element type,
#numbder of nodes and the list of node ids of each element
#the key of the dictionary is the element id
# element[eid]=[etype,numberOfNodesInElement, nodes]
#thickness is a dictionary with the node id as its key and the list of nodal thicknesses as its value
#thickness[eid]=[t1,t2,t3] (4 vlaues in the list for Q)

def GetElementData(content):

    element_ext={}
    element={}
    thickness={}
    numbderLength=8
    elementTypes=['CQUAD4','CTRIA3']

    def GetNodeIDandConnector(str):
        connector=str[-numbderLength:]
        split_lastItemInLine=str.split('.')
        lastNodeID=int(split_lastItemInLine[0][:-1])
        return lastNodeID, connector

    def GetNodalValues(str):
        parts = [str[i:i+numbderLength] for i in range(0, len(str), numbderLength)]
        f_parts = [float(i) for i in parts]
        return f_parts


    for line in content.splitlines():

        l=line.split()
        if len(l) == 0 : continue
        if l[0] in elementTypes:
            etype=l[0]
            eid=int(l[1])
            numberOfNodesInElement=int(l[2])
            lastItemInLine=l[-1]
            lastNodeID, connector = GetNodeIDandConnector(lastItemInLine)
            element_ext[connector]=eid
            nodes=[]

            for i in range(numberOfNodesInElement-1):
                nodes.append(int(l[3+i]))
            nodes.append(lastNodeID)
            element[eid]=[etype,numberOfNodesInElement, nodes]
            # emty thr list
            #nodes[:]=[]

        elif l[0] in element_ext.keys():
            eid=element_ext[l[0]]
            numberOfNodesInElement=element[eid][1]
            thickness[eid]=GetNodalValues(l[-1][1:])
        else:
            pass

    return element, thickness



#print(element)
#print(thickness)
