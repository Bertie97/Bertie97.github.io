
$(function() {
    var playing = false;
    var video = $('#video');
    var time = 1000;
    $('#choices').hide();
    video.click(function() {
        if(playing) {
            video.trigger('pause');
            $('#playpause').html('||');
            $('#playpause').attr('style', 'padding-left: calc(0.2 * var(--radius));');
        }
        else {
            video.trigger('play');
            $('#playpause').html('▶');
            $('#playpause').attr('style', 'padding-left: calc(0.3 * var(--radius));');
        }
        playing = !playing;
        $('#playpause').fadeOut();
    });
    video.click();
    setInterval(function() {
        if(video[0].currentTime == time && time > 0) {
            $('#choices').fadeIn();
        }
        time = video[0].currentTime
    }, 100);
    $(window).keydown(function(event) {
        if(event.keyCode == '32') {
            video.click();
            return false;
        }
    })
})
