#dataset = pd.read_csv('C:\Users\wfky1\OneDrive\Documents\PythonFolder\PythonOlr\olr_python_package\data\crudeoildata.csv')
#responseName = dataset[['CrudeOil']]
#predictorNames = dataset[['SPX', 'RigCount', 'API', 'FieldProduction', 'RefinerNetInput', 'OperableCapacity', 'Imports', 'StocksExcludingSPR', 'NonCommercialLong', 'NonCommercialShort', 'CommercialLong', 'CommercialShort', 'TotalLong', 'TotalShort', 'NonReportablePositionsLong', 'NonReportablePositionsShort', 'OpenInterest']]

#olr(dataset, responseName, predictorNames, adjr2 = "True")


import pandas as pd
import numpy as np
import statsmodels.formula.api as sm

import itertools

from itertools import combinations

import functools

def reduce_concat(x, sep=""):
	return functools.reduce(lambda x, y: str(x) + sep + str(y), x)

def paste(*lists, sep=" ", collapse=None):
	result = map(lambda x: reduce_concat(x, sep=sep), zip(*lists))
	if collapse is not None:
		return reduce_concat(result, sep=collapse)
	return list(result)

summarylist = []

def olr(dataset, responseName = None, predictorNames = None, adjr2 = "TRUE"):

        if responseName is None and predictorNames is None: 

                columnrange = len(list(dataset.columns.values))

                predictorNames = dataset.iloc[:,1:len(list(dataset.columns.values))]

                responseName = dataset[[dataset.columns.values[0]]]
 
        elif responseName is not None and predictorNames is not None: #not NULL not using the data set

                columnrange = len(list(predictorNames.columns.values))+1

                predictorNames = predictorNames

                responseName = responseName

        if adjr2 == ("TRUE") or adjr2 == ("True") or adjr2 == ("true"):

                xmod = ["+".join(i) for i in range(1,columnrange) for i in list(combinations(predictorNames,i))]

                ymod = [paste(responseName, "~") for i in xmod]

                zmod = [i[0] for i in ymod]

                mod = paste(zmod,xmod)

                output = [sm.ols(formula = i, data=dataset).fit().rsquared_adj for i in mod]

                maxoutput = max(output)
        
                summarylist = list(enumerate([sm.ols(formula = i, data=dataset).fit().summary() for i in mod]))

                return(summarylist[output.index(maxoutput)])

        elif adjr2 == ("FALSE") or adjr2 == ("False") or adjr2 == ("false"):

                xmod = ["+".join(i) for i in range(1,columnrange) for i in list(combinations(predictorNames,i))]

                ymod = [paste(responseName, "~") for i in xmod]

                zmod = [i[0] for i in ymod]

                mod = paste(zmod,xmod)

                output = [sm.ols(formula = i, data=dataset).fit().rsquared for i in mod]

                maxoutput = max(output)

                summarylist = list(enumerate([sm.ols(formula = i, data=dataset).fit().summary() for i in mod]))

                return(summarylist[output.index(maxoutput)])


#to get the model you want in the list type olrmodels(dataset, responseName = None, predictorNames = None)[x], where x equals the number in the list of summaries/models
def olrmodels(dataset, responseName = None, predictorNames = None):
        
        if responseName is None and predictorNames is None: 

                columnrange = len(list(dataset.columns.values))

                predictorNames = dataset.iloc[:,1:len(list(dataset.columns.values))]

                responseName = dataset[[dataset.columns.values[0]]]
 
        elif responseName is not None and predictorNames is not None: #not NULL not using the data set

                columnrange = len(list(predictorNames.columns.values))+1

                predictorNames = predictorNames

                responseName = responseName

        print("To get the model you want in the list type olrmodels(dataset, responseName = None, predictorNames = None)[x], where x equals the number in the list of summaries/models")

        xmod = ["+".join(i) for i in range(1,columnrange) for i in list(combinations(predictorNames,i))]

        ymod = [paste(responseName, "~") for i in xmod]

        zmod = [i[0] for i in ymod]
  
        mod = paste(zmod,xmod)

        output = list(enumerate([sm.ols(formula = i, data=dataset).fit().summary() for i in mod]))

        return(output)


def olrformulas(dataset, responseName = None, predictorNames = None):
        
        if responseName is None and predictorNames is None: 

                columnrange = len(list(dataset.columns.values))

                predictorNames = dataset.iloc[:,1:len(list(dataset.columns.values))]

                responseName = dataset[[dataset.columns.values[0]]]
 
        elif responseName is not None and predictorNames is not None: #not NULL not using the data set

                columnrange = len(list(predictorNames.columns.values))+1

                predictorNames = predictorNames

                responseName = responseName

        xmod = ["+".join(i) for i in range(1,columnrange) for i in list(combinations(predictorNames,i))]

        ymod = [paste(responseName, "~") for i in xmod]

        zmod = [i[0] for i in ymod]

        mod = paste(zmod,xmod)

        return(mod)


def olrformulasorder(dataset, responseName = None, predictorNames = None):
        
        if responseName is None and predictorNames is None: 

                columnrange = len(list(dataset.columns.values))

                predictorNames = dataset.iloc[:,1:len(list(dataset.columns.values))]

                responseName = dataset[[dataset.columns.values[0]]]
 
        elif responseName is not None and predictorNames is not None: #not NULL not using the data set

                columnrange = len(list(predictorNames.columns.values))+1

                predictorNames = predictorNames

                responseName = responseName

        xmod = ["+".join(i) for i in range(1,columnrange) for i in list(combinations(predictorNames,i))]

        sortedxmod = sorted(xmod)

        ymod = [paste(responseName, "~") for i in sortedxmod]

        zmod = [i[0] for i in ymod]

        mod = paste(zmod,sortedxmod)

        return(mod)


def adjr2list(dataset, responseName = None, predictorNames = None):
        
        if responseName is None and predictorNames is None: 

                columnrange = len(list(dataset.columns.values))

                predictorNames = dataset.iloc[:,1:len(list(dataset.columns.values))]

                responseName = dataset[[dataset.columns.values[0]]]
 
        elif responseName is not None and predictorNames is not None: #not NULL not using the data set

                columnrange = len(list(predictorNames.columns.values))+1

                predictorNames = predictorNames

                responseName = responseName

        xmod = ["+".join(i) for i in range(1,columnrange) for i in list(combinations(predictorNames,i))]

        ymod = [paste(responseName, "~") for i in xmod]

        zmod = [i[0] for i in ymod]

        mod = paste(zmod,xmod)

        output = [sm.ols(formula = i, data=dataset).fit().rsquared_adj for i in mod]

        return(output)


def r2list(dataset, responseName = None, predictorNames = None):
        
        if responseName is None and predictorNames is None: 

                columnrange = len(list(dataset.columns.values))

                predictorNames = dataset.iloc[:,1:len(list(dataset.columns.values))]

                responseName = dataset[[dataset.columns.values[0]]]
 
        elif responseName is not None and predictorNames is not None: #not NULL not using the data set

                columnrange = len(list(predictorNames.columns.values))+1

                predictorNames = predictorNames

                responseName = responseName

        xmod = ["+".join(i) for i in range(1,columnrange) for i in list(combinations(predictorNames,i))]

        ymod = [paste(responseName, "~") for i in xmod]

        zmod = [i[0] for i in ymod]

        mod = paste(zmod,xmod)

        output = [sm.ols(formula = i, data=dataset).fit().rsquared for i in mod]

        return(output)
