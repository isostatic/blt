var runClock = 0;
function toggleTime() {
    if (runClock) {
        stopTime();
    } else {
        startTime();
    }
}
function stopTime() {
    runClock = 0;
    document.getElementById('toggleTime').innerHTML = "Start Clock";
    document.getElementById('thetime').innerHTML = "..:..:..:..+..ms";
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