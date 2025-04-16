
function sendReadingSessionData(startTime,course_id) {
    let endTime = new Date(); 
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    

    $.ajax({
        type: 'POST',
        url: '/store_reading_time/'+course_id+'/', 
        data: {
            csrfmiddlewaretoken: csrftoken,
            start_time: startTime.toISOString(), // Convert to ISO 8601 format
            end_time: endTime.toISOString(), // Convert to ISO 8601 format
        },
        success: function(response) {
            console.log('Reading session data stored successfully');
        },
        error: function(xhr, status, error) {
            console.error('Error storing reading session data:', error);
        }
    });
}