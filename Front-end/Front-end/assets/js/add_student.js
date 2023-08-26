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

document.addEventListener('DOMContentLoaded', () => {
  const webcamElement = document.getElementById('video');
  const canvasElement = document.getElementById('canvas');
  const captureButton = document.getElementById('capture');

  async function startWebcam() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      webcamElement.srcObject = stream;
    } catch (error) {
      console.error('Error accessing webcam:', error);
    }
  }

  function captureImage() {
    canvasElement.width = webcamElement.videoWidth;
    canvasElement.height = webcamElement.videoHeight;
    canvasElement
      .getContext('2d')
      .drawImage(
        webcamElement,
        0,
        0,
        canvasElement.width,
        canvasElement.height
      );
    // You can now send the canvasElement.toDataURL() to the server or perform further actions with the image.
    console.log('Image captured:', canvasElement.toDataURL());
  }

  startWebcam();

  captureButton.addEventListener('click', captureImage);
});
