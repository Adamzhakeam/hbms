document
  .getElementById("resetPasswordForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const phoneNumber = document.getElementById("phoneNumber").value;
    const messageElement = document.getElementById("message");

    // Clear previous messages
    messageElement.textContent = "";

    // Send POST request to password reset API
    try {
      const response = await fetch("http://127.0.0.1:5000/resetPassword", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ phoneNumber: phoneNumber }),
      });

      const result = await response.json();

      if (result.status) {
        // If password reset is successful, send an email
        const emailResponse = await sendPasswordResetEmail(
          result.email,
          result.log
        );
        if (emailResponse.status) {
          messageElement.style.color = "green";
          messageElement.textContent =
            "Password reset successful! Check your email.";
        } else {
          messageElement.textContent =
            "Password reset successful, but there was an issue sending the email.";
        }
      } else {
        messageElement.textContent =
          result.log || "Password reset failed. Please try again.";
      }
    } catch (error) {
      console.error("Error:", error);
      messageElement.textContent = "An error occurred. Please try again later.";
    }
  });

// Function to send email after password reset
async function sendPasswordResetEmail(email, logMessage) {
  const payload = {
    subject: "Password Reset",
    recipients: [email],
    message: logMessage,
  };

  try {
    const response = await fetch("http://127.0.0.1:5000/sendMail", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Error sending email:", error);
    return { status: false, log: "Error sending email" };
  }
}
