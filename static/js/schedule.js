window.addEventListener('load', (event) => {
    let events = $('.coursetime')
    events.each(function () {
        let start_time = $(this).attr('data-start-time')
        let end_time = $(this).attr('data-end-time')

        let div_height = (parseInt(end_time.substring(0, 2)) + (parseInt(end_time.substring(3, 5)) / 60))
        div_height -= (parseInt(start_time.substring(0, 2)) + (parseInt(start_time.substring(3, 5)) / 60))
        div_height *= 100
        $(this).css('height', div_height + 'px')


        let div_margin_top = (parseInt(start_time.substring(0, 2)) - 7) * 100 + 80
        if (parseInt(start_time.substring(3, 5))) {
            div_margin_top += (parseInt(start_time.substring(3, 5)) / 60) * 100
        }
        $(this).animate(
            {marginTop: div_margin_top + 'px'},
            500,
            "swing"
        )

    })
});
