
$(document).ready(function () {
    if ($("#form-success").val() === 'True') {
      $("#modal-notification").modal("show");
    }
  }
)
const modalClose = document.querySelector('#modal-close-btn')


const amountField = document.querySelector('#id_amount')

// amountField.addEventListener('input', function(){
//   let digitValue = $('#id_amount').attr('data-digit-value')
//   if(!digitValue){
//     digitValue = this.value
//   }
//   let amount = parseInt(digitValue)
//   console.log(amount)
//   amount = digitValue.toLocaleString('en-PK', {
//       maximumFractionDigits: 2,
//       style: 'currency',
//       currency: 'PKR'
//   })
//   console.log(amount)
//   $('#id_amount').val(amount)
//   $('#id_amount').attr('data-digit-value', digitValue)

// })


// modalClose.addEventListener('click', function() {
//   $("#modal-notification").modal("hide");
// })

//selecting all required elements
const dropArea = document.querySelector("#display-img"),
  dragText = dropArea.querySelector("header"),
  button = dropArea.querySelector("button"),
  input = document.querySelector("#imagefile");
let file; //this is a global variable and we'll use it inside multiple functions
// button.onclick = () => {
//   input.click(); //if user click on the button then the input also clicked
// };

input.addEventListener("change", function () {
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  file = this.files[0];
  dropArea.classList.add("active");
  console.log("first")
  showFile(); //calling function
});

//If user Drag File Over DropArea
dropArea.addEventListener("dragover", (event) => {
  event.preventDefault(); //preventing from default behaviour
  dropArea.classList.add("active");
  dragText.textContent = "Release to Upload File";
});

//If user leave dragged File from DropArea
dropArea.addEventListener("dragleave", () => {
  dropArea.classList.remove("active");
  dragText.textContent = "Drag & Drop to Upload File";
});

//If user drop File on DropArea
dropArea.addEventListener("drop", (event) => {
  event.preventDefault(); //preventing from default behaviour
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  file = event.dataTransfer.files[0];
  showFile(); //calling function
});

function showFile() {
  let fileType = file.type; //getting selected file type
  let validExtensions = ["image/jpeg", "image/jpg", "image/png"]; //adding some valid image extensions in array
  if (validExtensions.includes(fileType)) {
    //if user selected file is an image file
    let fileReader = new FileReader(); //creating new FileReader object
    fileReader.onload = () => {
      let fileURL = fileReader.result; //passing user file source in fileURL variable

      let imgTag = `<img height='150' width='150' src="${fileURL}" alt="">`; //creating an img tag and passing user selected file source inside src attribute
      dropArea.outerHTML = imgTag; //adding that created img tag inside dropArea container
    };
    fileReader.readAsDataURL(file);
  } else {
    alert("This is not an Image File!");
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload File";
  }
}
