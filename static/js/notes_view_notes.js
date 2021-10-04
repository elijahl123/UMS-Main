function saveNotes() {
    let form = $("#view_notes_form")
    $.ajax({
        type: "POST",
        url: form.attr('action'),
        data: form.serialize(), // serializes the form's elements.
        success: function (data) {
        }
    });
}