
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
    var autostart = false;
    var autostarted = false;
    setInterval(function() {
        console.log(video[0].readyState)
        if(autostart) {
            video.trigger('play');
            autostart = false;
        }
        if(video[0].buffered.length > 0 && !autostarted) {
            autostart = true;
            autostarted = true;
        }
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
