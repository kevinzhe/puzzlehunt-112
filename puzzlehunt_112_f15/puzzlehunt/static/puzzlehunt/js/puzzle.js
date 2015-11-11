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
        var self = this;
        var timeToShow = $(this).data('time-to-show');
        var shownAfter = $(this).data('show-after');
        var remaining = Math.max(timeToShow-now, 0);
        var puzzle_id = location.pathname.split('/')[2];
        var hint_id = $(this).data('id');
        console.log(hint_id);
        if (remaining > 0) {
            window.setTimeout(function() {
                $.ajax({
                    url: '/p/'+puzzle_id+'/hint/'+hint_id,
                    type: 'GET',
                    dataType: 'json'
                }).done(function(data) {
                    $(self).find('.hint-text').html(data.text);
                    $(self).find('.hint-timer').remove();
                    $(self).removeClass('inactive');
                });
            }, remaining*1000+500);
        }
    });

});
