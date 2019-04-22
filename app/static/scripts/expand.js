function expand(id, id2) {
    var x = document.getElementById(id);
    if (x.style.display === "none") {
        x.style.display = "table-cell";
        id2.value = "-";
        id2.style.backgroundColor = "#f04b4c";
    } else {
        x.style.display = "none";
        id2.value = "+";
        id2.style.backgroundColor = "#009688";
    }
}
