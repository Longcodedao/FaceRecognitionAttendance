document.addEventListener("DOMContentLoaded", function () {
  const searchField = document.getElementById("searchForm");

  searchField.addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(searchField);
    const searchQuery = formData.get("searchVal");
    if (searchQuery) {
      performSearch(searchQuery);
    }
  });

  const table_body = document.getElementById("attendance-std");
  async function performSearch(query) {
    try {
      const response = await fetch(`/search?query=${query}`);
      if (!response.ok) {
        throw new Error("Network response was not ok.");
      }

      const data = await response.json();
      console.log("Search results:", data);
      console.log("Name is: ", data.classname);

      refreshingTable();
      displayTable(data);
    } catch (error) {
      console.error("Error:", error);
    }
  }
});

function refreshingTable() {
  const deleteRow = document.querySelectorAll("#deleteElement");

  deleteRow.forEach((LOL) => {
    let row = LOL.closest("tr");
    if (row) {
      row.remove();
    }
  });
}

function displayTable(data) {
  const loadingScreen = document.getElementById("loadingScreen");
  const tableAttenddance = document.getElementById("attendance-table");
  const tableAttendanceName = document.getElementById("table-name");
  const attendanceList = document.getElementById("attendance-std");

  loadingScreen.setAttribute("style", "display: none !important");
  tableAttenddance.setAttribute("style", "display: block");
  tableAttendanceName.textContent = data["classname"];

  attendance_list = data["attendance"];

  attendance_list.forEach((attendance) => {
    var tr = document.createElement("tr");
    attendanceList.appendChild(tr);

    var deleteEle = document.createElement("td");
    deleteEle.id = "deleteElement";
    deleteEle.setAttribute("style", "display: none !important");
    tr.appendChild(deleteEle);

    var td_1 = document.createElement("td");
    tr.appendChild(td_1);

    var div_1 = document.createElement("div");
    div_1.classList.add("d-flex", "px-2", "py-1");
    td_1.appendChild(div_1);

    var div_12 = document.createElement("div");
    div_12.classList.add("d-flex", "flex-column", "justify-content-center");
    div_1.appendChild(div_12);

    var h6_1 = document.createElement("h6");
    h6_1.classList.add("mb-0", "text-sm");
    h6_1.textContent = `${attendance["name"]}`;
    div_12.appendChild(h6_1);

    var p_1 = document.createElement("p");
    p_1.classList.add("text-xs", "text-secondary", "mb-0");
    p_1.textContent = `${attendance["time"]}`;
    div_12.appendChild(p_1);

    var td_2 = document.createElement("td");
    tr.appendChild(td_2);

    var p_12 = document.createElement("p");
    p_12.classList.add("text-xs", "font-weight-bold", "mb-0");
    p_12.textContent = `${attendance["classroom_name"]}`;
    td_2.appendChild(p_12);

    var p_22 = document.createElement("p");
    p_22.classList.add("text-xs", "text-secondary", "mb-0");
    if (attendance["late"] == true) {
      p_22.textContent = `Late`;
    } else {
      p_22.textContent = `On Time`;
    }
    // p_22.textContent = `${attendance["late"]}`;
    td_2.appendChild(p_22);
  });

  console.log(data.classname);
  console.log("Hello World");
}
