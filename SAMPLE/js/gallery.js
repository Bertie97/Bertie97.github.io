
$(function(){
    $('#closepop').click(function(){
        $('#cover').fadeOut()
        $('#popout').fadeOut()
        $('#closepop').fadeOut()
        $('#popcontent').fadeOut()
    });
    $('#cover').click(function(){
        $('#cover').fadeOut()
        $('#popout').fadeOut()
        $('#closepop').fadeOut()
        $('#popcontent').fadeOut()
    });
    $('.topop').click(function(){
        $('#popcontent').html('<center><img src="' + $(this).attr('name') +
                              '" width="100%" style="border-radius:0.4rem"/></center>')
        $('#cover').fadeIn()
        $('#popout').fadeIn()
        $('#closepop').fadeIn()
        $('#popcontent').fadeIn()
    });
});

// function showimg(path) {
//     document.getElementById('popcontent').innerHtml = '<img src="' + path + '" width="80%"/>'
// }
