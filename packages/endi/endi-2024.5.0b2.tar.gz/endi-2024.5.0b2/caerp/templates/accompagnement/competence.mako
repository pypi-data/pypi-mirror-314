<%inherit file="${context['main_template'].uri}" />
<%block name='actionmenucontent'>
<div class='layout flex main_actions'>
    <a class='btn'
        href="${request.route_path('competence_grid', id=request.context.id, _query={'action': 'radar'})}"
        title="Voir le profil de compétences entrepreneuriales"
        >
        <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#chart-line"></use></svg>Voir le profil<span class="no_mobile">&nbsp;de compétences entrepreneuriales</span>
    </a>
</div>
</%block>
<%block name="content">
<div class='layout flex two_cols quarter'>
	<div class='vertical-tabs-container'>
		<div id='itemslist'></div>
		<div id='messageboxes'></div>
	</div>
	<div class='tab-content' id='itemcontainer'>
		<div class='alert alert-info'>
			<span class="icon"><svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#info-circle"></use></svg></span> 
			Sélectionner une compétence dans la liste
		</div>
	</div>
</div>
</%block>
<%block name="footerjs">
AppOptions = {};
AppOptions['loadurl'] = "${loadurl}";
AppOptions['contexturl'] = "${contexturl}";
</%block>
