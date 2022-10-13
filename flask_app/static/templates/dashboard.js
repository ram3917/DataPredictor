$(document).ready(function(){  
    $('#switch').click(()=>
    {
    $([".light [class*='-light']", ".dark [class*='-dark']"]).each((i,ele)=>{
        $(ele).toggleClass('bg-light bg-dark')
        $(ele).toggleClass('btn-light btn-dark')
        $(ele).toggleClass('btn-secondary btn-dark')
        $(ele).toggleClass('table-light table-dark')
    })
    //toggle heading color
    // $('#heading').toggleClass('headingLight headingDark')
    $('#navigationbar').toggleClass('bg-secondary bg-dark')
    // toggle body class selector
    $('body').toggleClass('bg-light bg-dark')
    $('#switchText').text(
        $('#switchText').text() == 'Dark' ? 'Light' : 'Dark'
    );
})

});

function updateIndices(value)
{
    $.ajax({
        type: "POST",
        url: "/updateIndex",
        data: JSON.stringify(value),
        contentType: "application/json",
        dataType: 'json',
        success: function(response)
        {
            $("#stockList").html(response);
        }
    });
    $("#index").val(value);
    $("#index").text(value);
}

function updateCountry(value)
{
    ("#country").dropdown;
    $.ajax({
        type: "POST",
        url: "/updateCountry",
        data: JSON.stringify(value),
        contentType: "application/json",
        dataType: 'json',
        success: function(response)
        {
            $("#stockList").html(response);
        }
    });
    $("#country").val(value);
    $("#country").text(value);
}

function updateGraph(value)
{   
    options = document.getElementById('stockList');
    elements = options.getElementsByTagName("li");
    for(e of elements)
    {
        e.classList.remove('active');
    }

    option = document.getElementById(value);
    option.classList.add('active');

    $.ajax({
        type: "POST",
        url: "/updateGraph",
        data: JSON.stringify(value),
        contentType: "application/json",
        dataType: 'json',
        success: function(response)
        {
            Plotly.newPlot('myDiv', response, layout);
        }
    });
}

function filter(inputName, listName)
{
   input = document.getElementById(inputName).value.toUpperCase();

   options = document.getElementById(listName);
   elements = options.getElementsByTagName("a");
   for(e of elements)
   {
    txtValue = e.innerText;
    if (!txtValue.toUpperCase().includes(input)) 
    {
      e.style.display = "none";
    }
    else
    {
        e.style.display = "";
    }
   }
}