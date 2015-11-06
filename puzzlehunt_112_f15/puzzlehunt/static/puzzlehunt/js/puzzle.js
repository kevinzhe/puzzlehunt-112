$(document).ready(function() {
    var setProgress = function() {
        var progressBar = $('#puzzle-progress');
        var startTime = progressBar.data('starttime');
        var limit = progressBar.data('parlimit');
        var now = Math.floor(Date.now()/1000);
        var progress = Math.min(((now-startTime)/limit*100),100);
        progressBar.css({width:progress+'%'});
    };
    setProgress();
    window.setInterval(setProgress, 5000);
});
