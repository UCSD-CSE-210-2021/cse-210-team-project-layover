// Builds HTML table using the table Structure
function buildTableHTML(availability){
	
    var currTime = new Date(startingTimeStr);
    var currCellId = 0;
    var table = '<table id=tableSchedule>';

    table += [
        "<tr>",
        "  <th></th> <th>Sun</th> <th>Mon</th> <th>Tue</th>",
        "  <th>Wed</th> <th>Thu</th> <th>Fri</th> <th>Sat</th>",
        "</tr> "
    ].join("\n")

    // Loop through all the times we want
    for(var aTime = 0 ; aTime < numTimes ; aTime++){
        // append time or blank cell
        table += "<tr>"
        table += createTimeCell(currTime)
        // append remaining cells
        for(var j = 0 ; j < availability[0].length ; j++){
            table += createBlankCellWithId(currCellId);
            currCellId++;
        }

        table += "</tr>"

        // Create three rows of empty cells below time cell
        for(var numSlots = 0 ; numSlots < 3 ; numSlots++){
            table += "<tr>"
            table += createBlankCellWithoutId()

            // append remaining rows
            for(var j = 0 ; j < availability[0].length ; j++){
                table += createBlankCellWithId(currCellId);
                currCellId++;
            }
            table += "</tr>"
        }
    }
    table += '</table>'
    return table
}

function createBlankCellWithId(currCellId){
    ret = "<td id=" + currCellId + " class=clickable><br></td>";
    return ret
}

function createBlankCellWithoutId(){
    ret = "<td><br></td>";
    return ret
}

function createTimeCell(currTime){
    ret = "<td class=aaa>" + currTime.getHours() + ":00</td>";
    currTime.setHours(currTime.getHours() + 1);
    return ret;
}