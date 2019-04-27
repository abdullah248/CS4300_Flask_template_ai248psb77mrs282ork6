function expand(id, id3) {
    console.log("Expanding");
    var x = document.getElementById(id);
    var y = document.getElementById(id+50);
    if (x.style.display === "none") {
        x.style.display = "table-cell";
        x.style.borderTopRightRadius = "10px";
        x.style.borderBottomRightRadius = "10px";
        y.style.borderTopRightRadius = "0px";
        y.style.borderBottomRightRadius = "0px";
        id3.value = "-";
        id3.style.backgroundColor = "#f04b4c";
    } else {
        x.style.display = "none";
        y.style.borderTopRightRadius = "10px";
        y.style.borderBottomRightRadius = "10px";
        id3.value = "+";
        id3.style.backgroundColor = "#009688";
    }
}
