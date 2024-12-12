<%doc>
Search form layout template
</%doc>

<%def name="searchform()">
    % if form is not UNDEFINED and form:
        <div class='collapsible search_filters'>
            <h2 class='collapse_title'>
            <a href='javascript:void(0);' onclick='toggleCollapse( this );' aria-expanded='true' accesskey='R' title='Masquer les champs de recherche' aria-label='Masquer les champs de recherche'>
                <span class="icon"><svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#search"></use></svg></span>
                Recherche
                <svg class="arrow"><use href="${request.static_url('caerp:static/icons/endi.svg')}#chevron-down"></use></svg>
            </a>
            % if '__formid__' in request.GET:
                <span class='help_text'>
                    <small><em>Des filtres sont actifs</em></small>
                </span>
                <span class='help_text'>
                    <a href="${request.current_route_path(_query={})}">
                        <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#times"></use></svg> Supprimer tous les filtres
                    </a>
                </span>
            % endif
            </h2>
            <div class='collapse_content'>
                <div>
                    ${form|n}
                </div>
            </div>
        </div>
    % endif
</%def>
