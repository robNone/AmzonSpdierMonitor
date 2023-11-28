import PyPDF2,os,re,sys

sys.path.append('../Delivery/')
from update import setScreenXls,readFile,getXlsList,setScreenXlsAsin,setScreenXlsa

div='pdf'
# div='2'

# text=pdf_reader.pages[0].extract_text()
#用PdfReader打开PDF文件
# text=pdf_reader.pages[0].extract_text().split('\n')	#获取第1页的文本


def sv(t):
    indexStar=0
    # print(t) 
    
    indexEnd=0
    for vr in t:
        if vr.find ('申报日期')>=0:
            outdata=vr.replace('申报日期','') 
        if vr.find ('海关编号')>=0:
            hai=vr.replace('海关编号：','')
        if vr.find('随附单据')>=0:
            containerId=vr.replace('随附单据','')
        if vr.find('商品序号')>=0:
            indexStar=t.index(vr)
        if vr.find('运费')>=0:
            yp=vr.replace('运费','')
        if vr.find('保费')>=0:
            fat=vr.replace('保费','')
        if vr.find('税费征收情况')>=0:
            indexEnd=t.index(vr)
    ct= t[indexStar+1:indexEnd]
    aList,rc=[],[]
    # aList.extend
    name,price,unmber,unit,all='','','','',''
    [aList.extend(c) for c in  [   x.split(' ') for x in ct]]
    cList=aList
    print(len(aList))
        # if len(cct.split(' ')[0])==11:
        #     name=cct.split(' ')[1]
        #     return [hai,containerId,name,price,unmber,unit]
        # if cct.find('美国')>=0:pass
    for cct in (cList):
        if (len(cct)==11 or len(cct)==10 ) and re.findall('\d{10,11}',cct)!=[]: 
            name=aList[aList.index(cct)+1]
        if cct.find('USD')>=0:
            price=aList[aList.index(cct)-2]
            all=aList[aList.index(cct)-1]
        if cct.find('申报数量')>=0:
            unmber=aList[aList.index(cct)+1][:-1]
            unit=aList[aList.index(cct)+1][-1]
            aList=aList[aList.index(cct)+2:]
            rc.append([hai,containerId,outdata,yp,fat,name,price,all,unmber,unit])
    return rc
fileList=[]
for root, dirs, files in os.walk(div):
    for f in files:
        file = os.path.join(root, f)
        # print(len(PyPDF2.PdfReader(file)	.pages[0].extract_text().split('\n')))
        for pReader in PyPDF2.PdfReader(file).pages:
            fileList+=sv(pReader.extract_text().split('\n'))
        
setScreenXls([fileList,],'pdf.xlsx')
