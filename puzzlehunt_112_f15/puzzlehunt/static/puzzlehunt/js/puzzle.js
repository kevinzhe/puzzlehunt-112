$(document).ready(function() {
    //var setProgress = function() {
    //    var progressBar = $('#puzzle-progress');
    //    var startTime = progressBar.data('starttime');
    //    var limit = progressBar.data('parlimit');
    //    var now = Math.floor(Date.now()/1000);
    //    var progress = Math.min(((now-startTime)/limit*100),100);
    //    progressBar.css({width:progress+'%'});
    //};
    //setProgress();
    //window.setInterval(setProgress, 5000);


    var parTimer = $('#par-timer');

    var startTime = parTimer.data('start-time');
    var limit = parTimer.data('par-limit');
    var now = Math.floor(Date.now()/1000);
    var elapsed = now - startTime;
    var remaining = Math.min(limit - elapsed, 0);

    parTimer.timer({
        seconds: elapsed,
    });

    $('.hint').each(function() {
        var timeToShow = $(this).data('time-to-show');
        var shownAfter = $(this).data('show-after');
        var remaining = Math.max(timeToShow-now, 0);
    });
});
