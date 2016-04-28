// Initialize collapse button
$(".button-collapse").sideNav();
// Initialize collapsible (uncomment the line below if you use the dropdown variation)
//$('.collapsible').collapsible();
$('.modal-trigger').leanModal();


$('input#search').focus(function() { $(this).parent().addClass('focused'); });
    $('input#search').blur(function() {
      if (!$(this).val()) {
        $(this).parent().removeClass('focused');
      }
    });