function prompt(){
	var progress=document.getElementById("progBar");
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
		//	sleep(3000);
			//$("#progBar").hide("fast");
			$("#success-upload").show("slow");
		}
	}
}
$('#upFile').change(function(){
	var progress=document.getElementById("progBar");
	progress.style = "width:0%";
	progress.innerHTML="0%";
});
