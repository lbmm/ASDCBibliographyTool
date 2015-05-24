$(document).ready(function() {
$("div.holder").jPages({
   containerID : "listPublications",
   perPage: 10
  });
});


$(document).ready(function () {
    $('#selectall').click(function () {
        $('.selectedId').prop('checked', this.checked);
        $("#exportPDF").removeAttr("disabled");
    });

    $('.selectedId').change(function () {
        var check = ($('.selectedId').filter(":checked").length == $('.selectedId').length);
        $('#selectall').prop("checked", check);
        $("#exportPDF").removeAttr("disabled");
    });
});

$(document).ready(function(){
    $('input').keyup(function(){
        var value = $(this).val();
        $("#listPublications > li").each(function() {
            if ($(this).text().search(new RegExp(value, "i")) > -1) {
                $(this).show();
            }
            else {
                $(this).hide();
            }
        });
    });
});

