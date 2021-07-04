
#
# Dictionary converter for extremely nested dictionary to and fro to excel data tabular format
#


import pandas as pd
# from pprint import pprint


def varsheet(dic):
	ndic = {'FIND':[], 'REPLACE':[]}
	for k, v in dic.items(): 
		ndic['FIND'].append(k)
		ndic['REPLACE'].append(v)
	return ndic

def appendkey(dic, prefix=""):
	if not prefix: return dic
	ndic = {}
	for key, value in dic.items():
		ndic[prefix + "_" + key ] = value
	return ndic

def recursive_dic(dic, prevkey=''):
	opd = {}
	for dickey, dicvalue in dic.items():
		if isinstance(dicvalue, dict):
			opd.update( appendkey(recursive_dic(dicvalue, dickey), dickey ))
		else:
			opd[dickey] = dicvalue
	return opd

def standup_dic(dic, ikp):
	ndic = {'inttype':[], 'intid':[], 'intvalues':[]}
	for dickey, dicvalue in dic.items():
		for dicvaluek, dicvaluev in dicvalue.items():
			if dickey in ikp:
				ndic['inttype'].append(dickey)
				ndic['intid'].append(dicvaluek)
			else:
				ndic['inttype'].append('')
				ndic['intid'].append('')
			ndic['intvalues'].append(dicvaluev)			# Hungami
	return ndic

def expand_var_dict(dic):
	return {k:v for k, v in zip(dic['FIND'].values(),  dic['REPLACE'].values() )}

def expand_table_dict(dic):
	opd = {}
	inttypeset = set(dic['inttype'].values())
	for i, intid in dic['intid'].items():
		respectiveinttype = dic['inttype'][i]
		if not opd.get(respectiveinttype):
			opd[respectiveinttype] = {}
		if not opd[respectiveinttype].get(intid):
			opd[respectiveinttype][intid] = {}
	diccopy = dic.copy()
	for k, v in diccopy.items():
		if k in ('intid', 'inttype'): continue
		keys = k.split("_")
		for i, vitem in v.items():
			if not vitem: continue
			respectiveinttype = dic['inttype'][i]
			respectiveint = dic['intid'][i]
			dd = opd[respectiveinttype][respectiveint]
			opd[respectiveinttype][respectiveint] = update_nested_key(dd, keys, vitem)
	for k, v in diccopy.items():
		del(dic[k])
	return opd

def update_nested_key(dic, keys, vitem):
	nd = dic
	for i, key in enumerate(keys):
		if i > 0:
			nd = dic[prevkey]
		if not nd.get(key): nd[key] = {}
		prevkey = key
	nd[key] = vitem
	return dic


class ConvDict():

	def __init__(self, dic):
		self.dic = dic

	def set_var_table_keys(self, var, table):
		self.var = var
		self.table = table

	def set_index_keys_parents(self, ikp=('phyint', 'vlint', )):
		self.index_keys_parents = ikp

	def convert_table_dic(self):		
		ndic = standup_dic(self.dic[self.table], self.index_keys_parents)
		ndiclen = len(ndic['intvalues'])
		for i, d in enumerate(ndic['intvalues']):
			rd = recursive_dic(d)
			for k, v in rd.items():
				if not ndic.get(k):
					ndic[k] = ["" for _ in range(ndiclen)]
				ndic[k][i] = v
		del(ndic['intvalues'])
		return ndic

	def convert_var_dic(self):
		return varsheet(self.dic[self.var])

	def to_dataframe(self, sheetname):
		if sheetname == self.var:
			return pd.DataFrame(self.convert_var_dic())
		if sheetname == self.table:
			return pd.DataFrame(self.convert_table_dic())

	def expand_to_dict(self, df_var, df_table):
		d_var = df_var.to_dict()
		opdv = self.expand_dfdic_to_dict(self.var, d_var)
		d_table = df_table.to_dict()
		opdt = self.expand_dfdic_to_dict(self.table, d_table)
		return {self.var: opdv, self.table: opdt}

	def expand_dfdic_to_dict(self, sheetname, dic):
		if sheetname == self.var:
			return expand_var_dict(dic)
		if sheetname == self.table:
			return expand_table_dict(dic)


if __name__ == '__main__':

	# d is an input nested dictionary
	CD = ConvDict(d)
	CD.set_var_table_keys(var='var', table='table')
	CD.set_index_keys_parents(('phyint', 'vlint', ))

	dfv = CD.to_dataframe('var')
	dft = CD.to_dataframe('table')	

	opd = CD.expand_to_dict(df_var=dfv, df_table=dft)

	print(opd)
	print(d == opd)
	