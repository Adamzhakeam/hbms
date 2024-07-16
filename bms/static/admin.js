// add hovered class to selected list item
let list = document.querySelectorAll(".navigation li");

function activeLink() {
  list.forEach((item) => {
    item.classList.remove("hovered");
  });
  this.classList.add("hovered");
}

list.forEach((item) => item.addEventListener("mouseover", activeLink));

// Menu Toggle
let toggle = document.querySelector(".toggle");
let navigation = document.querySelector(".navigation");
let main = document.querySelector(".main");

toggle.onclick = function () {
  navigation.classList.toggle("active");
  main.classList.toggle("active");
};
// fetching all products 
document.addEventListener('DOMContentLoaded', () => {
  fetchTotalProducts();
});

function fetchTotalProducts() {
  fetch('http://127.0.0.1:5000/fetchAllProducts', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      }
  })
  .then(response => response.json())
  .then(data => {
      if (data.status) {
          updateTotalProducts(data.log.length);
      } else {
          console.error('Failed to fetch products:', data.log);
          updateTotalProducts(0); // Set to 0 if there's an error or no products
      }
  })
  .catch(error => {
      console.error('Error fetching products:', error);
      updateTotalProducts(0); // Set to 0 if there's an error
  });
}

function updateTotalProducts(total) {
  const totalProductsElement = document.getElementById('totalNumberOfProducts');
  totalProductsElement.textContent = total;
}
// -----the sales fetch on the sals card 
document.addEventListener('DOMContentLoaded', () => {
  fetchTotalSales();
});

function fetchTotalSales() {
  fetch('http://127.0.0.1:5000/fetchAllSales', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      }
  })
  .then(response => response.json())
  .then(data => {
      if (data.status) {
          updateTotalSales(data.log.length);
      } else {
          console.error('Failed to fetch sales:', data.log);
          updateTotalSales(0); // Set to 0 if there's an error or no sales
      }
  })
  .catch(error => {
      console.error('Error fetching sales:', error);
      updateTotalSales(0); // Set to 0 if there's an error
  });
}

function updateTotalSales(total) {
  const totalSalesElement = document.getElementById('totalSales');
  totalSalesElement.textContent = total;
}
// ----these are the total sales 
document.addEventListener('DOMContentLoaded', () => {
  fetchTotalAmountPaid();
});

function fetchTotalAmountPaid() {
  fetch('http://127.0.0.1:5000/fetchAllSales', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      }
  })
  .then(response => response.json())
  .then(data => {
      if (data.status) {
          const totalAmountPaid = calculateTotalAmountPaid(data.log);
          updateTotalAmountPaid(totalAmountPaid);
      } else {
          console.error('Failed to fetch sales:', data.log);
          updateTotalAmountPaid(0); // Set to 0 if there's an error or no sales
      }
  })
  .catch(error => {
      console.error('Error fetching sales:', error);
      updateTotalAmountPaid(0); // Set to 0 if there's an error
  });
}

function calculateTotalAmountPaid(sales) {
  let total = 0;
  sales.forEach(sale => {
      total += parseFloat(sale.amountPaid);
  });
  return total;
}

function updateTotalAmountPaid(total) {
  const totalAmountPaidElement = document.getElementById('totalAmountPaid');
  totalAmountPaidElement.textContent = `ugx${total.toFixed(2)}`;
}
// -----this js below is responsible for the table 
// ----chart----

	// global options variable
	var options = {
		responsive: true,
		easing:'easeInExpo',
		scaleBeginAtZero: true,
        // you don't have to define this here, it exists inside the global defaults
		legendTemplate: "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<segments.length; i++){%><li><span style=\"background-color:<%=segments[i].fillColor%>\"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>"
	}

		// PIE
		// PROPERTY TYPE DISTRIBUTION
		// context
		var ctxPTD = $("#property_types").get(0).getContext("2d");
		// data
		var dataPTD = [
			{
				label: "Single Family Residence",
				color: "#5093ce",
				highlight: "#78acd9",
				value: 52
			},
			{
				label: "Townhouse/Condo",
				color: "#c7ccd1",
				highlight: "#e3e6e8",
				value: 12
			},
			{
				label: "Land",
				color: "#7fc77f",
				highlight: "#a3d7a3",
				value: 6
			},
			{
				label: "Multifamily",
				color: "#fab657",
				highlight: "#fbcb88",
				value: 8
			},
			{
				label: "Farm/Ranch",
				color: "#eaaede",
				highlight: "#f5d6ef",
				value: 8
			},
			{
				label: "Commercial",
				color: "#dd6864",
				highlight: "#e6918e",
				value: 14
			},
			
		]

		// Property Type Distribution
		var propertyTypes = new Chart(ctxPTD).Pie(dataPTD, options);
			// pie chart legend
			$("#pie_legend").html(propertyTypes.generateLegend());


// ++++++==========this is for the table 



document.addEventListener('DOMContentLoaded', () => {
  fetchCategories();
});

function fetchCategories() {
  fetch('http://127.0.0.1:5000/fetchAllCategories', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      }
  })
  .then(response => response.json())
  .then(data => {
      if (data.status) {
          populateCategories(data.log);
      } else {
          console.error('Failed to fetch categories:', data.log);
      }
  })
  .catch(error => {
      console.error('Error fetching categories:', error);
  });
}

function populateCategories(categories) {
  categories.forEach((category, index) => {
      const categoryElement = document.getElementById(`category${index + 1}`);
      if (categoryElement) {
          categoryElement.innerHTML = `${category.category} <br> <span>${category.category}</span>`;
      }
  });
}
