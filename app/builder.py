from app.deps import get_templates, get_config
import uuid

class FlashPage:
    def __init__(self, title="FlashPage App", request=None):
        self.title = title
        self.request = request
        self.components = []
        
    def header(self, text):
        self.components.append(f"<h2 class='mb-4'>{text}</h2>")
        return self
        
    def text(self, text):
        self.components.append(f"<p>{text}</p>")
        return self
        
    def metric(self, label, value, delta=None):
        delta_html = ""
        if delta:
            color = "text-success" if delta.startswith("+") else "text-danger" if delta.startswith("-") else "text-muted"
            delta_html = f'<div class="{color} small fw-bold">{delta}</div>'
            
        html = f"""
        <div class="card mb-3 shadow-sm border-0">
            <div class="card-body">
                <h6 class="text-muted text-uppercase mb-2" style="font-size: 0.8rem; letter-spacing: 0.5px;">{label}</h6>
                <h3 class="mb-0 fw-bold">{value}</h3>
                {delta_html}
            </div>
        </div>
        """
        self.components.append(html)
        return self
        
    def chart(self, chart_type, labels, values, title=None):
        chart_id = f"chart-{uuid.uuid4().hex[:8]}"
        html = f"""
        <div class="card mb-4 shadow-sm border-0">
            {"<div class='card-header bg-transparent fw-bold'>" + title + "</div>" if title else ""}
            <div class="card-body">
                <canvas id="{chart_id}" height="250"></canvas>
            </div>
        </div>
        <script>
        document.addEventListener("DOMContentLoaded", function() {{
            if (typeof Chart !== 'undefined') {{
                new Chart(document.getElementById("{chart_id}"), {{
                    type: '{chart_type}',
                    data: {{
                        labels: {labels},
                        datasets: [{{
                            label: 'Data',
                            data: {values},
                            backgroundColor: 'rgba(54, 162, 235, 0.5)',
                            borderColor: 'rgb(54, 162, 235)',
                            borderWidth: 2,
                            borderRadius: 4
                        }}]
                    }},
                    options: {{ 
                        responsive: true, 
                        maintainAspectRatio: false,
                        plugins: {{ legend: {{ display: false }} }}
                    }}
                }});
            }}
        }});
        </script>
        """
        self.components.append(html)
        return self

    def table(self, data, title=None):
        import json
        table_id = f"table-{uuid.uuid4().hex[:8]}"
        html = f"""
        <div class="card mb-4 shadow-sm border-0">
            {"<div class='card-header bg-transparent fw-bold'>" + title + "</div>" if title else ""}
            <div class="card-body">
                <div id="{table_id}"></div>
            </div>
        </div>
        <script>
        document.addEventListener("DOMContentLoaded", function() {{
            if (typeof Tabulator !== 'undefined') {{
                new Tabulator("#{table_id}", {{
                    data: {json.dumps(data)},
                    layout: "fitColumns",
                    pagination: "local",
                    paginationSize: 10,
                    autoColumns: true,
                }});
            }} else {{
                document.getElementById("{table_id}").innerHTML = "<div class='alert alert-warning'>Tabulator library not loaded.</div>";
            }}
        }});
        </script>
        """
        self.components.append(html)
        return self
        
    def columns(self, n):
        cols = [FlashPageContainer(self) for _ in range(n)]
        # We append a tuple to be resolved during render
        self.components.append(cols)
        return cols

    def text_input(self, id, label, value=""):
        html = f"""
        <div class="mb-3">
            <label for="{id}" class="form-label fw-bold small">{label}</label>
            <input type="text" class="form-control bg-light" id="{id}" data-fp-widget="text_input" value="{value}">
        </div>
        """
        self.components.append(html)
        return self

    def button(self, id, label):
        html = f"""
        <button type="button" class="btn btn-primary" id="{id}">{label}</button>
        """
        self.components.append(html)
        return self

    def html(self, raw_html):
        self.components.append(raw_html)
        return self

    def render(self):
        final_html = []
        for comp in self.components:
            if isinstance(comp, list):
                # It's a columns layout
                n = len(comp)
                cols_html = "<div class='row'>"
                for c in comp:
                    cols_html += f"<div class='col-md'>{c._render_inner()}</div>"
                cols_html += "</div>"
                final_html.append(cols_html)
            else:
                final_html.append(comp)
                
        body_content = "\n".join(final_html)
        
        templates = get_templates()
        config = get_config()
        tmpl = templates.get_template("apps/app_layout.html")
        return tmpl.render(
            request=self.request,
            site=config.get('site', {}),
            page={"title": self.title},
            body_content=body_content
        )

class FlashPageContainer:
    def __init__(self, parent):
        self.parent = parent
        self.components = []
        
    def metric(self, *args, **kwargs):
        temp = FlashPage()
        temp.metric(*args, **kwargs)
        self.components.append(temp.components[0])
        return self
        
    def text(self, *args, **kwargs):
        temp = FlashPage()
        temp.text(*args, **kwargs)
        self.components.append(temp.components[0])
        return self
        
    def chart(self, *args, **kwargs):
        temp = FlashPage()
        temp.chart(*args, **kwargs)
        self.components.append(temp.components[0])
        return self

    def table(self, *args, **kwargs):
        temp = FlashPage()
        temp.table(*args, **kwargs)
        self.components.append(temp.components[0])
        return self
        
    def html(self, *args, **kwargs):
        temp = FlashPage()
        temp.html(*args, **kwargs)
        self.components.append(temp.components[0])
        return self
        
    def _render_inner(self):
        return "\n".join(self.components)
