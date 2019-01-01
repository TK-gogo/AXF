$(function () {

    //全部类型点击
    $('#all_type').click(function () {
        console.log('alltype');
        $('#all_type_container').toggle();
        $('#all_type_icon').addClass('glyphicon-chevron-up').toggleClass('glyphicon-chevron-down')

        //主动触发点击
        $('#sort_type_container').trigger('click')

    });

    // 点击灰色的地方
    $('#all_type_container').click(function () {
        $(this).hide();
        $('#all_type_icon').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')


    });

    //点击综合排序
    $('#sort_type').click(function () {
        console.log('alltype');
        $('#sort_type_container').toggle();
        $('#sort_type_icon').addClass('glyphicon-chevron-up').toggleClass('glyphicon-chevron-down')

        //主动触发点击
        $('#all_type_container').trigger('click')
    });


    // 点击灰色的地方
    $('#sort_type_container').click(function () {
        $(this).hide();
        $('#sort_type_icon').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')

    });


    $('.addtocart').click(function () {

        let goodsid = $(this).attr('goodsid');
        let num = $(this).prev().find('.num').html()

        console.log(num)
        console.log(goodsid);
        $.get('/axf/add_to_cart/',{goodsid:goodsid,num:num}, function (data) {
            console.log(data)
            if (data.status == 0){
                location.href = '/axf/login/'
            }else if (data.status==1){
                alert('添加成功')
            }
        })
    })

    //+
    $('.add').click(function () {
        let num = $(this).prev();

        num.html(parseInt( num.html() ) + 1)
    });

    $('.sub').click(function () {
        let num = $(this).next();

        if ( (num.html()) > 1 ){
            num.html(parseInt( num.html() ) - 1)
        }


    })

});