$( document ).ready(function() {
console.log("hello world");

setPain = x => {
  $('.pain-btn').css('text-shadow', 'none')
  $(`#pain${x}`).css('text-shadow', '1px 1px 5px red')
}

setPain($('.pain-chart')[0].id)

let display = $('.answer-toggler').length > 0 ? 'none' : 'block';
$('.hiders').css('display', display)
$('#current-answer').css('display', 'none')

function showAnswer(e) {
  e.preventDefault()
  const $button = $('.answer-toggler');
  const $x = $('#current-answer');
  $('.hiders').fadeIn()
  if ($x.css('display') === "none") {
    $x.fadeIn();
    $button.text("Hide Previous Answer");
  } else {
    $x.fadeOut();
    $button.text("Show Previous Answer");
  }
}
// function showAnswer(e) {
//   e.preventDefault()
//   button = document.querySelector('.answer-toggler');
//   const x = document.getElementById('current-answer');
//   const y = document.querySelector('.hiders');
//   if (x.style.display === "none") {
//     x.style.display = "block";
//     button.innerHTML = "Hide Previous Answer"
//   } else {
//     x.style.display = "none";
//     button.innerHTML = "Show Previous Answer"
//   }
//   y.style.display = "block";
// }


handlePain = data => {
  console.log('handeld through whaterver', data)
  setPain(data.pain_level)//realistic update :)
}

handleAnswer = data => {
  console.log('ajax answer response', data)
  $('#current-answer>h4').text(data.content) //realistic update :)
}


sendPain = e => {
  e.preventDefault();
  pain = {
    "level":e.target.id.slice(-1), 
    "question_id":$('.question')[0].id
  }
  setPain(pain.level) // optimistic update :)
  create_post('/pain', pain, handlePain)
}

sendAnswer = () => {
  let ansArr = $('.answerform').serializeArray();
  if(ansArr[0].value === ''){
    alert('still havent handled empty response, zack ?')
  }else{
    answer = {
      "public":ansArr.length,
      "content": ansArr[0].value,
      "question_id":$('.question')[0].id
    }
    $('#current-answer>h4').text(answer.content) //optimistic update :)

    console.log(answer)
    create_post('/answer', answer, handleAnswer)
  }
}







function create_post(url, data, 
  success=response => console.log(response)) {
    // adds csrf to data
    csrf = $('.csrf').children()[0]
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


  

$('.pain-chart').on('click', 'button', sendPain)
$('#showAnswer').on('click', showAnswer)
$('#sendAnswer').on('click', sendAnswer)



// $(document).ready(function(){
    // $(".toggle_container").hide(); 
    // $("button.reveal").click(function(){
    //     $(this).toggleClass("active").next().slideToggle("fast");
        
    //     if ($.trim($(this).text()) === 'Show Answer') {
    //         $(this).text('Hide Answer');
    //     } else {
    //         $(this).text('Show Answer');        
    //     }
        
    //     return false; 
    // });
    //  $("a[href='" + window.location.hash + "']").parent(".reveal").click();
    // });


// $(answers).each((i,child)=> {
//   console.log('adding data['+child.name+']='+child.value);
//   data[child.name]=child.value})


//   data[child.name]=child.value
// console.log('[get red')
// getRed()




});