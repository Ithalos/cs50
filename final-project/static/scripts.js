window.onload = function()
{
    // If this page has a login form, attach functionality to it
    var login = document.getElementById("login");
    if (login)
    {
        attachLoginEvents(login);
    }

    // If this page has a register form, attach functionality to it
    var register = document.getElementById("register");
    if (register)
    {
        attachRegisterEvents(register);
    }

    // Check if we are on the /tasks page
    var taskForm = document.getElementById("task_form");
    if (taskForm)
    {
        // Populate the table data elements for days left
        setTaskDates();
        // Add date field verification
        attachDateEvents(taskForm);
        // Add task field verification
        emptyFieldCheck(taskForm, taskForm.task_text);
    }

    // Check if we are on the /birthdays page
    var birthdayForm = document.getElementById("birthday_form");
    if (birthdayForm)
    {
        // Populate the table data elements for days left
        setBirthdayDates();
        // Add date field verification
        attachDateEvents(birthdayForm);
        // Add birthday field verification
        emptyFieldCheck(birthdayForm, birthdayForm.birthday_person);
    }

    // Check if we are on the /memos page
    var memoForm = document.getElementById("memo_form");
    if (memoForm)
    {
        // Add memo field verification
        emptyFieldCheck(form, form.memo_text);
    }
};

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

// Get HTML element references
function getDates()
{
    return document.getElementsByClassName("js_date");
}

// Get HTML element references
function getDaysLeft()
{
    return document.getElementsByClassName("js_daysleft");
}

// Attach functionality to login form
function attachLoginEvents(login)
{
    attachUsernameEvents(login.username);
    attachPasswordEvents(login.password);
    attachFormValidation(login);
}

// Attach functionality to register form
function attachRegisterEvents(register)
{
    attachUsernameEvents(register.username);
    attachPasswordConfirmationEvents(register.password, register.confirmation);
    attachFormValidation(register);
}

// Colours the username input of a form
function attachUsernameEvents(username)
{
    username.addEventListener("input", function()
    {
        colourSingleInput(username, 4);
    });
}

// Colours the password input of a form
function attachPasswordEvents(password)
{
    password.addEventListener("input", function()
    {
        colourSingleInput(password, 8);
    });
}

// Colours the password and confirmation input of a form
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

// Colours the given input, depending on its length
function colourSingleInput(input, length)
{
    if (input.value.length === 0)
        input.style.color = "";
    else if (input.value.length < length)
        input.style.color = "red";
    else
        input.style.color = "green";
}

/*
 * Colours the given inputs, depending on their lengths,
 * and whether or not they match.
*/
function colourDualInputs(firstInput, secondInput, length)
{
    if (firstInput.value.length >= length && secondInput.value.length >= length)
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
        colourSingleInput(firstInput, length);
    }
}

/*
 * Validates a login or register form. Returns an array, whose first index
 * will be a boolean that reflects the validity of the form.
 * If the form was invalid, all further indices will be separate
 * error messages that state which inputs were invalid and why.
*/
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
    if (form.confirmation)
    {
        if (form.password.value !== form.confirmation.value)
        {
            values[0] = false;
            values.push("Your password & confirmation do not match!");
        }
    }

    return values;
}

/*
 * Stops submission of the login or register form unless all inputs are valid.
 * Prints an error message for every invalid input when the form is submitted.
*/
function attachFormValidation(form)
{
    form.addEventListener("submit", function(event)
    {
        // Prevent form submission
        event.preventDefault();

        // Clean up potential errors that already exist from a previous attempt
        var errors = document.getElementsByClassName("error");
        while (errors.length > 0)
            errors[0].remove();

        // Check form validity
        var values = formValidation(form);
        if (values[0])
        {
            form.submit();
        }
        else
        {
            // Iterate over error messages and display them on screen.
            // This loop must be 1-indexed, else the boolean
            // value will also be displayed.
            for (var i = 1; i < values.length; i++)
            {
                var element = document.createElement("p");
                var text = document.createTextNode(values[i]);
                element.appendChild(text);
                element.className = "error";
                element.style.color = "red";
                form.appendChild(element);
            }
        }
    });
}

// Check whether a string is a valid ISO date. (YYYY-MM-DD)
function validateISODateString(date)
{
    var date = new Date(date);
    return !isNaN(date.getTime());
}

/*
 * Validate the date field when creating a new task or birthday.
 * If the date is not a valid ISO format, display an error.
*/
function attachDateEvents(form)
{
    form.addEventListener("submit", function(event)
    {
        // Prevent form submission
        event.preventDefault();

        if (validateISODateString(form.isodate.value))
        {
            form.submit();
        }
        else
        {
            // Display error message
            form.isodate.focus();
            form.isodate.value = "";
            form.isodate.style.color = "red";
            form.isodate.placeholder = "Date format must be YYYY-MM-DD!";
        }
    });

    // Reset date field styling and placeholder on new input
    form.isodate.addEventListener("input", function()
    {
        form.isodate.placeholder = "YYYY-MM-DD";
        form.isodate.style.color = "";
    });
}

/*
 * Validate a form field on submission.
 * If the field is empty, display an error.
*/
function emptyFieldCheck(form, field)
{
    var defaultPlaceholder = field.placeholder;

    form.addEventListener("submit", function(event)
    {
        // Prevent form submission
        event.preventDefault();

        // Check for empty field
        if (field.value.length === 0)
        {
            // Display error message
            field.focus();
            field.style.color = "red";
            field.placeholder = "Please fill in this field!";
        }
        else
        {
            form.submit();
        }
    });

    // Reset field styling and placeholder on new input
    field.addEventListener("input", function()
    {
        field.placeholder = defaultPlaceholder;
        field.style = "";
    });
}

