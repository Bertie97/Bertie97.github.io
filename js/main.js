
$(function(){
    $("#mainbutton").click(function(){
        window.location.href="about.html";
    })
    $(window).scroll(function(){
        if($(this).scrollTop() > 200){
            $('#arrowUP').fadeOut();
        }else{
            $('#arrowUP').fadeIn();
        }
    })
    $('#arrowUP').click(function(){
        $('html, body').animate({scrollTop: $('html, body').height() - $(window).height()}, 300);
        return false;
    })
})
