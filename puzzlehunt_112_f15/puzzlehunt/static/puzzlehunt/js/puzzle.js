$(document).ready(function() {
    var parTimer = $('#par-timer');

    var startTime = parTimer.data('start-time');
    var limit = parTimer.data('par-limit');
    var now = Math.floor(Date.now()/1000);
    var elapsed = now - startTime;
    var remaining = Math.min(limit - elapsed, 0);

    parTimer.timer({
        seconds: elapsed,
        format: '%h:%m:%s',
    });

    $('.hint').each(function() {
        var timeToShow = $(this).data('time-to-show');
        var shownAfter = $(this).data('show-after');
        var remaining = Math.max(timeToShow-now, 0);
    });

});
