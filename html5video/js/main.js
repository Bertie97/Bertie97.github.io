
$(function() {
    var video = $('#video');
    $('#playpause').hide();
    $('#choices').hide();
    $('.title').hide();
    video.click(function() {
        if(!video[0].paused) {
            video.trigger('pause');
            $('#playpause').html('||');
            $('#playpause').attr('style', 'padding-left: calc(0.2 * var(--radius));');
        }
        else {
            video.trigger('play');
            $('#playpause').html('▶');
            $('#playpause').attr('style', 'padding-left: calc(0.3 * var(--radius));');
        }
        $('#playpause').fadeOut();
    });
    // video.click();
    var autostart = -1;
    setInterval(function() {
        if(autostart > 0) {autostart -= 1;}
        if(autostart == 0) {video.trigger('play');}
        if(autostart == -1 && video[0].readyState >= 4) {autostart = 5;}
        if(video[0].currentTime > 2 && $('.title').is(':hidden')) {
            $('.title').fadeIn(2000);
        }
        if(video[0].currentTime == video[0].duration) {
            if(!video[0].paused) {video.click();}
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
