from pyomo.environ import *
from pyomo.solvers.plugins import *
from pyomo.opt import SolverFactory
from bentso.filesystem import create_dir
from bentso.client import CachingDataClient
import pandas as pd
import os

def LoadModelData():
    cwd = os.getcwd()
    temp_path = os.path.join(cwd,'temp_opt')
    data = DataPortal()
    data.load(filename= os.path.join(temp_path,'spot_prices.csv'),format='set', set='H')
    data.load(filename= os.path.join(temp_path,'spot_prices.csv'),index='H',param='ClearingPrice')
    data.load(filename= os.path.join(temp_path,'storage_generation.csv'),index='H', param='gen_phs')
    data.load(filename= os.path.join(temp_path,'scalar.dat'))
    return data
    
def StorageConsumptionAllocation(sense):
    
    m = AbstractModel()
    # Sets
    m.H = Set() # time
    # Parameters
    m.ClearingPrice= Param(m.H) # get_day_ahead_prices from ENTSOE
    m.gen_phs = Param(m.H)
    m.cap_phs = Param()
    m.storage_hours = Param()
    m.roundtrip_eff = Param()
    m.initial_E_share = Param()
    # Variables
    m.CONSUMPTION_phs = Var(m.H, domain=NonNegativeReals)
    m.ENERGY_LEVEL_phs = Var(m.H, domain=NonNegativeReals)
    # m.cap_phs = Var(domain=NonNegativeReals) # if this code is enable then the parameter must be commented out. When m.cap_phs is variable the capacity is determined.
    def expression_max_ngr(m):
        return  m.storage_hours * m.cap_phs
    m.MAX_ENERGY_phs = Expression(rule=expression_max_ngr)
    def objective_rule(m):
        return sum(m.CONSUMPTION_phs[h]*m.ClearingPrice[h] for h in m.H)
    # verify the data of clearing price to check if the generation ocours at pick prices, in that case set 'sense=minimize'
    m.OBJ = Objective(rule=objective_rule,sense=sense)
    def C1(m,h):
        if h == 0:
            return m.ENERGY_LEVEL_phs[h] == m.initial_E_share*m.MAX_ENERGY_phs + m.CONSUMPTION_phs[h]*(m.roundtrip_eff+1)/2 - m.gen_phs[h]/(m.roundtrip_eff+1)*2
        else:
            return m.ENERGY_LEVEL_phs[h] == m.ENERGY_LEVEL_phs[h-1] + m.CONSUMPTION_phs[h]*(m.roundtrip_eff+1)/2 - m.gen_phs[h]/(m.roundtrip_eff+1)*2
    m.C1 = Constraint(m.H, rule=C1)
    def C2(m,h):
        return m.ENERGY_LEVEL_phs[h] <= m.MAX_ENERGY_phs
    m.C2 = Constraint(m.H, rule=C2)
    def C3(m,h):
        return m.CONSUMPTION_phs[h] <= m.cap_phs - m.gen_phs[h]
    m.C3 = Constraint(m.H, rule=C3)
    return m

# LP model

class Model:
    """docstring for "ctr,year,storage_hours = 6, roundtrip_eff = 0.7, initial_E_share = 1, sense = 1"  """
    def __init__(self,ctr,year,storage_hours = 6, roundtrip_eff = 0.7, initial_E_share = 1, sense = 1):
        self.ctr = ctr
        self.year = year
        self.storage_hours = storage_hours
        self.roundtrip_eff = roundtrip_eff
        self.initial_E_share = initial_E_share
        self.sense = sense
        
    def run(self):
        
        self.cwd = os.getcwd()
        self.temp_path = os.path.join(self.cwd,'temp_opt')
        create_dir(self.temp_path)
        
        c = CachingDataClient()
        self.ctr_yr = c.get_generation(self.ctr,self.year)
        self.ctr_price = c.get_day_ahead_prices(self.ctr,self.year)
        self.ctr_cap = c.get_capacity(self.ctr,self.year)
        '''
        here we have to check the resolution of the data,
        for the optimization model the amount of rows of generation file and price file should be equal.
        DE 2016 presents the generation every 15 minutes while the prices is hourly.
        Now the model shows an error for this case.
        '''
        self.gen = pd.DataFrame(self.ctr_yr['Hydro Pumped Storage']).reset_index(drop=True).rename(columns={'Hydro Pumped Storage':'gen_phs'})
        self.pcs = pd.DataFrame(self.ctr_price, columns=['ClearingPrice']).reset_index(drop=True)
        self.gen.to_csv(os.path.join(self.temp_path,'storage_generation.csv'),index_label='H')
        self.pcs.to_csv(os.path.join(self.temp_path,'spot_prices.csv'),index_label='H')
        if len(self.gen) == len(self.pcs):
            self.cap_phs = self.ctr_cap['Hydro Pumped Storage'][0]
            self.scalar = {'cap_phs':self.cap_phs,'storage_hours':self.storage_hours,'roundtrip_eff':self.roundtrip_eff,'initial_E_share':self.initial_E_share}

            self.f=open(os.path.join(self.temp_path,"scalar.dat"), "w+")
            for k, v in self.scalar.items():
                 self.f.write("table %s := %f; \r\n"%(k,v))
            self.f.close()
            self.LP = StorageConsumptionAllocation(self.sense)
            self.data = LoadModelData()
            self.instance = self.LP.create_instance(self.data)
            self.opt = SolverFactory('clp') # clp is the solver, in windows the .exe file has to be stated as the example: SolverFactory('glpk', executable='C:/bin/glpk/w64/glpsol.exe')
            self.outcome = self.opt.solve(self.instance,symbolic_solver_labels=False,tee=False,keepfiles = False)
        else:
            print('in the optimization length not match for price and gen')
            raise Exception('Price data length is not equal to generation data length... for %s and %d'%(self.ctr,self.year))

        self.cons_list = []
        for h in self.instance.H.value:
            self.cons_list.append({'Cons_phs':round(value(self.instance.CONSUMPTION_phs[h]),1)})

        self.consumption_phs = pd.DataFrame(self.cons_list)
        self.ctr_yr.reset_index(drop=True,inplace=True)
        self.new = self.ctr_yr.copy()
        self.new.drop('Hydro Pumped Storage',axis=1,inplace=True)
        self.ctr_gen = pd.DataFrame()
        self.ctr_gen = self.new.apply(lambda row: row/row.sum(),axis=1)*self.consumption_phs.values
        self.ctr_year = self.new - self.ctr_gen
        self.ctr_year.loc[:,'Hydro Pumped Storage'] = self.ctr_yr['Hydro Pumped Storage']
        return self.ctr_year
