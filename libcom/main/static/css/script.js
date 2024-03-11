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


    // Intercept form submission
    $('.save-rating').on('click', function(event) {
        const modal = $(this).parent().parent()

        const general = modal.find('.general-rating').find('input[type="radio"]:checked').val()
        const plot = modal.find('.plot-rating').find('input[type="radio"]:checked').val()
        const characters = modal.find('.characters-rating').find('input[type="radio"]:checked').val()
        const style = modal.find('.style-rating').find('input[type="radio"]:checked').val()
        const review = modal.find('[name="review"]').val()

        const formData = new FormData()
        formData.append('general', general)
        formData.append('plot', plot)
        formData.append('characters', characters)
        formData.append('style', style)
        formData.append('review', review)

        $(modal).find('.save-rating').hide()
        $(modal).find('.modal-footer').append('<div class="spinner-border" role="status"></div>')

        $.ajax({
            type: 'POST',
            url: $(this).data('action'), // Use the form's action attribute as URL
            data: formData,
            processData: false,
            contentType: false,
            beforeSend: function(xhr, settings) {
                // Get CSRF token from cookies
                var csrftoken = getCookie('csrftoken');
                
                // Set CSRF token in request headers
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(response) {
                $(modal).find('.save-rating').show()
                $(modal).find('.spinner-border').remove()
                $(modal).find('.btn-close').click()

                $('.alert-complete').find('.text-alert-input').text('Оценка успешно добавлена')
                $('.alert-complete').css('display', 'flex')
                $('.alert-complete').show('slow')
                setTimeout(() => {  $('.alert-complete').hide('slow') }, 2000);
            },
            error: function(xhr, errmsg, err) {
                // Handle error if needed
                console.log(xhr.status + ": " + xhr.responseText); // Log error message
            }
        })
    })

        // Intercept form submission
    $('.want-read-btn').on('click', function(event) {
        $.ajax({
            type: 'POST',
            url: $(this).data('action'),
            processData: false,
            contentType: false,
            beforeSend: function(xhr, settings) {
                // Get CSRF token from cookies
                var csrftoken = getCookie('csrftoken');
                
                // Set CSRF token in request headers
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(response) {
                $('.alert-complete').find('.text-alert-input').text('Вы успешно добавили книгу в Хочу прочитать')
                $('.alert-complete').css('display', 'flex')
                $('.alert-complete').show('slow')
                setTimeout(() => {  $('.alert-complete').hide('slow') }, 2000);
            },
            error: function(xhr, errmsg, err) {
                // Handle error if needed
                console.log(xhr.status + ": " + xhr.responseText); // Log error message
            }
        })
    })

    $('.read-now-btn').on('click', function(event) {
        $.ajax({
            type: 'POST',
            url: $(this).data('action'),
            processData: false,
            contentType: false,
            beforeSend: function(xhr, settings) {
                // Get CSRF token from cookies
                var csrftoken = getCookie('csrftoken');
                
                // Set CSRF token in request headers
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(response) {
                $('.alert-complete').find('.text-alert-input').text('Вы успешно добавили книгу в Читаю сейчас')
                $('.alert-complete').css('display', 'flex')
                $('.alert-complete').show('slow')
                setTimeout(() => {  $('.alert-complete').hide('slow') }, 2000);
            },
            error: function(xhr, errmsg, err) {
                // Handle error if needed
                console.log(xhr.status + ": " + xhr.responseText); // Log error message
            }
        })
    })

    // Function to get CSRF token from cookies
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
})