function sct(date) {
    var tableObj = document.getElementsByClassName("table")[0];
    var str = "";
    var i = 1;
    //str += tableObj.innerHTML.replace("</tbody>", "").replace(" </table>", "");
    str =    '\
     <div class="col-md-31">\
    <table id="table" class="table">\
        <thead>\
            <tr>\
                <th>#</th>\
                <th>asin</th>\
                <th>isDog</th>\
                <th>title</th>\
                <th>price</th>\
                <th>Review</th>\
                <th>storeName</th>\
                <th>storeId</th>\
                <th>offers</th>\
                <th>updataTime</th>\
                <th>brand</th>\
                <th>Ranks</th>\
                <th>isBuybox</th>\
                <th>us</th>\
                <th>Off_time</th>\
                <th>Shelf_time</th>\
                <th>creat_time</th>\
            </tr>\
        </thead>\
        <tbody>\
        </tbody>\
    </table>'
    date.forEach(element => {
        console.log(element);
        var tile = element.name;
        if (element.name.length >= 36) {
            tile = tile.substring(0, 36)
        }

        str += "  </tr> <tr>  <th>" + i + "</th> <th>" + element.asin + "</th>" +
            " <th id=\"" + element.asin + "\" name=\"" + element.name + "\" onmouseover=\"showTie(" + element.asin + ")\" onmouseout=\"hideTie(" + element.asin + ")\" >" + tile + "</th>" +
            " <th>" + element.reviews + "</th>" +
            " <th>" + element.reviewsNumber + "</th>" +
            " <th>" + element.AnsweredQuestions + "</th>" +
            " <th>" + element.BigSellersRankTit + "</th>" +
            " <th>" + element.BigSellersRank + "</th>" +
            " <th>" + element.SamlSellersRankTit + "</th>" +
            " <th>" + element.SamlSellersRank + "</th>" +
            " <th>" + element.updataTime + "</th>" +
            " <th><a onclick=\"updataAsin('" + element.asin + "')\">updata</a></th></tr>";
        i += 1;
    });
    str += "</tbody> </table>"
    tableObj.innerHTML = str;
};

function showTie(tie) {
    console.log(tie.getAttribute("name"));
    tie.innerText = tie.getAttribute("name")
};

function hideTie(tie) {
    var tit = tie.getAttribute("name");
    if (tit.length > 36) {
        tie.innerText = tit.substring(0, 36);
    }
};


function updataAsin(asin) {

    $.ajax({
            type: "post",
            url: "/UpdataByasin",
            dataType: "text",
            async: "true",
            data: {
                "asin": asin
            },
            success: function(data) {},
        }

    );

};