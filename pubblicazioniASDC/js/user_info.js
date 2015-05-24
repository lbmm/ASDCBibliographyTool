$(document).ready(function() {


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






















});
