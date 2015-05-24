$(function() {
    $(".click").click(function() {
       $(".hidden").hide();
       $(".hidden", this).toggle();

     })

 });