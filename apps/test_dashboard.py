from app.builder import FlashPage

def build(request):
    page = FlashPage("Test Dashboard", request=request)
    
    page.header("Sales Overview")
    page.text("This is an interactive dashboard generated purely in Python using the new Builder API.")
    
    cols = page.columns(2)
    cols[0].metric("Total Revenue", "$45,231", delta="+12%")
    cols[1].metric("Active Users", "1,204", delta="-3%")
    
    page.chart("bar", labels=["Q1", "Q2", "Q3", "Q4"], values=[10, 20, 15, 30], title="Quarterly Growth")
    
    # Interactive search
    page.header("Interactive Search")
    page.text_input("query", "Search Term")
    page.button("btn_search", "Run Search")
    
    page.html("""
    <div id="app-search-results" class="mt-3 p-3 bg-light rounded border">Results will appear here.</div>
    <script>
    document.addEventListener("DOMContentLoaded", function() {
        document.getElementById("btn_search").addEventListener("click", function() {
            const query = FlashPageState.get("query", "");
            document.getElementById("app-search-results").innerHTML = "Searching for: <strong>" + query + "</strong>...";
            
            fetch("/api/apps/test_dashboard/search?q=" + encodeURIComponent(query))
                .then(r => r.json())
                .then(data => {
                    document.getElementById("app-search-results").innerHTML = "Found " + data.results.length + " items: <br>" + data.results.join(", ");
                })
                .catch(e => {
                    document.getElementById("app-search-results").innerHTML = "<span class='text-danger'>Error: " + e + "</span>";
                });
        });
    });
    </script>
    """)
    
    return page.render()

def handle_api(query_name, params):
    if query_name == "search":
        q = params.get("q", "").lower()
        items = ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape"]
        if q:
            results = [item for item in items if q in item.lower()]
        else:
            results = items
        return {"results": results}
    
    return {"error": "Unknown query"}
