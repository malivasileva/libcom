document.addEventListener("DOMContentLoaded", () => {
    if (document.querySelector('#datepicker')) {
        $('#datepicker').datepicker({
            uiLibrary: 'bootstrap5'
        })

        $('#datepickerTo').datepicker({
            uiLibrary: 'bootstrap5'
        })
    }

    $('.multiple-card-slider .carousel').each(function(){
        var currentCarouselId = '#' + $(this).attr('id');
        const multipleItemCarousel = document.querySelector(currentCarouselId);
    
        if(window.matchMedia("(min-width:576px)").matches){
            const carousel = new bootstrap.Carousel(multipleItemCarousel, {
                interval: false,
                wrap: false
            })
            var carouselWidth = $(currentCarouselId + ' .carousel-inner')[0].scrollWidth;
            var cardWidth = $(currentCarouselId + ' .carousel-item').width();
            var scrollPosition = 0;    
            $(currentCarouselId + ' .carousel-control-next').on('click', function(){
                if(scrollPosition < (carouselWidth - (cardWidth * 4))){
                    console.log('next');
                    scrollPosition = scrollPosition + cardWidth;
                    $(currentCarouselId + ' .carousel-inner').animate({scrollLeft: scrollPosition},600);
                }
            });
            $(currentCarouselId + ' .carousel-control-prev').on('click', function(){
                if(scrollPosition > 0){
                    console.log('prev');
                    scrollPosition = scrollPosition - cardWidth;
                    $(currentCarouselId + ' .carousel-inner').animate({scrollLeft: scrollPosition},600);
                }
            });
        }else{
            $(multipleItemCarousel).addClass('slide');
        }
    });


    let books = document.querySelectorAll('.book-plus')

    if (books) {
        books.forEach((book) => {
            book.addEventListener("click", () => {
                if (book.parentNode.parentNode.classList.contains('active-item')) {
                    book.parentNode.parentNode.classList.remove('active-item')
                    book.parentNode.parentNode.querySelector('.book-btns').classList.remove('active-btns')
                } else {
                    book.parentNode.parentNode.classList.add('active-item')
                    book.parentNode.parentNode.querySelector('.book-btns').classList.add('active-btns')
                }
            })
        })   
    }
})