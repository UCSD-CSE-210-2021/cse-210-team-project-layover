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
        table += createTimeCell(currTime, '12h')
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

function createTimeCell(currTime, timeFormat){
    let displayTime
    let meridiem
    if (timeFormat == '12h') {
        if (currTime < 12) {
            displayTime = currTime == 0 ? 12: currTime
            meridiem = 'AM'
        } else {
            displayTime = currTime == 12 ? 12: currTime - 12
            meridiem = 'PM'
        }
        return "<td class='noClick timeDisplay'>" + displayTime + ' ' + meridiem + "</td>";
    } else {
        return "<td class='noClick timeDisplay'>" + currTime + ":00</td>";
    }
}