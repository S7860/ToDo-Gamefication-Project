function change_progress() {
    var elem = document.getElementById("myBar");
    val = parseInt(document.getElementById("number").value);
    var width = 0;
    var id = setInterval(frame, val);
    function frame() {
        if (width >= val) {
            clearInterval(id);
        } else {
            width++; 
            elem.style.width = width + '%'; 
            elem.innerHTML = width * 1  + '%';
        }
    }  
}