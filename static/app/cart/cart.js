$(function () {


    $('.add').click(function () {

        let cartid = $(this).parents('li').attr('cartid')
        let that = this;
        console.log(cartid);


        $.get('/axf/cart_num_add/', {cartid:cartid}, function (data) {
            console.log(data)
            if (data.status==1){
                console.log($(this))
                $(that).prev().html(data.num)
            }
        })

    });


    $('.sub').click(function () {

        let cartid = $(this).parents('li').attr('cartid')
        let that = this;
        console.log(cartid);


        $.post('/axf/cart_num_reduce/', {cartid:cartid}, function (data) {
            console.log(data)
            if (data.status==1){
                console.log($(this))
                $(that).next().html(data.num)
            }
        })

    });

    $('.delbtn').click(function () {

        let cartid = $(this).parents('li').attr('cartid')
        let that = this;
        console.log(cartid);


        $.post('/axf/cart_del/', {cartid:cartid}, function (data) {
            console.log(data)
            if (data.status==1){
                $(that).parents('li').remove()
            }
        })

    });

    $('.confirm').click(function () {
        let cartid = $(this).parents('li').attr('cartid');
        let that = this;
        $.post('/axf/cart_select/', {cartid:cartid}, function (data) {
            console.log(data)
            if (data.status==1){

                $(that).find('span').find('span').html(data.select?'√':'')

            }
        })

    });

    $('.all_select').click(function () {

        //对当前的状态去反
        //如果当前是√的状态就取0，反之取1
        let select = $(this).find('span').find('span').html()?0:1
        let that = this
        console.log(select);

        $.post('/axf/cart_select_all_or_none/', {select:select}, function (data) {
            console.log(data)
            if (data.status==1){
                $('.confirm').find('span').find('span').html(select?'√':'')
                $(that).find('span').find('span').html(select?'√':'')
            }
        })

    });

    checkselect();

    function checkselect() {

        let unselect = [];

        $('.menuList').each(function () {
            let is_select = $(this).find('span').find('span').html()

            if (is_select){
                unselect.push($(this).attr('cartid'))
            }

        });

        if (unselect.length==0){
            $('.all_select').find('span').find('span').html('')
        }

    }



});