function addDate(element, course_id) {
    let weekday = $(element).text().trim()

    if ($(element).attr('data-checked') === 'true') {
        $(element).attr('data-checked', 'false')
    } else {
        $(element).attr('data-checked', 'true')
    }

    let weekday_total = ''

    $('.weekday-choices-' + course_id).each(function () {
        if ($(this).attr('data-checked') === 'true') {
            let weekday_value = '\'' + $(this).text().trim() + '\'' + ', '
            weekday_total += weekday_value
            if ($(this).attr('data-checked') === 'true') {
                $(this).removeClass('btn-transparent-primary')
                $(this).addClass('btn-primary')
            }

        } else {
            $(this).addClass('btn-transparent-primary')
            $(this).removeClass('btn-primary')
        }
    })

    weekday_total = weekday_total.substring(0, weekday_total.length - 2)

    $('input[name="weekday"]').attr('value', '[' + weekday_total + ']')

}