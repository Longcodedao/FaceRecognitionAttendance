// navigator.mediaDevices
//   .getUserMedia({ video: true })
//   .then(function (stream) {
//     var video = document.getElementById('video');
//     video.srcObject = stream;
//   })
//   .catch(function (error) {
//     console.log('Error accessing webcam: ' + error);
//   });

// var captureButton = document.getElementById('capture');
// captureButton.addEventListener('click', function () {
//   var video = document.getElementById('video');
//   var canvas = document.createElement('canvas');
//   canvas.width = video.videoWidth;
//   canvas.height = video.videoHeight;
//   var ctx = canvas.getContext('2d');
//   ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

//   var dataURL = canvas.toDataURL('image/png');

//   fetch('/upload_capture_img', {
//     method: 'POST',
//     body: JSON.stringify({ image: dataURL }),
//     headers: {
//       'Content-Type': 'application/json',
//     },
//   })
//     .then((response) => response.text())
//     .then((result) => console.log(result))
//     .then(() => (window.location.href = '/'))
//     .catch((error) => console.log('Error uploading image: ' + error));
// });

// Capturing the image
let imageURL = '';

const openOverlayButton = document.getElementById('openOverlayBtn');
const closeOverlayButton = document.getElementById('closeOverlayBtn');
const imageOverlay = document.getElementById('imageOverlay');
const webcamElement = document.getElementById('webcam');
const captureButton = document.getElementById('captureBtn');
const downloadButton = document.getElementById('downloadBtn');
const downloadLink = document.getElementById('downloadLink');
// const imageDataInput = document.getElementById('imageData');
const downloadLocation = document.getElementById('downloadLocation');
const firstName = document.getElementById('first-name');

async function startWebcam() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    webcamElement.srcObject = stream;
  } catch (error) {
    console.error('Error accessing webcam:', error);
  }
}

function captureImage() {
  const canvas = document.createElement('canvas');
  canvas.width = webcamElement.videoWidth;
  canvas.height = webcamElement.videoHeight;
  canvas
    .getContext('2d')
    .drawImage(webcamElement, 0, 0, canvas.width, canvas.height);
  imageURL = canvas.toDataURL('image/png'); // You can also use 'image/png'
  downloadLocation.value = imageURL;
  closeImageOverlay();
}

// function
function openImageOverlay() {
  imageOverlay.style.display = 'flex';
  startWebcam();
}

function closeImageOverlay() {
  imageOverlay.style.display = 'none';
  webcamElement.srcObject.getTracks().forEach((track) => track.stop());
}

// async function uploadImage() {
//   try {
//     console.log(firstName.value);
//     const response = await fetch('/upload_capture_img', {
//       method: 'POST',
//       body: JSON.stringify({ image: imageURL, name: firstName.value }),
//       headers: {
//         'Content-Type': 'application/json',
//       },
//     });

//     if (response.ok) {
//       const result = await response.text();
//       console.log(result);
//       // Redirect to the desired location after successful upload
//       window.location.href = '/';
//     } else {
//       console.log('Image upload failed with status:', response.status);
//     }
//   } catch (error) {
//     console.log('Error uploading image:', error);
//   }
// }
openOverlayButton.addEventListener('click', openImageOverlay);
closeOverlayButton.addEventListener('click', closeImageOverlay);
captureButton.addEventListener('click', captureImage);
// downloadButton.addEventListener('click', uploadImage);

//  Form validation Field
const addStudentForm = document.getElementById('addStudentForm');

addStudentForm.addEventListener('submit', async (event) => {
  event.preventDefault();

  console.log('Hello World');
  const firstName = document.getElementById('first-name').value;
  const lastName = document.getElementById('last-name').value;
  const email = document.getElementById('email').value;
  const studentID = document.getElementById('student-id').value;
  const classStudy = document.getElementById('class').value;

  if (!checkValidate()) {
    // console.log('Wrong');
    return;
  }

  const formData = {
    first_name: firstName,
    last_name: lastName,
    email: email,
    student_id: studentID,
    class_study: classStudy,
    image: imageURL,
  };

  try {
    const response = await fetch('/addNewStudent', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    });

    if (response.ok) {
      alert('Student added successfully!');
      // Clear form fields after successful submission
      addStudentForm.reset();
      window.location.href = '/tableNew';
    } else {
      console.error('Add student request failed with status:', response.status);
      alert('Failed to add student.');
    }
  } catch (error) {
    console.error('Error adding student:', error);
    alert('An error occurred while adding student.');
  }

  function checkValidate() {
    let isValid = true;

    if (!firstName.trim()) {
      isValid = false;
      document.getElementById('first-name-warning').textContent =
        'Please enter First Name';
    }

    if (!lastName.trim()) {
      isValid = false;
      document.getElementById('last-name-warning').textContent =
        'Please enter Last Name';
    }

    if (!email.trim()) {
      isValid = false;
      document.getElementById('email-warning').textContent =
        'Please enter your email';
    }

    if (!studentID.trim()) {
      isValid = false;
      document.getElementById('studentid-warning').textContent =
        'Please enter your student ID';
    }

    if (!classStudy.trim()) {
      isValid = false;
      document.getElementById('class-warning').textContent =
        'Please enter your class';
    }

    if (!imageURL) {
      isValid = false;
      document.getElementById('image-warning').textContent =
        'Please insert an image';
    }

    return isValid;
  }
});
