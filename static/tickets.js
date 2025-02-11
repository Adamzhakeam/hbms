const wrapper = document.querySelector(".wrapper"),
  form = document.querySelector("form"),
  fileInp = form.querySelector("input"),
  infoText = form.querySelector("p"),
  closeBtn = document.querySelector(".close"),
  copyBtn = document.querySelector(".copy"),
  verifyBtn = document.querySelector(".verify"); // Added the Verify button

let qrResult = ""; // Store the scanned QR code result

// Function to handle fetching QR code content
function fetchRequest(file, formData) {
  infoText.innerText = "Scanning QR Code...";
  fetch("http://api.qrserver.com/v1/read-qr-code/", {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((result) => {
      result = result[0].symbol[0].data;
      infoText.innerText = result
        ? "QR Code Scanned Successfully"
        : "Couldn't scan QR Code";
      if (!result) return;
      qrResult = result; // Save the result for verification
      document.querySelector("textarea").innerText = result;
      form.querySelector("img").src = URL.createObjectURL(file);
      wrapper.classList.add("active");
    })
    .catch(() => {
      infoText.innerText = "Couldn't scan QR Code";
    });
}

// Event listener for file input change (scanning QR)
fileInp.addEventListener("change", async (e) => {
  let file = e.target.files[0];
  if (!file) return;
  let formData = new FormData();
  formData.append("file", file);
  fetchRequest(file, formData);
});

// Copy QR code content
copyBtn.addEventListener("click", () => {
  let text = document.querySelector("textarea").textContent;
  navigator.clipboard.writeText(text);
});

// Open file input on form click
form.addEventListener("click", () => fileInp.click());

// Close QR details
closeBtn.addEventListener("click", () => wrapper.classList.remove("active"));

// Verify QR Code Data with the Backend
verifyBtn.addEventListener("click", () => {
  if (!qrResult) {
    infoText.innerText = "No QR code to verify";
    return;
  }

  // Sending QR data to the /verifyQr endpoint
  fetch("http://127.0.0.1:5000/verifyQr", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ qr_data: qrResult }), // Send the QR code data
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.status) {
        infoText.innerText = "Verification successful: " + data.log;
      } else {
        infoText.innerText = "Verification failed: " + data.log;
      }
    })
    .catch((err) => {
      infoText.innerText = "Error verifying QR Code";
      console.error(err);
    });
});

// const wrapper = document.querySelector(".wrapper"),
//   form = document.querySelector("form"),
//   fileInp = form.querySelector("input"),
//   infoText = form.querySelector("p"),
//   closeBtn = document.querySelector(".close"),
//   copyBtn = document.querySelector(".copy");

// function fetchRequest(file, formData) {
//   infoText.innerText = "Scanning QR Code...";
//   fetch("http://api.qrserver.com/v1/read-qr-code/", {
//     method: "POST",
//     body: formData,
//   })
//     .then((res) => res.json())
//     .then((result) => {
//       result = result[0].symbol[0].data;
//       infoText.innerText = result
//         ? "Upload QR Code to Scan"
//         : "Couldn't scan QR Code";
//       if (!result) return;
//       document.querySelector("textarea").innerText = result;
//       form.querySelector("img").src = URL.createObjectURL(file);
//       wrapper.classList.add("active");
//     })
//     .catch(() => {
//       infoText.innerText = "Couldn't scan QR Code";
//     });
// }

// fileInp.addEventListener("change", async (e) => {
//   let file = e.target.files[0];
//   if (!file) return;
//   let formData = new FormData();
//   formData.append("file", file);
//   fetchRequest(file, formData);
// });

// copyBtn.addEventListener("click", () => {
//   let text = document.querySelector("textarea").textContent;
//   navigator.clipboard.writeText(text);
// });

// form.addEventListener("click", () => fileInp.click());
// closeBtn.addEventListener("click", () => wrapper.classList.remove("active"));
