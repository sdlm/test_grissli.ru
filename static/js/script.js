

// using jQuery
function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function prepareAJAX() {
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}
		}
	});
}

function scrollDown() {
	var execLog = $('.execution-log');
	if(execLog.length) {
		execLog.scrollTop(execLog[0].scrollHeight - execLog.height());
	}

	var resultLog = $('.results-log');
	if(resultLog.length) {
		resultLog.scrollTop(resultLog[0].scrollHeight - resultLog.height());
	}
}


$( document ).ready(function() {

	// scroll terminals
	scrollDown();

	// setup WebSocket
	var socket = new io.Socket();
	socket.connect();
	socket.on('connect', function() {
		socket.subscribe('terminal');

		socket.on('message',function(data) {
			console.log('Received a message from the server!', data);
			if (data.action === 'rerender_terminals') {
				$('.execution-log').val(data.runLog);
				$('.results-log').val(data.resultsLog);
				scrollDown();
			}
		});
		
	});

	// setup modal window input
	$('.modal-content #timeInput').mask("99:99");

	// setup modal window actions
	$('.confirm-add-url').click(function(){
		prepareAJAX();

		$.ajax({
			type: "POST",
			url: "/api/admin",
			dataType: 'json',
			data: {
				action: 'addUrl', 
				url: $('.modal-content #urlInput').val(),
				shift: $('.modal-content #timeInput').val(),
			},
			success: function(data, textStatus, jqXHR) {
				if (data.success === true) {
					console.log('successfully add task');
					$('#add-url').modal('hide');
				}
				else {
					console.log('backend error occured');
					console.log('textStatus: '+textStatus);
					$('#add-url').modal('hide');
				}
			},
			fail: function(data, textStatus, jqXHR) {
				console.log('AJAX request fail. Something go wrang ...');
				console.log('textStatus: '+textStatus);
				$('#add-url').modal('hide');
			}
		});
	});
	$('.confirm-add-urls-list').click(function(){
		prepareAJAX();

		$.ajax({
			type: "POST",
			url: "/api/admin",
			dataType: 'json',
			data: {
				action: 'check',
			}
		});
	});
});