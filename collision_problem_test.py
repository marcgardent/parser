# pip install pytest-benchmark
import math
import time
import random

def f_vanilla(r_a, r_b, x_a, x_av, x_b, x_bv, y_a, y_av, y_b, y_bv):
    return (-math.sqrt((math.pow(-x_b,2)+2*x_a*x_b-math.pow(x_a,2)+math.pow(r_b,2)+2*r_a*r_b+math.pow(r_a,2))*math.pow(y_bv,2)+(((2*x_b-2*x_a)*x_bv-2*x_av*x_b+2*x_a*x_av)*y_b+(2*math.pow(x_b,2)-4*x_a*x_b+2*math.pow(x_a,2)-2*math.pow(r_b,2)-4*r_a*r_b-2*math.pow(r_a,2))*y_av+((2*x_a-2*x_b)*x_bv+2*x_av*x_b-2*x_a*x_av)*y_a)*y_bv+(math.pow(-x_bv,2)+2*x_av*x_bv-math.pow(x_av,2))*math.pow(y_b,2)+(((2*x_a-2*x_b)*x_bv+2*x_av*x_b-2*x_a*x_av)*y_av+(2*math.pow(x_bv,2)-4*x_av*x_bv+2*math.pow(x_av,2))*y_a)*y_b+(math.pow(-x_b,2)+2*x_a*x_b-math.pow(x_a,2)+math.pow(r_b,2)+2*r_a*r_b+math.pow(r_a,2))*math.pow(y_av,2)+((2*x_b-2*x_a)*x_bv-2*x_av*x_b+2*x_a*x_av)*y_a*y_av+(math.pow(-x_bv,2)+2*x_av*x_bv-math.pow(x_av,2))*math.pow(y_a,2)+(math.pow(r_b,2)+2*r_a*r_b+math.pow(r_a,2))*math.pow(x_bv,2)+(-2*math.pow(r_b,2)-4*r_a*r_b-2*math.pow(r_a,2))*x_av*x_bv+(math.pow(r_b,2)+2*r_a*r_b+math.pow(r_a,2))*math.pow(x_av,2))-(y_b-y_a)*y_bv+y_av*y_b-y_a*y_av-(x_b-x_a)*x_bv+x_av*x_b-x_a*x_av)/(math.pow(y_bv,2)-2*y_av*y_bv+math.pow(y_av,2)+math.pow(x_bv,2)-2*x_av*x_bv+math.pow(x_av,2))

def f_compressed(r_a, r_b, x_a, x_av, x_b, x_bv, y_a, y_av, y_b, y_bv):
  v0 = x_b*2
  v1 = x_a*2
  v2 = x_b*v1
  v3 = v2+-x_b*x_b
  v4 = v3-x_a*x_a
  v5 = v4+r_b*r_b
  v6 = r_a*2
  v7 = v6*r_b
  v8 = v7+v5
  v9 = v0-v1
  v10 = x_bv*(v9)
  v11 = x_av*v1
  v12 = x_av*2
  v13 = x_b*v12
  v14 = v10-v13
  v15 = v14+v11
  v16 = r_b*r_b*2
  v17 = r_a*4
  v18 = v17*r_b
  v19 = r_a*r_a*2
  v20 = v1-v0
  v21 = x_bv*(v20)
  v22 = v21+v13
  v23 = v22-v11
  v24 = x_bv*v12
  v25 = v24+-x_bv*x_bv
  v26 = v25-x_av*x_av
  v27 = v7+r_b*r_b
  return (y_b*y_av+-math.sqrt(y_bv*y_bv*(v8+r_a*r_a)+y_bv*(y_b*(v15)+y_av*(x_b*x_b*2-x_b*x_a*4+x_a*x_a*2-v16-v18-v19)+y_a*(v23))+y_b*y_b*(v26)+y_b*(y_av*(v23)+y_a*(x_bv*x_bv*2-x_bv*x_av*4+x_av*x_av*2))+y_av*y_av*(v8+r_a*r_a)+y_av*y_a*(v15)+y_a*y_a*(v26)+x_bv*x_bv*(v27+r_a*r_a)+x_bv*x_av*(-v16-v18-v19)+x_av*x_av*(v27+r_a*r_a))-y_bv*(y_b-y_a)-y_av*y_a-x_bv*(x_b-x_a)+x_b*x_av-x_av*x_a)/(y_bv*y_bv-y_bv*y_av*2+y_av*y_av+x_bv*x_bv-v24+x_av*x_av)
def test_f_compressed(benchmark):

    benchmark(f_compressed, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
 
if __name__ == '__main__':
    r_a = 5
    r_b = 10
    x_a = 1
    x_av = 2
    x_b = 3
    x_bv = 4
    y_a = 5
    y_av = 6
    y_b = 7
    y_bv = 8


    print(f_vanilla(r_a, r_b, x_a, x_av, x_b, x_bv, y_a, y_av, y_b, y_bv))
    print(f_compressed(r_a, r_b, x_a, x_av, x_b, x_bv, y_a, y_av, y_b, y_bv))

