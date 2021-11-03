$(document).ready(function() {
    var all_data = jQuery.parseJSON(data)
    $("#results_btn").attr("href", "/results/" + all_data.meeting_id);
    $("#meeting_id").attr("value", all_data.meeting_id);

    $('#schedule').append(
        buildTableHTML()
    )

    var tableStructure;
    var currCellId;
    var currTime;
    var numCol;
    var numTimes;
    // Builds HTML table using the table Structure
    function buildTableHTML(){
        currCellId = 0;
        numCol = 8;
        numTimes = 24;
        currTime = new Date('December 17, 1995 00:00:00');

        // Initialize backend data structure to store times. Fill with 0's
        tableStructure = Array(numTimes * 4).fill().map(() => Array(numCol - 1).fill(0));
        var table = '<table id=schedule>';

        table += [
            "<tr>",
            "  <th></th> <th>Sunday</th> <th>Monday</th> <th>Tuesday</th>",
            "  <th>Wednesday</th> <th>Thursday</th> <th>Friday</th> <th>Saturday</th>",
            "</tr> "
          ].join("\n")

        // Loop through all the times we want
        for(var i = 0 ; i < numTimes ; i++){
            // append time or blank cell
            table += "<tr>"
            table += createTimeCell()
            // append remaining cells
            for(var j = 0 ; j < numCol - 1 ; j++){
                table += createBlankCellWithId();
            }

            table += "</tr>"

            // Create three rows of empty cells below time cell
            for(var numSlots = 0 ; numSlots < 3 ; numSlots++){
                table += "<tr>"
                table += createBlankCellWithoutId()

                // append remaining rows
                for(var j = 0 ; j < numCol - 1 ; j++){
                    table += createBlankCellWithId();
                }
                table += "</tr>"
            }
        }
        table += '</table>'
        return table
    }

    function createBlankCellWithId(){
        var currId = currCellId
        var row = Math.floor(currId / (numCol - 1))
        var col = currId %(numCol - 1)
        var cellVal = tableStructure[row][col]

        ret = "<td id=" + currCellId + " class=clickable bgcolor=" ;
        if(cellVal === 0){
            ret += "white";
        }else if( cellVal === 0.75){
            ret += "yellow";
        }else{
            ret += "green";
        }

        ret += "><br></td>";
        currCellId++;
        return ret 
    }

    function createBlankCellWithoutId(){
        ret = "<td><br></td>";
        return ret 
    }

    function createTimeCell(){
        ret = "<td>" + currTime.getHours() + ":00</td>"; 
        currTime.setHours(currTime.getHours() + 1);
        return ret;
    }

    $(".clickable").click(function(){
        var currColor = $(this).attr("bgcolor")
        var currId = parseInt($(this).attr("id"))
        var row = Math.floor(currId / (numCol - 1))
        var col = currId %(numCol - 1)
        console.log("currColor is: " + currColor);
        if(currColor === "white"){
            $(this).attr("bgcolor","green");
            tableStructure[row][col] = 1;
        }
        else if(currColor === "green"){
            $(this).attr("bgcolor","yellow");
            tableStructure[row][col] = 0.75;
        }else{
            $(this).attr("bgcolor","white");
            tableStructure[row][col] = 0;
        }

        console.log("changing cell color");
        console.log($(this));
        console.log(tableStructure);

    });

    $("#abab").click(function(){
        console.log("submitting availability");
        $.ajax
        ({
            type: "POST",
            url: '/submitAvailability',
            data : JSON.stringify({tableStructure: tableStructure}),
            contentType : 'application/json',
            dataType: 'json'
        })
    });

});