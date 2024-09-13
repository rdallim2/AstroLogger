const visualDropArea = document.getElementById("visual-drop-area");
const visualInputFile = document.getElementById("visual-input-file");
const visualImageView = document.getElementById("visual-img-view");

visualInputFile.addEventListener("change", function(){
  uploadImage(visualInputFile, visualImageView);
});

const imagingDropArea = document.getElementById("imaging-drop-area");
const imagingInputFile = document.getElementById("imaging-input-file");
const imagingImageView = document.getElementById("imaging-img-view");

imagingInputFile.addEventListener("change", function(){
  uploadImage(imagingInputFile, imagingImageView);
});


function uploadImage(inputFile, imageView){
  const file = inputFile.files[0];
  let imgLink = URL.createObjectURL(file);
  imageView.style.backgroundImage = `url(${imgLink})`;
  imageView.textContent = "";
  imageView.style.border = 0;

    // Send the image via FormData to the backend
    const formData = new FormData();
    formData.append("input-file", file);
  
    // Send formData via fetch API
    fetch("/submit_data", {
      method: "POST",
      body: formData
    })
    .then(result => {
      console.log("Image upload success:", result);
    })
    .catch(error => {
      console.error("Error uploading image:", error);
    });
}

imagingDropArea.addEventListener("dragover", function(e){
  e.preventDefault();
});
imagingDropArea.addEventListener("drop", function(e){
  e.preventDefault();
  inputFile.files = e.dataTransfer.files;
  uploadImage();
});

visualDropArea.addEventListener("dragover", function(e){
  e.preventDefault();
});
visualDropArea.addEventListener("drop", function(e){
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