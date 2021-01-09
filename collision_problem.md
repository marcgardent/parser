## Equation

```maxima

solve((x_a+ x_av*t - (x_b+ x_bv*t))^2+(y_a+ y_av*t - (y_b+y_bv*t))^2=(r_a+r_b)^2,t);

## Prepare smoketest
```
ev((-sqrt((-x_b^2+2*x_a*x_b-x_a^2+r_b^2+2*r_a*r_b+r_a^2)*y_bv^2+(((2*x_b-2*x_a)*x_bv-2*x_av*x_b+2*x_a*x_av)*y_b+(2*x_b^2-4*x_a*x_b+2*x_a^2-2*r_b^2-4*r_a*r_b-2*r_a^2)*y_av+((2*x_a-2*x_b)*x_bv+2*x_av*x_b-2*x_a*x_av)*y_a)*y_bv+(-x_bv^2+2*x_av*x_bv-x_av^2)*y_b^2+(((2*x_a-2*x_b)*x_bv+2*x_av*x_b-2*x_a*x_av)*y_av+(2*x_bv^2-4*x_av*x_bv+2*x_av^2)*y_a)*y_b+(-x_b^2+2*x_a*x_b-x_a^2+r_b^2+2*r_a*r_b+r_a^2)*y_av^2+((2*x_b-2*x_a)*x_bv-2*x_av*x_b+2*x_a*x_av)*y_a*y_av+(-x_bv^2+2*x_av*x_bv-x_av^2)*y_a^2+(r_b^2+2*r_a*r_b+r_a^2)*x_bv^2+(-2*r_b^2-4*r_a*r_b-2*r_a^2)*x_av*x_bv+(r_b^2+2*r_a*r_b+r_a^2)*x_av^2)-(y_b-y_a)*y_bv+y_av*y_b-y_a*y_av-(x_b-x_a)*x_bv+x_av*x_b-x_a*x_av)/(y_bv^2-2*y_av*y_bv+y_av^2+x_bv^2-2*x_av*x_bv+x_av^2), r_a = 5,r_b = 10,x_a = 1,x_av = 2,x_b = 3,x_bv = 4,y_a = 5,y_av = 6,y_b = 7,y_bv = 8)

(-15*2^(3/2)-8)/8 = -6.303300858899107
```

## Compress expression
 
 ```sh

 py .\compress.py --language 'pseudocode' --expression '(-sqrt((-x_b^2+2*x_a*x_b-x_a^2+r_b^2+2*r_a*r_b+r_a^2)*y_bv^2+(((2*x_b-2*x_a)*x_bv-2*x_av*x_b+2*x_a*x_av)*y_b+(2*x_b^2-4*x_a*x_b+2*x_a^2-2*r_b^2-4*r_a*r_b-2*r_a^2)*y_av+((2*x_a-2*x_b)*x_bv+2*x_av*x_b-2*x_a*x_av)*y_a)*y_bv+(-x_bv^2+2*x_av*x_bv-x_av^2)*y_b^2+(((2*x_a-2*x_b)*x_bv+2*x_av*x_b-2*x_a*x_av)*y_av+(2*x_bv^2-4*x_av*x_bv+2*x_av^2)*y_a)*y_b+(-x_b^2+2*x_a*x_b-x_a^2+r_b^2+2*r_a*r_b+r_a^2)*y_av^2+((2*x_b-2*x_a)*x_bv-2*x_av*x_b+2*x_a*x_av)*y_a*y_av+(-x_bv^2+2*x_av*x_bv-x_av^2)*y_a^2+(r_b^2+2*r_a*r_b+r_a^2)*x_bv^2+(-2*r_b^2-4*r_a*r_b-2*r_a^2)*x_av*x_bv+(r_b^2+2*r_a*r_b+r_a^2)*x_av^2)-(y_b-y_a)*y_bv+y_av*y_b-y_a*y_av-(x_b-x_a)*x_bv+x_av*x_b-x_a*x_av)/(y_bv^2-2*y_av*y_bv+y_av^2+x_bv^2-2*x_av*x_bv+x_av^2)'
 ```



 ```python
import math

def f_vanilla(r_a, r_b, x_a, x_av, x_b, x_bv, y_a, y_av, y_b, y_bv):
    return (-math.sqrt((math.pow(-x_b,2)+2*x_a*x_b-math.pow(x_a,2)+math.pow(r_b,2)+2*r_a*r_b+math.pow(r_a,2))*math.pow(y_bv,2)+(((2*x_b-2*x_a)*x_bv-2*x_av*x_b+2*x_a*x_av)*y_b+(2*math.pow(x_b,2)-4*x_a*x_b+2*math.pow(x_a,2)-2*math.pow(r_b,2)-4*r_a*r_b-2*math.pow(r_a,2))*y_av+((2*x_a-2*x_b)*x_bv+2*x_av*x_b-2*x_a*x_av)*y_a)*y_bv+(math.pow(-x_bv,2)+2*x_av*x_bv-math.pow(x_av,2))*math.pow(y_b,2)+(((2*x_a-2*x_b)*x_bv+2*x_av*x_b-2*x_a*x_av)*y_av+(2*math.pow(x_bv,2)-4*x_av*x_bv+2*math.pow(x_av,2))*y_a)*y_b+(math.pow(-x_b,2)+2*x_a*x_b-math.pow(x_a,2)+math.pow(r_b,2)+2*r_a*r_b+math.pow(r_a,2))*math.pow(y_av,2)+((2*x_b-2*x_a)*x_bv-2*x_av*x_b+2*x_a*x_av)*y_a*y_av+(math.pow(-x_bv,2)+2*x_av*x_bv-math.pow(x_av,2))*math.pow(y_a,2)+(math.pow(r_b,2)+2*r_a*r_b+math.pow(r_a,2))*math.pow(x_bv,2)+(-2*math.pow(r_b,2)-4*r_a*r_b-2*math.pow(r_a,2))*x_av*x_bv+(math.pow(r_b,2)+2*r_a*r_b+math.pow(r_a,2))*math.pow(x_av,2))-(y_b-y_a)*y_bv+y_av*y_b-y_a*y_av-(x_b-x_a)*x_bv+x_av*x_b-x_a*x_av)/(math.pow(y_bv,2)-2*y_av*y_bv+math.pow(y_av,2)+math.pow(x_bv,2)-2*x_av*x_bv+math.pow(x_av,2))

def f_compressed(r_a, r_b, x_a, x_av, x_b, x_bv, y_a, y_av, y_b, y_bv):
  v0 = x_b*2
  v1 = x_a*2
  v2 = v0-v1
  v3 = x_bv*(v2)
  v4 = x_av*v1
  v5 = x_av*2
  v6 = x_b*v5
  v7 = v3-v6
  v8 = v7+v4
  v9 = math.pow(x_a,2)
  v10 = math.pow(r_b,2)
  v11 = r_a*4
  v12 = v11*r_b
  v13 = math.pow(r_a,2)
  v14 = v13*2
  v15 = v1-v0
  v16 = x_bv*(v15)
  v17 = v6+v16
  v18 = v17-v4
  v19 = math.pow(y_bv,2)
  v20 = x_b*v1
  v21 = math.pow(-x_b,2)
  v22 = v21+v20
  v23 = v22-v9
  v24 = v23+v10
  v25 = r_a*2
  v26 = v25*r_b
  v27 = v26+v24
  v28 = math.pow(x_bv,2)
  v29 = math.pow(x_av,2)
  v30 = x_bv*v5
  v31 = math.pow(-x_bv,2)
  v32 = v31+v30
  v33 = v32-v29
  v34 = math.pow(y_av,2)
  v35 = v26+v13
  return (y_b*y_av+-math.sqrt(y_bv*(y_b*(v8)+y_av*(v9*2+math.pow(x_b,2)*2-x_b*x_a*4-v10*2-v12-v14)+y_a*(v18))+v19*(v27+v13)+y_b*(y_av*(v18)+y_a*(v29*2+v28*2-x_bv*x_av*4))+math.pow(y_b,2)*(v33)+y_av*y_a*(v8)+v34*(v27+v13)+v28*(v35+v10)+math.pow(y_a,2)*(v33)+x_bv*x_av*(v10*-2-v12-v14)+v29*(v35+v10))-y_bv*(y_b-y_a)-y_av*y_a-x_bv*(x_b-x_a)+x_b*x_av-x_av*x_a)/(v34+v28+v19-y_bv*y_av*2-v30+v29)     
   
```

## Results

```
--------------------------------------------------------------------------------------- benchmark: 4 tests --------------------------------------------------------------------------------------
Name (time in us)                  Min                Max              Mean            StdDev            Median               IQR            Outliers  OPS (Kops/s)            Rounds  Iterations      
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------      
test_f_compressed_nopower       2.7087 (1.0)       5.6087 (1.0)      2.9854 (1.0)      0.5388 (1.0)      2.7413 (1.0)      0.0440 (1.33)      287;433      334.9596 (1.0)        1984         184      
test_f_compressed_power_fun     3.2286 (1.19)      6.1877 (1.10)     3.5977 (1.21)     0.7036 (1.31)     3.2682 (1.19)     0.0786 (2.38)      309;436      277.9526 (0.83)       1982         154      
test_f_compressed               4.5312 (1.67)     10.0046 (1.78)     4.7728 (1.60)     0.6027 (1.12)     4.5688 (1.67)     0.0330 (1.0)       186;360      209.5197 (0.63)       1987         109
test_f_vanilla                  8.7440 (3.23)     21.3360 (3.80)     9.6971 (3.25)     1.6887 (3.13)     8.8100 (3.21)     1.2415 (37.59)     153;124      103.1237 (0.31)       1136         100      
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------      
```