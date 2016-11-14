function sendInfo() {

    // Get the information from the form
    var location = document.getElementById('location').value;
    var recipe = document.getElementById('recipe').value;
    
    // Send result to new page
    window.location = "result.html?location=" + location + ";recipe=" + recipe;
}
