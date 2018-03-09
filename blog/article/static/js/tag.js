function addLoadEvent(func) {
    var oldFunc = window.onload;
    if (typeof window.onload != 'function') {
        window.onload = func;
    } else {
        window.onload = function() {
            oldFunc();
            func();
        }
    }
}

function setColor() {
    var oBox = document.getElementById('box');
    var oList = oBox.getElementsByTagName('li');
    for (var i=0; i<oList.length; i++) {
        oList[i].style.background = randColor();
    }
}

function randColor() {
    var colors = Math.floor(Math.random()*(255*255*255));
    colors = colors.toString(16);
    if (colors.length < 6) {
        colors = '0' + colors;
    }
    return '#' +colors;
}

function logoFont() {
    //指定logo字体颜色等
    var elem = document.getElementByClassName("logo");
    elem.style.fontWeight = "bold";
    elem.style.fontSize = "1.2em";
    elem.style.fontFamily = '"微软雅黑", Arial, "Times New Roman"';
    elem.style.backgroundColor = "yellow";
}
addLoadEvent(setColor);
addLoadEvent(logoFont);
