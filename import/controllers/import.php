<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

session_start( ); 

class Import extends MX_Controller
{
	
	public function startImport( ) {
		
		$output = shell_exec('/var/www/vhosts/dev.applications.ene.gov.on.ca/httpdocs/python27/bin/python2.7 ./assets/python/htmlParser.py ' . $_GET['url'] . ' 2>&1');

	}
	public function importExisting(){
		$assetId = $_POST['assetId'];
		$data = $_POST['data'];
		$title = $_POST['title'];
		$pid = $_POST['pid'];
		$keepTags = $_POST['keepTags'];
		
		$importModel = $this->load->model('import_model');	
		$data = strip_tags($data, $keepTags);
		$id = $importModel->import_existing(strip_tags($title), $assetId, $data, $pid);
		print "id:" . $id . ":id";
		//file_put_contents("text", $title, FILE_APPEND );
	}

	public function deleteSections(){
		
		$assetId = $_POST['assetId'];
		$data = $_POST['data'];
		$title = $_POST['title'];			
		$pid = $_POST['pid'];
		$importModel = $this->load->model('import_model');
		$importModel->deleteSections($assetId);
	}
	

}
