import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_blueprint():
    fig, ax = plt.subplots(figsize=(16, 10), facecolor='#0B0C10')
    ax.set_facecolor('#0B0C10')
    
    # 1. BOUNDARIES
    ax.add_patch(patches.Rectangle((0.5, 7.6), 15.0, 1.8, linewidth=2, edgecolor='#1F2833', facecolor='#15222E'))
    ax.text(0.8, 9.0, "☁️ CLOUD COMPUTE INFRASTRUCTURE TIER (Google Edge Network)", color='#66FCF1', fontsize=12, fontweight='bold')

    ax.add_patch(patches.Rectangle((0.5, 0.4), 15.0, 6.8, linewidth=2, edgecolor='#1F2833', facecolor='#121214'))
    ax.text(0.8, 6.85, "💻 HARDWARE RUNTIME: System76 Galago Pro (Linux Ubuntu x64)", color='#C5C6C7', fontsize=12, fontweight='bold')

    ax.add_patch(patches.Rectangle((0.8, 0.6), 10.2, 5.8, linewidth=1.5, edgecolor='#45a29e', facecolor='#1A1A1D'))
    ax.text(1.0, 6.1, "📟 8GB DDR4 PHYSICAL RAM POOL (Volatile Workspace)", color='#45A29E', fontsize=10, fontweight='bold')

    ax.add_patch(patches.Rectangle((11.4, 0.6), 3.8, 5.8, linewidth=1.5, edgecolor='#ef8354', facecolor='#1C1917'))
    ax.text(11.6, 6.1, "💾 PERSISTENT NVMe STORAGE DISK", color='#ef8354', fontsize=10, fontweight='bold')

    ax.add_patch(patches.Rectangle((1.1, 0.8), 5.1, 5.0, linewidth=1.2, edgecolor='#2d6a4f', facecolor='#0B1A12'))
    ax.text(1.3, 5.5, "🐍 LangGraph Execution Loop Sandbox (venv)", color='#2d6a4f', fontsize=9, fontweight='bold')

    ax.add_patch(patches.Rectangle((6.5, 0.8), 4.2, 5.0, linewidth=1.2, edgecolor='#2A4B7C', facecolor='#0D1B2A'))
    ax.text(6.7, 5.5, "🐋 Virtualized Docker Daemon Container", color='#2A4B7C', fontsize=9, fontweight='bold')

    # 2. ENTITIES (BOXES)
    ax.add_patch(patches.Rectangle((1.5, 7.9), 4.0, 0.8, facecolor='#023e8a', edgecolor='#66FCF1', linewidth=1))
    ax.text(3.5, 8.3, "gemini-embedding-001\n(Context Vectorization API)", color='#FFFFFF', fontsize=9, ha='center', va='center')
    
    ax.add_patch(patches.Rectangle((10.5, 7.9), 4.0, 0.8, facecolor='#023e8a', edgecolor='#66FCF1', linewidth=1))
    ax.text(12.5, 8.3, "gemini-2.5-flash\n(Structured Diagnostics & Repair)", color='#FFFFFF', fontsize=9, ha='center', va='center')

    ax.add_patch(patches.Rectangle((1.4, 4.4), 2.2, 0.8, facecolor='#781D1D', edgecolor='#FF4D4D', linewidth=1))
    ax.text(2.5, 4.8, "HealerState Queue Matrix\n[pending_files Queue]", color='#FFFFFF', fontsize=8, ha='center', va='center', fontweight='bold')
    
    nodes = [
        ("Node 1: fetch_context\n(Qdrant Context Reader)", 1.4, 3.1, '#B35400'),
        ("Node 2: analyze_route\n(Vulnerability Parser)", 1.4, 1.3, '#B35400'),
        ("Queue Control Node\nselect_next_target", 3.8, 1.3, '#005f73'),
        ("Node 3: auto_heal_node\n(Iterative Patch Surgeon)", 3.8, 2.8, '#B35400'),
        ("Physical OS Tool\nos.write Remediation Pipe", 3.8, 4.3, '#D90429')
    ]
    for name, x, y, color in nodes:
        ax.add_patch(patches.Rectangle((x, y), 2.2, 0.8, facecolor=color, edgecolor='#FFFFFF', linewidth=1))
        ax.text(x+1.1, y+0.4, name, color='#FFFFFF', fontsize=8, ha='center', va='center')

    ax.add_patch(patches.Rectangle((6.8, 1.6), 3.6, 3.2, facecolor='#190903', edgecolor='#dc2f02', linewidth=1.5))
    ax.text(8.6, 4.5, "Qdrant Vector DB Server", color='#FF6B35', fontsize=9.5, ha='center', fontweight='bold')
    
    ax.add_patch(patches.Rectangle((7.0, 2.0), 3.2, 2.0, facecolor='#370617', edgecolor='#9d0208', linewidth=1))
    ax.text(8.6, 3.0, "local_codebase Collection\n\n[INT8 Scalar Quantized\nTarget Vectors]", color='#FFD23F', fontsize=8.5, ha='center', va='center')

    files = [
        ("./mock_project/auth.py\n(REMEDIATED TARGET SOURCE)", 11.6, 4.5, '#2B3A42'),
        ("./mock_project/payment.py\n(VULNERABLE PRODUCTION ASSET)", 11.6, 2.8, '#2B3A42'),
        ("./mock_project/router.py\n(SAFE BENIGN ASSET - SKIP)", 11.6, 1.1, '#2B3A42')
    ]
    for name, x, y, color in files:
        ax.add_patch(patches.Rectangle((x, y), 3.4, 0.9, facecolor=color, edgecolor='#ef8354', linewidth=1.2))
        ax.text(x+1.7, y+0.45, name, color='#FFFFFF', fontsize=8.5, ha='center', va='center')

    # 3. ZERO-COLLISION LINE ROUTING
    ax.annotate("", xy=(2.5, 4.4), xytext=(2.5, 3.9), arrowprops=dict(arrowstyle="-|>", color='#66FCF1', lw=1.5, mutation_scale=12))
    ax.annotate("", xy=(1.4, 3.5), xytext=(6.8, 3.5), arrowprops=dict(arrowstyle="<-", color='#FFD23F', lw=1.5))
    ax.annotate("", xy=(2.5, 2.1), xytext=(2.5, 3.1), arrowprops=dict(arrowstyle="-|>", color='#C5C6C7', lw=1.5, mutation_scale=12))
    
    # Node 2 pushes to Queue Controller Node
    ax.annotate("", xy=(3.8, 1.7), xytext=(3.6, 1.7), arrowprops=dict(arrowstyle="-|>", color='#66FCF1', lw=1.5))
    
    # Queue Controller Node loops up to Node 3 (Conditional Edge evaluation)
    ax.annotate("", xy=(4.9, 2.8), xytext=(4.9, 2.1), arrowprops=dict(arrowstyle="-|>", color='#FFB703', lw=1.8, mutation_scale=12))
    ax.text(5.0, 2.4, "IF QUEUE NOT EMPTY", color='#FFB703', fontsize=7.5, va='center')

    # Node 3 triggers OS write tool
    ax.annotate("", xy=(4.9, 4.3), xytext=(4.9, 3.6), arrowprops=dict(arrowstyle="-|>", color='#FF4D4D', lw=1.5, mutation_scale=12))

    # Node 3 loops back down around to Queue Controller Node to step through the collection array
    ax.annotate("", xy=(3.8, 1.7), xytext=(3.8, 3.2),
                arrowprops=dict(arrowstyle="-|>", color='#00F5D4', lw=2.0, connectionstyle="arc3,rad=0.4"))
    ax.text(3.1, 2.5, "Loop Next Item", color='#00F5D4', fontsize=7.5, ha='center')

    # Sweep rewrite line directly across storage media planes
    ax.annotate("", xy=(11.6, 3.25), xytext=(6.0, 4.5),
                arrowprops=dict(arrowstyle="-|>", color='#D90429', lw=3.5, mutation_scale=22, connectionstyle="arc3,rad=-0.35"))
    ax.text(8.5, 6.4, "🚨 CYCLIC BATCH REWRITE TRACK\nIterative File Remediation Loop (os.write)", 
            color='#FF4D4D', fontsize=9.5, fontweight='bold', ha='center', bbox=dict(facecolor='#0B0C10', alpha=0.8, edgecolor='none'))

    # API reasoning calls
    ax.annotate("", xy=(3.5, 7.9), xytext=(3.5, 5.2), arrowprops=dict(arrowstyle="<->", color='#45A29E', lw=1.5, linestyle=':'))
    ax.annotate("", xy=(10.5, 8.5), xytext=(1.4, 1.7), arrowprops=dict(arrowstyle="<->", color='#45A29E', lw=1.5, connectionstyle="arc3,rad=-0.4", linestyle='--'))
    ax.annotate("", xy=(12.0, 7.9), xytext=(4.9, 3.6), arrowprops=dict(arrowstyle="<->", color='#45A29E', lw=1.5, connectionstyle="arc3,rad=-0.15"))

    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('self_healing_architecture.png', dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    print("🎯 Success! System diagram blueprint updated and compiled to: 'self_healing_architecture.png'")

if __name__ == "__main__":
    create_blueprint()