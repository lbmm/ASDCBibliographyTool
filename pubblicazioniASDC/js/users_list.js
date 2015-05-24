$(document).ready(function() {
        var table = $("#users");
        var oTable = table.dataTable({"sPaginationType": "full_numbers", "bStateSave": true});

        $('#form').submit( function() {
		var sData = $('input', oTable.fnGetNodes()).serialize();
		//alert( "The following data would have been submitted to the server: \n\n"+sData );
		return true;
	    });


      $(".editable_email").editable("/users_update_email", {
       id        : 'user_id',
       name      : 'email',
       type   : 'textarea',
       submit : 'OK'
       });

       $('.editable_mission').editable('/users_update_missions', {
        loadurl : "/json_missions",
        id      : 'user_id',
        name    : 'missions',
        type    : 'selectmulti',
        submit  : 'OK',
        submitdata : function(value, setting) {
        var array_val = new Array();
        var values = $(this).find('select').val();
        array_val['missions'] = values.join();
        return array_val;
        }});

        $('.editable_role').editable('/users_update_role', {
        loadurl : "/json_roles",
        id      : 'user_id',
        name    : 'role',
        type    : 'select',
        submit  : 'OK',
        submitdata : function(value, setting) {
        var array_val = new Array();
        var role = $(this).find('select').val();
        return role;
        }});



        $(document).on("click", ".delete", function() {
                var user_id = $(this).attr("id").replace("delete-", "");
                if (confirm("Are you sure to remove user: " + user_id)) {
                var parent = $("#"+user_id);
                $.ajax({
                        type: "post",
                        url: "/remove_user",
                        data: "user="+user_id,
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
                                     alert("error removing user: " +user_id);
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
