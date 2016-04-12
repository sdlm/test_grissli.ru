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

function checkFileAPI() {
	if (window.File && window.FileReader && window.FileList && window.Blob) {
		reader = new FileReader();
		return true; 
	} else {
		return false;
	}
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
				$('.success-counter .badge').text(data.count.success);
				$('.failure-counter .badge').text(data.count.failure);
				if (data.count.success > 0) {
					$('.success-counter').removeClass('hide');
				}
				else {
					if (!$('.success-counter').hasClass('hide')) {
						$('.success-counter').addClass('hide');
					}
				}
				if (data.count.failure > 0) {
					$('.failure-counter').removeClass('hide');
				}
				else {
					if (!$('.failure-counter').hasClass('hide')) {
						$('.failure-counter').addClass('hide');
					}
				}
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

	// send file over ajax
	$('.confirm-add-urls-list').click(function(){
		// var fileInput = $('#add-urls-list #file-input')[0];
		// var file = fileInput.files[0];
		// var xhr = new XMLHttpRequest();
		// xhr.addEventListener('load', function(e) {
		// 	console.log('xhr upload complete', e, this.responseText);
		// });
		// xhr.open('post', '/api/upload', true);
		// xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
		// xhr.send(file);

		if (checkFileAPI()) {
			var input = $('#add-urls-list #file-input')[0];

			var reader = new FileReader();
			reader.onload = function(){
				var text = reader.result;

				// socket.send('add_urls_request', {action: 'add_urls_request', data: text});

				prepareAJAX();

				$.ajax({
					type: "POST",
					url: "/api/admin",
					dataType: 'json',
					data: {
						action: 'add_urls_request', 
						text: text
					},
					success: function(data, textStatus, jqXHR) {
						if (data.success === true) {
							console.log('successfully add tasks');
							$('#add-urls-list').modal('hide');
						}
						else {
							console.log('backend error occured');
							console.log('textStatus: '+textStatus);
							$('#add-urls-list').modal('hide');
						}
					},
					fail: function(data, textStatus, jqXHR) {
						console.log('AJAX request fail. Something go wrang ...');
						console.log('textStatus: '+textStatus);
						$('#add-urls-list').modal('hide');
					}
				});
			};
			reader.readAsText(input.files[0]);
		}
	});

	$('.confirm-drop-results').click(function(){
		socket.send('drop_results_request');
		$('#drop-results').modal('hide');
	});
});