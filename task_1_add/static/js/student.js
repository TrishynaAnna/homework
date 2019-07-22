$("button[name='btn_delete_student']").click(function() {

    var data = { student_code : $(this).data('student_code')}

    $.ajax({
      type: 'POST',
      url: "/delete_student",
      data: data,
      dataType: "text",
      success: function(resultData) {
          location.reload();
      }
});
});


$("button[name='btn_edit_student']").click(function() {

    window.location = "edit_student?student_code="+$(this).data('student_code');

});


$("button[name='btn_new_student']").click(function() {

    window.location = "new_student";

});

$("button[name='btn_new_work']").click(function() {

    window.location = "new_work?student_code="+$(this).data('student_code');

});
