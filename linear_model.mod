# Linear Problem IP;

# Define the set
param I;
param J;
param T;
set CONSUMERS := 1..I;
set PRODUCTS := 1..J;
set PERIODS := 1..T;

# Define parameters
param beta;
param b;
param c{j in PRODUCTS};
param M := 10* sum{j in PRODUCTS}c[j]; #Constraint 15
param ini{i in CONSUMERS};
param r {i in CONSUMERS, j in PRODUCTS, t in PERIODS}:=
  if (j = 1 and t = 1) 
  then ini[i]
  else (j * r[i,1,1] - beta * (j - 1)^2) * exp(-b * (t - 1));



# Define the variable
var p{j in PRODUCTS, t in PERIODS}; 
var k{i in CONSUMERS, j in PRODUCTS, t in PERIODS};
var s{i in CONSUMERS};
var x{CONSUMERS, PRODUCTS, PERIODS}, binary;
var y{j in PRODUCTS, t in PERIODS}, binary;
var l{j in PRODUCTS, t in PERIODS};

# Fonction objective
maximize Total_Profit:
  sum {i in CONSUMERS, j in PRODUCTS, t in PERIODS} (k[i,j,t] - c[j]* x[i,j,t]);

# Contraintes 

Constraint3_2{i in CONSUMERS, j in PRODUCTS, t in PERIODS}: k[i,j,t] - M * (1 - x[i,j,t]) <= p[j,t];
Constraint3_3{i in CONSUMERS, j in PRODUCTS, t in PERIODS}: k[i,j,t] + M * (1 - x[i,j,t]) >= p[j,t];
Constraint3_4{i in CONSUMERS, j in PRODUCTS, t in PERIODS}: k[i,j,t] - M * x[i,j,t] <= 0;
Constraint4_1{i in CONSUMERS}: s[i] = sum{j in PRODUCTS, t in PERIODS} (r[i,j,t] * x[i,j,t] - k[i,j,t]);
Constraint5_1{i in CONSUMERS, j in PRODUCTS, t in PERIODS}: s[i] >= r[i,j,t] * y[j,t] - l[j,t];
Constraint5_2{j in PRODUCTS, t in PERIODS}: l[j,t] - M * (1 - y[j,t]) <= p[j,t];
Constraint5_3{j in PRODUCTS, t in PERIODS}: l[j,t] + M * (1 - y[j,t]) >= p[j,t];
Constraint5_4{j in PRODUCTS, t in PERIODS}: l[j,t] - M * y[j,t] <= 0;

Customer_choice {i in CONSUMERS, j in PRODUCTS, t in PERIODS}:(r[i,j,t]*x[i,j,t]-k[i,j,t]) >= 0; #Constraint 6
Single_Purchase {i in CONSUMERS}:sum {j in PRODUCTS, t in PERIODS} x[i,j,t] <= 1; #Constraint 8
Single_Bundle {t in PERIODS}: sum {j in PRODUCTS} y[j,t] <= 1;#Constraint 9
Production_Limit {i in CONSUMERS, j in PRODUCTS, t in PERIODS}: x[i,j,t] <= y[j,t]; #Constraint 10
NonNegative_S {i in CONSUMERS}: s[i] >= 0; #Constraint 11
NonNegative_P {j in PRODUCTS, t in PERIODS}:  p[j,t] >= 0; #Constraint 12
NonNegative_K {i in CONSUMERS, j in PRODUCTS, t in PERIODS}:  k[i,j,t] >= 0; #Constraint 16
NonNegative_L {j in PRODUCTS, t in PERIODS}:  l[j,t] >= 0; #Constraint 17
solve;

# Sortie des résultats
printf "Le profit vaut %5.2f € \n",Total_Profit;
printf "Suivi des achats : \n";
printf{i in CONSUMERS, j in PRODUCTS, t in PERIODS : x[i,j,t] = 1}"Achat par le client %d, d'un pack de %d produits  à la période %d \n",i,j,t;
printf "\nSuivi des propositions du commerçant : \n";
printf{t in PERIODS,j in PRODUCTS : y[j,t] = 1}"Le commercant propose un pack de %d à la période %d, au prix de %5.2f €\n",j,t,p[j,t];

#Apport des données
data;
param I := 10;
param J := 10;
param T := 6;

param b := 0.5;
param beta := 0.04;

param : ini :=
  1 8
  2 10
  3 8
  4 11
  5 8
  6 8
  7 9
  8 12
  9 9
  10 10;

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

end;
