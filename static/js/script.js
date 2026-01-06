(function ($) {

  "use strict";

  var initPreloader = function () {
    $(document).ready(function ($) {
      var Body = $('body');
      Body.addClass('preloader-site');
    });
    $(window).load(function () {
      $('.preloader-wrapper').fadeOut();
      $('body').removeClass('preloader-site');
    });
  }

  // background color when scroll 
  var initScrollNav = function () {
    var scroll = $(window).scrollTop();

    if (scroll >= 200) {
      $('.navbar.fixed-top').addClass("bg-primary");
    } else {
      $('.navbar.fixed-top').removeClass("bg-primary");
    }
  }

  $(window).scroll(function () {
    initScrollNav();
  });


   /*[ Back to top ]
    ===========================================================*/
    var windowH = $(window).height()/2;

    $(window).on('scroll',function(){
        if ($(this).scrollTop() > windowH) {
            $("#myBtn").css('display','flex');
        } else {
            $("#myBtn").css('display','none');
        }
    });

    $('#myBtn').on("click", function(){
        $('html, body').animate({scrollTop: 0}, 300);
    });



  // init Chocolat light box
  var initChocolat = function () {
    Chocolat(document.querySelectorAll('.image-link'), {
      imageSize: 'contain',
      loop: true,
    })
  }


  var initProductQty = function () {

    $('.product-qty').each(function () {

      var $el_product = $(this);
      var quantity = 0;

      $el_product.find('.quantity-right-plus').click(function (e) {
        e.preventDefault();
        var quantity = parseInt($el_product.find('#quantity').val());
        $el_product.find('#quantity').val(quantity + 1);
      });

      $el_product.find('.quantity-left-minus').click(function (e) {
        e.preventDefault();
        var quantity = parseInt($el_product.find('#quantity').val());
        if (quantity > 0) {
          $el_product.find('#quantity').val(quantity - 1);
        }
      });

    });

  }

  // document ready
  $(document).ready(function () {

    AOS.init({
      duration: 1200,
      once: true,
    })

    // swiper slider home 2
    var swiper = new Swiper(".slideshow", {
      slidesPerView: 1,
      spaceBetween: 0,
      speed: 1000,
      loop: true,
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      navigation: {
        nextEl: '.icon-arrow-right',
        prevEl: '.icon-arrow-left',
      }
    });

    // product single page
    var thumb_slider = new Swiper(".product-thumbnail-slider", {
      loop: true,
      slidesPerView: 3,
      autoplay: true,
      direction: "horizontal",
      spaceBetween: 0,
    });

    var large_slider = new Swiper(".product-large-slider", {
      loop: true,
      slidesPerView: 1,
      autoplay: true,
      effect: 'fade',
      thumbs: {
        swiper: thumb_slider,
      },
    });

    var swiper = new Swiper(".testimonial-swiper", {
      effect: "coverflow",
      grabCursor: true,
      centeredSlides: true,
      loop: true,
      slidesPerView: "auto",
      coverflowEffect: {
        fade: true,
      },
      pagination: {
        el: ".testimonial-swiper-pagination",
        clickable: true,
      },
    });

    window.addEventListener("load", (event) => {

      var $grid = $('.entry-container').isotope({
        itemSelector: '.entry-item',
        layoutMode: 'masonry'
      });

    });



    initPreloader();
    initChocolat();
    initProductQty();




  }); // End of a document

})(jQuery);

let offset = 5;
const btn = document.getElementById('load-more');

btn?.addEventListener('click', () => {
    let offset = parseInt(btn.dataset.offset);
    const url = btn.dataset.url;

    fetch(`${url}?offset=${offset}`)
        .then(res => res.json())
        .then(data => {

            // Append reviews
            data.reviews.forEach(r => {
                document.getElementById('review-list').insertAdjacentHTML(
                    'beforeend',
                    `
                    <div class="review-item">
                        <img src="${r.image}">
                        <div>
                            <strong>${r.username}</strong>
                            <div class="stars">
                                ${'★'.repeat(r.rating)}${'☆'.repeat(5 - r.rating)}
                            </div>
                            <p>${r.message}</p>
                        </div>
                    </div>
                    `
                );
            });

            // Update offset
            btn.dataset.offset = data.loaded_count;

            // Hide button if no more reviews
            if (!data.has_more || data.reviews.length === 0) {
                btn.style.display = 'none';
            }
        });
});