$("button[name='btn_delete_attempt']").click(function() {

    var data = { work_title_fk : $(this).data('work_title_fk'), mark_date : $(this).data('mark_date')}

    $.ajax({
      type: 'POST',
      url: "/delete_attempt",
      data: data,
      dataType: "text",
      success: function(resultData) {
          location.reload();
      }
});
});


$("button[name='btn_edit_attempt']").click(function() {

    window.location = "edit_attempt?work_title_fk="+$(this).data('work_title_fk')+"&mark_date="+$(this).data('mark_date');

});
