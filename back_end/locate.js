var byresid = [
    ["ID : ", "<input type = \"number\" name = \"resID\">"]
]

var byphone = [
    ["Phone Number : ", "<input type = \"tel\" name = \"phone\">"]
]

var bycoord = [
    ["Latitude : ", "<input type = \"number\" step = \"0.000001\" name = \"lat\">"],
    ["Longitude : ", "<input type = \"number\" step = \"0.000001\" name = \"long \">"]
]

function onLoadLocate() {
    var table = document.getElementById("table");
    var mode = document.getElementById("modeID");

    var changed;
    if(mode.value == "byresid") {
        changed = byresid;
    }

    if(mode.value == "byphone") {
        changed = byphone;
    }

    if(mode.value == "bycoord") {
        changed = bycoord;
    }

    var innerText = "";
    for(var i = 0; i < changed.length; i++) {
        innerText += "<tr>\n"
        for(var j = 0; j < changed[i].length; j++) {
            innerText += "<td>" + changed[i][j] + "</td>\n";
        }
        innerText += "</tr>\n";
    }
    table.innerHTML = innerText;

}