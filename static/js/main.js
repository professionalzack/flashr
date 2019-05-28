$( document ).ready(function() {
console.log("hello world");
$(`#pain${$('.pain-chart')[0].id}`).css('box-shadow', '1px 1px 5px 5px red')

function showAnswer() {
  button = document.querySelector('.answer-toggler')
  const x = document.getElementById("myDIV");
  if (x.style.display === "none") {
    x.style.display = "block";
    button.innerHTML = "hide answer"
  } else {
    x.style.display = "none";
    button.innerHTML = "show answer"
  }
}

// Sending Pain
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
    console.log('Error received: ', data.error);
  } else {
    console.log('vote: response included: ', data.vote)
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
    $(e.target).siblings('.vote-count').text(voteValue);
    $(e.target).removeClass('fas').addClass('far');
  } else if (action === 'up' && state === 'off') {
    vote = 1; // voted yes
    $(e.target).siblings('.vote-count').text(voteValue + 1)
    $(e.target).removeClass('far').addClass('fas');
    $(e.target).siblings('.vote').removeClass('fas').addClass('far');
  } else if (action === 'down' && state === 'off') {
    vote = -1; // voted no
    $(e.target).siblings('.vote-count').text(voteValue - 1)
    $(e.target).removeClass('far').addClass('fas');
    $(e.target).siblings('.vote').removeClass('fas').addClass('far');
  }
  // Send the ajax request
  vote = {
    vote: vote,
    answer_id: id,
  }
  console.log('sending.. ', vote)
  create_post('/vote', vote, handleVote, submitVote);
}

sendAnswer = e => {
  e.preventDefault();
  let ansArr = $('.answerform').serializeArray();
  answer = {
    "public":ansArr.length,
    "content": ansArr[0].value,
    "question_id":$('.question')[0].id
  }
  console.log(answer)
  create_post('/answer', answer)
}

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

// Event Handlers
$('.pain-chart').on('click', 'button', sendPain);
$('.vote').on('click', sendVote);
$('.answering').on('click', sendAnswer);




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
// console.log('[get red')
// getRed()




});