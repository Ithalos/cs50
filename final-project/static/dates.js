window.onload = function()
{
    // Get the name of the current page
    var currentPage = window.location.pathname;

    // Get references to the HTML elements we need
    var dates = getDates();
    var daysLeft = getDaysLeft();
}

/*
 * Populates the table data elements for days left in /tasks
*/
function setTaskDates(dates, daysLeft)
{
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

