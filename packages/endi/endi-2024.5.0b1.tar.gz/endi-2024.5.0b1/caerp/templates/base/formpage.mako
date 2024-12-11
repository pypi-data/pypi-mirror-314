<%doc>
    Simple page for form rendering
</%doc>

<%inherit file="${context['main_template'].uri}" />

<%block name="content">
    ${request.layout_manager.render_panel(
        'help_message_panel',
        parent_tmpl_dict=context.kwargs
    )}
    <div class="limited_width width40">
        ${form|n}
    </div>
</%block>
