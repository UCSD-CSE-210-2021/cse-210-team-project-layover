$(document).ready(function() {
    var all_data = jQuery.parseJSON(data);                  // Read in data
    $("#meeting_name").html(all_data.name + " Results")     // Write the heading dynamically

    // Display all results in an unordered list
    // TODO: Use data to calculate table to display
    var fullList = "<ul>"
    $.each(all_data.users, function(i, value){              // Iterate through users
        fullList += "<li>" + i + "<ul>";                    // Create top level list and nested list
        $.each(value, function(j, v){                       // Iterate through user details
            fullList += "<li>" + j + " = " + v + "</li>"    // Populate nested list results
        })
        fullList += "</ul></li>"                            // End list for individual user
    });
    fullList += "</ul>"                                     // End list for all users
    $("#topDiv").html(fullList)                             // Display list in topDiv id from HTML file
});