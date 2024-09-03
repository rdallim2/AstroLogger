const dropArea = document.getElementById("drop-area");
const inputFile = document.getElementById("input-file");
const imageView = document.getElementById("img-view");

inputFile.addEventListener("change", uploadImage);

function uploadImage(){
  inputFile.files[0];
  let imgLink = URL.createObjectURL(inputFile.files[0]);
  imageView.style.backgroundImage = `url(${imgLink})`;
  imageView.textContent = "";
  imageView.style.border = 0;
}

dropArea.addEventListener("dragover", function(e){
  e.preventDefault();
});
dropArea.addEventListener("drop", function(e){
  e.preventDefault();
  inputFile.files = e.dataTransfer.files;
  uploadImage();
});



  function fetchCoordinates(zipCode) {
    $.ajax({
      url : '/ziptocoords',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ zip_code: zipCode }),
      success: function(data) {
        $('#inlineFormLatitude').val(data.latitude);
        $('#inlineFormLongitude').val(data.longitude);
      },
      error: function() {
        alert('ZIP code not found or invalid.');
        $('#inlineFormLatitude').val('');
        $('#inlineFormLongitude').val('');
      }
    });
  }
  $(document).ready(function() {
  $('#inlineFormLatitude, #inlineFormLongitude').on('input', function() {
            console.log("input recieved");
            const input = $(this).val();

            if (input.length === 5 && $.isNumeric(input)) { // Check if input is a 5-digit ZIP code
                fetchCoordinates(input);
            }
        });
});