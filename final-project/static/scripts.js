window.onload = function()
{
    // Get the name of the current page
    var currentPage = window.location.pathname;


    // Populate the table data elements for days left
    if (currentPage === "/tasks")
        setTaskDates(dates, daysLeft);
    else if (currentPage === "/birthdays")
        setBirthdayDates(dates, daysLeft);
}

/*
 * Populates the table data elements for days left in /tasks
*/
function setTaskDates(dates, daysLeft)
{
    // Get references to the HTML elements we need
    var dates = getDates();
    var daysLeft = getDaysLeft();

    var today = new Date();

    for (var i = 0; i < dates.length; i++)
    {
        var entry = new Date(dates[i].innerHTML);
        var diff = getDateDifference(today, entry);

        if (diff > 0)
        {
            daysLeft[i].style.color = "green";
            daysLeft[i].innerHTML = diff;
        }
        else if (diff < 0)
        {
            daysLeft[i].style.color = "red";
            daysLeft[i].innerHTML = "Passed";
        }
        else
        {
            daysLeft[i].style.color = "orange";
            daysLeft[i].innerHTML = "Today";
        }
    }
}

/*
 * Populates the table data elements for days left in /birthdays
*/
function setBirthdayDates(dates, daysLeft)
{
    // Get references to the HTML elements we need
    var dates = getDates();
    var daysLeft = getDaysLeft();

    var today = new Date();

    for (var i = 0; i < dates.length; i++)
    {
        var entry = new Date(dates[i].innerHTML);

        // The HTML values read in are birthdates, which means
        // they are all in the past. Set the year that was
        // read in to the next year, then calculate the difference.
        entry.setFullYear(today.getFullYear() + 1);

        var diff = getDateDifference(today, entry) % 365;
        daysLeft[i].innerHTML = diff;
    }
}

/*
 * Returns the difference between two dates, in days.
*/
function getDateDifference(today, entry)
{
    // Subtracting two dates returns a value in milliseconds.
    // 1000 * 60 * 60 * 24 is the amount of milliseconds in one day.
    return Math.floor((entry - today) / (1000 * 60 * 60 * 24)) + 1;
}

function getDates()
{
    return document.getElementsByClassName("js_date");
}

function getDaysLeft()
{
    return document.getElementsByClassName("js_daysleft");
}

