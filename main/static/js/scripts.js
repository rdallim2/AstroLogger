$("form[name=signup_form").submit(function(e){
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize(); //bundles data objects from form to send to backend

    $.ajax({
        url: "/user/signup",
        type: "POST",
        data: data,
        dataType: "json", 
        success: function(resp) {
            console.log(resp);
        },
        error: function(resp){
            console.log(resp)
            $error.text(resp.responseJSON.error).removeClass("error-hidden"); //get error message from models.py and remove hidden feature from html
        }
    });

    e.preventDefault();
});