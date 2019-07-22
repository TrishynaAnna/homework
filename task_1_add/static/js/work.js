$("button[name='btn_delete_work']").click(function() {

    var data = { work_title : $(this).data('work_title')}

    $.ajax({
      type: 'POST',
      url: "/delete_work",
      data: data,
      dataType: "text",
      success: function(resultData) {
          location.reload();
      }
});
});


$("button[name='btn_edit_work']").click(function() {

    window.location = "edit_work?work_title="+$(this).data('work_title');

});


$("button[name='btn_new_attempt']").click(function() {

    window.location = "new_attempt?work_title="+$(this).data('work_title');

});
