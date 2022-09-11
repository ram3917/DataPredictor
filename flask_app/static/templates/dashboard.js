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