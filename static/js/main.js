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
                }

                if (!element.completed && !(due < today) && isSoon(due)) {
                    due_soon += 1
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
    $.ajax({
        url: '/api/coursetimes/view/',
        success: function (data) {
            const today = new Date()
            const weekday = today.toLocaleString("default", {weekday: "long"})

            let nextClass = []

            let start_time

            $.each(data, function (index, element) {
                if (element.weekday.includes(weekday)) {
                    const today_date = new Date(today)
                    today_date.setDate(today_date.getDate() - 1)
                    start_time = new Date(today_date.toISOString().substring(0, 10) + 'T' + element.start_time)
                    if (start_time.getTime() > today.getTime()) {
                        nextClass.push(element)
                    }
                }
            })

            let coursetime = nextClass[0]

            if (coursetime) {
                let html_str = `<div class="list-group-item-${coursetime.course.color} rounded p-3">
                                    <p class="mb-1" style="font-weight: bold;">Next Class</p>
                                    <h3 style="font-weight: bold;">${coursetime.course.name}</h3>`
                if (coursetime.link) {
                    html_str += `<a class="btn btn-${coursetime.course.color} btn-sm" role="button" href="${coursetime.link}" target="_blank" style="font-weight: bold;">
                                        Go to Class
                                    </a>
                                    <small class="text-white bg-secondary rounded m-2 py-1 px-2" style="font-weight: bold;border: 1px solid transparent">Password: ${coursetime.zoom_password}</small>
                                </div>`
                } else {
                    html_str += `</div>`
                }

                $('#navbar-collapse > .col').append(html_str)
            }
        }
    })

});