var oTable;


$(document).ready(function() {
	$('#form').submit( function() {
		var sData = $('input', oTable.fnGetNodes()).serialize();
		//alert( "The following data would have been submitted to the server: \n\n"+sData );
		return true;
	} );

    var table = $("#publications");
	oTable = table.dataTable({"sPaginationType": "full_numbers", "bStateSave": true, "iDisplayLength": 50});

	$(document).on("click", ".delete", function() {
	            var all_bib = $(this).attr("id").replace("delete-", "");
	            var bib_s = all_bib.split("-")
	            var nice_id = bib_s[0]
	            var bib_id = bib_s[1]
	            if (confirm("Are you sure to remove pub: " + bib_id)) {

                  var parent = $("#"+nice_id);
                  $.ajax({
                         type: "post",
                         url: "/remove_publication",
                         data: "biblicode="+bib_id,
                         beforeSend: function() {
                                 table.block({
                                         message: "",
                                         css: {
                                                 border: "none",
                                                 backgroundColor: "none"
                                         },
                                         overlayCSS: {
                                                 backgroundColor: "#fff",
                                                 opacity: "0.5",
                                                 cursor: "wait"
                                         }
                                 });
                         },
                         success: function(response) {
                                 table.unblock();
                                 var get = response.split(",");
                                 if(get[0] == "error") {
                                      alert("error removing publication: " +bib_id);
                                 }
                                 if(get[0] == "success") {
                                         $(parent).fadeOut(200,function() {
                                                 $(parent).remove();
                                                });
                                 }
                         }

                });

			 }
              else {
            return false;
         }
   });



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





