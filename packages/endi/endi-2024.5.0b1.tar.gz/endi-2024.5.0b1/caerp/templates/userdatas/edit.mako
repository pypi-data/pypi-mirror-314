
<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/utils.mako" import="company_list_badges" name="utils"/>
<%block name="mainblock">
<div>
    ${request.layout_manager.render_panel('help_message_panel', parent_tmpl_dict=context.kwargs)}
    <div class="layout flex full content_vertical_padding separate_bottom">
    	<div class="align_right">
			% if api.has_permission('context.delete_userdata'):
				<%utils:post_action_btn url="${delete_url}" icon="trash-alt"
				  _class="btn negative"
				  onclick="return confirm('En supprimant cette fiche de gestion sociale, vous supprimerez également \nles données associées (documents sociaux, parcours, historiques…). \n\nContinuer ?')"
				title="Supprimer la fiche"
				>
					Supprimer<span class="no_mobile">&nbsp;la fiche</span>
				</%utils:post_action_btn>
			% endif
    	</div>
	</div>
    ${form|n}
</div>
</%block>
<%block name="footerjs">
    setAuthCheckBeforeSubmit('#deform');
</%block>
