import os
import sys
import django

# Setup Django
script_dir = os.path.dirname(os.path.abspath(__file__))
mysite_dir = os.path.join(script_dir, 'mysite')
sys.path.insert(0, mysite_dir)
os.chdir(mysite_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.apps import apps

def generate_beautiful_schema():
    """Generate a beautiful HTML schema visualization"""
    print("🎨 GENERATING BEAUTIFUL SCHEMA VISUALIZATION")
    print("=" * 60)
    
    # Get all models
    all_models = list(apps.get_models())
    
    # Group by app
    apps_data = {}
    for model in all_models:
        app_name = model._meta.app_label
        if app_name not in apps_data:
            apps_data[app_name] = []
        apps_data[app_name].append(model)
    
    # Generate HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Django Chat App - Database Schema</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            color: white;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .stat-card {{
            background: rgba(255,255,255,0.95);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .stat-label {{
            margin-top: 10px;
            color: #666;
            font-weight: 500;
        }}
        
        .app-section {{
            background: rgba(255,255,255,0.95);
            margin-bottom: 30px;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        .app-header {{
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: white;
            padding: 20px 30px;
            font-size: 1.3em;
            font-weight: bold;
        }}
        
        .models-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 0;
        }}
        
        .model-card {{
            padding: 25px 30px;
            border-right: 1px solid #eee;
            border-bottom: 1px solid #eee;
        }}
        
        .model-card:nth-child(even) {{
            background: #f8f9fa;
        }}
        
        .model-name {{
            font-size: 1.2em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .table-badge {{
            background: #e9ecef;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            color: #6c757d;
            font-weight: normal;
        }}
        
        .fields-container {{
            margin-top: 15px;
        }}
        
        .field-item {{
            padding: 8px 0;
            border-bottom: 1px solid #f1f3f4;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .field-item:last-child {{
            border-bottom: none;
        }}
        
        .field-name {{
            font-weight: 600;
            color: #2c3e50;
        }}
        
        .field-type {{
            background: #e3f2fd;
            color: #1565c0;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 500;
        }}
        
        .field-type.primary {{
            background: #ffebee;
            color: #c62828;
        }}
        
        .field-type.foreign {{
            background: #fff3e0;
            color: #ef6c00;
        }}
        
        .relationships {{
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #007bff;
        }}
        
        .relationship {{
            margin: 8px 0;
            font-size: 0.9em;
            color: #495057;
        }}
        
        .toggle-btn {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 6px 15px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.8em;
            transition: all 0.3s ease;
            margin-left: auto;
        }}
        
        .toggle-btn:hover {{
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }}
        
        .hidden {{
            display: none;
        }}
        
        .search-container {{
            margin-bottom: 30px;
            text-align: center;
        }}
        
        .search-box {{
            padding: 12px 20px;
            font-size: 1.1em;
            border: none;
            border-radius: 25px;
            background: rgba(255,255,255,0.9);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            width: 300px;
            max-width: 100%;
        }}
        
        .search-box:focus {{
            outline: none;
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-database"></i> Django Chat App Schema</h1>
            <p>Complete database structure and relationships</p>
        </div>
        
        <div class="search-container">
            <input type="text" class="search-box" placeholder="🔍 Search models..." onkeyup="searchModels(this.value)">
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(all_models)}</div>
                <div class="stat-label"><i class="fas fa-table"></i> Total Models</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(apps_data)}</div>
                <div class="stat-label"><i class="fas fa-cube"></i> Django Apps</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{sum(len(get_relationships(model)) for model in all_models)}</div>
                <div class="stat-label"><i class="fas fa-link"></i> Relationships</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{sum(len(model._meta.get_fields()) for model in all_models)}</div>
                <div class="stat-label"><i class="fas fa-columns"></i> Total Fields</div>
            </div>
        </div>

        {generate_apps_html(apps_data)}
    </div>

    <script>
        function toggleFields(modelId) {{
            const fieldsDiv = document.getElementById('fields-' + modelId);
            const btn = document.getElementById('btn-' + modelId);
            
            if (fieldsDiv.classList.contains('hidden')) {{
                fieldsDiv.classList.remove('hidden');
                btn.innerHTML = '<i class="fas fa-eye-slash"></i> Hide';
            }} else {{
                fieldsDiv.classList.add('hidden');
                btn.innerHTML = '<i class="fas fa-eye"></i> Show';
            }}
        }}

        function searchModels(searchTerm) {{
            const modelCards = document.querySelectorAll('.model-card');
            const appSections = document.querySelectorAll('.app-section');
            searchTerm = searchTerm.toLowerCase();
            
            modelCards.forEach(card => {{
                const modelName = card.querySelector('.model-name').textContent.toLowerCase();
                if (modelName.includes(searchTerm) || searchTerm === '') {{
                    card.style.display = 'block';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
            
            // Hide empty app sections
            appSections.forEach(section => {{
                const visibleCards = section.querySelectorAll('.model-card[style="display: block"], .model-card:not([style*="none"])');
                if ((searchTerm && visibleCards.length === 0) || (searchTerm && Array.from(visibleCards).every(card => card.style.display === 'none'))) {{
                    section.style.display = 'none';
                }} else {{
                    section.style.display = 'block';
                }}
            }});
        }}

        // Auto-expand first few models
        document.addEventListener('DOMContentLoaded', function() {{
            const firstFewBtns = document.querySelectorAll('.toggle-btn');
            for (let i = 0; i < Math.min(3, firstFewBtns.length); i++) {{
                firstFewBtns[i].click();
            }}
        }});
    </script>
</body>
</html>
"""
    
    return html_content

def generate_apps_html(apps_data):
    """Generate HTML for each app section"""
    html = ""
    
    for app_name, models in apps_data.items():
        html += f"""
        <div class="app-section">
            <div class="app-header">
                <i class="fas fa-cube"></i> {app_name.upper()} ({len(models)} models)
            </div>
            <div class="models-grid">
        """
        
        for model in models:
            model_id = f"{app_name}_{model.__name__}".replace('.', '_').replace('-', '_')
            relationships = get_relationships(model)
            
            html += f"""
                <div class="model-card" data-model="{model.__name__.lower()}">
                    <div class="model-name">
                        <i class="fas fa-table"></i>
                        {model.__name__}
                        <span class="table-badge">{model._meta.db_table}</span>
                        <button class="toggle-btn" id="btn-{model_id}" onclick="toggleFields('{model_id}')">
                            <i class="fas fa-eye"></i> Show
                        </button>
                    </div>
                    
                    <div id="fields-{model_id}" class="fields-container hidden">
            """
            
            # Add fields
            for field in model._meta.get_fields():
                if hasattr(field, 'name'):  # Skip reverse relations without names
                    field_type_class = "field-type"
                    icon = "fas fa-circle"
                    
                    if getattr(field, 'primary_key', False):
                        field_type_class += " primary"
                        icon = "fas fa-key"
                    elif hasattr(field, 'related_model'):
                        field_type_class += " foreign"
                        icon = "fas fa-link"
                    
                    field_type_name = type(field).__name__
                    
                    # Add field attributes
                    field_attrs = []
                    if hasattr(field, 'max_length') and field.max_length:
                        field_attrs.append(f"max={field.max_length}")
                    if hasattr(field, 'null') and field.null:
                        field_attrs.append("null")
                    if hasattr(field, 'unique') and field.unique:
                        field_attrs.append("unique")
                    if hasattr(field, 'blank') and field.blank:
                        field_attrs.append("blank")
                    
                    attrs_str = f" [{', '.join(field_attrs)}]" if field_attrs else ""
                    
                    html += f"""
                        <div class="field-item">
                            <span class="field-name">
                                <i class="{icon}"></i> {field.name}{attrs_str}
                            </span>
                            <span class="{field_type_class}">{field_type_name}</span>
                        </div>
                    """
            
            # Add relationships
            if relationships:
                html += '<div class="relationships"><strong><i class="fas fa-project-diagram"></i> Relationships:</strong>'
                for rel in relationships:
                    html += f'<div class="relationship">• {rel}</div>'
                html += "</div>"
            
            html += """
                    </div>
                </div>
            """
        
        html += """
            </div>
        </div>
        """
    
    return html

def get_relationships(model):
    """Get relationships for a model"""
    relationships = []
    for field in model._meta.get_fields():
        if hasattr(field, 'related_model') and field.related_model and hasattr(field, 'name'):
            rel_type = type(field).__name__
            related_model = field.related_model.__name__
            relationships.append(f"{field.name} ({rel_type}) → {related_model}")
        elif hasattr(field, 'related_model') and field.related_model and field.one_to_many:
            # Reverse relationships
            rel_type = "OneToMany"
            related_model = field.related_model.__name__
            relationships.append(f"← {related_model} ({rel_type})")
    return relationships

if __name__ == '__main__':
    try:
        html_content = generate_beautiful_schema()
        
        # Save to file
        output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'django_schema_visualization.html')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Beautiful schema visualization generated!")
        print(f"📁 File: django_schema_visualization.html")
        print(f"🔗 Full path: {output_file}")
        print(f"\n🌐 To view: Open the file in your web browser")
        
        # Try to open automatically
        try:
            import webbrowser
            webbrowser.open(f'file://{output_file}')
            print("🚀 Opening in your default browser...")
        except:
            print("💡 Manually open the HTML file in your browser")
            
    except Exception as e:
        print(f"❌ Error generating schema: {e}")
        import traceback
        traceback.print_exc()
