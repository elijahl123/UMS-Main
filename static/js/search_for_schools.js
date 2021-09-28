function searchForSchools(element) {
    let selectedSchools = []
    for (let i = 0; i < schools.length; i++) {
        let schoolName = schools[i].name
        if (schoolName.toLowerCase().includes($(element).val().toLowerCase())) {
            if (selectedSchools.length < 10) {
                selectedSchools.push(schools[i])
            }
        }
    }
    let html_list = ''
    $.each(selectedSchools, function (i, element) {
        let html_str = `
            <li class="list-group-item py-3 px-4" style="background: var(--secondary-color);">
                <form method="post" enctype="multipart/form-data">
                    ${csrfToken}
                    <input type="hidden" name="school" value="${element.name}">
                    <span style="color: slategray;font-size: 20px;font-weight: bold;">${element.name}</span>
                    <div class="d-flex flex-column flex-sm-row mt-2">
                        <button type="submit" class="btn btn-success btn-sm me-sm-2 me-0 mb-2 mb-sm-0"
                                style="font-weight: bold;">Select School
                        </button>
                        <a class="btn btn-secondary btn-sm" role="button" style="font-weight: bold;"
                           href="${element.web_pages[0]}" target="_blank">School
                            Website</a>
                    </div>
                </form>
            </li>
        `
        html_list += html_str
    })
    $('#schools-searched-list').html(html_list)
}
