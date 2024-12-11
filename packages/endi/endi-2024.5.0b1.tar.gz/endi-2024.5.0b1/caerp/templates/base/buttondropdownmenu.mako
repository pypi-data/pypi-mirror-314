% if elem.items:
    <div class="btn-group" role='group'>
        <button type="button" class="btn btn-primary dropdown-toggle" data-toggle="dropdown">
            % if elem.icon:
                <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#${elem.icon}"></use></svg>&nbsp;
            % endif
            ${elem.name}
            &nbsp;
            <svg class="menu_arrow"><use href="${request.static_url('caerp:static/icons/endi.svg')}#chevron-down"></use></svg>
        </button>
        <ul class="dropdown-menu" role="menu">
            % for item in elem.items:
                % if item.permitted(request.context, request):
                    <li>${item.render(request)|n}</li>
                % endif
            % endfor
        </ul>
    </div>
% endif
