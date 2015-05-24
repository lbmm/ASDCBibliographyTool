var oTable;

$(document).ready(function() {
	$('#form').submit( function() {
		var sData = $('input', oTable.fnGetNodes()).serialize();
		//alert( "The following data would have been submitted to the server: \n\n"+sData );
		return true;
	} );

    var table = $("#publications");
	oTable = table.dataTable({"sPaginationType": "full_numbers", "bStateSave": true, "iDisplayLength": 50});


	$('.editable_mission').editable('/publications_update_missions', {
        loadurl : "/json_missions",
        id      : 'biblicode',
        name    : 'missions',
        type    : 'selectmulti',
        submit  : 'OK',
        submitdata : function(value, setting) {
        var array_val = new Array();
        var values = $(this).find('select').val();
        array_val['missions'] = values.join();
        return array_val;
        }});


});