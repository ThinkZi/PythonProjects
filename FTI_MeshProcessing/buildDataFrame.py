def GetDataFrame(nodes_dict,element_dict,output_dict):
    import pandas as pd
    nodal_value={}
    extended_nodal_value={}

    for eid_temp in element_dict.keys():
        for i in range(len(element_dict[eid_temp][-1])):
            tempNID=element_dict[eid_temp][-1][i]
            nodal_value[tempNID]=output_dict[eid_temp][i]
            extended_nodal_value[tempNID]=[nodes_dict[tempNID][0],nodes_dict[tempNID][1],nodes_dict[tempNID][2],nodal_value[tempNID]]

    df=pd.DataFrame(extended_nodal_value).transpose()
    df.columns=['x','y','z','result']

    return df
