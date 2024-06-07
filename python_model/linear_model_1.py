from gurobipy import *
import numpy as np
np.set_printoptions(suppress=True)
import pandas as pd


# Parameters
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


rng = np.random.default_rng(78794)


# Compute reservation prices
def reservation_prices(I,J,T,beta,b,min_r,max_r):
    r = np.full((I,J,T),0.)
    r[:,0,0] = rng.uniform(min_r,max_r,I)
    for i in range(I):
        for j in range(J):
            for t in range(T):
                    if j+t>0 :
                        r[i][j][t] = ((j + 1) * r[i][0][0] - beta *(j**2))* np.exp(-b * (t))
    return r



def linear_model(I,J,T,M,c,r):
    model = Model("Linear_Problem_IP")
    # Variables
    p = model.addVars(J, T, name="p", lb=0)
    s = model.addVars(I, name="s", lb=0)
    x = model.addVars(I, J, T, vtype=GRB.BINARY, name="x")
    y = model.addVars(J, T, vtype=GRB.BINARY, name="y")
    l = model.addVars(J, T, name="l", lb=0)
    k = model.addVars(I, J, T, name="k", lb=0)
    model_vars = {"p":p,"s":s,"x":x,"y":y,"l":l,"k":k}
    # Objective function
    model.setObjective(
        quicksum(k[i, j, t] - c[j] * x[i, j, t] for i in range(I) for j in range(J) for t in range(T)),
        GRB.MAXIMIZE
    )

    # Constraints
    model.addConstrs((k[i, j, t] - M * (1 - x[i, j, t]) <= p[j, t] for i in range(I) for j in range(J) for t in range(T)), name="Linearisation_kijt_1")
    model.addConstrs((k[i, j, t] + M * (1 - x[i, j, t]) >= p[j, t] for i in range(I) for j in range(J) for t in range(T)), name="Linearisation_kijt_2")
    model.addConstrs((k[i, j, t] - M * x[i, j, t] <= 0 for i in range(I) for j in range(J) for t in range(T)), name="Linearisation_kijt_3")
    model.addConstrs((s[i] == quicksum(r[i][j][t] * x[i, j, t] - k[i, j, t] for j in range(J) for t in range(T)) for i in range(I)), name="Linear_Si")
    model.addConstrs((s[i] >= r[i][j][t] * y[j, t] - l[j, t] for i in range(I) for j in range(J) for t in range(T)), name="Linearisation_Ljt_1")
    model.addConstrs((l[j, t] - M * (1 - y[j, t]) <= p[j, t] for j in range(J) for t in range(T)), name="Linearisation_Ljt_2")
    model.addConstrs((l[j, t] + M * (1 - y[j, t]) >= p[j, t] for j in range(J) for t in range(T)), name="Linearisation_Ljt_3")
    model.addConstrs((l[j, t] - M * y[j, t] <= 0 for j in range(J) for t in range(T)), name="Linearisation_Ljt_4")
    model.addConstrs((r[i][j][t] * x[i, j, t] - k[i, j, t] >= 0 for i in range(I) for j in range(J) for t in range(T)), name="Customer_choice")
    model.addConstrs((quicksum(x[i, j, t] for j in range(J) for t in range(T)) <= 1 for i in range(I)), name="Single_Purchase")
    model.addConstrs((quicksum(y[j, t] for j in range(J)) == 1 for t in range(T)), name="Single_Bundle")
    #model.addConstrs((quicksum(y[j, t] for j in range(J)) <= 1 for t in range(T)), name="Single_Bundle")
    model.addConstrs((x[i, j, t] <= y[j, t] for i in range(I) for j in range(J) for t in range(T)), name="Production_Limit")

    # Solve the model
    model.optimize()
    if model.status == GRB.OPTIMAL: return model,model_vars
    else:print("No optimal solution found.")

#optimize the model
r = reservation_prices(I,J,T,beta,b,min_r,max_r)
model,variables = linear_model(I,J,T,M,c,r)

#create df for results
columns = ["beta","b","Si","Results","Profit","lambda"]
Export_df = pd.DataFrame(columns=columns)

def new_line_df(beta = beta, b = b, lamb = lamb):
    #Table like article table
    A = np.full((T,4),0.)
    A[:,0]=[t+1 for t in range(T)]
    for j in range(J):
        for t in range(T):
            if variables["y"][j,t].x == 1 :
                A[t,1]=j+1
                A[t,2]=variables["p"][j,t].x
                A[t,3]=A[t,2]/A[t,1]

    S = [variables["s"][i].x for i in range(I)]
    return [beta,b,S,A,model.ObjVal,lamb]

Export_df.loc[0] = new_line_df()
print(Export_df["Profit"])
loo=False

if loo:
    beta_list = [0.2,0.5,0.8]
    lambda_list = [0.2,0.5,0.8]
    b_list = [0.01,0.04,0.07]

    df_indice = 0

    #Test multiple beta values
    for temp_beta in beta_list:
        r = reservation_prices(I,J,T,temp_beta,b,min_r,max_r)
        model,variables = linear_model(I,J,T,M,c,r)
        Export_df.loc[df_indice] = new_line_df(beta = temp_beta)
        df_indice+=1

    #Test multiple b values
    for temp_b in b_list:
        r = reservation_prices(I,J,T,beta,temp_b,min_r,max_r)
        model,variables = linear_model(I,J,T,M,c,r)
        Export_df.loc[df_indice] = new_line_df(b = temp_b)
        df_indice+=1


    #Test multiple lambda values
    for temp_lamb in lambda_list:
        temp_min_r = temp_lamb*max_r
        r = reservation_prices(I,J,T,beta,b,temp_min_r,max_r)
        model,variables = linear_model(I,J,T,M,c,r)
        Export_df.loc[df_indice] = new_line_df(lamb=temp_lamb)
        df_indice+=1

        
    Export_df.to_json("GP30_Results.json",orient="records",lines=True)

