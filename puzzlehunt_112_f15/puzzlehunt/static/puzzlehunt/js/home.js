$(document).ready(function() {
    var reflow = function() {
        var height = $('img').height();
        $('.btn-container').css({'margin-top':height});
    };
    reflow();
    $(window).on('resize', reflow);
});
