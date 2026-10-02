"""Numeric aggregates and fixed-baseline evaluation. No train or merge methods."""
import math

def number(value):
    if type(value) not in (int,float) or not math.isfinite(value) or abs(value)>1e100:
        raise ValueError('Expected bounded finite number')
    return value

def state_values(state,keys):
    if type(state) is not dict or set(state)!=set(keys):
        raise ValueError('Invalid state fields')
    if type(state['n']) is not int or not 0<=state['n']<=10**9:
        raise ValueError('Invalid count')
    for key in keys:
        if key!='n':number(state[key])
    return state

class Numeric:
    version='numeric/1'
    def __init__(self,state=None):
        self.values=state_values(dict(n=0,mean=0.0,m2=0.0) if state is None else dict(state),('n','mean','m2'))
        if self.values['m2']<0 or (not self.values['n'] and (self.values['mean'] or self.values['m2'])):
            raise ValueError('Inconsistent numeric state')
    def process(self,value):
        value=number(value)
        if abs(value)>1e40:raise ValueError("Input range")
        n=self.values['n']+1
        if n>10**9:raise ValueError('Count limit')
        delta=value-self.values['mean']
        mean=self.values['mean']+delta/n
        m2=self.values['m2']+delta*(value-mean)
        state_values(dict(n=n,mean=mean,m2=m2),('n','mean','m2'))
        self.values=dict(n=n,mean=mean,m2=m2)
        return dict(count=n,mean=mean,sample_variance=m2/(n-1) if n>1 else None)
    def state(self):return dict(self.values)

class Evaluator:
    version='evaluator/1'
    def __init__(self,state=None):
        self.values=state_values(dict(n=0,absolute_error=0.0,squared_error=0.0) if state is None else dict(state),('n','absolute_error','squared_error'))
        if self.values['absolute_error']<0 or self.values['squared_error']<0:
            raise ValueError('Invalid errors')
    def process(self,value):
        if type(value) is not dict or set(value)!={'prediction','target'}:
            raise ValueError('Expected prediction and held-out target')
        prediction,target=number(value['prediction']),number(value['target'])
        if abs(prediction)>1e40 or abs(target)>1e40:raise ValueError('Input range')
        error=prediction-target
        n=self.values['n']+1
        if n>10**9:raise ValueError('Count limit')
        absolute=self.values['absolute_error']+abs(error)
        squared=self.values['squared_error']+error*error
        state_values(dict(n=n,absolute_error=absolute,squared_error=squared),('n','absolute_error','squared_error'))
        self.values=dict(n=n,absolute_error=absolute,squared_error=squared)
        return dict(count=n,mae=absolute/n,rmse=math.sqrt(squared/n))
    def state(self):return dict(self.values)

REGISTRY={'numeric':Numeric,'evaluator':Evaluator}
