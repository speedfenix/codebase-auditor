import os
from graphviz import Digraph

# Ensure output directory exists
os.makedirs("./diagrams", exist_ok=True)

def create_ai_orchestration_diagram():
    """Diagram 1: LangGraph State Machine & Orchestration Flow"""
    dot = Digraph('AI_Orchestration', comment='LangGraph State Machine Matrix')
    dot.attr(rankdir='TB', size='10,12', bgcolor='#F8FAFC', fontname='Helvetica')
    dot.attr('node', fontname='Helvetica', shape='box', style='filled,rounded', penwidth='2')
    dot.attr('edge', fontname='Helvetica', fontsize='10', color='#64748B', penwidth='1.5')

    # Status/Virtual Boundaries
    dot.node('START', 'START\n(Entrypoint)', color='#475569', fillcolor='#E2E8F0', fontcolor='#0F172A', shape='circle')
    dot.node('END', 'END\n(Halt Runtime)', color='#475569', fillcolor='#E2E8F0', fontcolor='#0F172A', shape='doublecircle')

    # State Nodes
    dot.node('N1', '🔍 [NODE 1]\nfetch_context_node\n\n- Scrolls Qdrant payloads\n- Pulls 6 structural chunks\n- Extracts literal file_path', color='#0F766E', fillcolor='#E0F2FE', fontcolor='#0369A1')
    dot.node('N2', '🧠 [NODE 2]\nanalyze_and_route_node\n\n- Invokes Gemini-2.5-Flash\n- Structured JSON Audit output\n- Normalizes paths to targets/\n- Guards against 503 errors', color='#0F766E', fillcolor='#CCFBF1', fontcolor='#115E59')
    dot.node('N3', '🔄 [QUEUE CONTROLLER]\nselect_next_target_node\n\n- Pops current_file from memory\n- Mutates pending_files state', color='#B45309', fillcolor='#FEF3C7', fontcolor='#92400E')
    dot.node('N4', '🚨 [NODE 3]\nauto_heal_node\n\n- Source File Code Surgery\n- Invokes Gemini Secure Rewrite\n- Writes clean file over OS asset\n- Guards against 503 errors', color='#0F766E', fillcolor='#F1F5F9', fontcolor='#334155')

    # Routing Decisions
    dot.node('DECISION', '❓ Router Edge\nroute_after_queue_check\n\nAre pending items empty?', color='#B91C1C', fillcolor='#FEE2E2', fontcolor='#991B1B', shape='diamond')

    # Backoff Indicators (Visual Overlays)
    dot.node('BO1', '🛡️ Exponential Backoff Loop\n(Max 5 attempts | x2 delay multiplier)', color='#B91C1C', fillcolor='#FFE4E6', fontcolor='#991B1B', style='dashed,filled')
    dot.node('BO2', '🛡️ Exponential Backoff Loop\n(Max 5 attempts | x2 delay multiplier)', color='#B91C1C', fillcolor='#FFE4E6', fontcolor='#991B1B', style='dashed,filled')

    # Connect Backoff annotations to active nodes
    dot.edge('BO1', 'N2', style='dotted', arrowhead='none', color='#F87171')
    dot.edge('BO2', 'N4', style='dotted', arrowhead='none', color='#F87171')

    # Core Orchestration Flow Pipeline
    dot.edge('START', 'N1', 'Initialize HealerState matrix')
    dot.edge('N1', 'N2', 'Appends context_chunks text')
    dot.edge('N2', 'N3', 'Populates findings & pending_files lists')
    dot.edge('N3', 'DECISION', 'Exposes next current_file target')
    dot.edge('DECISION', 'N4', 'No: Continue to targets path', color='#059669', penwidth='2')
    dot.edge('DECISION', 'END', 'Yes: Task finished', color='#475569', penwidth='2')
    dot.edge('N4', 'N3', 'Re-enters evaluation stack loop')

    dot.render('./diagrams/01_ai_orchestration_graph', format='png', cleanup=True)
    print("✅ Successfully generated: ./diagrams/01_ai_orchestration_graph.png")


def create_uml_sequence_diagram():
    """Diagram 2: Process Timeline Interaction Sequence"""
    dot = Digraph('UML_Sequence', comment='Temporal Lifecycle Timeline Flow')
    dot.attr(rankdir='LR', bgcolor='#F8FAFC', fontname='Helvetica')
    dot.attr('node', fontname='Helvetica', shape='box', style='filled', penwidth='1.5')
    dot.attr('edge', fontname='Helvetica', fontsize='10', penwidth='1.5')

    # Lifelines represented as structured horizontal blocks
    with dot.subgraph(name='cluster_lifelines') as c:
        c.attr(label='⚙️  SYSTEM LAYER LIFELINES (Left-to-Right Invocation Timeline)', fontname='Helvetica-Bold', bgcolor='#F1F5F9', color='#CBD5E1')
        c.node('L1', '📊 Python Run Engine\n(State Manager)', fillcolor='#334155', fontcolor='#FFFFFF', color='#1E293B')
        c.node('L2', '🗄️ Local Vector DB\n(Qdrant Port 6333)', fillcolor='#0284C7', fontcolor='#FFFFFF', color='#0369A1')
        c.node('L3', '🧠 Remote AI Service\n(Gemini 2.5 Flash API)', fillcolor='#0D9488', fontcolor='#FFFFFF', color='#0F766E')
        c.node('L4', '💾 Local File System\n(./targets/mock_project/)', fillcolor='#475569', fontcolor='#FFFFFF', color='#334155')

    # Sequence of Transactions
    dot.edge('L1', 'L2', '1. client.scroll() request', color='#0284C7')
    dot.edge('L2', 'L1', '2. Returns context payload + payload["file_path"]', color='#0284C7', style='dashed')
    
    dot.edge('L1', 'L3', '3. ai_client.models.generate_content() [Audit Plan]', color='#0D9488')
    dot.edge('L3', 'L1', '4. 🛑 503 Spike Intercepted -> Backoff Retries Sleep Loop', color='#B91C1C', penwidth='2.5')
    dot.edge('L3', 'L1', '5. Returns validated structural JSON findings payload', color='#0D9488', style='dashed')
    
    dot.edge('L1', 'L4', '6. Reads existing source code resource string data', color='#475569')
    dot.edge('L4', 'L1', '7. Code character string loaded to active memory space', color='#475569', style='dashed')
    
    dot.edge('L1', 'L3', '8. ai_client.models.generate_content() [Secure Surgery Rewrite]', color='#0D9488')
    dot.edge('L3', 'L1', '9. Returns clean, functional vulnerability-free patch code', color='#0D9488', style='dashed')
    
    dot.edge('L1', 'L4', '10. Overwrites resource target path file system asset', color='#059669', penwidth='2.5')

    dot.render('./diagrams/02_uml_sequence', format='png', cleanup=True)
    print("✅ Successfully generated: ./diagrams/02_uml_sequence.png")


def create_c4_component_diagram():
    """Diagram 3: C4 Model Component / Functional Architecture Mapping"""
    dot = Digraph('C4_Component', comment='Component Level Functional Architecture Mapping')
    dot.attr(rankdir='TB', bgcolor='#F8FAFC', fontname='Helvetica')
    dot.attr('node', fontname='Helvetica', shape='box', style='filled,rounded', penwidth='2')
    dot.attr('edge', fontname='Helvetica', fontsize='10', color='#64748B')

    # System Script Container Context
    with dot.subgraph(name='cluster_container') as c:
        c.attr(label='📦 Python Script Execution Context: agent_healer.py', fontname='Helvetica-Bold', bgcolor='#E2E8F0', color='#94A3B8')
        
        c.node('C_STATE', '📊 Memory Structure Matrix\n[HealerState - TypedDict]\n\n- context_chunks: list[str]\n- findings: list[dict]\n- pending_files: list[str]\n- current_file: str', color='#D97706', fillcolor='#FEF3C7', fontcolor='#78350F')
        c.node('F1', '⚙️ Component Node\nfetch_context_node()', color='#0F766E', fillcolor='#CCFBF1', fontcolor='#115E59')
        c.node('F2', '⚙️ Component Node\nanalyze_and_route_node()', color='#0F766E', fillcolor='#CCFBF1', fontcolor='#115E59')
        c.node('F3', '⚙️ Component Node\nselect_next_target_node()', color='#0F766E', fillcolor='#CCFBF1', fontcolor='#115E59')
        c.node('F4', '⚙️ Component Node\nauto_heal_node()', color='#0F766E', fillcolor='#CCFBF1', fontcolor='#115E59')

    # External Tools/Layers Boundaries
    dot.node('EXT_QDRANT', '🗄️ Database Service Container\nQdrant DB (Port 6333)\nCollection: local_codebase', color='#0369A1', fillcolor='#E0F2FE', fontcolor='#0369A1')
    dot.node('EXT_GEMINI', '🧠 SaaS Cognitive Engine\nGoogle Gemini 2.5 Flash\nLLM Reasoning Services API', color='#0F766E', fillcolor='#E2E8F0', fontcolor='#0F172A')
    dot.node('EXT_FS', '💾 Operating System Disk FS\nPath Target: ./targets/mock_project/*', color='#334155', fillcolor='#F1F5F9', fontcolor='#334155')

    # Inter-component connectivity
    dot.edge('F1', 'EXT_QDRANT', 'Queries collection documents vectors')
    dot.edge('EXT_QDRANT', 'F1', 'Hydrates file payloads context')
    dot.edge('F1', 'C_STATE', 'Mutates state: context_chunks')
    
    dot.edge('C_STATE', 'F2', 'Reads injected context lists data window')
    dot.edge('F2', 'EXT_GEMINI', 'Pushes audit parameters prompts window via SDK')
    dot.edge('EXT_GEMINI', 'F2', 'Returns JSON strings schema matches')
    dot.edge('F2', 'C_STATE', 'Mutates state: findings & pending_files')
    
    dot.edge('C_STATE', 'F3', 'Evaluates remaining items left in queue list')
    dot.edge('F3', 'C_STATE', 'Pops list asset to current_file memory space')
    
    dot.edge('C_STATE', 'F4', 'Extracts exact isolated current_file value path')
    dot.edge('F4', 'EXT_FS', 'Reads target code characters string')
    dot.edge('F4', 'EXT_GEMINI', 'Dispatches code healing synthesis prompt request')
    dot.edge('EXT_GEMINI', 'F4', 'Returns clean code text strings')
    dot.edge('F4', 'EXT_FS', 'Writes fresh safe code blocks to asset disk storage', color='#059669', penwidth='2')

    dot.render('./diagrams/03_c4_component', format='png', cleanup=True)
    print("✅ Successfully generated: ./diagrams/03_c4_component.png")


def create_physical_deployment_diagram():
    """Diagram 4: Physical Deployment Architecture & Hardware Storage Mapping"""
    dot = Digraph('Physical_Deployment', comment='Physical Deployment Blueprint and VRAM Space Allocation')
    dot.attr(rankdir='LR', bgcolor='#F8FAFC', fontname='Helvetica')
    dot.attr('node', fontname='Helvetica', shape='box3d', style='filled', penwidth='2')
    dot.attr('edge', fontname='Helvetica', fontsize='10', color='#475569', penwidth='1.5')

    # Main Local Hardware Machine Box
    with dot.subgraph(name='cluster_host') as host:
        host.attr(label='💻 Local Host Development Machine: fca-GalagoPro Laptop', fontname='Helvetica-Bold', bgcolor='#E2E8F0', color='#94A3B8')
        
        # Local RAM Partition Node Box
        with host.subgraph(name='cluster_system_ram') as ram:
            ram.attr(label='⚡ Volatile System Memory (RAM Tiers)', fontname='Helvetica-Bold', bgcolor='#F1F5F9', color='#CBD5E1', style='dashed')
            ram.node('RAM_VENV', '🐍 Python 3.12 Process (venv Space)\n\n- Holds LangGraph runtime state\n- Stores HealerState TypedDict matrix\n- Runs tenacity retry routines in RAM thread', shape='box', style='filled,rounded', fillcolor='#FEF3C7', color='#D97706', fontcolor='#78350F')
            ram.node('RAM_QDRANT', '📦 Docker daemon virtual memory allocation\n\n- Holds vector search buffer cache pools\n- Keeps local HNSW indexes pinned in memory', shape='box', style='filled,rounded', fillcolor='#E0F2FE', color='#0284C7', fontcolor='#0369A1')
        
        # Local Persistent Storage Nodes
        host.node('DISK_FS', '📁 Hard Drive Storage (NVMe SSD)\n\n- Path: ./targets/mock_project/\n- Files: auth.py, payment.py\n- Modified directly via open(..., "w")', fillcolor='#F8FAFC', color='#475569', fontcolor='#0F172A')
        host.node('CONTAINER_QDRANT', '🐳 Running Docker Container instance\n\n- Image: qdrant/qdrant\n- Mapped Port: localhost:6333\n- Stores embedded code vectors payload', fillcolor='#E0F2FE', color='#0284C7', fontcolor='#0369A1')

    # Cloud Tier Architecture Node Boundary
    with dot.subgraph(name='cluster_cloud') as cloud:
        cloud.attr(label='☁️  Upstream Cloud Hyperscaler Layer', fontname='Helvetica-Bold', bgcolor='#F1F5F9', color='#CBD5E1')
        cloud.node('CLOUD_GEMINI', '🤖 Google Cloud AI Engine Infrastructure\nModel: gemini-2.5-flash\n\n- Executes neural token weights math calculations\n- Experiences transient capacity traffic spikes\n- Throws 503 errors when load constraints peak', fillcolor='#F0FDF4', color='#16A34A', fontcolor='#14532D')

    # Network, I/O Port and Storage Mappings Wiring Connections
    dot.edge('RAM_VENV', 'CONTAINER_QDRANT', 'Local TCP Request\n(HTTP REST API Port 6333)', color='#0284C7')
    dot.edge('RAM_VENV', 'CLOUD_GEMINI', 'HTTPS Outbound Internet Gateway\n(External Secure API Handshake)', color='#16A34A', penwidth='2')
    dot.edge('RAM_VENV', 'DISK_FS', 'OS Kernel Disk System I/O operations\n(POSIX Read/Write system commands)', color='#475569')

    dot.render('./diagrams/04_physical_deployment', format='png', cleanup=True)
    print("✅ Successfully generated: ./diagrams/04_physical_deployment.png")


if __name__ == "__main__":
    print("🚀 Compiling automated multi-view AI system architecture diagrams suite...")
    print("="*80)
    create_ai_orchestration_diagram()
    print("-"*80)
    create_uml_sequence_diagram()
    print("-"*80)
    create_c4_component_diagram()
    print("-"*80)
    create_physical_deployment_diagram()
    print("="*80)
    print("🎉 All architectural views compiled successfully. Look inside the './diagrams/' folder! 🏁\n")