function searchForTimezones() {
    let search_text = $('#search-for-timezones').val().toLowerCase()
    let rstring = new RegExp(search_text, 'gi')
    $.each($('.timezone-option'), function (i, element) {
        let text = $(element).text().toLowerCase()
        if (!text.match(rstring)) {
            $(element).addClass('d-none')
        } else {
            $(element).removeClass('d-none')
        }
    })
}

function submitForm(element) {
    $('#tz-input').val($(element).attr('data-tz'))
    $('#tz-form').submit()
}