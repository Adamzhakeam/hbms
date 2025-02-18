document.getElementById("resetForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    const phoneNumber = document.getElementById("phoneNumber").value;
    const responseMessage = document.getElementById("responseMessage");
    
    responseMessage.textContent = "Processing...";
    responseMessage.style.color = "black";
    
    try {
        const response = await fetch("http://127.0.0.1:5000/resetPassword", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ phoneNumber })
        });
        
        const result = await response.json();
        responseMessage.textContent = result.log || "Password reset successful";
        responseMessage.style.color = result.status ? "green" : "red";
    } catch (error) {
        responseMessage.textContent = "Error processing request";
        responseMessage.style.color = "red";
    }
});
