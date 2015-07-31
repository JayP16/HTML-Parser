function importFiles(dir) {
	console.log($("#my-dropzone").serialize());
	$.ajax({
            type: 'GET',
            url: 'http://www.dev.applications.ene.gov.on.ca/dams/import/startImport',
            data: "url="+encodeURIComponent(dir),
            contentType: false,
			cache: false,
            async: false,
            success: function(data) {
                console.log("processed.");				
				//
				if (myDropzone.getQueuedFiles().length > 0){
					myDropzone.processQueue();
				}
				else{
					
					$("#result").html('<div class="alert alert-success">Successfully updated Assets!</div>');
				}
            },
        }); 
}
