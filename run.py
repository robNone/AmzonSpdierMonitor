# -*- coding: utf-8 -*-
import os,sys,time  ,schedule 
import rcpublic.rcpublic as rc 
sys.path.append('/')
sys.path.append('/Delivery/')
sys.path.append('rcpublic/')
import config

import rcpublic.run_reviews as run_reviews
import Delivery.PostEmail as PostEmail
config=config.config
def run():
    
    os.system(config['python.pythonPath']+' '+config['getJsonPath'])    
    rc.runPrice()
    run_reviews.start()
    os.system(config['java']+' -jar '+config['cSpider_jar'])    
    PostEmail.Emails("monitor@hzallin.com",' ','Active ASINs Review监控',config['Qx']+'ActiveASINsReview'+rc.gettoday()+'.xls')
    
if __name__ == '__main__':
    run()
    schedule.every().day.at("00:20").do(run,)
    while True:
        schedule.run_pending()
        time.sleep(1)



