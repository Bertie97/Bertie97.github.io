
$(function() {
    var playing = false;
    var video = $('#video');
    $('#choices').hide();
    $('.title').hide();
    // $('.title').fadeIn('slow');
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
        if(video[0].currentTime > 2 && $('.title').is(':hidden')) {
            $('.title').fadeIn(2000);
        }
        if(video[0].currentTime == video[0].duration) {
            if(playing) {video.click();}
            $('#choices').fadeIn();
        }
        wp = video[0].currentTime * 100 / video[0].duration
        $('#prog').attr('style', 'width:' + wp + '%')
    }, 100);
    $(window).keydown(function(event) {
        if(event.keyCode == '32') {
            video.click();
            return false;
        }
    })
})
