document.addEventListener("DOMContentLoaded", () => {
  const createUnitForm = document.getElementById("createUnitForm");
  const unitsTableBody = document.getElementById("unitsTableBody");

  // Fetch user data on page load
  fetchUserData();

  // Handle create unit form submission
  createUnitForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(createUnitForm);
      const payload = {};

      formData.forEach((value, key) => {
          payload[key] = value;
      });

      try {
          const response = await fetch("http://127.0.0.1:5000/createUnit", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json",
                  Authorization: `Bearer ${localStorage.getItem("token")}`
              },
              body: JSON.stringify(payload)
          });

          const data = await response.json();
          if (data.status) {
              alert("Unit created successfully");
              fetchAllUnits();
          } else {
              alert("Error creating unit: " + data.log);
          }
      } catch (error) {
          console.error("Error creating unit:", error);
      }
  });

  // Fetch all units
  async function fetchAllUnits() {
      try {
          const response = await fetch("http://127.0.0.1:5000/fetchAllUnits", {
              method: "POST",
              headers: {
                  Authorization: `Bearer ${localStorage.getItem("token")}`
              }
          });

          const data = await response.json();
          if (data.status) {
              displayUnits(data.log);
          } else {
              alert("Error fetching units: " + data.log);
          }
      } catch (error) {
          console.error("Error fetching units:", error);
      }
  }

  // Display units in table
  function displayUnits(units) {
      unitsTableBody.innerHTML = "";
      units.forEach((unit) => {
          const row = document.createElement("tr");
          row.innerHTML = `
              <td>${unit.unitId}</td>
              <td>${unit.unit}</td>
              <td>${unit.others || "N/A"}</td>
          `;
          unitsTableBody.appendChild(row);
      });
  }

  // Fetch user data
  async function fetchUserData() {
      const token = localStorage.getItem("token");
      if (!token) {
          alert("User not authenticated");
          window.location.href = "/bms/templates/index.html";
          return;
      }

      try {
          const response = await fetch("http://127.0.0.1:5000/profile", {
              method: "POST",
              headers: {
                  Authorization: `Bearer ${token}`
              }
          });

          const result = await response.json();
          if (result.status) {
              document.getElementById("greeting").textContent = `Hello, ${result.userName}`;
              document.getElementById("user-info").textContent = `Logged in as: ${result.userName}`;
          } else {
              alert(result.log);
              window.location.href = "/bms/templates/index.html";
          }
      } catch (error) {
          console.error("Error fetching user data:", error);
          alert("Failed to fetch user data");
          window.location.href = "/bms/templates/index.html";
      }
  }

  // Logout function
  document.getElementById("logout").onclick = function() {
      localStorage.removeItem("token");
      window.location.href = "/bms/templates/index.html";
  };

  // Home button function
  window.goHome = function() {
      window.location.href = "/bms/templates/usersDashboard.html";
  };
});
