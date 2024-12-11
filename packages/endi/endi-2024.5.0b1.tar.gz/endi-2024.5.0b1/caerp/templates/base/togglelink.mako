<%doc>
Toggle link template
</%doc>
% if elem.permitted(request.context, request):
   <a href='javascript:void(0);' onclick='toggleCollapse( this );' aria-expanded='${elem.expanded}' title='${elem.title}' aria-label='${elem.title}' 
   % if elem.css:
    class="${elem.css}"
   % endif
   >
   %if elem.icon:
       <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#${elem.icon}"></use></svg>
   % endif
   ${elem.label}
  </a>
% endif
