// Builds HTML table using the table Structure
function buildTableHTML(startTime, endTime){
	
    var currTime = startTime;
    
    var currCellId = 0;
    var table = '<table id=tableSchedule>';

    table += [
        "<tr>",
        "  <th></th> <th>Sun</th> <th>Mon</th> <th>Tue</th>",
        "  <th>Wed</th> <th>Thu</th> <th>Fri</th> <th>Sat</th>",
        "</tr> "
    ].join("\n")

    while(currTime != endTime){
        // append time or blank cell
        table += "<tr>"
        table += createTimeCell(currTime)
        // append remaining cells
        for(var j = 0 ; j < numCol - 1 ; j++){
            table += createBlankCellWithId(currCellId);
            currCellId++;
        }

        table += "</tr>"

        // Create three rows of empty cells below time cell
        for(var numSlots = 0 ; numSlots < 3 ; numSlots++){
            table += "<tr>"
            table += createBlankCellWithoutId()

            // append remaining rows
            for(var j = 0 ; j < numCol - 1 ; j++){
                table += createBlankCellWithId(currCellId);
                currCellId++;
            }
            table += "</tr>"
        }
        currTime++;
    }
    table += '</table>'
    return table
}

function createBlankCellWithId(currCellId){
    ret = "<td id=" + currCellId + " class=clickable><br></td>";
    return ret
}

function createBlankCellWithoutId(){
    ret = "<td class='noClick'><br></td>";
    return ret
}

function createTimeCell(currTime){
    ret = "<td class='noClick'>" + currTime + ":00</td>";
    return ret;
}