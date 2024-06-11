"""

Run linear optimisation for every parameters values
In the case  study of GP30 class
author : Nathan Davouse

"""
#Useful librairies
import numpy as np
np.set_printoptions(suppress=True)
import pandas as pd
#import bundle_model functions
from bundle_model import reservation_prices 
from bundle_model import linear_model

"""-----------Parameters----------"""
I = 10  # number of consumers
J = 10  # number of bundles
T = 6   # number of periods
beta = 0.5  # decreasing rate for the creation of bundles
b = 0.04    # deterioration rate over time
c = [4*(j+1) for j in range(J)]# Costs of bundles
M = 10 * sum(c)  # Big M
max_r = 12
lamb = 0.5
min_r = max_r*lamb
rdm_seed = 654654

#Controls variables
loo=True
expo = True

"""-----------Make a list with keys results----------"""
def new_line_df(beta = beta, b = b, lamb = lamb):
    #Table like article table
    A = np.full((T,5),0.)
    A[:,0]=[t+1 for t in range(T)]
    for j in range(J):
        for t in range(T):
            if variables["y"][j,t].x == 1 :
                A[t,1]=j+1
                A[t,2]=variables["p"][j,t].x
                A[t,3]=A[t,2]/A[t,1]
                A[t,4] = sum([variables["x"][i,j,t].x for i in range (I)])
    S = [variables["s"][i].x for i in range(I)]

    return [beta,b,lamb,S,A,model.ObjVal]

"""-----------optimize with initial results----------"""
r = reservation_prices(I,J,T,beta,b,min_r,max_r,rdm_seed)
model,variables = linear_model(I,J,T,M,c,r)

"""-----------Create Dataframe and save with initial results----------"""
columns = ["beta","b","lambda","Si","Results","Profit"]
Export_df = pd.DataFrame(columns=columns)
Export_df.loc[0] = new_line_df()
print(Export_df["Profit"])

"""-----------Optimize and save with sensibility analysis----------"""
if loo:
    #Define list of values for sensibility analysis
    beta_list = [0.2,0.8] #remove 0.5 since it's initial value
    lambda_list = [0.2,0.8] #remove 0.5 since it's initial value
    b_list = [0.01,0.07] #remove 0.04 since it's initial value

    df_indice = 1
    #Test multiple beta values
    for temp_beta in beta_list:
        r = reservation_prices(I,J,T,temp_beta,b,min_r,max_r,rdm_seed)
        model,variables = linear_model(I,J,T,M,c,r)
        Export_df.loc[df_indice] = new_line_df(beta = temp_beta)
        df_indice+=1

    #Test multiple b values
    for temp_b in b_list:
        r = reservation_prices(I,J,T,beta,temp_b,min_r,max_r,rdm_seed)
        model,variables = linear_model(I,J,T,M,c,r)
        Export_df.loc[df_indice] = new_line_df(b = temp_b)
        df_indice+=1


    #Test multiple lambda values
    for temp_lamb in lambda_list:
        temp_min_r = temp_lamb*max_r
        r = reservation_prices(I,J,T,beta,b,temp_min_r,max_r,rdm_seed)
        model,variables = linear_model(I,J,T,M,c,r)
        Export_df.loc[df_indice] = new_line_df(lamb=temp_lamb)
        df_indice+=1

if expo:       
    Export_df.to_json("GP30_Results_anthony.json",orient="records",lines=True)