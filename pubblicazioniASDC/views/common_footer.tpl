%if not username:
% include public_menu.tpl
% else:
% if not is_admin:
% include user_menu.tpl username=username
% else:
% include admin_menu.tpl
% end



