$('#update_quotas').click(function(){
	username = $('#username').html()
	$.get('/updatequotaswebservice/' + username,function(json){
		var data = JSON.parse(json)
		$('#quotas_used').html(data.size)
		quotas_color()
	});
});
quotas_color()
function quotas_color(){
	quotas_limit = $('#quotas_limit').attr('value');
	quotas_used = $('#quotas_used').html();
	pourcentage_quotas = parseInt(quotas_used) * 100 / parseInt(quotas_limit);
	pourcentage_quotas = Math.round(pourcentage_quotas * 100 ) / 100;
	$('#quotas_used_p').html(" ("+pourcentage_quotas+"%)")
	if (parseInt(quotas_limit) >= parseInt(quotas_used)){
		$('#quotas_used').prop('class','success_color');
		$('#quotas_used_p').prop('class','success_color');
	}else{
		$('#quotas_used').prop('class','error_color');
		$('#quotas_used_p').prop('class','error_color');
	}
}
