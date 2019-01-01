$(function () {

    initTopSwiper();

    initSwiperMenu();

})

function initTopSwiper() {


		  var mySwiper = new Swiper ('#topSwiper', {
//		    direction: 'vertical', // 垂直切换选项
		    loop: true, // 循环模式选项
		    autoplay:2000,
		    // 如果需要分页器
		    pagination: '.swiper-pagination',

		  });

}

function initSwiperMenu() {
    var swiper = new Swiper("#swiperMenu",{
       slidesPerView: 3
    });
}