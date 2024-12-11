   <div class="content_vertical_padding">
        <h3>Facturation</h3>
        <p>
            <em>Reste à facturer : ${api.format_amount(to_invoice, precision=5) | n}&nbsp;€ TTC</em>
        </p>
        <div class="timeline">
            <ul>
                % for item in items:
                    ${request.layout_manager.render_panel(
                        "timeline_item", 
                        context=item, 
                        business=request.context
                    )}
                % endfor
            </ul>
        </div>
    </div>