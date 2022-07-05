function find() {
    var str = document.getElementById("htmlText").value.replace(/\n/g, "").replace(/\t/g, "");
    var count = 0;
    var AddHtml = " <
    div id = \"findRun\">" + " <
    table class = \"table\" id=\ "
    table\ "> \n" + " <
    thead > \n " + " <
        tr > \n " + " <
        th > # < /th>\n" + " <
    th > Order Id < /th>\n" + " <
    th > title < /th>\n" + " <
    th > Quantity < /th>\n" + " <
    th class = \"f\">sku</th>\n" + " <
    th > asin < /th>\n" + " <
    th > Ardess < /th>\n" + " <
    th > Customizations < /th>\n" + " </tr > " + " <
        /thead>" + " <
    tbody > " ; str.split("
    Order ID: ").forEach(html => { if (count == 0) { count += 1; } else { var order = html.match(/.+?(?= <
    div) / g)[0];
var Quantity = h tml.match(/(?<=a-text-center table-border.>).+?(?= <
.td > ) / g)[0];
var title = html.match(/(? <=
a - text - left table - border. + ? class = "a-text-bold" > ). + ? ( ? = <
.span) / g)[0];
var sku = h tml.match(/(?<=SKU:.+?<span>).+?(?= <
.span) / g)[0];
var asin = h tml.match(/(?<=ASIN:.+?<span>).+?(?= <
.span) / g)[0];
var Ardess = h tml.match(/(?<=id=.myo-order-details-buyer-address. class=.myo-wrap.>).+?(?=<br>)/g)[0];
var Customizations = html.match(/(? <=
ul class = .a - unordered - list a - nostyle a - vertical. > ). + ? ( ? = <
.ul > ) / )[0]; //id="myo-order-details-buyer-address" class="myo-wrap"> var Customization = ""; console.log(Customizations); var cv = 0; Customizations.split(/
<
span class = .a - list - item. > /g).forEach(crs => {
if (cv == 0) { cv += 1; } else {
    Customization += crs.match(/(?<=a-color-base.>).+?(?=<.span>)/)[0]
    try {
        Customization += crs.match(/(?<=<span>).+?(?=<.span>)/)[0] + "\r\n"

    } finally {}
}
});

AddHtml += "  </tr> <tr>  <th>" + count + "</th> <th>" + order + "</th>" +
    " <th>" + title + "</th>" +
    " <th>" + Quantity + "</th>" +
    " <th>" + sku + "</th>" +
    " <th>" + asin + "</th>" +
    " <th>" + Ardess + "</th>" +
    " <th>" + Customization + "</th>" +
    "";
count += 1;
}
});
AddHtml += "</tbody> </table></div>"
document.getElementById("findRun").innerHTML = AddHtml

}