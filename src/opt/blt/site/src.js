var runClock = 0;
function toggleTime() {
    if (runClock) {
        stopTime();
    } else {
        startTime();
    }
}
function checkNTP() {
    document.getElementById('checkNTP').innerHTML = "";
    document.getElementById('ntpres').innerHTML = "Checking NTP...";
    var request = new XMLHttpRequest();
    console.log(request);
    request.onreadystatechange = function () {
        if ( request.readyState === 4 ) { 
            document.getElementById('ntpres').innerHTML = request.responseText;
        }
    };
    request.open("GET", "ntp.cgi");
    request.send();
}
function stopTime() {
    runClock = 0;
    if (document.getElementById('thetime')) {
        document.getElementById('toggleTime').innerHTML = "Start Clock";
        document.getElementById('thetime').innerHTML = "..:..:..:..+..ms";
    }
}
function startTime() {
    runClock = 1;
    document.getElementById('toggleTime').innerHTML = "Stop Clock";
    doTime();
}
function doTime() {
    if (runClock == 0) return;
    setTimeout(doTime, 5);
    var date = new Date();
    var hrs = date.getUTCHours();
    hrs = hrs < 10 ? '0'+hrs : hrs;

    var mins = date.getUTCMinutes();
    mins = mins < 10 ? '0'+mins : mins;

    var secs = date.getUTCSeconds();
    secs = secs < 10 ? '0'+secs : secs;

    var ms = date.getUTCMilliseconds();
    var frames =  Math.floor(ms / 40);
    frames = frames < 10 ? '0'+frames : frames;

    var subframes = ms % 40;
    subframes = subframes < 10 ? '0'+subframes : subframes;

    document.getElementById('thetime').innerHTML = hrs + ":" + mins + ":" + secs + ":" + frames + "+" + subframes  + "ms";
}

stopTime();
