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
            const today = new Date()
            const tomorrow = new Date(today)
            tomorrow.setDate(tomorrow.getDate() + 1)
            const isSoon = (d) => {
                return (d.getDate() === today.getDate() &&
                        d.getMonth() === today.getMonth() &&
                        d.getFullYear() === today.getFullYear()) ||
                    (d.getDate() === tomorrow.getDate() &&
                        d.getMonth() === tomorrow.getMonth() &&
                        d.getFullYear() === tomorrow.getFullYear())
            }
            let late_assignments = 0
            let due_soon = 0
            $.each(data, function (index, element) {
                const due = new Date(element.due_date + 'T' + element.due_time)
                if (!element.completed && due < today) {
                    late_assignments += 1
                    console.log(element, 'Late')
                }

                if (!element.completed && !(due < today) && isSoon(due)) {
                    due_soon += 1
                    console.log(element, 'Due Soon')
                }

            })
            if (late_assignments) {
                $('#homework-nav-link').append(`
                    <span class="badge bg-danger ms-2">${late_assignments} Late</span>
                `)
            }
            if (due_soon) {
                $('#homework-nav-link').append(`
                    <span class="badge bg-warning ms-2">${due_soon} Due Soon</span>
                `)
            }
        }
    })

});