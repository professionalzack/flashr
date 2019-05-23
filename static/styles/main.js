console.log("hello world");
function showAnswer() {
    button = document.querySelector('.answer-toggler')
    var x = document.getElementById("myDIV");
    if (x.style.display === "none") {
         x.style.display = "block";
         button.innerHTML = "hide answer"
    } else {
      x.style.display = "none";
      button.innerHTML = "show answer"
    }
  }
// $(document).ready(function(){
//     $(".toggle_container").hide(); 
//     $("button.reveal").click(function(){
//         $(this).toggleClass("active").next().slideToggle("fast");
        
//         if ($.trim($(this).text()) === 'Show Answer') {
//             $(this).text('Hide Answer');
//         } else {
//             $(this).text('Show Answer');        
//         }
        
//         return false; 
//     });
//      $("a[href='" + window.location.hash + "']").parent(".reveal").click();
//     });