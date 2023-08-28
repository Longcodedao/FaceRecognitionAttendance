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
  imageURL = canvas.toDataURL('image/jpeg'); // You can also use 'image/png'
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

openOverlayButton.addEventListener('click', openImageOverlay);
closeOverlayButton.addEventListener('click', closeImageOverlay);
captureButton.addEventListener('click', captureImage);

//  Submit event
const addStudentForm = document.getElementById('addStudentForm');

addStudentForm.addEventListener('submit', async (event) => {
  event.preventDefault();

  let firstName = document.getElementById('first-name').value;
  let lastName = document.getElementById('last-name').value;
  let email = document.getElementById('email').value;
  let studentID = document.getElementById('student-id').value;
  let classStudy = document.getElementById('class').value;

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
    } else {
      document.getElementById('first-name-warning').textContent = '';
    }

    if (!lastName.trim()) {
      isValid = false;
      document.getElementById('last-name-warning').textContent =
        'Please enter Last Name';
    } else {
      document.getElementById('last-name-warning').textContent = '';
    }

    if (!email.trim()) {
      isValid = false;
      document.getElementById('email-warning').textContent =
        'Please enter your email';
    } else {
      document.getElementById('email-warning').textContent = '';
    }

    if (!studentID.trim()) {
      isValid = false;
      document.getElementById('studentid-warning').textContent =
        'Please enter your student ID';
    } else {
      document.getElementById('studentid-warning').textContent = '';
    }

    if (!classStudy.trim()) {
      isValid = false;
      document.getElementById('class-warning').textContent =
        'Please enter your class';
    } else {
      document.getElementById('class-warning').textContent = '';
    }

    if (!imageURL) {
      isValid = false;
      document.getElementById('image-warning').textContent =
        'Please insert an image';
    } else {
      document.getElementById('image-warning').textContent = '';
    }

    return isValid;
  }
});
