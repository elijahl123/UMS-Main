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
    $.ajax({
        url: '/api/assignments/view/',
        success: function (data) {
            const d = new Date()
            let late_assignments = 0
            $.each(data, function (index, element) {
                const due = new Date(element.due_date + 'T' + element.due_time)
                if (!element.completed && due < d) {
                    late_assignments += 1
                }
            })
            if (late_assignments) {
                $('#homework-nav-link').append(`
                    <span class="badge bg-danger ms-2">${late_assignments} Late</span>
                `)
            }
        }
    })

});