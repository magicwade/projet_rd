value_index={
	'quotas_limit':parseInt($('#quotas_limit').html()),
	'quotas_used':parseInt($('#quotas_used').html()),
	'file_tmp': 0,
}



function prompt(){
	var progress=document.getElementById("progBar");
	$('#progBar').prop('class','progress-bar progress-bar-striped active');
	progress.style = "width:0%";
	//$("#progBar").show("slow");
	$("#success-upload").hide("fast");
//	alert(progress)
	var x=document.getElementById("upFile").value;
	if(x==null || x==""){
		alert("No file chosen. Please go back and try again");
		return false;
	}
	var input = document.getElementById("upFile");
	//var size = input.files[0].size;
	////var sizeField = document.getElementById("fileSize")
	////sizeField.value = size;

	var data = new FormData();
	data.append('myFile', document.getElementById("upFile").files[0]);

	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function() {
		    if (xhr.readyState == XMLHttpRequest.DONE) {
			    	all_my_files = JSON.parse(xhr.responseText);
			    	$("#success-upload").html("Success !");
				$('#progBar').prop('class','progress-bar progress-bar-striped');
				$('#all_files').html("");
				for (var file in all_my_files){
					$('#all_files').append(
						'<tr>'+
							'<td>'+all_my_files[file][1]+'</td>'+
							'<td class="center">'+all_my_files[file][2]+'</td>'+
							'<td class="center"><a href="/download/'+all_my_files[file][0]+'"><button class="btn btn-default btn-sm" type="button"> 						   <span aria-hiddent="true" class="glyphicon glyphicon-download-alt"> </span></button></a>'+
							'</td>'+
							'<td class="center">'+
								'<form action="../deletefilewebservice" method="POST"><input type="hidden" value="'+all_my_files[file][0]+'" name="file_id"><button class="btn btn-default btn-sm" type="submit"><span aria-hiddent="true" class="glyphicon glyphicon-glass"></span></button></form>'+
							'<td>'+
						'</tr>');
				}

		    }
	}
	xhr.upload.addEventListener("progress", updateProgress, false);
	xhr.open("POST", "/upload");
	xhr.send(data);
	
}
function updateProgress(evt){
	if(evt.lengthComputable){
		var percentComplete = Math.round((evt.loaded / evt.total)*100*10)/10;
		var progressBar = document.getElementById("progBar");
		progressBar.style = "width:"+percentComplete+"%";
		progressBar.innerHTML=percentComplete+"%";
		if (percentComplete==100){
			value_index.quotas_used = value_index.quotas_used + value_index.file_tmp;
		//	sleep(3000);
			//$("#progBar").hide("fast");
			$("#success-upload").html("Fichier en cours d'enregistrement sur nos serveurs <br > Veuillez patientez...");
			$("#success-upload").show("slow");
		}
	}
}
$('#upFile').change(function(){
	var progress=document.getElementById("progBar");
	progress.style = "width:0%";
	progress.innerHTML="0%";
	alert(this.files[0].size);
	value_index.file_tmp = this.files[0].size;
	if (value_index.file_tmp + value_index.quotas_used > value_index.quotas_limit){
		$('#submitFile').prop('disabled', true)
		
	}else{
		$('#submitFile').prop('disabled', false)
	}
	$('#quotas_used').html(value_index.file_tmp + value_index.quotas_used)
});


$('#search_files').click(function(){
	search_namefile = $('#search_namefile').val()
	search_user_id = $('#search_user_id option:selected').val()
	$.get('/searchuserfileswebservice/' + search_user_id + "/" + search_namefile ,function(json){
		var data = JSON.parse(json)
		$('#all_files').html("");
		for (var file in data){
			$('#all_files').append(
				'<tr>'+
					'<td>'+data[file][1]+'</td>'+
					'<td class="center">'+data[file][2]+'</td>'+
					'<td class="center"><a href="/download/'+data[file][0]+'"><button class="btn btn-default btn-sm" type="button"> 						   <span aria-hiddent="true" class="glyphicon glyphicon-download-alt"> </span></button></a>'+
					'</td>'+
					'<td class="center">'+
						'<form action="../deletefilewebservice" method="POST"><input type="hidden" value="'+data[file][0]+'" name="file_id"><button class="btn btn-default btn-sm" type="submit"><span aria-hiddent="true" class="glyphicon glyphicon-glass"></span></button></form>'+
					'<td>'+
				'</tr>');
		}
	});
});





