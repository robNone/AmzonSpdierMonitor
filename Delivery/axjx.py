
getQty="""
function countTime() {
            var bdata =SetData();
            let qty=0
            $.ajax({
                url : "https://www.amazon.com/cart/ref=ox_sc_update_quantity_1%7C2%7C999",
                type : "POST",
                dataType : 'json',
                data :bdata,
                success:function (data) {
                    console.log(data);
                    console.log( data['features']['nav-cart']['cartQty']);
                    qty= data['features']['nav-cart']['cartQty'];
					document.getElementById('twotabsearchtextbox').name=qty;
                    var Delt=SetDelData(bdata ,qty);
                    $.ajax({
                        url : "https://www.amazon.com/cart/ref=ox_sc_cart_actions_1",
                        type : "POST",
                        dataType : 'json',
                        data :Delt,
                        success:function (data) {
                            console.log(data);
                            }
					
                    })
                    }
            })

        }

function SetData(){
    var bs=document.getElementsByClassName('sc-list-item-content')[0].parentElement;
    var itemid= bs.getAttribute('data-itemid');
    var asin =bs.getAttribute('data-asin');
    var encodedOffering=bs.getAttribute('data-encoded-offering');
    var price =bs.getAttribute('data-price');
    var token =document.getElementsByName('token')[0].value
    var timeStamp =document.getElementsByName('timeStamp')[0].value
    // var submit='submit.update-quantity.'+ bs.getAttribute('data-itemid');
    var   data={

        'pageAction': 'update-quantity',
        'displayedSavedItemNum': 0,
        'actionItemID': itemid,
        'actionType': 'update-quantity',
        'asin': asin,
        'encodedOffering': encodedOffering,
        'hasMoreItems': false,
        'addressId': '',
        'addressZip': '',
        'closeAddonUpsell': 1,
        'displayedSavedItemNum': 0,
        'activeItems': '0|'+itemid+'|1|0|2|'+price+'||||||1',
        'timeStamp': timeStamp,
        'requestID': opts['requestId']        ,
        'token': token,
        'redirectToFullPage': 1,



    }
    data['quantity.'+[itemid]]=999
    data['submit.update-quantity.'+[itemid]]=1


    return data
}

function SetDelData(bdata,qty){
    var bs=document.getElementsByClassName('sc-list-item-content')[0].parentElement;
    var price =bs.getAttribute('data-price');

    // var submit='submit.update-quantity.'+ bs.getAttribute('data-itemid');
    var d={
        'hasMoreItems': false,
        'addressId': '',
        'addressZip': '',
        'closeAddonUpsell': 1,
        'displayedSavedItemNum': 0,
        'activeItems': '0|'+bdata['actionItemID']+'|1|0|'+qty+'|'+price+'||||||1',
        'timeStamp':bdata['timeStamp']  ,
        'requestID': bdata['requestID'] ,
        'token': bdata['token'] ,
        'redirectToFullPage': 1,
    }
    d['submit.cart-actions']=1
    d['pageAction']='cart-actions'
    d['actionPayload']=[{"type":"DELETE_START","payload":{"itemId": bdata["actionItemID"],"list":"activeItems","relatedItemIds":[],"isPrimeAsin":false}}]
    console.log(d)
    return d
}
return countTime()
"""