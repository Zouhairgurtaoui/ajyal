$(document).ready(function () {
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();  

    function startTimer(duration) {
        var timerDisplay = $('#timer-display');
        var remainingTime = duration;

        var intervalId = setInterval(function() {
            var minutes = Math.floor(remainingTime / 60);
            var seconds = remainingTime % 60;

            
            var formattedSeconds = (seconds < 10 ? '0' : '') + seconds;

            
            timerDisplay.text(minutes + ':' + formattedSeconds);

            
            if (--remainingTime < 0) {
                clearInterval(intervalId); 
                sendQuizEndRequest(); 
            }
        }, 1000); 
    }
    function sendQuizEndRequest() {
        var pathname = window.location.pathname;

        var segments = pathname.split('/');

        var value = segments[segments.length - 1]
        $.ajax({
            url: '/take-quiz/'+value+'',
            type: 'POST',
            data: {
                csrfmiddlewaretoken: csrftoken,
                is_quiz_end: true
            },
            success: function (data) {
                if (data.success) {
                    console.log('Quiz time is up. Quiz end request sent successfully.');
                } else {
                    console.error('Error sending quiz end request: ' + data.error);
                }
            },
            error: function () {
                console.error('AJAX request failed');
            }
        });
    }

    
    startTimer(300);
    });