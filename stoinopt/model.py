from pyomo.environ import *
from pyomo.solvers.plugins import *
from pyomo.opt import SolverFactory
from .filesystem import create_dir
from .client import CachingDataClient
import os

# LP model
     
def LoadModelData():
    cwd = os.getcwd()
    temp_path = os.path.join(cwd,'temp_opt')
    data = DataPortal()
    data.load(filename= os.path.join(temp_path,'spot_prices.csv'),format='set', set='H')
    data.load(filename= os.path.join(temp_path,'spot_prices.csv'),index='H',param='ClearingPrice')
    data.load(filename= os.path.join(temp_path,'storage_generation.csv'),index='H', param='gen_phs')
    data.load(filename= os.path.join(temp_path,'scalar.dat'))
    return data
    
def StorageConsumptionAllocation():
    
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
    m.OBJ = Objective(rule=objective_rule,sense=maximize)
    
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
    
    
def PHS_consumption_subtraction(ctr,year,storage_hours = 6, roundtrip_eff = 0.7, initial_E_share = 1):
    
    cwd = os.getcwd()
    temp_path = os.path.join(cwd,'temp_opt')
    create_dir(temp_path)
    
    #here is missing call
    
    ctr_yr = c.get_generation(ctr,year)
    ctr_price = c.get_day_ahead_prices(ctr,year)
    ctr_cap = c.get_capacity(ctr,year)
    '''
    here we have to check the resolution of the data,
    for the optimization model the amount of rows of generation file and price file should be equal.
    DE 2016 presents the generation every 15 minutes while the prices is hourly.
    Now the model shows an error for this case.
    '''
    gen = pd.DataFrame(ctr_yr['Hydro Pumped Storage']).reset_index(drop=True).rename(columns={'Hydro Pumped Storage':'gen_phs'})
    pcs = pd.DataFrame(ctr_price, columns=['ClearingPrice']).reset_index(drop=True)
    gen.to_csv(os.path.join(temp_path,'storage_generation.csv'),index_label='H')
    pcs.to_csv(os.path.join(temp_path,'spot_prices.csv'),index_label='H')
    if len(gen) == len(pcs):
        cap_phs = ctr_cap['Hydro Pumped Storage'][0]
        scalar = {'cap_phs':cap_phs,'storage_hours':storage_hours,'roundtrip_eff':roundtrip_eff,'initial_E_share':initial_E_share}

        f=open(os.path.join(temp_path,"scalar.dat"), "w+")
        for k, v in scalar.items():
             f.write("table %s := %f; \r\n"%(k,v))
        f.close()
        LP = StorageConsumptionAllocation()
        data = LoadModelData()
        instance = LP.create_instance(data)
        opt = SolverFactory('clp') # clp is the solver, in windows the .exe file has to be stated as the example: SolverFactory('glpk', executable='C:/bin/glpk/w64/glpsol.exe')
        outcome = opt.solve(instance,symbolic_solver_labels=False,tee=False,keepfiles = False)
    else:
        print('in the optimization length not match for price and gen')
        raise Exception('Price data length is not equal to generation data length... for %s and %d'%(ctr,year))

    cons_list = []
    for h in instance.H.value:
        cons_list.append({'Cons_phs':round(value(instance.CONSUMPTION_phs[h]),1)})

    consumption_phs = pd.DataFrame(cons_list)
    ctr_yr.reset_index(drop=True,inplace=True)
    new = ctr_yr.copy()
    new.drop('Hydro Pumped Storage',axis=1,inplace=True)
    ctr_gen = pd.DataFrame()
    ctr_gen = new.apply(lambda row: row/row.sum(),axis=1)*consumption_phs.values
    ctr_year = new - ctr_gen
    ctr_year.loc[:,'Hydro Pumped Storage'] = ctr_yr['Hydro Pumped Storage']
    return ctr_year
