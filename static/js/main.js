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

// Sending Pain
handlePain = data => {
  console.log('handling pain: ', data)
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

// Sending a Vote
submitVote = () => {
  // Disable voting while ajax call is happening
  console.log('vote: starting send...')
  $('.vote').off();
  $('.vote').addClass('disabled')
}
handleVote = data => {
  // Re-enable disabled vote buttons
  console.log('vote: send successful!')
  $('.vote').on('click', sendVote);
  $('.vote').removeClass('disabled')
  if (data.error) {
    console.log('Error received: ', data);
  } else {
    console.log('vote: response included: ', data)
  }
  // Update the total vote count based on ajax response and starting value
  // if un-voting, change by 1
  // If yes/no, move but remember the center value so toggling yes/no works
  const clickedAnswer = $(`[data-answer-pk="${data.a_id}"]`)
  const storedVoteValue = parseInt(clickedAnswer.find('.vote-count').attr('data-vote'));
  let voteValue = parseInt(clickedAnswer.find('.vote-count').text());
  const vote = parseInt(data.vote);
  if (vote === 0) {
    if (data.action === 'up') {
      clickedAnswer.find('.vote-count').text(voteValue - 1);
      clickedAnswer.find('.vote-count').attr('data-vote', voteValue - 1)
    } else if (data.action === 'down') {
      clickedAnswer.find('.vote-count').text(voteValue + 1);
      clickedAnswer.find('.vote-count').attr('data-vote', voteValue + 1)
    }
  } else if (vote === 1 || vote === -1) {
    clickedAnswer.find('.vote-count').text(storedVoteValue + vote);
  }  
}
sendVote = e => {
  // e.preventDefault();
  const id = parseInt($(e.target).closest('.answer-item').attr('data-answer-pk'));
  const voteValue = parseInt($(e.target).siblings('.vote-count').attr('data-vote'));
  let action, state, vote;
  // get info on action
  if (e.target.classList.contains('fa-arrow-alt-circle-up')) {
    action = 'up';
  }
  if (e.target.classList.contains('fa-arrow-alt-circle-down')) {
    action = 'down';
  }
  if (e.target.classList.contains('far')) {
    state = 'off';
  }
  if (e.target.classList.contains('fas')) {
    state = 'on';
  }
  // determine vote action and perform optimistic update
  if (state === 'on') {
    vote = 0; // "un-voting" a voted action
    $(e.target).removeClass('fas').addClass('far');
  } else if (action === 'up' && state === 'off') {
    vote = 1; // voted yes
    $(e.target).removeClass('far').addClass('fas');
    $(e.target).siblings('.vote').removeClass('fas').addClass('far');
  } else if (action === 'down' && state === 'off') {
    vote = -1; // voted no
    $(e.target).removeClass('far').addClass('fas');
    $(e.target).siblings('.vote').removeClass('fas').addClass('far');
  }
  // Send the ajax request
  vote = {
    vote: vote,
    action: action,
    answer_id: id,
  }
  console.log('sending.. ', vote)
  create_post('/vote', vote, handleVote, submitVote);
}

// Sending an Answer
sendAnswer = () => {
  let ansArr = $('.answerform').serializeArray();
  if(ansArr[0].value === ''){
    alert('still havent handled empty answer response, zack ?')
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

// Ajax function
function create_post(url, data, 
  success=response => console.log(response),
  handleSend=()=> console.log('click')) {
    console.log('vote ajax starting')
    // adds csrf to data
    csrf = $('.csrf').children()[0]
    data[csrf.name] = csrf.value
    console.log(data)
    $.ajax({
      url : url,
      method : "POST",
      data : data,
      beforeSend: handleSend,
      success : success,
      error : error => console.log(error)
    });
}

// Event Listeners
$('.pain-chart').on('click', 'a', sendPain);
$('.vote').on('click', sendVote);
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