<%doc>
    Template used to render action buttons (see utils/widgets.py)
    item is the current item the action is made on
    elem is the current link object
</%doc>
% if elem.permitted(item, request):
    <a title='${elem.title}' aria-label='${elem.title}' href="${elem.url(item, request)}"
      %if elem.onclick():
          onclick="${elem.onclick()}"
      %endif
% if elem.css:
    class="${elem.css}"
       % endif
      >
      %if elem.icon:
        %if hasattr(elem.icon, "__iter__"):
            %for icon in elem.icon:
                <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#${icon}"></use></svg>
            % endfor
        %else:
                <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#${elem.icon}"></use></svg>
        % endif
      % endif
      <span class="no_mobile">
      ${elem.label}
      </span>
    </a>
% endif
