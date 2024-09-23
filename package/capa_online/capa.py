from .utils import *

def capa_normal_mean(size) :
    return (normal_mean(size),
            lambda x,beta,beta_dash : x*x,
            lambda x,beta,beta_dash : 1 + beta_dash)

def capa_cpts(cpts) :
    value,_,cardinality,_,_ = cpts
    pos = cardinality() - 1
    locations = []
    while pos > 0 :
        location,category = value(pos) # no anomaly
        if category == 0 : # collective anomaly
            locations.insert(0,(pos-location,pos))
        pos = pos - location
        if category == 2 : # point anomaly
            locations.insert(0,pos)
    return locations

def capa(cost,beta,beta_dash) :
    C1,C2,C3 = cost
    cost = C1
    _,_,_,capacity,_ = cost
    F = class_ordered_function(deque([],maxlen=capacity()))
    cpts = class_ordered_function(deque([],maxlen=capacity()))
    S = (cost,F,cpts)
    def push(x) :
        nonlocal S,beta,beta_dash
        (_,_,_,capacity,_),(value,_,cardinality,_,_),_ = S
        fprev = inf
        if cardinality() > 1 :
            fprev = value(cardinality()-1)
        _,F,cpts = S = op(S,x,beta)
        value,_,cardinality,push,insert = F
        f = value(cardinality()-1)
        value,_,cardinality,_,_ = cpts
        pos = value(cardinality()-1)
        value,category = min((f,0),(fprev+C2(x,beta,beta_dash),1),(fprev+C3(x,beta,beta_dash),2))
        insert(cardinality()-1,value)
        _,_,cardinality,_,insert = cpts
        insert(cardinality()-1,(pos,category))
        S = scale_F(S)
        return capa_cpts(cpts)
    return push
