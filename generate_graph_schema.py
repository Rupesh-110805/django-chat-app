import os
import sys
import django
import json

# Setup Django
script_dir = os.path.dirname(os.path.abspath(__file__))
mysite_dir = os.path.join(script_dir, 'mysite')
sys.path.insert(0, mysite_dir)
os.chdir(mysite_dir)
os        // Colors for different app types with enhanced grouping
        const appColors = {
            'auth': '#e74c3c',           // Red - Central Authentication (CORE)
            'admin': '#9b59b6',          // Purple - Admin System
            'contenttypes': '#8e44ad',   // Dark Purple - Content Management  
            'sessions': '#3498db',       // Blue - Session Management
            'socialaccount': '#f39c12',  // Orange - Social Auth (Google OAuth)
            'account': '#e67e22',        // Dark Orange - Account Management
            'chatapp': '#27ae60',        // Green - Your Chat Application
            'sites': '#95a5a6',          // Gray - Sites Framework
            'django': '#34495e'          // Dark Gray - Django Core
        };
        
        // System categories for better visualization
        const systemCategories = {
            'CORE_AUTH': ['auth'],
            'SESSION_MGMT': ['sessions'],
            'SOCIAL_AUTH': ['socialaccount', 'account'], 
            'ADMIN_SYSTEM': ['admin', 'contenttypes', 'sites'],
            'CHAT_APP': ['chatapp'],
            'DJANGO_CORE': ['django']
        };tdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.apps import apps

def generate_graph_schema():
    """Generate an interactive graph-based schema visualization"""
    print("🕸️  GENERATING INTERACTIVE GRAPH SCHEMA")
    print("=" * 60)
    
    # Collect data
    models_data = collect_models_data()
    relationships_data = collect_relationships_data()
    
    # Generate HTML with interactive graph
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Django Database Schema Graph</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            overflow: hidden;
            height: 100vh;
        }}
        
        .container {{
            position: relative;
            width: 100vw;
            height: 100vh;
        }}
        
        .header {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 15px;
            text-align: center;
            z-index: 1000;
        }}
        
        .header h1 {{
            font-size: 1.8em;
            margin-bottom: 5px;
        }}
        
        .controls {{
            position: absolute;
            top: 80px;
            left: 20px;
            z-index: 1000;
            background: rgba(0, 0, 0, 0.8);
            padding: 15px;
            border-radius: 10px;
            color: white;
        }}
        
        .control-btn {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 8px 15px;
            margin: 5px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.9em;
            transition: all 0.3s ease;
        }}
        
        .control-btn:hover {{
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }}
        
        .legend {{
            position: absolute;
            bottom: 20px;
            left: 20px;
            z-index: 1000;
            background: rgba(0, 0, 0, 0.8);
            padding: 15px;
            border-radius: 10px;
            color: white;
            font-size: 0.9em;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            margin: 5px 0;
        }}
        
        .legend-color {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
            margin-right: 10px;
        }}
        
        .info-panel {{
            position: absolute;
            top: 80px;
            right: 20px;
            z-index: 1000;
            background: rgba(0, 0, 0, 0.9);
            padding: 20px;
            border-radius: 10px;
            color: white;
            max-width: 300px;
            display: none;
        }}
        
        .info-panel.visible {{
            display: block;
        }}
        
        .info-title {{
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #64b5f6;
        }}
        
        .field-list {{
            max-height: 200px;
            overflow-y: auto;
            margin-top: 10px;
        }}
        
        .field-item {{
            padding: 3px 0;
            font-size: 0.8em;
            border-bottom: 1px solid #333;
        }}
        
        #canvas {{
            display: block;
            cursor: grab;
        }}
        
        #canvas:active {{
            cursor: grabbing;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🕸️ Django Database Schema Graph</h1>
            <p>Interactive visualization of models and their relationships</p>
        </div>
        
        <div class="controls">
            <div style="margin-bottom: 10px; font-weight: bold;">Controls:</div>
            <button class="control-btn" onclick="resetView()">🏠 Reset View</button>
            <button class="control-btn" onclick="togglePhysics()">⚡ Toggle Physics</button>
            <button class="control-btn" onclick="exportImage()">📸 Export PNG</button>
            <div style="margin-top: 10px; font-size: 0.8em;">
                💡 Drag nodes • Scroll to zoom • Click for details
            </div>
        </div>
        
        <div class="legend">
            <div style="font-weight: bold; margin-bottom: 10px;">Legend:</div>
            <div class="legend-item">
                <div class="legend-color" style="background: #4fc3f7;"></div>
                <span>Django Built-in Models</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #81c784;"></div>
                <span>Chat App Models</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #ffb74d;"></div>
                <span>Auth/Social Models</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #f06292;"></div>
                <span>Admin/System Models</span>
            </div>
        </div>
        
        <div id="info-panel" class="info-panel">
            <div id="info-content"></div>
        </div>
        
        <canvas id="canvas"></canvas>
    </div>

    <script>
        // Data from Django
        const modelsData = {json.dumps(models_data, indent=2)};
        const relationshipsData = {json.dumps(relationships_data, indent=2)};
        
        // Canvas setup
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        let width, height;
        
        // Graph state
        let nodes = [];
        let edges = [];
        let isDragging = false;
        let dragNode = null;
        let offset = {{ x: 0, y: 0 }};
        let scale = 1;
        let physicsEnabled = true;
        
        // Colors for different app types
        const appColors = {{
            'auth': '#4fc3f7',
            'admin': '#f06292',
            'contenttypes': '#f06292',
            'sessions': '#f06292',
            'socialaccount': '#ffb74d',
            'account': '#ffb74d',
            'chatapp': '#81c784',
            'sites': '#f06292'
        }};
        
        function resizeCanvas() {{
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        }}
        
        function initGraph() {{
            resizeCanvas();
            createNodes();
            createEdges();
            positionNodes();
            animate();
        }}
        
        function createNodes() {{
            nodes = [];
            let nodeId = 0;
            
            for (const [modelKey, modelData] of Object.entries(modelsData)) {{
                const appLabel = modelData.app_label;
                const color = appColors[appLabel] || '#9e9e9e';
                
                nodes.push({{
                    id: nodeId++,
                    modelKey: modelKey,
                    label: modelData.model_name,
                    fullLabel: modelKey,
                    tableName: modelData.table_name,
                    appLabel: appLabel,
                    fields: modelData.fields,
                    x: Math.random() * (width - 200) + 100,
                    y: Math.random() * (height - 200) + 100,
                    vx: 0,
                    vy: 0,
                    radius: Math.max(20, Math.min(40, modelData.fields.length * 2)),
                    color: color,
                    targetX: 0,
                    targetY: 0
                }});
            }}
        }}
        
        function createEdges() {{
            edges = [];
            
            relationshipsData.forEach(rel => {{
                const fromNode = nodes.find(n => n.modelKey === rel.from_model);
                const toNode = nodes.find(n => n.modelKey === rel.to_model);
                
                if (fromNode && toNode) {{
                    edges.push({{
                        from: fromNode,
                        to: toNode,
                        type: rel.relationship_type,
                        fieldName: rel.field_name
                    }});
                }}
            }});
        }}
        
        function positionNodes() {{
            // Circular layout with app grouping
            const apps = [...new Set(nodes.map(n => n.appLabel))];
            const centerX = width / 2;
            const centerY = height / 2;
            const radius = Math.min(width, height) * 0.3;
            
            apps.forEach((app, appIndex) => {{
                const appNodes = nodes.filter(n => n.appLabel === app);
                const appAngle = (appIndex / apps.length) * 2 * Math.PI;
                const appCenterX = centerX + Math.cos(appAngle) * radius;
                const appCenterY = centerY + Math.sin(appAngle) * radius;
                
                appNodes.forEach((node, nodeIndex) => {{
                    const nodeAngle = (nodeIndex / appNodes.length) * 2 * Math.PI;
                    const nodeRadius = 50 + appNodes.length * 5;
                    
                    node.x = appCenterX + Math.cos(nodeAngle) * nodeRadius;
                    node.y = appCenterY + Math.sin(nodeAngle) * nodeRadius;
                    node.targetX = node.x;
                    node.targetY = node.y;
                }});
            }});
        }}
        
        function applyForces() {{
            if (!physicsEnabled) return;
            
            const damping = 0.8;
            const repulsion = 1000;
            const attraction = 0.1;
            const centerForce = 0.01;
            
            // Reset forces
            nodes.forEach(node => {{
                node.fx = 0;
                node.fy = 0;
            }});
            
            // Node repulsion
            for (let i = 0; i < nodes.length; i++) {{
                for (let j = i + 1; j < nodes.length; j++) {{
                    const dx = nodes[j].x - nodes[i].x;
                    const dy = nodes[j].y - nodes[i].y;
                    const distance = Math.sqrt(dx * dx + dy * dy);
                    
                    if (distance > 0) {{
                        const force = repulsion / (distance * distance);
                        const fx = (dx / distance) * force;
                        const fy = (dy / distance) * force;
                        
                        nodes[i].fx -= fx;
                        nodes[i].fy -= fy;
                        nodes[j].fx += fx;
                        nodes[j].fy += fy;
                    }}
                }}
            }}
            
            // Edge attraction
            edges.forEach(edge => {{
                const dx = edge.to.x - edge.from.x;
                const dy = edge.to.y - edge.from.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance > 0) {{
                    const force = attraction * distance;
                    const fx = (dx / distance) * force;
                    const fy = (dy / distance) * force;
                    
                    edge.from.fx += fx;
                    edge.from.fy += fy;
                    edge.to.fx -= fx;
                    edge.to.fy -= fy;
                }}
            }});
            
            // Center attraction
            const centerX = width / 2;
            const centerY = height / 2;
            
            nodes.forEach(node => {{
                const dx = centerX - node.x;
                const dy = centerY - node.y;
                
                node.fx += dx * centerForce;
                node.fy += dy * centerForce;
            }});
            
            // Apply forces
            nodes.forEach(node => {{
                if (!node.dragging) {{
                    node.vx = (node.vx + node.fx) * damping;
                    node.vy = (node.vy + node.fy) * damping;
                    node.x += node.vx;
                    node.y += node.vy;
                }}
            }});
        }}
        
        function draw() {{
            ctx.clearRect(0, 0, width, height);
            
            ctx.save();
            ctx.translate(offset.x, offset.y);
            ctx.scale(scale, scale);
            
            // Draw edges
            ctx.lineWidth = 2;
            edges.forEach(edge => {{
                const gradient = ctx.createLinearGradient(
                    edge.from.x, edge.from.y,
                    edge.to.x, edge.to.y
                );
                gradient.addColorStop(0, edge.from.color + '80');
                gradient.addColorStop(1, edge.to.color + '80');
                
                ctx.strokeStyle = gradient;
                ctx.beginPath();
                ctx.moveTo(edge.from.x, edge.from.y);
                ctx.lineTo(edge.to.x, edge.to.y);
                ctx.stroke();
                
                // Draw arrow
                const dx = edge.to.x - edge.from.x;
                const dy = edge.to.y - edge.from.y;
                const angle = Math.atan2(dy, dx);
                const arrowLength = 15;
                const arrowAngle = Math.PI / 6;
                
                const endX = edge.to.x - Math.cos(angle) * edge.to.radius;
                const endY = edge.to.y - Math.sin(angle) * edge.to.radius;
                
                ctx.strokeStyle = edge.to.color;
                ctx.beginPath();
                ctx.moveTo(endX, endY);
                ctx.lineTo(
                    endX - arrowLength * Math.cos(angle - arrowAngle),
                    endY - arrowLength * Math.sin(angle - arrowAngle)
                );
                ctx.moveTo(endX, endY);
                ctx.lineTo(
                    endX - arrowLength * Math.cos(angle + arrowAngle),
                    endY - arrowLength * Math.sin(angle + arrowAngle)
                );
                ctx.stroke();
            }});
            
            // Draw nodes
            nodes.forEach(node => {{
                // Node circle
                ctx.fillStyle = node.color;
                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.arc(node.x, node.y, node.radius, 0, 2 * Math.PI);
                ctx.fill();
                ctx.stroke();
                
                // Node label
                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 12px Segoe UI';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                
                // Multi-line text for long labels
                const words = node.label.split(/(?=[A-Z])/);
                if (words.length > 1 && node.label.length > 8) {{
                    ctx.fillText(words[0], node.x, node.y - 6);
                    ctx.fillText(words.slice(1).join(''), node.x, node.y + 6);
                }} else {{
                    ctx.fillText(node.label, node.x, node.y);
                }}
                
                // App label
                ctx.fillStyle = '#ffffff';
                ctx.font = '10px Segoe UI';
                ctx.fillText(node.appLabel, node.x, node.y + node.radius + 15);
            }});
            
            ctx.restore();
        }}
        
        function animate() {{
            applyForces();
            draw();
            requestAnimationFrame(animate);
        }}
        
        function getNodeAt(x, y) {{
            const canvasX = (x - offset.x) / scale;
            const canvasY = (y - offset.y) / scale;
            
            return nodes.find(node => {{
                const dx = canvasX - node.x;
                const dy = canvasY - node.y;
                return dx * dx + dy * dy <= node.radius * node.radius;
            }});
        }}
        
        function showNodeInfo(node) {{
            const infoPanel = document.getElementById('info-panel');
            const infoContent = document.getElementById('info-content');
            
            let fieldsHtml = node.fields.map(field => {{
                const typeClass = field.is_primary_key ? 'primary' : 
                                 field.is_foreign_key ? 'foreign' : 'regular';
                const icon = field.is_primary_key ? '🔑' : 
                            field.is_foreign_key ? '🔗' : '📋';
                return `<div class="field-item">${{icon}} ${{field.name}} (${{field.type}})</div>`;
            }}).join('');
            
            infoContent.innerHTML = `
                <div class="info-title">${{node.fullLabel}}</div>
                <div><strong>Table:</strong> ${{node.tableName}}</div>
                <div><strong>App:</strong> ${{node.appLabel}}</div>
                <div><strong>Fields:</strong> ${{node.fields.length}}</div>
                <div class="field-list">${{fieldsHtml}}</div>
            `;
            
            infoPanel.classList.add('visible');
        }}
        
        function hideNodeInfo() {{
            document.getElementById('info-panel').classList.remove('visible');
        }}
        
        // Event handlers
        canvas.addEventListener('mousedown', (e) => {{
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const node = getNodeAt(x, y);
            if (node) {{
                isDragging = true;
                dragNode = node;
                dragNode.dragging = true;
                showNodeInfo(node);
            }} else {{
                hideNodeInfo();
            }}
        }});
        
        canvas.addEventListener('mousemove', (e) => {{
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            if (isDragging && dragNode) {{
                const canvasX = (x - offset.x) / scale;
                const canvasY = (y - offset.y) / scale;
                
                dragNode.x = canvasX;
                dragNode.y = canvasY;
                dragNode.vx = 0;
                dragNode.vy = 0;
            }}
        }});
        
        canvas.addEventListener('mouseup', () => {{
            isDragging = false;
            if (dragNode) {{
                dragNode.dragging = false;
                dragNode = null;
            }}
        }});
        
        canvas.addEventListener('wheel', (e) => {{
            e.preventDefault();
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const zoom = e.deltaY > 0 ? 0.9 : 1.1;
            const newScale = Math.max(0.1, Math.min(3, scale * zoom));
            
            offset.x = x - (x - offset.x) * (newScale / scale);
            offset.y = y - (y - offset.y) * (newScale / scale);
            scale = newScale;
        }});
        
        // Control functions
        function resetView() {{
            scale = 1;
            offset = {{ x: 0, y: 0 }};
            positionNodes();
        }}
        
        function togglePhysics() {{
            physicsEnabled = !physicsEnabled;
        }}
        
        function exportImage() {{
            const link = document.createElement('a');
            link.download = 'django_schema_graph.png';
            link.href = canvas.toDataURL();
            link.click();
        }}
        
        // Resize handler
        window.addEventListener('resize', resizeCanvas);
        
        // Initialize
        initGraph();
    </script>
</body>
</html>
"""
    
    return html_content

def collect_models_data():
    """Collect detailed data about all models"""
    models_data = {}
    
    for model in apps.get_models():
        model_key = f"{model._meta.app_label}.{model.__name__}"
        
        fields_data = []
        for field in model._meta.get_fields():
            if hasattr(field, 'name'):  # Skip reverse relations without names
                fields_data.append({
                    "name": field.name,
                    "type": type(field).__name__,
                    "is_primary_key": getattr(field, 'primary_key', False),
                    "is_foreign_key": hasattr(field, 'related_model'),
                    "is_nullable": getattr(field, 'null', False),
                    "is_unique": getattr(field, 'unique', False),
                    "max_length": getattr(field, 'max_length', None)
                })
        
        models_data[model_key] = {
            "model_name": model.__name__,
            "app_label": model._meta.app_label,
            "table_name": model._meta.db_table,
            "fields": fields_data
        }
    
    return models_data

def collect_relationships_data():
    """Collect relationship data between models"""
    relationships = []
    
    for model in apps.get_models():
        model_key = f"{model._meta.app_label}.{model.__name__}"
        
        for field in model._meta.get_fields():
            if hasattr(field, 'related_model') and field.related_model and hasattr(field, 'name'):
                related_model_key = f"{field.related_model._meta.app_label}.{field.related_model.__name__}"
                
                relationships.append({
                    "from_model": model_key,
                    "to_model": related_model_key,
                    "field_name": field.name,
                    "relationship_type": type(field).__name__
                })
    
    return relationships

if __name__ == '__main__':
    try:
        html_content = generate_graph_schema()
        
        # Save to file
        output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'django_schema_graph.html')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Interactive graph schema generated!")
        print(f"📁 File: django_schema_graph.html")
        print(f"🔗 Full path: {output_file}")
        print(f"\n🌐 Features:")
        print(f"   • Interactive node dragging")
        print(f"   • Zoom and pan")
        print(f"   • Physics simulation")
        print(f"   • Click nodes for details")
        print(f"   • Export to PNG")
        
        # Try to open automatically
        try:
            import webbrowser
            webbrowser.open(f'file://{output_file}')
            print("🚀 Opening in your default browser...")
        except:
            print("💡 Manually open the HTML file in your browser")
            
    except Exception as e:
        print(f"❌ Error generating graph: {e}")
        import traceback
        traceback.print_exc()
