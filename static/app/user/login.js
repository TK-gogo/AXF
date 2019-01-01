$(function () {


    $('#login').click(function () {

        //密码MD5加密
        $('#password').val(md5($('#password').val()))
        console.log($('#password').val())
    })

})