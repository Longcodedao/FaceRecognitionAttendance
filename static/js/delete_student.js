function deleteStudent(studentId) {
  console.log("deleteStudent() called");
  if (confirm("Are you sure you want to delete this student?")) {
    // Make an AJAX request to delete the student
    fetch(`/deleteStudent/${studentId}`, {
      method: "DELETE",
    })
      .then((response) => {
        console.log("Response status:", response.status);
        return response.json();
      })
      .then((data) => {
        console.log("Response data:", data);

        if (data[0].message === "success") {
          console.log("reloading page");
          window.location.reload();
        }
      })
      .catch((error) => {
        console.error("Error deleting student:", error);
      });
  }
}
