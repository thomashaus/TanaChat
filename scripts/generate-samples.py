#!/usr/bin/env python3
"""
Generate sample Tana files for testing and documentation.
"""

import json
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

# Sample data pools
WORDS = [
    "project", "task", "meeting", "idea", "note", "deadline", "goal",
    "strategy", "design", "development", "testing", "deployment",
    "review", "documentation", "research", "analysis", "report",
    "presentation", "workshop", "conference", "training", "learning"
]

PEOPLE = [
    "alice@company.com", "bob@company.com", "carol@company.com",
    "dave@company.com", "eve@company.com", "frank@company.com"
]

PROJECTS = [
    "Website Redesign", "Mobile App", "API Integration", "Database Migration",
    "Security Audit", "Performance Optimization", "UI/UX Refresh",
    "Documentation Update", "Feature Release", "Bug Sprint"
]

SUPERTAGS = [
    {"uid": "tag-project", "name": "Project"},
    {"uid": "tag-task", "name": "Task"},
    {"uid": "tag-meeting", "name": "Meeting"},
    {"uid": "tag-idea", "name": "Idea"},
    {"uid": "tag-urgent", "name": "Urgent"},
    {"uid": "tag-review", "name": "Review"},
    {"uid": "tag-blocked", "name": "Blocked"},
    {"uid": "tag-waiting", "name": "Waiting"}
]

def generate_uid() -> str:
    """Generate a unique ID."""
    return str(uuid.uuid4())[:8]

def generate_date(days_ago: int = 0) -> str:
    """Generate ISO date string."""
    date = datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 23))
    return date.isoformat() + "Z"

def create_minimal_node() -> Dict[str, Any]:
    """Create a minimal valid Tana node."""
    return {
        "uid": generate_uid(),
        "name": "Root Node",
        "created": generate_date(),
        "edited": generate_date(),
        "type": "node"
    }

def create_task_node(name: str, todo_state: str = "todo") -> Dict[str, Any]:
    """Create a task node."""
    created = generate_date(random.randint(1, 30))
    return {
        "uid": generate_uid(),
        "name": name,
        "created": created,
        "edited": generate_date(random.randint(0, 30)),
        "type": "node",
        "todoState": todo_state,
        "supertags": [random.choice(SUPERTAGS), {"uid": "tag-task", "name": "Task"}]
    }

def create_project_node(name: str) -> Dict[str, Any]:
    """Create a project node with tasks."""
    project_uid = generate_uid()
    created = generate_date(random.randint(1, 60))

    # Generate 3-7 tasks
    num_tasks = random.randint(3, 7)
    children = []

    for i in range(num_tasks):
        task_name = f"Task {i+1}: {random.choice(WORDS).title()}"
        todo_state = random.choice(["todo", "done", "todo", "done", "todo"])  # More todos
        children.append(create_task_node(task_name, todo_state))

    return {
        "uid": project_uid,
        "name": name,
        "description": f"Project for {name.lower()}",
        "created": created,
        "edited": generate_date(random.randint(0, 60)),
        "type": "node",
        "supertags": [
            {"uid": "tag-project", "name": "Project"},
            random.choice(SUPERTAGS)
        ],
        "children": children
    }

def create_meeting_node() -> Dict[str, Any]:
    """Create a meeting node with fields."""
    meeting_uid = generate_uid()
    created = generate_date(random.randint(1, 30))

    return {
        "uid": meeting_uid,
        "name": f"{random.choice(['Daily', 'Weekly', 'Monthly'])} {random.choice(['Standup', 'Review', 'Planning'])}",
        "created": created,
        "edited": generate_date(random.randint(0, 30)),
        "type": "date",
        "children": [
            {
                "uid": generate_uid(),
                "name": "Attendees",
                "type": "field",
                "children": [
                    {"uid": generate_uid(), "name": person, "type": "node"}
                    for person in random.sample(PEOPLE, random.randint(2, 4))
                ]
            },
            {
                "uid": generate_uid(),
                "name": "Notes",
                "type": "node",
                "children": [
                    {
                        "uid": generate_uid(),
                        "name": f"Discussed {random.choice(WORDS)}",
                        "type": "node"
                    }
                ]
            },
            {
                "uid": generate_uid(),
                "name": "Action Items",
                "type": "node",
                "children": [
                    create_task_node(f"Follow up on {random.choice(WORDS)}")
                ]
            }
        ]
    }

def generate_tif_file(num_nodes: int = 10) -> Dict[str, Any]:
    """Generate a complete TIF file."""
    nodes = []

    # Always start with a root node
    nodes.append({
        "uid": "root",
        "name": "Generated Workspace",
        "description": f"Auto-generated workspace with {num_nodes} nodes",
        "created": generate_date(30),
        "edited": generate_date(1),
        "type": "node"
    })

    # Add different types of nodes
    for _ in range(num_nodes - 1):
        node_type = random.choice(["project", "task", "meeting", "note"])

        if node_type == "project":
            nodes.append(create_project_node(random.choice(PROJECTS)))
        elif node_type == "task":
            nodes.append(create_task_node(f"{random.choice(WORDS).title()} Task"))
        elif node_type == "meeting":
            nodes.append(create_meeting_node())
        else:  # note
            nodes.append({
                "uid": generate_uid(),
                "name": f"Note about {random.choice(WORDS)}",
                "created": generate_date(random.randint(1, 30)),
                "edited": generate_date(random.randint(0, 30)),
                "type": "node",
                "children": [
                    {
                        "uid": generate_uid(),
                        "name": f"Detail: {random.choice(WORDS)}",
                        "type": "node"
                    }
                ]
            })

    # Calculate summary
    total_nodes = len(nodes)
    calendar_nodes = sum(1 for node in nodes if node.get("type") == "date")
    todo_nodes = sum(1 for node in nodes if node.get("todoState"))

    return {
        "version": "TanaIntermediateFile V0.1",
        "summary": {
            "leafNodes": total_nodes,
            "topLevelNodes": total_nodes,
            "totalNodes": total_nodes,
            "calendarNodes": calendar_nodes,
            "fields": random.randint(5, 15),
            "brokenRefs": 0
        },
        "nodes": nodes
    }

def generate_large_file(num_nodes: int = 1000) -> Dict[str, Any]:
    """Generate a large TIF file for performance testing."""
    print(f"Generating large file with {num_nodes} nodes...")

    nodes = []
    nodes.append({
        "uid": "root",
        "name": "Large Test Workspace",
        "description": f"Performance test file with {num_nodes} nodes",
        "created": generate_date(365),
        "edited": generate_date(1),
        "type": "node"
    })

    # Create a hierarchical structure
    for i in range(1, num_nodes):
        if i % 100 == 0:
            print(f"  Generated {i}/{num_nodes} nodes...")

        node = {
            "uid": f"node_{i:05d}",
            "name": f"Test Node {i}",
            "created": generate_date(random.randint(1, 365)),
            "edited": generate_date(random.randint(0, 365)),
            "type": random.choice(["node", "date", "url"])
        }

        # Add children for some nodes
        if i % 3 == 0 and i < num_nodes - 1:
            node["children"] = [
                {
                    "uid": f"child_{i:05d}_1",
                    "name": f"Child {i}.1",
                    "created": generate_date(random.randint(1, 365)),
                    "edited": generate_date(random.randint(0, 365)),
                    "type": "node"
                }
            ]

        nodes.append(node)

    return {
        "version": "TanaIntermediateFile V0.1",
        "nodes": nodes
    }

def main():
    """Main generation script."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate Tana sample files")
    parser.add_argument("--type", choices=["small", "medium", "large", "test"], default="small")
    parser.add_argument("--count", type=int, default=10, help="Number of nodes to generate")
    parser.add_argument("--output", type=str, help="Output file path")
    parser.add_argument("--test", action="store_true", help="Run in test mode (use fixed seeds)")

    args = parser.parse_args()

    if args.test:
        random.seed(42)  # For reproducible test data

    if args.type == "large":
        data = generate_large_file(1000)
        filename = "samples/tana/imports/valid/large-export.json"
    elif args.type == "medium":
        data = generate_tif_file(100)
        filename = "samples/tana/imports/valid/medium-workspace.json"
    else:  # small
        data = generate_tif_file(args.count)
        filename = args.output or "samples/tana/imports/valid/generated-small.json"

    # Ensure output directory exists
    Path(filename).parent.mkdir(parents=True, exist_ok=True)

    # Write the file
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Generated {filename}")
    print(f"  Nodes: {len(data['nodes'])}")
    if "summary" in data:
        print(f"  Summary: {data['summary']}")

if __name__ == "__main__":
    main()