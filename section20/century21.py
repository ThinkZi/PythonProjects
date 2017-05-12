
# coding: utf-8

# In[45]:

import requests
from bs4 import BeautifulSoup
r=requests.get("http://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/")
c=r.content
soup=BeautifulSoup(c,"html.parser")
all=soup.find_all("div",{"class":"propertyRow"})
#Get the number of pages 
page_nr=soup.find_all("a",{"class":"Page"})[-1].text
print(page_nr)

l=[]
base_url="http://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
for page in range(0,int(page_nr)*10,10):
    print(base_url+str(page)+".html")
    r=requests.get(base_url+str(page)+".html")
    c=r.content
    soup=BeautifulSoup(c,"html.parser")
    all=soup.find_all("div",{"class":"propertyRow"})
    for item in all:
        d={}
        d["price"]=item.find("h4",{"class","propPrice"}).text.replace("\n","").replace(" ","")
        d["streetAddress"]=item.find_all("span",{"class":"propAddressCollapse"})[0].text
        d["city"]=item.find_all("span",{"class":"propAddressCollapse"})[1].text

        try:
            d["NumberOfBeds"]=item.find("span",{"class","infoBed"}).find("b").text
        except:
            d["NumberOfBeds"]=None

        try:
            d["SquareFeet"]=item.find("span",{"class","infoSqFt"}).find("b").text
        except:
            d["SquareFeet"]=None

        try:
            d["NumberOfFullBaths"]=item.find("span",{"class","infoValueFullBath"}).find("b").text
        except:
            d["[NumberOfFullBaths"]=None 

        try:
            d["NumberOfHalfBaths"]=item.find("span",{"class","infoValueHalfBath"}).find("b").text
        except:
            d["NumberOfHalfBaths"]=None

        for column_group in item.find_all("div",{"class":"columnGroup"}):
            for feature_group, feature_name in zip(item.find_all(column_group.find_all("span", {"class":"featureGroup"})), item.find_all("span",{"class":"featureName"})):
                if "Lot Size" in feature_group.text:
                    d["LotSize"]=feature_name.text
                else: 
                    LotSize=None
        l.append(d)


import pandas
df=pandas.DataFrame(l)
df.to_csv("Output.csv")


# In[44]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



