
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
})
