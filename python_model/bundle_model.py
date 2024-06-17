"""

Functions used to define models and reservation prices
In the case  study of GP30 class
author : Nathan Davouse

"""

#Maximum willingness to pay
def reservation_prices(I,J,T,beta,b,min_r,max_r,seed = 78794 ):
    """----------- Import numpy librairy ----------"""
    import numpy as np
    """----------- Define R1ii with uniform generation ----------"""
    rng = np.random.default_rng(seed)
    r = np.full((I,J,T),0.)
    r[:,0,0] = rng.uniform(min_r,max_r,I)
    """----------- Compute Rijt ----------"""
    for i in range(I):
        for j in range(J):
            for t in range(T):
                    if j+t>0 :
                        r[i][j][t] = ((j + 1) * r[i][0][0] - beta *(j**2))* np.exp(-b * (t))
    return r


#Define the linear model and optimize it
def linear_model(I,J,T,M,c,r):
    """----------- Import function from gurobipy librairy ----------"""
    from gurobipy import Model
    from gurobipy import GRB
    from gurobipy import quicksum

    """----------- Create Gurobipy model ----------"""
    model = Model("Linear_Problem_IP")
    
    """----------- Add variables ----------"""
    p = model.addVars(J, T, name="p", lb=0)
    s = model.addVars(I, name="s", lb=0)
    x = model.addVars(I, J, T, vtype=GRB.BINARY, name="x") #Include constraint 13
    y = model.addVars(J, T, vtype=GRB.BINARY, name="y") #Include constraint 14
    l = model.addVars(J, T, name="l", lb=0)
    k = model.addVars(I, J, T, name="k", lb=0)
    #Make a dictionnary with all variables to return it
    model_vars = {"p":p,"s":s,"x":x,"y":y,"l":l,"k":k}

    """----------- Set Objective function ----------"""
    model.setObjective(
        quicksum(k[i, j, t] - c[j] * x[i, j, t] for i in range(I) for j in range(J) for t in range(T)),
        GRB.MAXIMIZE
    )

    """----------- Add Constraints ----------"""
    #Constraint 3.2
    model.addConstrs((k[i, j, t] - M * (1 - x[i, j, t]) <= p[j, t] 
                      for i in range(I) for j in range(J) for t in range(T)), 
                      name="Linearisation_kijt_1")
    #Constraint 3.3
    model.addConstrs((k[i, j, t] + M * (1 - x[i, j, t]) >= p[j, t] 
                      for i in range(I) for j in range(J) for t in range(T)), 
                      name="Linearisation_kijt_2")
    #Constraint 3.4
    model.addConstrs((k[i, j, t] - M * x[i, j, t] <= 0 
                      for i in range(I) for j in range(J) for t in range(T)), 
                      name="Linearisation_kijt_3")
    #Constraint 4.1
    model.addConstrs((s[i] == quicksum(r[i][j][t] * x[i, j, t] - k[i, j, t] 
                                       for j in range(J) for t in range(T)) for i in range(I)), 
                                       name="Linear_Si")
    #Constraint 5.1
    model.addConstrs((s[i] >= r[i][j][t] * y[j, t] - l[j, t] 
                      for i in range(I) for j in range(J) for t in range(T)), 
                      name="Linearisation_Ljt_1")
    #Constraint 5.2
    model.addConstrs((l[j, t] - M * (1 - y[j, t]) <= p[j, t] 
                      for j in range(J) for t in range(T)), 
                      name="Linearisation_Ljt_2")
    #Constraint 5.3
    model.addConstrs((l[j, t] + M * (1 - y[j, t]) >= p[j, t] 
                      for j in range(J) for t in range(T)), 
                      name="Linearisation_Ljt_3")
    #Constraint 5.4
    model.addConstrs((l[j, t] - M * y[j, t] <= 0 
                      for j in range(J) for t in range(T)), 
                      name="Linearisation_Ljt_4")
    #Constraint 6
    model.addConstrs((r[i][j][t] * x[i, j, t] - k[i, j, t] >= 0 
                      for i in range(I) for j in range(J) for t in range(T)), 
                      name="Customer_choice")
    #Constraint 8
    model.addConstrs((quicksum(x[i, j, t] 
                               for j in range(J) for t in range(T)) <= 1 for i in range(I)), 
                               name="Single_Purchase")
    #Constraint 9 : 
    model.addConstrs((quicksum(y[j, t] for j in range(J)) <= 1 
                      for t in range(T)), 
                      name="Single_Bundle")
    #Constraint 9 bis : Force retailer to propose one bundle
    #model.addConstrs((quicksum(y[j, t] for j in range(J)) == 1 
        # for t in range(T)), 
        # name="Single_Bundle")
    #Constraint 10
    model.addConstrs((x[i, j, t] <= y[j, t] 
                      for i in range(I) for j in range(J) for t in range(T)), 
                      name="Production_Limit")

    # Solve the model
    model.optimize()
    if model.status == GRB.OPTIMAL: return model,model_vars
    else:print("No optimal solution found.")