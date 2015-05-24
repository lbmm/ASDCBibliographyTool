$(document).ready(function() {
        var table = $("#roles");
        var oTable = table.dataTable({"sPaginationType": "full_numbers", "bStateSave": true});



  $(document).on("click", ".delete", function() {
                var role_id = $(this).attr("id").replace("delete-", "");
                if (confirm("Are you sure to remove role: " + role_id)) {
                var parent = $("#"+role_id);
                $.ajax({
                        type: "post",
                        url: "/remove_role",
                        data: "code="+role_id,
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
                                     alert("error removing role: " +role_id);
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
