# Linear Problem IP;
#-----------------------------------------------------------------Define variables and parameters-----------------------------------------------------------------
# Define the sets
param I; #number of consumers
param J; #sizes of possible bundles
param T; #number of period
set CONSUMERS := 1..I; #set of consumers
set PRODUCTS := 1..J;#set of bundles
set PERIODS := 1..T;#set of period

# Define parameters
param beta; #decreasing rate for the creation of bundles
param b; #deterioration rate over time
param c{j in PRODUCTS};#cost of bundle
param M := 10* sum{j in PRODUCTS}c[j]; #define the big M
param ini{i in CONSUMERS};#Initial reservation price for each client 
param r {i in CONSUMERS, j in PRODUCTS, t in PERIODS}:= #reservation price = maximum prices that the client want to pay
  if (j = 1 and t = 1) 
  then ini[i] 
  else (j * r[i,1,1] - beta * (j - 1)^2) * exp(-b * (t - 1)); 

# Define the variables
var p{j in PRODUCTS, t in PERIODS}; #Prices of the bundle
var s{i in CONSUMERS}; #gain for the consumers for each purchases
var x{CONSUMERS, PRODUCTS, PERIODS}, binary; # choice of purchase by the consumers
var y{j in PRODUCTS, t in PERIODS}, binary; #Choice of bundle by the retailer
var l{j in PRODUCTS, t in PERIODS}; #linearisation of Pjt*Xjt
var k{i in CONSUMERS, j in PRODUCTS, t in PERIODS}; #linearisation of Pjt*Xijt

# ----------------------------------------------------------------- Objective fonction-----------------------------------------------------------------
maximize Total_Profit:  #Total profit : prices minus costs for each purchases
  sum {i in CONSUMERS, j in PRODUCTS, t in PERIODS} (k[i,j,t] - c[j]* x[i,j,t]); 

# -----------------------------------------------------------------Constraints-----------------------------------------------------------------
Linearisation_kijt_1{i in CONSUMERS, j in PRODUCTS, t in PERIODS}: k[i,j,t] - M * (1 - x[i,j,t]) <= p[j,t]; #Constraint 3.2 : if Xijt = 0; Kijt <= Pjt
Linearisation_kijt_2{i in CONSUMERS, j in PRODUCTS, t in PERIODS}: k[i,j,t] + M * (1 - x[i,j,t]) >= p[j,t]; #Constraint 3.3 : if Xijt = 0; Kijt >= Pjt
Linearisation_kijt_3{i in CONSUMERS, j in PRODUCTS, t in PERIODS}: k[i,j,t] - M * x[i,j,t] <= 0;#Constraint 3.3 : if Xijt = 0; Kijt = 0
Linear_Si{i in CONSUMERS}: s[i] = sum{j in PRODUCTS, t in PERIODS} (r[i,j,t] * x[i,j,t] - k[i,j,t]);#Constraint 4.1 : linear  version of Si = Xijt*(Rijt - Pjt)
Linearisation_Ljt_1{i in CONSUMERS, j in PRODUCTS, t in PERIODS}: s[i] >= r[i,j,t] * y[j,t] - l[j,t];#Constraint 5.1 : if Yjt=1, Si = Rijt - Pjt. if Yjt = 0, Si>= 0 
Linearisation_Ljt_2{j in PRODUCTS, t in PERIODS}: l[j,t] - M * (1 - y[j,t]) <= p[j,t];#Constraint 5.2 : if Yjt = 0; Ljt <= Pjt
Linearisation_Ljt_3{j in PRODUCTS, t in PERIODS}: l[j,t] + M * (1 - y[j,t]) >= p[j,t];#Constraint 5.3 : if Yjt = 0; Ljt >= Pjt
Linearisation_Ljt_4{j in PRODUCTS, t in PERIODS}: l[j,t] - M * y[j,t] <= 0;#Constraint 5.4 : if Yjt = 0; Ljt = 0
Customer_choice {i in CONSUMERS, j in PRODUCTS, t in PERIODS}:(r[i,j,t]*x[i,j,t]-k[i,j,t]) >= 0; #Constraint 6 : customer purchase if Pjt < Rijt
Single_Purchase {i in CONSUMERS}:sum {j in PRODUCTS, t in PERIODS} x[i,j,t] <= 1; #Constraint 8 : allow consumers to purchase maximum one product
Single_Bundle {t in PERIODS}: sum {j in PRODUCTS} y[j,t] <= 1;#Constraint 9 : allow retailler to propose maximum one bundle by period
Production_Limit {i in CONSUMERS, j in PRODUCTS, t in PERIODS}: x[i,j,t] <= y[j,t]; #Constraint 10 : consumers can only purchase product that are proposed by the retailer
NonNegative_S {i in CONSUMERS}: s[i] >= 0; #Constraint 11 : ensure that the surplus is non negative
NonNegative_P {j in PRODUCTS, t in PERIODS}:  p[j,t] >= 0; #Constraint 12 : ensure that the price is non negative
NonNegative_K {i in CONSUMERS, j in PRODUCTS, t in PERIODS}:  k[i,j,t] >= 0; #Constraint 16 : ensure that Kijt is non negative
NonNegative_L {j in PRODUCTS, t in PERIODS}:  l[j,t] >= 0; #Constraint 17 : ensure that L is non negative

#Solve the model
solve;

# -----------------------------------------------------------------Sortie des résultats-----------------------------------------------------------------
#Profit
printf "Le profit vaut %5.2f € \n",Total_Profit;

#Purchases 
printf "\nSuivi des achats : \n";
printf{i in CONSUMERS, j in PRODUCTS, t in PERIODS : x[i,j,t] = 1}"   Achat par le client %d, d'un pack de %d produits à la période %d \n",i,j,t;

#Bundles
printf "\nSuivi des propositions du commerçant : \n";
printf{t in PERIODS,j in PRODUCTS : y[j,t] = 1}"   Le commercant propose un pack de %d à la période %d, au prix de %5.2f €\n",j,t,p[j,t];

#Surplus
printf "\nSurplus de chaque client \n";
printf {i in CONSUMERS}"   Le client %d gagne un surplus de %5.2f €.\n",i,s[i];

#Brouillon
printf{i in CONSUMERS, j in PRODUCTS, t in PERIODS : x[i,j,t] = 1}"k : %5.2f ; x : %5.2f \n",k[i,j,t],x[i,j,t];

# -----------------------------------------------------------------Apport des données-----------------------------------------------------------------
data;

#Define the sets
param I := 10;
param J := 10;
param T := 6;

#Rates used to define reservation prices
param b := 0.5;
param beta := 0.04;

# Initial reservations prices
param : ini :=
  1 12
  2 7
  3 12
  4 8
  5 11
  6 6
  7 7
  8 12
  9 11
  10 10;

#Cost of bundles
  param : c :=
  1 4
  2 8
  3 12
  4 16
  5 20
  6 24
  7 28
  8 32
  9 36
  10 40;

#Fin du modèle
end;
