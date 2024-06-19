## Résumé du problème

### Description de la problématique

Les produits frais se détériorent au fil du temps, ce qui entraîne une diminution de leur qualité et de leur valeur. Ainsi, il est important de réfléchir à un autre moyen de les vendre.

La stratégie de regroupement présente plusieurs avantages et est un moyen efficace de promouvoir la vente. Premièrement, elle permet de proposer les produits à un prix plus bas et donc plus attrayant pour plus de consommateurs. Ainsi, un lot de 2 produits sera vendu moins cher que 2 produits vendus séparément. Deuxièmement, elle incite les clients à consommer plus et permet d'augmenter la vitesse de vente. Enfin, elle permet une gestion différente de la qualité et fraîcheur des produits, notamment avec la possibilité de proposer des réductions sur les packs moins frais afin d'éviter le gaspillage.

Cependant, cette stratégie d'emballage n'est pas simple à appliquer. En effet, il faut décider de la valeur de plusieurs paramètres pour créer un lot : il doit regrouper la bonne quantité de produits, avoir un prix approprié à sa fraîcheur et être proposé au bon moment. Tous ces paramètres doivent être choisis pour maximiser le profit du vendeur mais ils visent également à satisfaire les exigences de qualité des consommateurs.

L'article étudié[^1] propose donc un modèle mathématique permettant de prendre des décisions sur les paramètres exprimés ci-dessus pour des produits frais avec une détérioration de leur qualité au cours du temps. Les hypothèses sont les suivantes :

- les lots sont composés de produits de même fraîcheur;
- les lots sont constitués d'un unique type de produit;
- la valeur des produits frais en fonction de leur détérioration est représentée par la fonction exponentielle suivante : \(V(t) = e^{-b(t-1)}\) où \(b\) représente le facteur de diminution du produit frais (\(b > 0\));
- le problème est envisagé du point de vue du vendeur.

[^1]: [Bundle Pricing Decisions for Fresh Products with Quality Deterioration; Yan Fang et al](https://onlinelibrary.wiley.com/doi/10.1155/2018/1595807)

### Formulation et explication des contraintes

Pour répondre à la problématique, nous pouvons utiliser le modèle défini par l'article présenté. Ce modèle reprend l'ensemble des éléments définis plus haut, et les variables de décisions sont le regroupement choisi par le commerçant \(Y_{jt}\), le prix de ce regroupement \(P_{jt}\), la décision d'acheter le regroupement par le client \(X_{ijt}\) et le surplus par client, soit le gain qu'il effectue lorsqu'il achète le produit \(S_i\).

Pour se concentrer sur le modèle, nous allons détailler le fonctionnement et l'utilité de chaque contrainte : 

- (3) \(\max \sum_{i=1}^{I} \sum_{j=1}^{J} \sum_{t=1}^{T} (P_{jt} - c_j) X_{ijt}\)
  - Cette fonction est la fonction objective, qui cherche à maximiser le profit du commerçant. Le profit est exprimé comme le prix de vente moins le coût de production pour chaque achat qu'un client effectue.
- (4) \(S_i = \sum_{j=1}^{J} \sum_{t=1}^{T} (R_{ijt} - P_{jt}) X_{ijt}, \forall i\). 
  - Cette contrainte définie le surplus du consommateur, soit le gain qu'il fait en achetant le pack au prix proposé par rapport au prix maximum qu'il s'attendait à payer.
- (5)  \(S_i \geq (R_{ijt} - P_{jt}) Y_{jt}, \forall i; \forall j; \forall t.\)
  - Cette contrainte permet à chaque client de maximiser son surplus. Cela vérifie que le surplus correspond au choix est bien le surplus maximum possible pour le client.
- (6) \((R_{ijt} - P_{jt}) X_{ijt} \geq 0, \forall i; \forall j; \forall t.\)
  - Cette contrainte représente la rationalité du client : il ne choisira un lot que si son surplus est positif.
- (7) \(R_{ijt} = \left[ j R_{i11} - \beta (j - 1)^2 \right] \cdot e^{-b(t-1)}\)
  - Cette contrainte permet de calculer le contenu de la matrice \(R_{ijt}\), c'est-à-dire le prix de réservation par le client \(i\) du lot de taille \(j\) au moment \(t\). Ce "prix de réservation" correspond à la limite supérieure que le client est prêt à payer pour un produit (willingness to pay). Dans le cas envisagé ici, des lots de plusieurs produits frais, les coûts de réservation diminuent en accord avec la perte de fraîcheur des produits. Ces coûts prennent également en compte la loi de l'utilité marginale décroissante, c'est-à-dire que le ratio \(R_{ijt}/j\) diminue avec l'augmentation de la taille du lot.
- (8) \(\sum_{j=1}^{J} \sum_{t=1}^{T} X_{ijt} \leq 1, \forall i.\)
  - Cette contrainte empêche les clients de réserver plus d'un lot chacun.
- (9) \(\sum_{j=1}^{J} Y_{jt} \leq 1, \forall t.\)
  - Cette contrainte empêche le vendeur de proposer plus d'un lot différent par période.
- (10) \(X_{ijt} \leq Y_{jt}, \forall i; \forall j; \forall t.\)
  - Cette contrainte permet de ne rendre l'achat possible par les clients d'un certain lot que s'il est rendu disponible par le vendeur.
- (11) et (12) : Ces contraintes empêchent les variables \(S_i\) et \(P_{jt}\) de prendre des valeurs négatives. Cela semble logique pour le prix de vente et le surplus client.
- (13) et (14) : Ces contraintes assurent que les variables \(X_{ijt}\) et \(Y_{jt}\) soient binaires.

### Méthodes de résolution utilisées {#linear}

Le problème de ce modèle mathématique est qu'il est non linéaire et donc assez compliqué à résoudre. L'approche pour simplifier la résolution est de le convertir en modèle linéaire. Pour cela, il faut effectuer un changement au niveau des variables de décision. Les variables \(K_{ijt} = P_{jt}X_{ijt}\) et \(L_{jt} = P_{jt}Y_{jt}\) sont donc introduites afin d'éviter les multiplications entre variables de décision, ce qui rendait le problème non linéaire.

Ces nouvelles variables impactent directement le modèle. En effet, il est important de garantir que \(K_{ijt}\) et \(L_{jt}\) prennent bien les valeurs voulues. Pour cela, un big M est introduit. Il est défini dans les contraintes du modèle : (15) \(M = 10 \sum_{j=1}^{J} c_j\). De nouvelles contraintes utilisent ce big M pour encadrer la valeur des deux nouvelles variables de décision et forcer leur valeur. Par exemple, pour encadrer \(K_{ijt}\) les contraintes suivantes sont utilisées :

- (3.2) \(K_{ijt} - M (1 - X_{ijt}) \leq p_{jt}, \forall i.; \forall j.; \forall t.\)
  - Dans le cas où \(X_{ijt} = 1\), elle force \(K_{ijt} \leq p_{jt}\).
- (3.3) \(K_{ijt} + M (1 - X_{ijt}) \geq p_{jt}, \forall i.; \forall j.; \forall t.\)
  - Dans le cas où \(X_{ijt} = 1\), elle force \(K_{ijt} \geq p_{jt}\).
- (3.4) \(K_{ijt} - MX_{ijt} \leq 0, \forall i.; \forall j.; \forall t.\)
  - Dans le cas où \(X_{ijt} = 0\), elle force \(K_{ijt} \leq 0\).
- (16) \(K_{ijk} \geq 0\)
  - Cette contrainte force \(K_{ijt} \geq 0\).

Ces contraintes traduisent une disjonction des cas :

- Dans le cas \(X_{ijt} = 1\), alors \(P_{jt}X_{ijt} = P_{jt}\). Dans ce cas, les contraintes (3.2) et (3.3) permettent d'obtenir \(K_{ijt} = P_{jt} = P_{jt}X_{ijt}\).
- Dans le cas \(X_{ijt} = 0\), alors \(P_{jt}X_{ijt} = 0\). Dans ce cas, les contraintes (3.4) et (16) affectent \(K_{ijt}\) tel que \(K_{ijt} = 0 = P_{jt}X_{ijt}\).

De cette façon, la relation \(K_{ijt} = P_{jt}X_{ijt}\) est bien garantie.

Le même principe de linéarisation est utilisé pour garantir la valeur de la variable \(L_{jt}\). Ainsi, ce sont les contraintes (5.2), (5.3), (5.4) et (17) qui contraignent \(L_{jt}\), de sorte à ce que \(L_{jt} = P_{jt}.Y_{jt}\).

Une fois la linéarisation effective, l'enjeu est la programmation de ce modèle pour assurer une résolution. Dans un premier temps, le modèle non-linéaire (modèle non\_linear\_problem.lg4) ayant été réalisé sur Lingo, nous avons réalisé le modèle linéaire sur Lingo (modèle linear\_problem.lg4). Cependant, Lingo n'était pas adapté à un modèle linéaire de cette complexité ; les temps de calcul étaient trop longs et dépendaient de la génération aléatoire pour pouvoir correctement explorer et exploiter les résultats. C'est pour cela que nous avons travaillé sur un modèle utilisant [Gusek](https://gusek.sourceforge.net/gusek.html) et son solveur GLPK (modèle linear\_model.mod). Malheureusement, même si Gusek est fait pour les modèles linéaires, il n'était pas suffisamment puissant. C'est pour cela que nous avons réalisé le modèle sur [Gurobi](https://www.gurobi.com/), utilisant l'API sur python et sa librairie, gurobipy (modèle bundle\_model.py). En plus d'assurer un temps de calcul raisonnable (moins d'une minute par résolution), l'appel par python (fichier sensi\_analysis.py) permet d'automatiser les tests effectués par la suite.


\section{Analyse des résultats}

\subsection{Étude avec les données d'origine}

\begin{multicols}{2}
Dans cette partie, nous utilisons le modèle linéaire du \ref{linear} pour étudier les résultats et l'effet des différents paramètres. Sur la table suivante, nous avons la valeur des paramètres initiaux de l'instance.

% Tableau des paramètres d'origine
\begin{table}[H]
    \centering
    \begin{tabular}{c c c c c c c}
        \hline \hline
        I & J & T & $c_j (\$)$ & $R_{i11} (\$)$ & $\beta$ & b \\
        \hline 
        10 & 10 & 6 & $4j$ & $U(6,12)$ & 0,5 & 0,04 \\
        \hline \hline
    \end{tabular}
    \caption{Valeurs initiales des paramètres}
    \label{tab_para}
\end{table}
\columnbreak
Dans la table \ref{tab_para}, les 3 paramètres clés que sont $\beta$, b et $R_{i11}$ influent sur les valeurs de $R_{ijt}$, le prix de réservation. Pour rappel, $\beta$ affecte la réduction liée au groupement de produit, b affecte la réduction liée au temps qui passe, et $R_{i11}$ définit le prix de réservation initial du client $i$. C'est intéressant, puisque que les paramètres que l'on cherche à étudier ne représentent que le comportement de l'utilisateur, le reste est fixé ou s'adapte sur l'utilisateur.
\end{multicols}

\subsubsection{Étude du résultat d'une instance}
Pour comprendre les résultats et le fonctionnement du modèle, nous étudions tout d'abord les résultats pour une instance donnée, avec les paramètres de la table \ref{tab_para}. Ces résultats sont cependant fortement dépendants de l'aléatoire généré par la fonction uniforme concernant le prix de réservation. C'est pour cela que la valeur de génération aléatoire (\textit{random seed}) est fixée sur cette table, pour permettre de revenir aux mêmes résultats.

% Tableau des premiers résultats
\begin{table}[h]
    \begin{center}
        \begin{tabular}{c | c c c c | c c}
            \hline \hline 
            t  & Taille du pack & Prix du pack & Prix unitaire & Nombres d'acheteurs & Profit   & Surplus  \\
            \hline
            1  & 8 & 59,94 \$ & 7,49 \$ & 4,0 & \multirow{6}{*}{\centering 126,40 \$} & \multirow{6}{*}{\centering 25,86 \$} \\
            \cline{1-5}
            2  & 3  & 26,65 \$ & 8,88 \$ & 1,0 & & \\
            \cline{1-5}             
            3  & 3  & 30,59 \$ & 10,20 \$ & // & & \\
            \cline{1-5} 
            4  & 5  & 49,64 \$ & 9,93 \$ & // & & \\
            \cline{1-5} 
            5  & 0  & 0,0 \$ & 0,0 \$ & // & & \\
            \cline{1-5} 
            6  & 1  & 9,59 \$ & 9,59 \$ & // & & \\
            \hline \hline
        \end{tabular}
        \caption{Résultats de la simulation initiale (\textit{random seed} 78794)}
        \label{tab_res_1}
    \end{center}
\end{table}
\FloatBarrier

Par rapport à l'article original, nous avons fait le choix d'afficher le nombre de clients qui ont acheté le pack. Cela permet de comprendre les choix de packs proposés. De la sorte, nous pouvons voir que malgré des packs proposés à 5 périodes sur 6, seuls 5 clients achètent et seulement sur les 2 premières périodes. De cette façon, les packs proposés aux périodes 3 à 6 ne sont que peu importants, comme ils sont moins avantageux pour les clients que les précédents.

\subsubsection{Étude de la distribution des résultats en fonction de la génération aléatoire de $R_{i11}$}\label{etude_distri}
\begin{multicols}{2}
Le prix de réservation $R_{ijt}$ est basé sur une valeur unique par client $i, R_{i11}$. Ces valeurs sont générées par une loi uniforme de paramètres (6;12). Cette loi est dotée d'une moyenne de $9$, et d'un écart type d'environ $1,7$.

La figure 1 représente la distribution du profit après 100 tirages aléatoires du vecteur $R_{i11}$. Ce profit a pour moyenne $114,30$ \$ et comme médiane $113,95$ \$. Pour les paramètres équivalents, l'article annonce un profit de $156,58 \$ $, ce qui paraît être relativement loin de la médiane. On peut considérer leur résultat comme l'un des meilleurs qu'ils ont trouvés lors de leur simulation.

\columnbreak
\vspace*{\fill}
\begin{minipage}{\linewidth}
\centering
\includegraphics[width=7cm]{images/2.1.2_profit_histogramm.png}
\label{fig1}\\
Figure 1 - Distribution du profit
\end{minipage}
\vspace*{\fill}
\end{multicols}

\subsection{Analyses de sensibilité}

Comme précisé auparavant, les 3 paramètres clés sont $\beta$, $b$ et $R_{i11}$. Par la suite, nous allons étudier l'influence de ces 3 paramètres sur nos résultats, afin de pouvoir conclure sur la pertinence du choix des paramètres. Pour conserver un point de comparaison avec les premiers résultats, la valeur de génération aléatoire utilisée lors de la partie 2.1.1 est conservée pour la suite.

Pour permettre aux tableaux de données par la suite d'être compacts, les intitulés des 4 colonnes de la table \ref{tab_res_1} seront abrégés pour donner BS (Bundle size), BP (Bundle price), BP/BS (Bundle price per size : prix unitaire) et CN (Consumers numbers).

\subsubsection{Analyse de $\beta$}
Lors de l'optimisation initiale, $\beta$ avait pris la valeur de 0.5. Pour compléter cette valeur de la même façon que l'article, nous allons comparer la valeur initiale avec des simulations pour $\beta = [0,2;0,8]$. Comme vu dans la contrainte (7), $\beta$ pondère la perte de valeur des produits aux yeux des clients lorsqu'ils sont regroupés. De cette façon, plus $\beta$ est conséquent, moins les clients achèteront des packs à un prix élevé.

\begin{table}[h]
    \begin{center}
        \begin{tabular}{c || c c c c | c c c c | c c c c}
            \hline \hline
            $\beta$ & \multicolumn{4}{c|}{\(\beta = 0,2\)} & \multicolumn{4}{c|}{\(\beta = 0,5\)} & \multicolumn{4}{c}{\(\beta = 0,8\)} \\
            \hline \hline
             t & BS & BP & BP/BS & CN & BS & BP & BP/BS & CN & BS & BP & BP/BS & CN \\
            \hline
            1 & 10 & 83,06 \$ & 8,31 \$ & 5,0 & 8 & 59,94 \$ & 7,49 \$ & 4,0 & 5 & 34,64 \$ & 6,93 \$ & 3,0 \\
            \hline
            2 & 2 & 17,44 \$ & 8,72 \$ & 1,0 & 3 & 26,65 \$ & 8,88 \$ & 1,0 & 2 & 13,45 \$ & 6,73 \$ & 6,0 \\
            \hline
            3 & 5 & 41,90 \$ & 8,38 \$ & // & 3 & 30,59 \$ & 10,20 \$ & // & 10 & 164,26 \$ & 16,43 \$ & // \\
            \hline
            4 & 0 & 0,00 \$ & 0,00 \$ & // & 5 & 49,64 \$ & 9,93 \$ & // & 10 & 157,82 \$ & 15,78 \$ & // \\
            \hline
            5 & 0 & 0,00 \$ & 0,00 \$ & // & 0 & 0,00 \$ & 0,00 \$ & // & 10 & 151,63 \$ & 15,16 \$ & // \\
            \hline
            6 & 1 & 9,09 \$ & 9,09 \$ & // & 1 & 9,59 \$ & 9,59 \$ & // & 0 & 0,00 \$ & 0,00 \$ & // \\
            \hline \hline
            Profit & \multicolumn{4}{c|}{127,50 \$} & \multicolumn{4}{c|}{126,40 \$} & \multicolumn{4}{c}{162,00 \$} \\
            \hline \hline
        \end{tabular}
        \caption{Influence de $\beta$ sur les résultats de simulation}
        \label{tab_beta}
    \end{center}
\end{table}
\FloatBarrier

Les résultats de la table \ref{tab_beta} confirment que les clients sont moins enclins à acheter un pack quand $\beta$ est élevé. Les valeurs profit par période sont fortement influencées par $\beta$, allant de 127,50 \$ pour $\beta = 0,2$ à 162,00 \$ pour $\beta = 0,8$.

\subsubsection{Analyse de b}
Lors de l'optimisation initiale, b avait pris la valeur de 0.04. Pour compléter cette valeur de la même façon que l'article, nous allons comparer la valeur initiale avec des simulations pour b = [0.02; 0.06]. Comme vu dans la contrainte (7), b pondère la perte de valeur des produits aux yeux des clients au fur et à mesure que le temps passe. De cette façon, plus b est conséquent, plus les clients achèteront des packs dès le début de la période.

\begin{table}[h]
    \begin{center}
        \begin{tabular}{c || c c c c | c c c c | c c c c}
            \hline \hline
            b & \multicolumn{4}{c|}{\(b = 0,02\)} & \multicolumn{4}{c|}{\(b = 0,04\)} & \multicolumn{4}{c}{\(b = 0,06\)} \\
            \hline \hline
             t & BS & BP & BP/BS & CN & BS & BP & BP/BS & CN & BS & BP & BP/BS & CN \\
            \hline
            1 & 8 & 58,38 \$ & 7,30 \$ & 5,0 & 8 & 59,94 \$ & 7,49 \$ & 4,0 & 10 & 76,80 \$ & 7,68 \$ & 6,0 \\
            \hline
            2 & 6 & 58,98 \$ & 9,83 \$ & 2,0 & 3 & 26,65 \$ & 8,88 \$ & 1,0 & 1 & 6,52 \$ & 6,52 \$ & // \\
            \hline
            3 & 1 & 10,14 \$ & 10,14 \$ & // & 3 & 30,59 \$ & 10,20 \$ & // & 3 & 29,91 \$ & 9,97 \$ & // \\
            \hline
            4 & 2 & 16,18 \$ & 8,09 \$ & // & 5 & 49,64 \$ & 9,93 \$ & // & 3 & 28,43 \$ & 9,48 \$ & // \\
            \hline
            5 & 0 & 0,00 \$ & 0,00 \$ & // & 0 & 0,00 \$ & 0,00 \$ & // & 0 & 0,00 \$ & 0,00 \$ & // \\
            \hline
            6 & 0 & 0,00 \$ & 0,00 \$ & // & 1 & 9,59 \$ & 9,59 \$ & // & 0 & 0,00 \$ & 0,00 \$ & // \\
            \hline \hline
            Profit & \multicolumn{4}{c|}{143,70 \$} & \multicolumn{4}{c|}{126,40 \$} & \multicolumn{4}{c}{141,66 \$} \\
            \hline \hline
        \end{tabular}
        \caption{Influence de b sur les résultats de simulation}
        \label{tab_b}
    \end{center}
\end{table}
\FloatBarrier

Les résultats de la table \ref{tab_b} confirment que les clients sont plus enclins à acheter des packs en début de période quand b est élevé. Les valeurs profit par période sont légèrement influencées par b, allant de 126,40 \$ pour b = 0,04 à 143,70 \$ pour b = 0,02.

\subsubsection{Analyse de $R_{i11}$}
La génération aléatoire de $R_{i11}$ est influencée par les paramètres de la loi uniforme (6;12). Pour analyser l'impact de cette loi, nous avons simulé plusieurs résultats avec des lois différentes. Pour rappel, $R_{i11}$ est utilisé pour définir le prix de réservation initial des clients. La loi uniforme permet de simuler des valeurs de prix de réservation variant entre 6 et 12.

\begin{table}[h]
    \begin{center}
        \begin{tabular}{c || c c c c | c c c c | c c c c}
            \hline \hline
            \(R_{i11}\) & \multicolumn{4}{c|}{U(5;10)} & \multicolumn{4}{c|}{U(6;12)} & \multicolumn{4}{c}{U(7;14)} \\
            \hline \hline
             t & BS & BP & BP/BS & CN & BS & BP & BP/BS & CN & BS & BP & BP/BS & CN \\
            \hline
            1 & 8 & 53,25 \$ & 6,66 \$ & 4,0 & 8 & 59,94 \$ & 7,49 \$ & 4,0 & 10 & 81,31 \$ & 8,13 \$ & 5,0 \\
            \hline
            2 & 3 & 26,32 \$ & 8,77 \$ & 1,0 & 3 & 26,65 \$ & 8,88 \$ & 1,0 & 2 & 17,00 \$ & 8,50 \$ & 1,0 \\
            \hline
            3 & 3 & 30,45 \$ & 10,15 \$ & // & 3 & 30,59 \$ & 10,20 \$ & // & 1 & 8,78 \$ & 8,78 \$ & // \\
            \hline
            4 & 5 & 49,45 \$ & 9,89 \$ & // & 5 & 49,64 \$ & 9,93 \$ & // & 1 & 9,07 \$ & 9,07 \$ & // \\
            \hline
            5 & 0 & 0,00 \$ & 0,00 \$ & // & 0 & 0,00 \$ & 0,00 \$ & // & 0 & 0,00 \$ & 0,00 \$ & // \\
            \hline
            6 & 1 & 8,96 \$ & 8,96 \$ & // & 1 & 9,59 \$ & 9,59 \$ & // & 0 & 0,00 \$ & 0,00 \$ & // \\
            \hline \hline
            Profit & \multicolumn{4}{c|}{121,43 \$} & \multicolumn{4}{c|}{126,40 \$} & \multicolumn{4}{c}{116,15 \$} \\
            \hline \hline
        \end{tabular}
        \caption{Influence de $R_{i11}$ sur les résultats de simulation}
        \label{tab_r}
    \end{center}
\end{table}
\FloatBarrier

Les résultats de la table \ref{tab_r} montrent que la génération aléatoire de $R_{i11}$ influence les résultats de simulation. Les valeurs profit par période varient en fonction de la loi uniforme utilisée, allant de 116,15 \$ pour U(7;14) à 126,40 \$ pour U(6;12). Cela montre que le choix de la loi uniforme pour la génération de $R_{i11}$ a un impact sur les résultats de simulation.

\subsection{Conclusion}

L'analyse des résultats a montré que les paramètres $\beta$, b et $R_{i11}$ ont une influence significative sur les résultats de simulation. Les variations de ces paramètres peuvent affecter les valeurs profit par période et le comportement des clients. Il est donc important de bien choisir les valeurs de ces paramètres pour obtenir des résultats optimaux.

