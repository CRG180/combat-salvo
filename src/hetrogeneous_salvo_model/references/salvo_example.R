#A_i units  3 x units " Red in python code"
#B_j units  4 x units  " blue in python code"

# Matrix operations for Attrition of A units

# O is an j X i  matrix 
# This matrix describes how many shot each "B" unit type (B1, B2 ..) fires at each "A" unit type 
#             B1  B2 B3 B4
(O <-matrix(c( 2, 0,  1, 0,  #A1  So, Type B1 fires 2 rnds at Type A1 and Type B3 fires 1 rnd at A1
               0, .8, 0, 0,  #A2  So, Type A2 fires a degraded shot at Type B2 Maybe due to bad scouting..  
               0,  0, 0, 2  #A3   You get the point 
),
nrow = 3, byrow = T))
dim(O)

(B <- matrix(c(20,   #B1 # there are 20x B1 type units
               30,   #B2
               22,   #B3
               12))) #B4 

dim(B)
(off <-O %*% B) #  3 x 1 in terms of A_i units 
# "A units about to be his with this array of salvos


# D is an  i X i  matrix         Each row value is a sum defense coefficient on the diag
#               A1  A2  A3       #A1  D11 + .. + .. D1j  So this is Dot product really 
(D <- matrix(c( 1,  0,  0, #A1    (A1 vs B1)  + (A1 vs B2) + (A1 vs B3) + (A1 vs B4)   
                0,  1,  0, #A2    (A2 vs B1)  + (A2 vs B2) + (A2 vs B3) + (A2 vs B4)  
                0,  0,  2),#A3    (A3 vs B1)  + (A3 vs B2) + (A3 vs B3) + (A3 vs B4)  
             ncol =3, byrow = T))


(A <- matrix(c(10, #A1 there are 10x A1 type unis
               20, #A2
               30)))#A3


(def <- D %*% A)

(loss <- off - def)  # adjudication needs to occur if 
#1) neg value change to zero, because A can over defend  

(A - loss)  #        # adjudication needs to occur if value is neg because the unit is wiped out. 