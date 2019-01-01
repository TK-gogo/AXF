$(function () {


    // $('#username').change(function () {
    //     console.log('changed');
    //     //正则匹配username输入的字符
    //     if(/^[a-zA-Z_]\w{5,17}$/.test($(this).val())){
    //         console.log('输入正解');
    //         $('#user_msg').html('输入正解').css('color','green')
    //     } else {
    //         console.log('输入有误');
    //         $('#user_msg').html('用户名格式不正确').css('color','red')
    //     }
    //
    // });
    //
    //
    // $('#password').change(function () {
    //
    //     if(/^.{8,}$/.test($('#password').val())){
    //         $('#pwd_msg').html('密码正确').css('color','green')
    //     } else {
    //         $('#pwd_msg').html('密码格式不正确').css('color','red')
    //     }
    // });
    //
    // $('#re_password').change(function () {
    //     let re_password = $('#re_password').val();
    //     let password = $('#password').val();
    //
    //     if(re_password == password ){
    //         $('#rpwd_msg').html('密码一致').css('color','green')
    //     } else {
    //         $('#rpwd_msg').html('输入密码不一致').css('color','red')
    //     }
    // });
    //
    // $('#email').change(function () {
    //     if(/\w+@\w+(\.\w+)+/.test($('#email').val())){
    //         $('#email_msg').html('邮箱正确').css('color','green')
    //     } else {
    //         $('#email_msg').html('邮箱格式不正确').css('color','red')
    //     }
    // });
    //
    // //\w+@\w+(\.\w+)+  sdflj@ljl.com    lsjfd@lsldj.com.cn.cn
    //
    // $('#register').click(function () {
    //     return false
    // })


    //可以用flag判断
    // let usrname_flag = false


    $('#username').change(function () {
        console.log('changed');
        verify_username()

    });

    function verify_username(){
        //正则匹配username输入的字符
        if(/^[a-zA-Z_]\w{5,17}$/.test($('#username').val())){

            $.get('/axf/check_username/', {username:$('#username').val()}, function (data) {
                console.log(data)
                if (data.status == 0){
                    $('#user_msg').html('用户名已存在').css('color','orange')
                } else if (data.status == 1) {
                    $('#user_msg').html('用户名可用').css('color','green')
                } else {
                    $('#user_msg').html('不可用').css('color','red')
                }
            });

        } else {
            console.log('输入有误');
            $('#user_msg').html('用户名格式不正确').css('color','red')
        }

    }



    $('#password').change(function () {

        verify_password()
    });

    function verify_password(){
        if(/^.{8,}$/.test($('#password').val())){
            $('#pwd_msg').html('密码正确').css('color','green')
        } else {
            $('#pwd_msg').html('密码格式不正确').css('color','red')
        }
    }

    $('#re_password').change(function () {
        verify_repassword()
    });

    function verify_repassword(){
        let re_password = $('#re_password').val();
        let password = $('#password').val();

        if(re_password == password ){
            $('#rpwd_msg').html('密码一致').css('color','green')
        } else {
            $('#rpwd_msg').html('输入密码不一致').css('color','red')
        }
    }

    $('#email').change(function () {
        verify_email()
    });

    function verify_email(){
        if(/\w+@\w+(\.\w+)+/.test($('#email').val())){
            $('#email_msg').html('邮箱正确').css('color','green')
        } else {
            $('#email_msg').html('邮箱格式不正确').css('color','red')
        }
    }


    //页面刷新时匹配
    if ($('#username').val()){
        verify_username();

    }
    if ($('#password').val()){
        verify_password();
    }
    if ($('#re_password').val()){
        verify_repassword();
    }
    if ($('#email').val()){
        verify_email();
    }



    //\w+@\w+(\.\w+)+  sdflj@ljl.com    lsjfd@lsldj.com.cn.cn

    $('#register').click(function () {

        let user_css = $('#user_msg').css('color');
        let pwd_css = $('#pwd_msg').css('color');
        let rpwd_css = $('#rpwd_msg').css('color');
        let email_css = $('#email_msg').css('color');
        console.log(user_css);

        if (user_css == 'rgb(0, 128, 0)' && pwd_css == 'rgb(0, 128, 0)' && rpwd_css == 'rgb(0, 128, 0)' && email_css == 'rgb(0, 128, 0)'){
            return true
        } else {
            return false
        }

    })

})