$( document ).ready(function() {

	var execLog = $('.execution-log');
	if(execLog.length) {
		execLog.scrollTop(execLog[0].scrollHeight - execLog.height());
	}

	var resultLog = $('.results-log');
	if(resultLog.length) {
		resultLog.scrollTop(resultLog[0].scrollHeight - resultLog.height());
	}
});