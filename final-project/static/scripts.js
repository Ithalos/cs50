window.onload = function()
{
    // Get the name of the current page
    var currentPage = window.location.pathname;

    // Add some visual feedback to the login form
    var login = document.getElementById("login");
    if (login !== null)
    {
        attachLoginEvents(login);
    }

    // Add some visual feedback to the register form
    var register = document.getElementById("register");
    if (register !== null)
    {
        attachRegisterEvents(register);
    }

    // Populate the table data elements for days left
    if (currentPage === "/tasks")
        setTaskDates();
    else if (currentPage === "/birthdays")
        setBirthdayDates();
}

/*
 * Populates the table data elements for days left in /tasks
*/
function setTaskDates()
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
function setBirthdayDates()
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

function attachLoginEvents(login)
{
    attachUsernameEvents(login.username);
    attachPasswordEvents(login.password);
}

function attachRegisterEvents(register)
{
    attachUsernameEvents(register.username);
    attachPasswordConfirmationEvents(register.password, register.confirmation);
}

function attachUsernameEvents(username)
{
    username.addEventListener("input", function()
    {
        colourSingleInput(username, 4);
    });
}

function attachPasswordEvents(password)
{
    password.addEventListener("input", function()
    {
        colourSingleInput(password, 8);
    });
}

function attachPasswordConfirmationEvents(password, confirmation)
{
    password.addEventListener("input", function()
    {
        colourDualInputs(password, confirmation, 8);
    });

    confirmation.addEventListener("input", function()
    {
        colourDualInputs(confirmation, password, 8);
    });
}

function colourSingleInput(input, length)
{
    if (input.value.length === 0)
        input.style.color = "";
    else if (input.value.length < length)
        input.style.color = "red";
    else
        input.style.color = "green";
}

function colourDualInputs(firstInput, secondInput, length)
{
    if (firstInput.value.length >= length && secondInput.value.length >= 8)
    {
        if (firstInput.value === secondInput.value)
        {
            firstInput.style.color = "green";
            secondInput.style.color = "green";
        }
        else
        {
            firstInput.style.color = "red";
            secondInput.style.color = "red";
        }
    }
    else
    {
        colourSingleInput(firstInput, 8);
    }
}

function formValidation(form)
{
    var values = [];
    values[0] = true;

    if (form.username.value.length < 4)
    {
        values[0] = false;
        values.push("Your username must be at least 4 characters long!");
    }
    if (form.password.value.length < 8)
    {
        values[0] = false;
        values.push("Your password must be at least 8 characters long!");
    }
    if (form.confirmation !== null)
    {
        if (form.password.value !== form.confirmation.value)
        {
            values[0] = false;
            values.push("Your password & confirmation do not match!");
        }
    }

    return values;
}

