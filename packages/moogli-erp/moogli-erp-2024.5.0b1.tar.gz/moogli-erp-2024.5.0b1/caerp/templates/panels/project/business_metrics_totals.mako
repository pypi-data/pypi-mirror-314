<%
expense_warnings = []
if tva_on_margin:
    mode_label = 'TTC'
    total_expenses = instance.get_total_expenses(tva_on_margin=True)
    total_income = instance.get_total_income('ttc')
    total_estimated = instance.get_total_estimated('ttc')
    total_margin = instance.get_total_margin(tva_on_margin=True)

    if instance.get_total_expenses(tva_on_margin=False) > 0:
        expense_warnings.append(
            'les dépenses hors TVA sur marge ont été ignorées'
            )
    expense_info = ("Total des dépenses TTC")

else:
    mode_label = 'HT'
    total_expenses = instance.get_total_expenses()
    total_income = instance.get_total_income()
    total_estimated = instance.get_total_estimated()
    total_margin = instance.get_total_margin()
    expense_info = "Total des dépenses HT + TVA non déductible"

if instance.has_nonvalid_expenses():
    expense_warnings.append(
       "les dépenses rattachées mais non encore validées ont été prises en compte"
    )
%>
<table class="top_align_table">
	<tbody>
        <tr>
	        <th scope="row">Devisé ${mode_label}</th>
	        <td class="col_number">
		        ${api.format_amount(total_estimated, precision=5)}&nbsp;€
	        </td>
        </tr>
        <tr>
	        <th scope="row" title="Total Facturé ${mode_label}">Facturé ${mode_label}</th>
	        <td class="col_number">
		        ${api.format_amount(total_income, precision=5)}&nbsp;€
	        </td>
        </tr>
        % if total_expenses > 0 or total_margin != total_income:
            <tr><td colspan="2">&nbsp;</td></tr>
            <tr>
                <th scope="row" title="${' ; '.join([expense_info] + expense_warnings)}" aria-label="${' ; '.join([expense_info] + expense_warnings)}">
                    Dépenses ${mode_label}
                    <span class="icon">
                        ${api.icon('warning' if expense_warnings else 'question-circle')}
                    </span>
                </th>
                <td class="col_number">
                    ${api.format_amount(total_expenses)}&nbsp;€
                </td>
            </tr>
            <tr>
                <th scope="row">Marge ${mode_label}</th>
                <td class="col_number">
                    ${api.format_amount(total_margin, precision=5)}&nbsp;€
                </td>
            </tr>
        % endif
        <tr><td colspan="2">&nbsp;</td></tr>
        <tr>
	        <th scope="row">Restant dû</th>
	        <td class="col_number">
		        ${api.format_amount(instance.get_topay(), precision=5)}&nbsp;€
	        </td>
        </tr>
    </tbody>
</table>
