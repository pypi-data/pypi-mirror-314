<%inherit file="/layouts/default.mako" />

<%block name="headtitle">
<h1>
    ${layout.current_business_object.business_type.label} : ${layout.current_business_object.name}
</h1>
</%block>

<%block name='content'>
<% business = layout.current_business_object %>
<div class="totals grand-total">
	<div class="layout flex">
		<div>
			<p>
				<strong>Nom :</strong> 
				${business.name}
				% if api.has_permission("context.edit_business", business):
				<a
					class='btn icon only unstyled'
					href="${layout.edit_url}"
					title="Modifier le nom de cette affaire"
					aria-label="Modifier le nom de cette affaire"
				>
                    ${api.icon('pen')}
				</a>
				% endif
			</p>
			<p>
				<strong>Client :</strong>
				<% customer = business.get_customer() %>
				<a href="${request.route_path('/customers/{id}', id=customer.id)}">${customer.label}</a>
			</p>
			<p 
				title="${api.format_indicator_status(business.status)}"
				aria-label="${api.format_indicator_status(business.status)}"
				>
				<span class='icon status ${api.indicator_status_css(business.status)}'>
                    ${api.icon(api.indicator_status_icon(business.status))}
				</span>
				% if business.status == 'success':
					Cette affaire est complète
				% else:
				 <% url = request.route_path('/businesses/{id}/overview', id=request.context.id, _anchor='indicator-table') %>
					Des éléménts sont manquants dans cette affaire <a href='${url}' title="Voir la liste détaillée des éléments manquant">Voir le détail</a>
				% endif
			</p>
		</div>
		<div>
			<h4 class="content_vertical_padding">Totaux</h4>
            ${request.layout_manager.render_panel('business_metrics_totals', instance=business, tva_on_margin=business.business_type.tva_on_margin)}
		</div>
	</div>
</div>
<div>
    <div class='tabs'>
		<%block name='rightblock'>
			${request.layout_manager.render_panel('tabs', layout.businessmenu)}
		</%block>
    </div>
    <div class='tab-content'>
		<%block name='mainblock'>
			Main
		</%block>
   </div>
</div>
</%block>
