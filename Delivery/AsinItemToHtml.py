


heard="""

    <!DOCTYPE html>
    <html>

    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!--<meta name="viewport" content="width=device-width, initial-scale=1">-->
    <style type="text/css">
    </style>

    <script > 
    </script > 
    
        </head>

        <body>
                <div class="row">
                    <div class="table table-bordered" >
                        <table id="table" class="table" style=" border-;border-collapse: collapse;table-layout: fixed;min-width: 320px;width: 100%;background-color: #f2f4f6;" >
                            <thead >
                                <tr style="">

                """

end="""         



         </tbody>
                </table>
            </div>


        </div>
 

    </body>

    </html>
        """
        
        
htmlDic={ "heard" :heard ,"end":end}
def toHtml (Items):
    title="""                        </tr>
                        </thead>
                        <tbody>"""
    tr=""
    
    for asinItems in  Items:
        th =""
        # for  item in asinItems[0]:
            # th+="""<th   >""" +str(item) +"</th>"

        a=1
        for asinTtem in asinItems :
            tr+="<tr>"
            for item in asinTtem:
                if a!=1:
                    tr+="""<td  border="1px"  style="margin: 20px;text-align: center;margin-top: 50px ;border-collapse:collapse;">""" +str(item    )+"</td>"
                else:
                    tr+="""<td  border="1px"  style="margin: 20px;text-align: center;margin-top: 50px;font-size:20px;border-collapse:collapse;">""" +str(item    )+"</td>"
            a+=1        
            tr+="</tr>"
    body=th+title+tr
    return htmlDic["heard"]+body+htmlDic["end"]