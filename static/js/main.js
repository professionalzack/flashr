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
  handlePain = data => {
    console.log('handeld through whaterver', data)
    $('.pain-btn').css('box-shadow', 'none')
    $(`#pain${data.pain_level}`).css('box-shadow', '1px 1px 5px 5px red')
  }


  sendPain = e => {
    e.preventDefault();
    pain = {
      "level":e.target.value, 
      "question_id":$('.question')[0].id
    }
    create_post('/pain', pain, handlePain)
  }



  function create_post(url, data, success=response => console.log(response)) {
    csrf = $('.csrf').serializeArray()[0]
    data[csrf.name] = csrf.value
    console.log(data)
    $.ajax({
        url : url,
        method : "POST",
        data : data,
        success : success,
        error : error => console.log(error)
    });
}
  // sendPain = e => {
  //   e.preventDefault();
  //   pain = {"csrfmiddlewaretoken":$('.pain-chart')[0].id,"level":e.target.value, "question_id":$('.question')[0].id}
  //   console.log(JSON.stringify(pain))
  //   $.post('/pain')
  // }

  
  $('.pain-chart').on('click', 'button', sendPain)




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


// $(answers).each((i,child)=> {
//   console.log('adding data['+child.name+']='+child.value);
//   data[child.name]=child.value})


//   data[child.name]=child.value