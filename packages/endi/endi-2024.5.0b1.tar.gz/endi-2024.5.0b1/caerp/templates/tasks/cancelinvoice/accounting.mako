<%inherit file="${context['main_template'].uri}" />

<%block name='mainblock'>
    <% cancelinvoice = request.context %>
    <% url = request.route_path('/export/treasury/invoices/{id}', id=cancelinvoice.id, _query={'force': True}) %>
    % if cancelinvoice.exported:
        <div class='content_vertical_padding'>
            <span class='icon status success'><svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#check"></use></svg></span>
            Cet avoir a été exporté vers la comptabilité.
        </div>
        % if cancelinvoice.exports:
        <div class='content_vertical_padding'>
            <ul>
                % for export in cancelinvoice.exports:
                <li>Exporté le ${api.format_datetime(export.datetime)}
                par ${api.format_account(export.user)}</li>
                % endfor
            </ul>
        </div>
        % endif
        <div class='content_vertical_padding'>
            <a href="${url}" class='btn'>
                <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#file-export"></use></svg>
                Forcer la génération d’écritures pour cet avoir
            </a>
        </div>
    % else:
        <div class='separate_top content_vertical_padding'>
            <span class='icon status neutral'><svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#clock"></use></svg></span>
            Cet avoir n’a pas encore été exporté vers la comptabilité
        </div>
        % if api.has_permission('global.manage_accounting'):
        <div class='content_vertical_padding'>
            <a href="${url}" class='btn btn-primary'>
                <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#file-export"></use></svg>
                Générer les écritures pour cet avoir
            </a>
        </div>
        % endif
    % endif
</%block>