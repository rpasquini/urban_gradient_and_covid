__author__ = 'Ricardo Pasquini'
#rpasquini@gmail.com
import pandas as pd
import numpy as np

def to_summary_table(varnames_to_print, listofresults, labels_dict=None, specialrows=None):

    """ Transforms list of statsmodels results to publication style printing

    varnames_to_print: These are the actual variable names in the regression output
    list of results: list of results, results are statsmodels result objects
    labels_dict: Optional, will change the variable to those provided
    returns: dataframe

    """

    vars_names=[]


    # The idea is to create a list of contents for each column

    # First column
    row=0
    for var in varnames_to_print:
        # contenido de la 1ra fila

        if labels_dict is not None and var in labels_dict:
            vars_names.append(labels_dict[var])
        else:
            vars_names.append(var)

        row+=1
        vars_names.append('')
        row+=1


    if specialrows is not None:
        for varname in specialrows:
            vars_names.append(varname['varname'])
    # LISTA DE ESTADISTICOS DEL FINAL DE TABLA
    vars_names.append('Number of obs.')
    vars_names.append('Adj-R2')
    vars_names.append('F-statistic:')
    vars_names.append('Prob (F-statistic)')





    #
    data = {0: vars_names}

    column=1
    for results in listofresults:  #Loop for each column (each list of passed results)
        coefficients=[]
        standard_errors=[]
        row=0

        for var in varnames_to_print:

            if var in results.pvalues:
                if results.pvalues[var]<=0.01:
                    asterisk='***'
                elif results.pvalues[var]<=0.05:
                    asterisk='**'
                elif results.pvalues[var]<=0.1:
                    asterisk='*'
                else:
                    asterisk=''

                coefficients.append(   str(round(results.params[var],6)) + asterisk)
                row+=1

                # contenido de la 2da fila

                coefficients.append('('+str(round(results.bse[var],6))+')')
                row+=1
            else:  #la variable no esta en esa especificacion
                coefficients.append(' ')
                row+=1
                # contenido de la 2da fila
                coefficients.append(' ')
                row+=1

        if specialrows is not None:
            for varname in specialrows:
                coefficients.append(varname['values'][column-1])

        # PASAR LA LISTA DE ESTADISTICOS DEL FINAL DE TABLA EN EL MISMO ORDEN QUE ARRIBA
        coefficients.append(results.nobs)
        coefficients.append(round(results.rsquared_adj,3))
        try:
            valorf=round(results.fvalue[0][0],3)
        except IndexError:
            valorf=round(results.fvalue,3)
            

        coefficients.append(valorf)
        coefficients.append(np.round(results.f_pvalue,3))


        data[column]=coefficients
        column+=1





    return pd.DataFrame.from_dict(data)



