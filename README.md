# Combat-salvo

Combat salvo provides two low-resolution models: homogeneous and heterogeneous salvo models based on the work published by CAPT Wayne P. Hughes. The homogeneous model aggregates two forces to assess attrition via differential equations representing the offensive and defensive capabilities of each side. The heterogeneous model accounts for multiple units in each force to provide understanding of the contribution of system or units to a greater force.  


# Project is a work in progress and not ready for use 

## Areas for contribution

### Homogeneous Model

* DOE input support

+ Data output attributes

+ Data visualization of results 



### Heterogeneous Model

* Unit Test

+ Dynamic targeting between iterations

+ DOE input support

+ Map visualization (Flask, leaflet map viz possibly) 

+ Output visualization

+ Defense matrix trouble shooting



## R Code to help understanding of the the Heterogeneous Salvo Model 

```
#A_i units  3 x units
#B_j units  4 x units

# Matrix operations for Attrition of A units

# O is an j X i  matrix 
# This matrix describes how many shot each "B" unit type (B1, B2 ..) fires at each "A" unit type 
#             B1  B2 B3 B4
(O <-matrix(c( 2, 0,  1, 0,  #A1  So, Type B1 fires 2 rnds at type A1 and type B3 fires 1 rnd at A1
               0, .8, 0, 0,  #A2  So, Type A2 fires a degraded shot at type B2 Maybe due to bad scouting..  
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
                # "A units about to be hit with this array of salvos


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

```

