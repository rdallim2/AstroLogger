document.getElementById('view-past-logs-btn').addEventListener('click', function() {
    window.location.href = '/myLogs'; // Redirects to the specified URL
  });

document.getElementById('submission-btn').addEventListener('click', function() {
    window.location.href = '/submission'; // Redirects to the specified URL
    });

document.getElementById('login-btn').addEventListener('click', function() {
    window.location.href = '/'; // Redirects to the specified URL
    });

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
            window.location.href = "/myLogs"; //redirect to main page after account created
        },
        error: function(resp){
            console.log(resp)
            $error.text(resp.responseJSON.error).removeClass("error-hidden"); //get error message from models.py and remove hidden feature from html
        }
    });

    e.preventDefault();
});

$("form[name=login_form").submit(function(e){
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize(); //bundles data objects from form to send to backend

    $.ajax({
        url: "/user/login",
        type: "POST",
        data: data,
        dataType: "json", 
        success: function(resp) {
            console.log(resp);
            window.location.href = "/myLogs"; //redirect to main page after account created
        },
        error: function(resp){
            console.log(resp)
            $error.text(resp.responseJSON.error).removeClass("error-hidden"); //get error message from models.py and remove hidden feature from html
        }
    });

    e.preventDefault();
});