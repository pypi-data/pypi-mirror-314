<%inherit file="/workshops/workshop_base.mako" />
<%namespace file="/base/utils.mako" import="definition_list"/>
<% workshop = request.context %>
<%block name="after_details">
<div>
    <h2>
        Horaires et présence
    </h2>
    <div class="table_container">
		<table class="hover_table">
			<thead>
				<tr>
					<th scope="col" class="col_text">
						Nom de la tranche horaire
					</th>
					<th scope="col" class="col_text">
						Dates et horaires
					</th>
					<th scope="col" class="col_text">
						Votre statut
					</th>
				</tr>
			</thead>
			<tbody>
				% for label, time_str, status in timeslots_datas:
					<tr>
						<td class="col_text">
							${label}
						</td>
						<td class="col_text">
							${time_str}
						</td>
						<td class="col_text">
							${status}
						</td>
					</tr>
				% endfor
			</tbody>
		</table>
    </div>
</div>
</%block>
