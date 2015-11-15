$(document).ready(function() {
    /* Set up the timers and the hint AJAX-ing */
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


    /* Set up the solution AJAX-ing */
    $('#solution-form').on('submit', function(event) {
        event.preventDefault();
        var puzzle_id = location.pathname.split('/')[2];
        var form = $(this);
        $.ajax({
            url: '/p/'+puzzle_id+'/',
            type: 'POST',
            dataType: 'json',
            data: form.serialize()
        }).done(function(data) {
            console.log(data);
            if (typeof data.error !== 'undefined') {
                return;
            }
            if (data.correct) {
                var $sol = $('.real-solution');
                $sol.append(data.solution);
                var $score = $('.real-score');
                $score.append(data.score);
                $('.solution-form').remove();
                $('.finished-info').removeClass('hidden');
            } else {
                console.log('incorrect!');
            }
        });
        /* Return false to prevent default HTML submit */
        return false;
    });

});
