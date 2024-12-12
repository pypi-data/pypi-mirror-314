<%doc>
    Template used to render buttons (see utils/widgets.py)
</%doc>
% if elem.permitted(request.context, request):
    <a title='${elem.title}' aria-label='${elem.title}' href="#" onclick="${elem.onclick()}"
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
