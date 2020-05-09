#!/usr/bin/env python
# coding: utf-8

# In[1]:


import wptools


# In[19]:

def get_table(name):
	try:
		so = wptools.page(name).get_parse()
		infobox = so.data['infobox']
	except:
		return 
	return infobox


# In[20]:

def clean_table(infobox):
	chars = ['[',']','{','}','|','<br>','<br />','<br/>']
	for key in infobox:
	    for c in chars:
	        if(c in infobox[key]):
	            value1= infobox[key]
	            value1 = value1.replace(c,"")
	            infobox[key] = value1
	return infobox


# In[21]:

def get_parameters(infobox):
	origin = "origin"; abv = "abv"; manufacturer = "manufacturer"; al_type = "type" ; 
	value = {}
	value['location'] = origin
	value['origin'] = origin
	value['country of origin'] = origin
	value['Country of origin'] = origin
	value['location country'] = origin
	value['Founded'] = origin
	value['Foundation'] = origin

	value['volume'] = abv
	value['alcohol volume'] = abv
	value['alcohol percentage'] = abv
	value['abv 1'] = abv
	value['alcohol_by_volume'] = abv
	value['Alcohol by volume'] = abv
	value['abv'] = abv
	value['alcohol content'] = abv


	value['owner'] = manufacturer
	value['manufacturer'] = manufacturer
	value['Manufacturer'] = manufacturer
	value['ownership'] = manufacturer
	value['Parent'] = manufacturer

	
	value['type'] = al_type
	value['Type'] = al_type
	value['Products'] =al_type

	# In[5]:

	param = {}
	for key in infobox:
		# print(key)
		if key in value:
			if(key == "Products"):
				param[value[key]] = infobox[key].split(",")[0]
			else:
				param[value[key]] = infobox[key]
	return (param)

def get_output(name,table):
	params = []
	params.append(name.lower().capitalize())
	if table.get("type") == None:
		params.append("")                                        
	else:
		params.append(table.get("type").lower().capitalize())
	if table.get("manufacturer") == None:
		params.append("")
	else:
		params.append(table.get("manufacturer").lower().capitalize())
	if table.get("origin") == None:
		params.append("")
	else:
		params.append(table.get("origin").lower().capitalize())
	if table.get("abv") == None:
		params.append("")
	else:	
		params.append(table.get("abv").lower().capitalize())
	return params
# In[ ]:

def wiki(name):
	print("*****wiki()******")
	import pandas as pd
	import wikipedia as wp
	try: 
		html = wp.page(name).html().encode("UTF-8")
		df = pd.read_html(html)[0]
		ar = df.to_dict('r')
		param_dict = {}
		for i in ar:
		  param_dict[i.get(0)] = i.get(1)
		return param_dict
	except:
		return


def get_params(name):

	params = []
	table = wiki(name)
	print(table)
	
	table = get_parameters(table)
	params = get_output(name,table)
	print("params",params)
	table1 = get_table(name)

	if (table1 != None):
		table1 = clean_table(table)
		table1 = get_parameters(table)
		params1 = get_output(name,table)
		print("Params1",params1)
	if len(params) > len(params1):
		return params
	else:
		return params1

print(get_params("Smirnoff"))