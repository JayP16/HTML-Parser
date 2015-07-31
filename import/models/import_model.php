<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Import_model extends CI_Model
{
	private $id;
	private $title;
	private $content;
	private $sectionOrder;
	private $assetId;
	private $statusTypeId;
	private $assetTitle;
	private $breadcrumb;
	
	public function __construct( )
	{	
		$this->load->database( );
	}
	
	//--------------------------------------------------
	// INSERT SECTION
	//--------------------------------------------------

	public function import_existing($title,$assetId,$content, $pid)
	{	
		if ($pid == 0){
		
			$data = array('title' => $title, 'assetId' => $assetId, 'parentId' => $pid, 'content' => $content, 'breadcrumb' => $assetId, 'staffId' => "1");
		
		}else{
			
			$statement	= " SELECT section.breadcrumb FROM section 
							WHERE section.id = " . $pid;
			$query  	= $this->db->query($statement);
			$sections 	= $query->result_array( );
			
			$breadcrumb = $sections[0]['breadcrumb'] . "|" . $pid;
			$data = array('title' => $title, 'assetId' => $assetId, 'parentId' => $pid, 'content' => $content, 'breadcrumb' => $breadcrumb, 'staffId' => "1");
			
		}
		$statement = $this->db->insert_string('section', $data); 
		$this->db->query($statement);	
		$id = $this->db->insert_id( );
		return $id;
	}
	
	//--------------------------------------------------
	// UPDATE SECTION
	//--------------------------------------------------

	public function updateSection($id,$title,$content,$statusTypeId,$sectionOrder)
	{	
		$data = array('title' => $title, 'content' => $content, 'statusTypeId' => $statusTypeId, "sectionOrder" => $sectionOrder);
		$this->db->where('id', $id);
		$this->db->update('section', $data);
	}
	
	//--------------------------------------------------
	// INSERT REVISION
	//--------------------------------------------------

	public function insertRevision($id,$content,$summary,$staffId)
	{	
		$data = array('sectionId' => $id, 'content' => $content, 'summary' => $summary, 'createdDate' => date("Y-m-d H:i:s"), 'staffId' => $staffId);
		$statement = $this->db->insert_string('revision', $data); 
		$this->db->query($statement);	
	}
	
	//--------------------------------------------------
	// DELETE SECTION
	//--------------------------------------------------

	public function deleteSections($id)
	{		
		$statement	= " SELECT section.id FROM section 
						WHERE section.assetId = " . $id;
		$query  	= $this->db->query($statement);
		$sections 	= $query->result( );
		
		foreach($sections as $section)
		{
			$this->db->delete('section', array('id' => $section->id));
		}
	}
}