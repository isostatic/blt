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
    $('#toggleTime').text("Start Clock");
    $('#thetime').text("..:..:..:..+..ms");
}
function startTime() {
    runClock = 1;
    $('#toggleTime').text("Stop Clock");
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

    $('#thetime').html(hrs + ":" + mins + ":" + secs + ":" + frames + "+" + subframes  + "ms");
}
function doNTP() {
	$.get({url: "ntp.cgi", success: function(d) {
		// if -100 is returned, latency is 100 frames too high
		// if 100 is returned, latency is 100 frames too low
		$(".ntp").html("This reader: " + d);
	}});
}

stopTime();

$(function() {
	if ($(".ntp").length) {
		doNTP();
	}
});
