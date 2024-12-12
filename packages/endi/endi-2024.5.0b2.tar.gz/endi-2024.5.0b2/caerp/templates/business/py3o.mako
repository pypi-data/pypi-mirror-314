<%inherit file="${context['main_template'].uri}" />
<%block name="mainblock">

<div id="business_py3o_tab">
    % if help_message is not UNDEFINED and help_message is not None:
        <div class='alert alert-info'>
            <span class="icon"><svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#info-circle"></use></svg></span>
            ${help_message | n}
        </div>
    % endif

    <br/>

    % if templates == []:
        <div class='alert alert-warning'>
            <span class="icon"><svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#exclamation-triangle"></use></svg></span>
            Aucun modèle de document disponible pour ce type d'affaire.
        </div>
    % else:
        <ul>
        % for template in templates:
            <% url = request.current_route_path(_query=dict(file=template.file_type_id)) %>
            <li>
                <a href="${url}" class="icon">
                    <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#file-alt"></use></svg>
                    ${template.file_type.label} &nbsp; ( ${template.file.description} )
                </a>
            </li>
        % endfor
        </ul>
    % endif
</div>

</%block>
