$(document).ready(function() {
    var update = function() {
        $.ajax({
            url: 'scoreboard',
            type: 'GET',
            dataType: 'html'
        }).done(function(data) {
            var tbl = $(data).find('table');
            $('table').replaceWith(tbl);
        });
    };
    
    setInterval(update, 30000);
});
