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

function addIndexToList(value)
{
    $('.dropdown-toggle').dropdown();
    $.ajax({
        type: "POST",
        url: "/addIndexToList",
        data: JSON.stringify(value),
        contentType: "application/json",
        dataType: 'json' 
    });
    $('.dropdown-toggle').val(value);
    $('.dropdown-toggle').text(value);
}

function updateGraph(value)
{
    $.ajax({
        type: "POST",
        url: "/updateGraph",
        data: JSON.stringify(value),
        contentType: "application/json",
        dataType: 'json'
    });
}

function filter(indices)
{
   console.log(indices); 
   input = document.getElementById("filterInput").value.toUpperCase();

   options = document.getElementById('indexList');
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