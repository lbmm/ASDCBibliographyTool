$(document).ready(function() {
        var table = $("#missions");
        var oTable = table.dataTable({"sPaginationType": "full_numbers", "bStateSave": true});

        $('#form').submit( function() {
		var sData = $('input', oTable.fnGetNodes()).serialize();
		//alert( "The following data would have been submitted to the server: \n\n"+sData );
		return true;
	    } );


  $(document).on("click", ".delete", function() {
                var mission_id = $(this).attr("id").replace("delete-", "");
                if (confirm("Are you sure to remove mission: " + mission_id)) {
                var parent = $("#"+mission_id);
                $.ajax({
                        type: "post",
                        url: "/remove_mission",
                        data: "mission="+mission_id,
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
                                     alert("error removing user: " +mission_id);
                                }
                                if(get[0] == "success") {
                                        $(parent).fadeOut(200,function() {
                                                $(parent).remove();
                                        });
                                }
                        }
                });

              }else{
              return false;
              }
        });
});
