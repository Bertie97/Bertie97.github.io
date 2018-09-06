
$(function(){
    $('#goToTop').hide()
    $(window).scroll(function(){
        // console.log($(this).scrollTop());

        //当window的scrolltop距离大于1时，go to
        if($(this).scrollTop() > 100){
            $('#goToTop').fadeIn();
        }else{
            $('#goToTop').fadeOut();
        }
    });

    $('#goToTop a').click(function(){
        $('html ,body').animate({scrollTop: 0}, 300);
        return false;
    })
})
