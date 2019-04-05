import pandas as pd
from .client import CachingDataClient
from .filesystem import create_dir
from .storage_abstract_model import *
import os

c = CachingDataClient()

def InterateCountriesProduction_with_phs_consumption_subtract(year):
    cwd = os.getcwd()
    dest_dir = os.path.join(cwd,'DB_phs_consumption_subtract')
    create_dir(dest_dir)
    # toogle countries vector; short one just for test
    countries = ['AT','BA','BE','BG','BY','CH','CZ','DE','DK','EE','ES','FI','FR','GB','GB-NIR','GR','HR','HU','IE','IT','LT','LU','LV','ME','MK','MT','NL','NO','PL','PT','RO','RS','RU','RU-KGD','SE','SI','SK','TR','UA'];
    mom = list()
    country_not_included = {}
    for ctr in countries:
        try:
            ctr_year = c.get_generation(ctr, year)
        except:
            print('error after querring due to the country '+ ctr +' is not in the ENTSO-e database')
            continue
        try:
            ctr_year = PHS_consumption_subtraction(ctr,year)
        except:
            print('error after opt ',ctr)
            country_not_included[ctr] = year
            continue
        x = ctr_year.sum() # values in MWh
        x = x * 3600
        a = list(x.index)
        s = pd.Series(ctr)
        pap =  pd.DataFrame(data={'technology': list(x.index), 'country': list(s.repeat(len(x.index))), 'energy_MJ': list(x)})
        pap.to_csv(os.path.join(dest_dir,'gen_'+ctr+'_'+str(year)+'.csv'),index=False)
        mom.append(pap)
        
    f=open(os.path.join(dest_dir,"countries_omitted.dat"), "w+")
    for k, v in country_not_included.items():
         f.write("Omitted due to error in data of generation or prices during optimization %s := %d; \r\n"%(k,v))
    f.close()
    if len(mom) > 1:
        df = pd.concat(mom, ignore_index=True)
        df.to_csv(os.path.join(dest_dir,'gen_'+str(year)+'.csv'),index=False)
    else:
        df = pd.DataFrame()
    return(df)
