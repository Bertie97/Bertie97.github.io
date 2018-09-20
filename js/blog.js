
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

    $('#goToTop').click(function(){
        $('html, body').animate({scrollTop: 0}, 300);
        return false;
    })
    $('.pagination a').click(function(){
        var target = $($(this).attr('href')).offset();
        $("html, body").animate({scrollTop:target.top - 90}, 300);
        return;
    })
    // $('.filedownload').click(function(){
    //     var dlForm = $("<form method='get'></form>");
    //     dlForm.attr("action",$(this).attr('file'));
    //     $(document.body).append(dlForm);
    //     dlForm.submit();
    // })
})

var currentPage = 1;//当前页数
/**
 * 分页函数
 * pno--页数
 * psize--每页显示记录数
 * 分页部分是从真实数据行开始，因而存在加减某个常数，以确定真正的记录数
 * 纯js分页实质是数据行全部加载，通过是否显示属性完成分页功能
 **/
function go2Page(pno, psize) {
    var itable = document.getElementById("blogList");
    var num = itable.rows.length;//表格所有行数(所有记录数)
    var totalPage = 0;//总页数
    currentPage = pno;//当前页数
    pageSize = psize;//每页显示行数
    //总共分几页
    if(num/pageSize > parseInt(num/pageSize)) {
        totalPage=parseInt(num/pageSize)+1;
    }
    else {
        totalPage=parseInt(num/pageSize);
    }
    var startRow = (currentPage - 1) * pageSize + 1;//开始显示的行
    var endRow = currentPage * pageSize;//结束显示的行
    endRow = (endRow > num)? num : endRow;
    //遍历显示数据实现分页
    for(var i=1;i<(num+1);i++){
        var irow = itable.rows[i-1];
        if(i>=startRow && i<=endRow){
            irow.style.display = "table-row";
        }else{
            irow.style.display = "none";
        }
    }
    itable.style.table_layout = "fixed";

    for(var i=1;i<(totalPage+1);i++){
        document.getElementById("page" + i).classList.remove("active");
    }
    document.getElementById("page" + currentPage).className = "active";
}

function movePage(offset, pageSize) {
    var itable = document.getElementById("gallery");
    var num = itable.rows.length;//表格所有行数(所有记录数)
    var totalPage = 0;//总页数
    if(num/pageSize > parseInt(num/pageSize)) {
        totalPage=parseInt(num/pageSize)+1;
    }
    else {
        totalPage=parseInt(num/pageSize);
    }
    currentPage += offset;
    if(currentPage < 1) {currentPage = 1; return;}
    if(currentPage > totalPage) {currentPage = totalPage; return;}
    go2Page(currentPage, pageSize)
}
