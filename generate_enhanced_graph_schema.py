import os
import sys
import django
import json

# Setup Django
script_dir = os.path.dirname(os.path.abspath(__file__))
mysite_dir = os.path.join(script_dir, 'mysite')
sys.path.insert(0, mysite_dir)
os.chdir(mysite_dir)

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    django.setup()
except ImportError as e:
    print(f"⚠️  Import error: {e}")
    print("Installing required package...")
    import subprocess
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'django-extensions'], check=True)
    django.setup()

from django.apps import apps

def generate_enhanced_graph_schema():
    """Generate an enhanced interactive graph showing Django system connections"""
    print("🌐 GENERATING ENHANCED SYSTEM CONNECTION GRAPH")
    print("=" * 70)
    
    # Collect data
    models_data = collect_models_data()
    relationships_data = collect_relationships_data()
    
    # System analysis
    system_analysis = analyze_system_connections()
    
    # Generate HTML with enhanced visualization
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Django System Architecture - Interactive Graph</title>
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
            display: flex;
            flex-direction: column;
        }}
        
        .header {{
            background: rgba(255,255,255,0.95);
            padding: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 10px;
        }}
        
        .system-legend {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 15px;
            flex-wrap: wrap;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            background: white;
            padding: 8px 15px;
            border-radius: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .legend-color {{
            width: 16px;
            height: 16px;
            border-radius: 50%;
        }}
        
        .canvas-container {{
            flex: 1;
            position: relative;
            background: rgba(255,255,255,0.1);
        }}
        
        #graphCanvas {{
            display: block;
            cursor: move;
            border: none;
        }}
        
        .controls {{
            position: absolute;
            top: 20px;
            right: 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        
        .control-btn {{
            background: rgba(255,255,255,0.9);
            border: none;
            padding: 10px 15px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        
        .control-btn:hover {{
            background: white;
            transform: translateY(-2px);
        }}
        
        .info-panel {{
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(255,255,255,0.95);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            max-width: 350px;
            display: none;
        }}
        
        .info-panel.show {{
            display: block;
        }}
        
        .stats {{
            position: absolute;
            bottom: 20px;
            left: 20px;
            background: rgba(255,255,255,0.9);
            padding: 15px;
            border-radius: 8px;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏗️ Django System Architecture Graph</h1>
        <p style="text-align: center; color: #666; margin-top: 10px;">
            Interactive visualization showing how Auth, Admin, Sessions, and Chat systems connect
        </p>
        
        <div class="system-legend">
            <div class="legend-item">
                <div class="legend-color" style="background: #e74c3c;"></div>
                <span><strong>CORE AUTH</strong> - Central Authentication System</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #3498db;"></div>
                <span><strong>SESSION</strong> - Login State Management</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #f39c12;"></div>
                <span><strong>SOCIAL AUTH</strong> - Google OAuth & Email</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #9b59b6;"></div>
                <span><strong>ADMIN</strong> - Management Interface</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #27ae60;"></div>
                <span><strong>CHAT APP</strong> - Your Application</span>
            </div>
        </div>
    </div>
    
    <div class="canvas-container">
        <canvas id="graphCanvas"></canvas>
        
        <div class="controls">
            <button class="control-btn" onclick="resetView()">🔄 Reset View</button>
            <button class="control-btn" onclick="togglePhysics()">⚡ Toggle Physics</button>
            <button class="control-btn" onclick="exportGraph()">💾 Export</button>
            <button class="control-btn" onclick="focusOnAuth()">🔍 Focus Auth</button>
        </div>
        
        <div class="info-panel" id="infoPanel">
            <h3 id="nodeTitle">Node Information</h3>
            <div id="nodeDetails"></div>
            <button onclick="closeInfo()" style="margin-top: 10px; padding: 5px 10px; border: none; border-radius: 4px; background: #e74c3c; color: white; cursor: pointer;">Close</button>
        </div>
        
        <div class="stats">
            <div><strong>System Models:</strong> {len(models_data)}</div>
            <div><strong>Relationships:</strong> {len(relationships_data)}</div>
            <div><strong>Django Apps:</strong> {len(set(model['app'] for model in models_data))}</div>
        </div>
    </div>

    <script>
        // Enhanced color coding for system types
        const systemColors = {{
            'auth': '#e74c3c',           // Red - Central Authentication (CORE HUB)
            'admin': '#9b59b6',          // Purple - Admin System
            'contenttypes': '#8e44ad',   // Dark Purple - Content Management  
            'sessions': '#3498db',       // Blue - Session Management
            'socialaccount': '#f39c12',  // Orange - Social Auth (Google OAuth)
            'account': '#e67e22',        // Dark Orange - Account Management
            'chatapp': '#27ae60',        // Green - Your Chat Application
            'sites': '#95a5a6',          // Gray - Sites Framework
            'django': '#34495e'          // Dark Gray - Django Core
        }};
        
        // System importance levels (affects node size)
        const systemImportance = {{
            'auth': 3,      // MOST IMPORTANT - Everything connects to auth_user
            'chatapp': 2,   // High importance - Your main app
            'sessions': 2,  // High importance - Required for login
            'admin': 1.5,   // Medium importance
            'socialaccount': 1.5,
            'account': 1.5,
            'contenttypes': 1,
            'sites': 0.5,
            'django': 1
        }};

        const canvas = document.getElementById('graphCanvas');
        const ctx = canvas.getContext('2d');
        
        // Data from Django
        const models = {json.dumps(models_data, indent=8)};
        const relationships = {json.dumps(relationships_data, indent=8)};
        
        // Enhanced node positioning with system clustering
        let nodes = [];
        let edges = [];
        let physicsEnabled = true;
        let scale = 1;
        let offsetX = 0;
        let offsetY = 0;
        
        function initializeGraph() {{
            resizeCanvas();
            
            // Create nodes with system-aware positioning
            const systemClusters = {{
                'auth': {{ centerX: 0, centerY: 0, radius: 150 }},         // CENTER
                'chatapp': {{ centerX: 300, centerY: 0, radius: 120 }},    // RIGHT
                'sessions': {{ centerX: -300, centerY: 0, radius: 80 }},   // LEFT  
                'admin': {{ centerX: 0, centerY: -250, radius: 100 }},     // TOP
                'socialaccount': {{ centerX: 200, centerY: -200, radius: 80 }}, // TOP-RIGHT
                'account': {{ centerX: 200, centerY: -200, radius: 80 }},
                'contenttypes': {{ centerX: -150, centerY: -200, radius: 60 }},
                'sites': {{ centerX: -200, centerY: 100, radius: 40 }},
                'django': {{ centerX: 0, centerY: 200, radius: 60 }}
            }};
            
            models.forEach((model, index) => {{
                const app = model.app;
                const cluster = systemClusters[app] || systemClusters['django'];
                const importance = systemImportance[app] || 1;
                
                // Position within cluster
                const angle = (index % 8) * (Math.PI / 4);
                const clusterRadius = cluster.radius * (0.3 + Math.random() * 0.7);
                
                nodes.push({{
                    id: model.name,
                    app: app,
                    x: cluster.centerX + Math.cos(angle) * clusterRadius,
                    y: cluster.centerY + Math.sin(angle) * clusterRadius,
                    vx: 0,
                    vy: 0,
                    radius: 12 + (importance * 8), // Size based on system importance
                    color: systemColors[app] || '#95a5a6',
                    model: model,
                    connections: 0
                }});
            }});
            
            // Create edges with relationship strength
            relationships.forEach(rel => {{
                const fromNode = nodes.find(n => n.id === rel.from_model);
                const toNode = nodes.find(n => n.id === rel.to_model);
                
                if (fromNode && toNode) {{
                    // Determine edge importance
                    let importance = 1;
                    if (rel.from_model.includes('auth_user') || rel.to_model.includes('auth_user')) {{
                        importance = 3; // AUTH connections are most important
                    }} else if (rel.from_model.includes('chatapp') || rel.to_model.includes('chatapp')) {{
                        importance = 2; // Chat app connections
                    }}
                    
                    edges.push({{
                        from: fromNode,
                        to: toNode,
                        relationship: rel,
                        strength: importance,
                        width: 1 + importance
                    }});
                    
                    fromNode.connections++;
                    toNode.connections++;
                }}
            }});
            
            // Center the graph
            centerGraph();
            draw();
        }}
        
        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            ctx.save();
            ctx.translate(canvas.width / 2 + offsetX, canvas.height / 2 + offsetY);
            ctx.scale(scale, scale);
            
            // Draw system cluster backgrounds
            drawSystemClusters();
            
            // Draw edges (relationships)
            edges.forEach(edge => {{
                ctx.strokeStyle = `rgba(52, 73, 94, ${{0.3 + (edge.strength * 0.2)}})`;
                ctx.lineWidth = edge.width;
                ctx.beginPath();
                ctx.moveTo(edge.from.x, edge.from.y);
                ctx.lineTo(edge.to.x, edge.to.y);
                ctx.stroke();
                
                // Draw arrowhead for important relationships
                if (edge.strength > 1) {{
                    drawArrowhead(edge.from.x, edge.from.y, edge.to.x, edge.to.y, edge.strength);
                }}
            }});
            
            // Draw nodes
            nodes.forEach(node => {{
                // Node shadow
                ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
                ctx.beginPath();
                ctx.arc(node.x + 2, node.y + 2, node.radius, 0, Math.PI * 2);
                ctx.fill();
                
                // Node body
                ctx.fillStyle = node.color;
                ctx.beginPath();
                ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
                ctx.fill();
                
                // Node border (thicker for important systems)
                const borderWidth = node.app === 'auth' ? 4 : node.app === 'chatapp' ? 3 : 2;
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)';
                ctx.lineWidth = borderWidth;
                ctx.stroke();
                
                // Connection indicator (small dots around high-connection nodes)
                if (node.connections > 3) {{
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
                    for (let i = 0; i < Math.min(node.connections, 8); i++) {{
                        const angle = (i / 8) * Math.PI * 2;
                        const dotX = node.x + Math.cos(angle) * (node.radius + 5);
                        const dotY = node.y + Math.sin(angle) * (node.radius + 5);
                        ctx.beginPath();
                        ctx.arc(dotX, dotY, 2, 0, Math.PI * 2);
                        ctx.fill();
                    }}
                }}
                
                // Node label
                ctx.fillStyle = '#2c3e50';
                ctx.font = `${{node.app === 'auth' ? 'bold ' : ''}}12px Arial`;
                ctx.textAlign = 'center';
                
                const label = node.id.replace('_', ' ').replace(/([A-Z])/g, ' $1').trim();
                const shortLabel = label.length > 15 ? label.substring(0, 12) + '...' : label;
                
                ctx.fillText(shortLabel, node.x, node.y + node.radius + 15);
                
                // System type indicator
                ctx.font = '10px Arial';
                ctx.fillStyle = node.color;
                ctx.fillText(`[${{node.app.toUpperCase()}}]`, node.x, node.y + node.radius + 28);
            }});
            
            ctx.restore();
        }}
        
        function drawSystemClusters() {{
            const clusters = [
                {{ name: 'CORE AUTH', color: '#e74c3c20', x: 0, y: 0, radius: 180 }},
                {{ name: 'CHAT APP', color: '#27ae6020', x: 300, y: 0, radius: 150 }},
                {{ name: 'SESSION MGMT', color: '#3498db20', x: -300, y: 0, radius: 100 }},
                {{ name: 'ADMIN SYSTEM', color: '#9b59b620', x: 0, y: -250, radius: 120 }}
            ];
            
            clusters.forEach(cluster => {{
                ctx.fillStyle = cluster.color;
                ctx.beginPath();
                ctx.arc(cluster.x, cluster.y, cluster.radius, 0, Math.PI * 2);
                ctx.fill();
                
                ctx.strokeStyle = cluster.color.replace('20', '40');
                ctx.lineWidth = 2;
                ctx.setLineDash([5, 5]);
                ctx.stroke();
                ctx.setLineDash([]);
                
                // Cluster label
                ctx.fillStyle = cluster.color.replace('20', '');
                ctx.font = 'bold 14px Arial';
                ctx.textAlign = 'center';
                ctx.fillText(cluster.name, cluster.x, cluster.y - cluster.radius - 10);
            }});
        }}
        
        function drawArrowhead(fromX, fromY, toX, toY, strength) {{
            const angle = Math.atan2(toY - fromY, toX - fromX);
            const arrowSize = 8 + (strength * 2);
            
            // Position arrowhead at edge of target node
            const targetNode = nodes.find(n => n.x === toX && n.y === toY);
            const edgeX = toX - Math.cos(angle) * (targetNode?.radius || 12);
            const edgeY = toY - Math.sin(angle) * (targetNode?.radius || 12);
            
            ctx.fillStyle = `rgba(231, 76, 60, ${{0.5 + (strength * 0.2)}})`;
            ctx.beginPath();
            ctx.moveTo(edgeX, edgeY);
            ctx.lineTo(edgeX - arrowSize * Math.cos(angle - Math.PI/6), 
                       edgeY - arrowSize * Math.sin(angle - Math.PI/6));
            ctx.lineTo(edgeX - arrowSize * Math.cos(angle + Math.PI/6), 
                       edgeY - arrowSize * Math.sin(angle + Math.PI/6));
            ctx.closePath();
            ctx.fill();
        }}
        
        // Physics simulation for natural positioning
        function updatePhysics() {{
            if (!physicsEnabled) return;
            
            const damping = 0.85;
            const repulsion = 1000;
            const attraction = 0.01;
            
            // Apply forces between all nodes
            for (let i = 0; i < nodes.length; i++) {{
                for (let j = i + 1; j < nodes.length; j++) {{
                    const nodeA = nodes[i];
                    const nodeB = nodes[j];
                    
                    const dx = nodeB.x - nodeA.x;
                    const dy = nodeB.y - nodeA.y;
                    const distance = Math.sqrt(dx * dx + dy * dy);
                    
                    if (distance > 0) {{
                        // Repulsion (all nodes push away from each other)
                        const repulsionForce = repulsion / (distance * distance);
                        const repulsionX = (dx / distance) * repulsionForce;
                        const repulsionY = (dy / distance) * repulsionForce;
                        
                        nodeA.vx -= repulsionX;
                        nodeA.vy -= repulsionY;
                        nodeB.vx += repulsionX;
                        nodeB.vy += repulsionY;
                    }}
                }}
            }}
            
            // Apply attraction forces for connected nodes
            edges.forEach(edge => {{
                const dx = edge.to.x - edge.from.x;
                const dy = edge.to.y - edge.from.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance > 0) {{
                    const attractionForce = attraction * distance * edge.strength;
                    const attractionX = (dx / distance) * attractionForce;
                    const attractionY = (dy / distance) * attractionForce;
                    
                    edge.from.vx += attractionX;
                    edge.from.vy += attractionY;
                    edge.to.vx -= attractionX;
                    edge.to.vy -= attractionY;
                }}
            }});
            
            // Update positions
            nodes.forEach(node => {{
                node.vx *= damping;
                node.vy *= damping;
                node.x += node.vx;
                node.y += node.vy;
            }});
        }}
        
        // Event handlers and utility functions
        let isDragging = false;
        let dragNode = null;
        let lastMouseX = 0;
        let lastMouseY = 0;
        
        canvas.addEventListener('mousedown', (e) => {{
            const rect = canvas.getBoundingClientRect();
            const mouseX = (e.clientX - rect.left - canvas.width / 2 - offsetX) / scale;
            const mouseY = (e.clientY - rect.top - canvas.height / 2 - offsetY) / scale;
            
            // Check if clicking on a node
            const clickedNode = nodes.find(node => {{
                const dx = mouseX - node.x;
                const dy = mouseY - node.y;
                return Math.sqrt(dx * dx + dy * dy) < node.radius;
            }});
            
            if (clickedNode) {{
                dragNode = clickedNode;
                showNodeInfo(clickedNode);
            }} else {{
                isDragging = true;
                document.getElementById('infoPanel').classList.remove('show');
            }}
            
            lastMouseX = e.clientX;
            lastMouseY = e.clientY;
        }});
        
        canvas.addEventListener('mousemove', (e) => {{
            if (dragNode) {{
                const rect = canvas.getBoundingClientRect();
                dragNode.x = (e.clientX - rect.left - canvas.width / 2 - offsetX) / scale;
                dragNode.y = (e.clientY - rect.top - canvas.height / 2 - offsetY) / scale;
                dragNode.vx = 0;
                dragNode.vy = 0;
            }} else if (isDragging) {{
                offsetX += e.clientX - lastMouseX;
                offsetY += e.clientY - lastMouseY;
            }}
            
            lastMouseX = e.clientX;
            lastMouseY = e.clientY;
        }});
        
        canvas.addEventListener('mouseup', () => {{
            isDragging = false;
            dragNode = null;
        }});
        
        canvas.addEventListener('wheel', (e) => {{
            e.preventDefault();
            const zoomFactor = e.deltaY > 0 ? 0.9 : 1.1;
            scale *= zoomFactor;
            scale = Math.max(0.1, Math.min(3, scale));
        }});
        
        function showNodeInfo(node) {{
            const panel = document.getElementById('infoPanel');
            const title = document.getElementById('nodeTitle');
            const details = document.getElementById('nodeDetails');
            
            title.textContent = node.id.replace('_', ' ').toUpperCase();
            
            const systemRole = getSystemRole(node.app, node.id);
            
            details.innerHTML = `
                <div style="margin-bottom: 15px;">
                    <strong>🏷️ System:</strong> ${{node.app.toUpperCase()}}
                    <br><strong>🔗 Connections:</strong> ${{node.connections}}
                    <br><strong>⚡ Role:</strong> ${{systemRole}}
                </div>
                <div style="margin-bottom: 10px;">
                    <strong>📊 Fields:</strong>
                    <div style="max-height: 150px; overflow-y: auto; margin-top: 5px;">
                        ${{node.model.fields.map(field => 
                            `<div style="padding: 2px; background: #f8f9fa; margin: 2px 0; border-radius: 3px; font-size: 12px;">
                                <strong>${{field.name}}</strong>: ${{field.type}}
                            </div>`
                        ).join('')}}
                    </div>
                </div>
            `;
            
            panel.classList.add('show');
        }}
        
        function getSystemRole(app, modelName) {{
            const roles = {{
                'auth': modelName.includes('user') ? '🔑 CENTRAL HUB - Every user action starts here' :
                        modelName.includes('group') ? '👥 User Groups & Permissions' :
                        modelName.includes('permission') ? '🛡️ Access Control Rules' : '🔐 Authentication Core',
                'sessions': '🎫 Login Session Management - Keeps users logged in',
                'chatapp': modelName.includes('room') ? '💬 Chat Room Management' :
                          modelName.includes('message') ? '📨 Message Storage & Delivery' :
                          modelName.includes('profile') ? '👤 Extended User Information' : '🗨️ Chat System Component',
                'admin': '⚙️ Administrative Interface - Manage all data',
                'socialaccount': '🔗 Google OAuth Integration - Social login',
                'account': '📧 Email Verification & Account Management',
                'contenttypes': '📋 Model Registry - Enables admin for all models'
            }};
            
            return roles[app] || '🔧 Django System Component';
        }}
        
        function resetView() {{
            scale = 1;
            offsetX = 0;
            offsetY = 0;
            centerGraph();
        }}
        
        function togglePhysics() {{
            physicsEnabled = !physicsEnabled;
        }}
        
        function focusOnAuth() {{
            const authNode = nodes.find(n => n.id.includes('auth_user'));
            if (authNode) {{
                offsetX = -authNode.x * scale;
                offsetY = -authNode.y * scale;
                scale = 1.5;
            }}
        }}
        
        function centerGraph() {{
            const bounds = nodes.reduce((acc, node) => {{
                acc.minX = Math.min(acc.minX, node.x);
                acc.maxX = Math.max(acc.maxX, node.x);
                acc.minY = Math.min(acc.minY, node.y);
                acc.maxY = Math.max(acc.maxY, node.y);
                return acc;
            }}, {{ minX: Infinity, maxX: -Infinity, minY: Infinity, maxY: -Infinity }});
            
            const centerX = (bounds.minX + bounds.maxX) / 2;
            const centerY = (bounds.minY + bounds.maxY) / 2;
            
            offsetX = -centerX * scale;
            offsetY = -centerY * scale;
        }}
        
        function exportGraph() {{
            const link = document.createElement('a');
            link.download = 'django-system-graph.png';
            link.href = canvas.toDataURL();
            link.click();
        }}
        
        function closeInfo() {{
            document.getElementById('infoPanel').classList.remove('show');
        }}
        
        function resizeCanvas() {{
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight - 120;
        }}
        
        // Animation loop
        function animate() {{
            updatePhysics();
            draw();
            requestAnimationFrame(animate);
        }}
        
        // Initialize
        window.addEventListener('resize', resizeCanvas);
        initializeGraph();
        animate();
    </script>
</body>
</html>
"""

    # Save HTML file
    output_file = os.path.join(script_dir, 'django_enhanced_system_graph.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Enhanced system graph generated: {output_file}")
    print("\n🔍 SYSTEM CONNECTION ANALYSIS:")
    print(system_analysis)
    
    return output_file

def collect_models_data():
    """Collect all Django models and their fields"""
    models_data = []
    
    for model in apps.get_models():
        app_label = model._meta.app_label
        model_name = model._meta.db_table or f"{app_label}_{model.__name__.lower()}"
        
        fields_data = []
        for field in model._meta.get_fields():
            if hasattr(field, 'get_internal_type'):
                fields_data.append({
                    'name': field.name,
                    'type': field.get_internal_type(),
                    'null': getattr(field, 'null', False),
                    'blank': getattr(field, 'blank', False)
                })
        
        models_data.append({
            'name': model_name,
            'app': app_label,
            'model_class': model.__name__,
            'fields': fields_data
        })
    
    return models_data

def collect_relationships_data():
    """Collect foreign key and many-to-many relationships"""
    relationships = []
    
    for model in apps.get_models():
        app_label = model._meta.app_label
        model_name = model._meta.db_table or f"{app_label}_{model.__name__.lower()}"
        
        for field in model._meta.get_fields():
            if hasattr(field, 'related_model') and field.related_model:
                related_app = field.related_model._meta.app_label
                related_name = (field.related_model._meta.db_table or 
                               f"{related_app}_{field.related_model.__name__.lower()}")
                
                rel_type = "ForeignKey"
                if hasattr(field, 'many_to_many') and field.many_to_many:
                    rel_type = "ManyToMany"
                elif hasattr(field, 'one_to_many') and field.one_to_many:
                    rel_type = "OneToMany"
                elif hasattr(field, 'one_to_one') and field.one_to_one:
                    rel_type = "OneToOne"
                
                relationships.append({
                    'from_model': model_name,
                    'to_model': related_name,
                    'field_name': field.name,
                    'relationship_type': rel_type,
                    'from_app': app_label,
                    'to_app': related_app
                })
    
    return relationships

def analyze_system_connections():
    """Analyze how different Django systems are interconnected"""
    models_data = collect_models_data()
    relationships_data = collect_relationships_data()
    
    # Count connections per system
    system_connections = {}
    auth_connections = []
    
    for rel in relationships_data:
        from_app = rel['from_app']
        to_app = rel['to_app']
        
        # Track connections between systems
        connection_key = f"{from_app} → {to_app}"
        system_connections[connection_key] = system_connections.get(connection_key, 0) + 1
        
        # Track what connects to auth (most important)
        if 'auth_user' in rel['to_model']:
            auth_connections.append(f"{rel['from_model']} connects via {rel['field_name']}")
    
    analysis = f"""
    🔗 SYSTEM INTERCONNECTIONS:
    
    📊 Connection Counts:
    {chr(10).join([f"    • {k}: {v} relationships" for k, v in sorted(system_connections.items(), key=lambda x: x[1], reverse=True)])}
    
    🔑 AUTH_USER as CENTRAL HUB:
    {chr(10).join([f"    • {conn}" for conn in auth_connections[:10]])}
    {f"    ... and {len(auth_connections) - 10} more" if len(auth_connections) > 10 else ""}
    
    🏗️ ARCHITECTURE INSIGHTS:
    • auth_user is the central node - everything connects to it
    • sessions manages login state for all users
    • socialaccount enables Google OAuth login
    • admin provides management interface for all models
    • chatapp is your main application logic
    """
    
    return analysis

if __name__ == "__main__":
    output_file = generate_enhanced_graph_schema()
    print(f"\n🌐 Open this file in your browser: {output_file}")
