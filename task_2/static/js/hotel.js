$("button[name='btn_edit_hotel']").click(function() {

    window.location = "edit_hotel/"+$(this).data('hotel_id');

});
