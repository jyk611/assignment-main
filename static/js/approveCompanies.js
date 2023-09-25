$(document).ready(function() {
    // Listen for clicks on the "Approve" buttons
    $(".approve-button").click(function() {
        var companyName = $(this).data("company-name");

        // Send a POST request to the /approve_company route with the company name
        $.post("/approve_company", { compName: companyName }, function(data) {
            // Handle the response, e.g., show a success message
            console.log(data.message);
        }).fail(function(error) {
            // Handle errors, e.g., show an error message
            console.error(error.responseJSON.error);
        });
    });

    // Listen for clicks on the "Reject" buttons
    $(".reject-button").click(function() {
        var companyName = $(this).data("company-name");

        // Send a POST request to the /reject_company route with the company name
        $.post("/reject_company", { compName: companyName }, function(data) {
            // Handle the response, e.g., show a success message
            console.log(data.message);
        }).fail(function(error) {
            // Handle errors, e.g., show an error message
            console.error(error.responseJSON.error);
        });
    });
});