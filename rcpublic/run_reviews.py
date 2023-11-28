import requests,json, sys,datetime,keepa,time
from tqdm import tqdm
import rcpublic.rcpublic as rc
sys.path.append('../Delivery/')
sys.path.append('../')
import config
config=config.config

import Delivery.spider as spider
#import spider as spider

print(rc.gettoday())
from update import setScreenXls,readFile,getXlsList,setScreenXlsAsin,setScreenXlsa

def  readAsins():
    # return getXlsList('c:\\File\\keepa\\'+rc.gettoday()+'.xlsx')[1]
    return getXlsList(config['keepaPath']+rc.gettoday()+'.xlsx')[1]


def start():
    sp = spider.Spider(1)
    setScreenXls( [ [sp.get_Amazon_Rew(asin)  for asin in tqdm(readAsins())]],config['Qx']+rc.gettoday()+'.xlsx')
    sp.closeChrome()
# start()