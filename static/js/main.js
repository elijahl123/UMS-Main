window.addEventListener("load", function () {
    $.ajax({
        url: '/api/courses/view/',
        success: function (data) {
            $.each(data, function (index, element) {
                $('#courses-list').prepend(`
                    <a class="list-group-item list-group-item-action list-group-item-${element.color} w-100" href="/courses/view/${element.id}" style="font-weight: bold;">
                    ${element.name}
                    </a>
               `)
            })
        }
    })
});