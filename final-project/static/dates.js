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

