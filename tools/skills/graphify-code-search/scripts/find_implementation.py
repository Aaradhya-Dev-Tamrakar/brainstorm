#!/usr/bin/env python3
"""
find_implementation.py — Blazing fast implementation search engine powered by Graphify.

Enables developers and AI coding agents to instantly locate function and class definitions,
inspect caller/callee relationships, extract live code snippets, and trace dependency paths
across a repository using graphify-out/graph.json.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import sys
from collections import deque
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Ensure safe UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    @classmethod
    def disable(cls):
        for attr in dir(cls):
            if not attr.startswith("_") and isinstance(getattr(cls, attr), str):
                setattr(cls, attr, "")


def find_graph_path(start_path: Optional[str] = None) -> Optional[Path]:
    """Find graphify-out/graph.json starting at start_path and walking upwards."""
    curr = Path(start_path or os.getcwd()).resolve()
    for parent in [curr] + list(curr.parents):
        candidate = parent / "graphify-out" / "graph.json"
        if candidate.is_file():
            return candidate
        if (parent / ".git").exists() and parent != curr:
            break
    return None


def parse_line_number(loc: Any) -> Optional[int]:
    """Parse 'L72', '72', 'L72-L85', or integer into an integer line number."""
    if loc is None:
        return None
    if isinstance(loc, int):
        return loc
    s = str(loc).strip()
    m = re.search(r"(\d+)", s)
    return int(m.group(1)) if m else None


def extract_code_snippet(file_path: Path, start_line: Optional[int], count: int = 20) -> List[Tuple[int, str]]:
    """Extract snippet lines from file around start_line."""
    if not file_path.is_file() or not start_line or start_line < 1:
        return []
    try:
        lines = file_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return []

    total = len(lines)
    if start_line > total:
        return []

    idx_start = max(0, start_line - 1)
    idx_end = min(total, idx_start + count)

    return [(i + 1, lines[i]) for i in range(idx_start, idx_end)]


class GraphIndex:
    def __init__(self, graph_path: Path):
        self.graph_path = graph_path
        self.root_dir = graph_path.parent.parent.resolve()
        self.data: Dict[str, Any] = {}
        self.nodes: List[Dict[str, Any]] = []
        self.nodes_by_id: Dict[str, Dict[str, Any]] = {}
        self.incoming_edges: Dict[str, List[Dict[str, Any]]] = {}
        self.outgoing_edges: Dict[str, List[Dict[str, Any]]] = {}
        self._load()

    def _load(self):
        with open(self.graph_path, "r", encoding="utf-8", errors="replace") as f:
            self.data = json.load(f)

        self.nodes = self.data.get("nodes", [])
        for n in self.nodes:
            nid = n.get("id")
            if nid:
                self.nodes_by_id[nid] = n
                self.incoming_edges[nid] = []
                self.outgoing_edges[nid] = []

        links = self.data.get("links", [])
        for link in links:
            src = link.get("source")
            tgt = link.get("target")
            if src in self.outgoing_edges:
                self.outgoing_edges[src].append(link)
            if tgt in self.incoming_edges:
                self.incoming_edges[tgt].append(link)

    def search(
        self,
        query: str,
        exact: bool = False,
        file_filter: Optional[str] = None,
        type_filter: Optional[str] = None,
        limit: int = 10,
    ) -> List[Tuple[float, Dict[str, Any]]]:
        """Search nodes by symbol name or concept with relevance ranking."""
        query_norm = query.strip().lower()
        if not query_norm:
            return []

        tokens = [t for t in re.split(r"[^\w]+", query_norm) if t]
        scored_results: List[Tuple[float, Dict[str, Any]]] = []

        for node in self.nodes:
            source_file = node.get("source_file") or ""
            if file_filter:
                if not fnmatch.fnmatch(source_file.lower(), file_filter.lower()) and file_filter.lower() not in source_file.lower():
                    continue

            if type_filter:
                node_type = (node.get("file_type") or node.get("node_kind") or node.get("type") or "").lower()
                is_callable = node.get("_callable", False)
                is_class = node.get("_callable_class", False)
                tf = type_filter.lower()
                if tf in ("func", "function") and not (is_callable and not is_class):
                    continue
                elif tf in ("class", "struct") and not is_class:
                    continue
                elif tf not in ("func", "function", "class", "struct") and tf not in node_type:
                    continue

            label = node.get("label", "")
            label_norm = (node.get("norm_label") or label).lower()
            nid = node.get("id", "").lower()

            score = 0.0

            if exact:
                if label.lower() == query_norm or label_norm == query_norm or nid == query_norm:
                    score = 200.0
                else:
                    continue
            else:
                if label_norm == query_norm:
                    score += 150.0
                elif label.lower() == query_norm:
                    score += 140.0
                elif query_norm in label_norm:
                    score += 80.0
                elif query_norm in nid:
                    score += 50.0

                matched_tokens = 0
                for token in tokens:
                    if token in label_norm:
                        score += 30.0
                        matched_tokens += 1
                    elif token in nid:
                        score += 15.0
                        matched_tokens += 1
                    elif token in source_file.lower():
                        score += 5.0
                        matched_tokens += 1

                if matched_tokens == 0 and score == 0:
                    continue

                if node.get("_callable"):
                    score += 15.0
                if node.get("_callable_class"):
                    score += 10.0

                # Prefer non-test files slightly if query doesn't mention test
                if "test" not in query_norm and ("test" in source_file.lower() or "tests/" in source_file.lower()):
                    score -= 10.0

                if any(token in Path(source_file).name.lower() for token in tokens):
                    score += 10.0

            if score > 0:
                scored_results.append((score, node))

        scored_results.sort(key=lambda x: x[0], reverse=True)
        return scored_results[:limit]

    def get_callers(self, node_id: str) -> List[Dict[str, Any]]:
        results = []
        for edge in self.incoming_edges.get(node_id, []):
            src_id = edge.get("source")
            src_node = self.nodes_by_id.get(src_id)
            if src_node:
                results.append({"node": src_node, "edge": edge})
        return results

    def get_callees(self, node_id: str) -> List[Dict[str, Any]]:
        results = []
        for edge in self.outgoing_edges.get(node_id, []):
            tgt_id = edge.get("target")
            tgt_node = self.nodes_by_id.get(tgt_id)
            if tgt_node:
                results.append({"node": tgt_node, "edge": edge})
        return results

    def shortest_path(self, start_query: str, target_query: str) -> Optional[List[Dict[str, Any]]]:
        start_matches = self.search(start_query, limit=1)
        target_matches = self.search(target_query, limit=1)

        if not start_matches or not target_matches:
            return None

        start_id = start_matches[0][1]["id"]
        target_id = target_matches[0][1]["id"]

        if start_id == target_id:
            return [{"node": self.nodes_by_id[start_id], "edge": None}]

        queue: deque = deque([(start_id, [])])
        visited: Set[str] = {start_id}

        while queue:
            curr_id, path = queue.popleft()
            curr_node = self.nodes_by_id[curr_id]

            neighbors: List[Tuple[str, Dict[str, Any], str]] = []
            for edge in self.outgoing_edges.get(curr_id, []):
                tgt = edge.get("target")
                if tgt and tgt in self.nodes_by_id:
                    neighbors.append((tgt, edge, "outgoing"))
            for edge in self.incoming_edges.get(curr_id, []):
                src = edge.get("source")
                if src and src in self.nodes_by_id:
                    neighbors.append((src, edge, "incoming"))

            for nxt_id, edge, direction in neighbors:
                if nxt_id == target_id:
                    final_path = path + [{"node": curr_node, "edge": edge, "direction": direction}]
                    final_path.append({"node": self.nodes_by_id[target_id], "edge": None})
                    return final_path

                if nxt_id not in visited and len(path) < 7:
                    visited.add(nxt_id)
                    queue.append((nxt_id, path + [{"node": curr_node, "edge": edge, "direction": direction}]))

        return None


def format_node_badge(node: Dict[str, Any]) -> str:
    if node.get("_callable_class"):
        return f"{Style.MAGENTA}[CLASS]{Style.RESET}"
    if node.get("_callable"):
        return f"{Style.CYAN}[FUNC]{Style.RESET}"
    file_type = node.get("file_type") or "symbol"
    return f"{Style.BLUE}[{file_type.upper()}]{Style.RESET}"


def print_search_results(
    index: GraphIndex,
    results: List[Tuple[float, Dict[str, Any]]],
    show_snippet: bool = False,
    snippet_lines: int = 20,
    show_callers: bool = False,
    show_callees: bool = False,
):
    if not results:
        print(f"{Style.YELLOW}No matching implementations found in graph.{Style.RESET}")
        print(f"{Style.DIM}Tip: Try broader query keywords or run graphify update.{Style.RESET}")
        return

    print(f"\n{Style.BOLD}{Style.GREEN}Found {len(results)} matching implementation(s):{Style.RESET}\n")

    for i, (score, node) in enumerate(results, 1):
        label = node.get("label", "unknown")
        src_file = node.get("source_file", "unknown")
        src_loc = node.get("source_location", "")
        badge = format_node_badge(node)
        comm_name = node.get("community_name")

        location_str = f"{src_file}:{src_loc}" if src_loc else src_file
        abs_file = index.root_dir / src_file

        print(f"{Style.BOLD}{i}. {badge} {Style.WHITE}{label}{Style.RESET} {Style.DIM}(score: {score:.1f}){Style.RESET}")
        print(f"   {Style.YELLOW}Location:{Style.RESET}   {Style.UNDERLINE}{location_str}{Style.RESET}")
        if comm_name:
            print(f"   {Style.DIM}Community:{Style.RESET}  {comm_name}")

        callers = index.get_callers(node["id"])
        callees = index.get_callees(node["id"])
        print(f"   {Style.DIM}Relations:{Style.RESET}  {len(callers)} caller(s) | {len(callees)} callee(s)")

        if show_callers and callers:
            print(f"   {Style.CYAN}Incoming Callers / References:{Style.RESET}")
            for c in callers[:5]:
                c_node = c["node"]
                c_edge = c["edge"]
                c_loc = c_edge.get("source_location") or c_node.get("source_location") or ""
                c_file = c_edge.get("source_file") or c_node.get("source_file") or ""
                rel = c_edge.get("relation", "calls")
                print(f"     <- ({rel}) {Style.BOLD}{c_node.get('label')}{Style.RESET} in {c_file}:{c_loc}")

        if show_callees and callees:
            print(f"   {Style.MAGENTA}Outgoing Callees / Dependencies:{Style.RESET}")
            for c in callees[:5]:
                c_node = c["node"]
                c_edge = c["edge"]
                rel = c_edge.get("relation", "calls")
                c_loc = c_node.get("source_location") or ""
                c_file = c_node.get("source_file") or ""
                print(f"     -> ({rel}) {Style.BOLD}{c_node.get('label')}{Style.RESET} in {c_file}:{c_loc}")

        if show_snippet:
            line_no = parse_line_number(src_loc)
            if line_no and abs_file.is_file():
                snippet = extract_code_snippet(abs_file, line_no, count=snippet_lines)
                if snippet:
                    print(f"\n   {Style.DIM}--- Code Preview ({src_file}:{line_no}) ---{Style.RESET}")
                    for lno, line_content in snippet:
                        prefix = f"{Style.GREEN}>{Style.RESET}" if lno == line_no else " "
                        print(f"   {prefix} {Style.DIM}{lno:4d} |{Style.RESET} {line_content}")
                    print(f"   {Style.DIM}---------------------------------------------{Style.RESET}\n")
        print()


def run_callers_command(index: GraphIndex, symbol: str, file_filter: Optional[str] = None, limit: int = 15):
    matches = index.search(symbol, exact=False, file_filter=file_filter, limit=3)
    if not matches:
        print(f"{Style.YELLOW}Symbol '{symbol}' not found in knowledge graph.{Style.RESET}")
        return

    for score, node in matches:
        callers = index.get_callers(node["id"])
        print(f"\n{Style.BOLD}Callers & Usages for {Style.CYAN}{node.get('label')}{Style.RESET}:")
        print(f"Defined in: {Style.UNDERLINE}{node.get('source_file')}:{node.get('source_location')}{Style.RESET}")

        if not callers:
            print(f"  {Style.DIM}(No incoming callers recorded in graph){Style.RESET}\n")
            continue

        for i, c in enumerate(callers[:limit], 1):
            c_node = c["node"]
            c_edge = c["edge"]
            rel = c_edge.get("relation", "calls")
            c_loc = c_edge.get("source_location") or c_node.get("source_location") or ""
            c_file = c_edge.get("source_file") or c_node.get("source_file") or ""
            badge = format_node_badge(c_node)
            print(f"  {i:2d}. {badge} {Style.BOLD}{c_node.get('label')}{Style.RESET}")
            print(f"      Relation: {Style.GREEN}{rel}{Style.RESET} at {c_file}:{c_loc}")
        print()


def run_callees_command(index: GraphIndex, symbol: str, file_filter: Optional[str] = None, limit: int = 15):
    matches = index.search(symbol, exact=False, file_filter=file_filter, limit=3)
    if not matches:
        print(f"{Style.YELLOW}Symbol '{symbol}' not found in knowledge graph.{Style.RESET}")
        return

    for score, node in matches:
        callees = index.get_callees(node["id"])
        print(f"\n{Style.BOLD}Dependencies & Callees for {Style.MAGENTA}{node.get('label')}{Style.RESET}:")
        print(f"Defined in: {Style.UNDERLINE}{node.get('source_file')}:{node.get('source_location')}{Style.RESET}")

        if not callees:
            print(f"  {Style.DIM}(No outgoing callees recorded in graph){Style.RESET}\n")
            continue

        for i, c in enumerate(callees[:limit], 1):
            c_node = c["node"]
            c_edge = c["edge"]
            rel = c_edge.get("relation", "calls")
            c_loc = c_node.get("source_location") or ""
            c_file = c_node.get("source_file") or ""
            badge = format_node_badge(c_node)
            print(f"  {i:2d}. {badge} {Style.BOLD}{c_node.get('label')}{Style.RESET}")
            print(f"      Relation: {Style.MAGENTA}{rel}{Style.RESET} in {c_file}:{c_loc}")
        print()


def run_path_command(index: GraphIndex, start: str, target: str):
    path = index.shortest_path(start, target)
    if not path:
        print(f"{Style.YELLOW}No path found connecting '{start}' and '{target}'.{Style.RESET}\n")
        return

    print(f"\n{Style.BOLD}{Style.GREEN}Dependency / Call Path ({len(path)-1} hops):{Style.RESET}\n")
    for i, step in enumerate(path):
        node = step["node"]
        edge = step.get("edge")
        direction = step.get("direction", "outgoing")
        badge = format_node_badge(node)
        loc = f"{node.get('source_file')}:{node.get('source_location')}"

        print(f"  {i+1}. {badge} {Style.BOLD}{node.get('label')}{Style.RESET} {Style.DIM}({loc}){Style.RESET}")
        if edge and i < len(path) - 1:
            rel = edge.get("relation", "connects")
            arrow = "-->" if direction == "outgoing" else "<--"
            print(f"       | {arrow} {Style.CYAN}{rel}{Style.RESET}")
    print()


def run_explain_command(index: GraphIndex, symbol: str, file_filter: Optional[str] = None, snippet_lines: int = 15):
    matches = index.search(symbol, exact=False, file_filter=file_filter, limit=1)
    if not matches:
        print(f"{Style.YELLOW}Symbol '{symbol}' not found.{Style.RESET}\n")
        return

    node = matches[0][1]
    callers = index.get_callers(node["id"])
    callees = index.get_callees(node["id"])
    abs_file = index.root_dir / node.get("source_file", "")
    line_no = parse_line_number(node.get("source_location"))

    print(f"\n{Style.BOLD}{'='*60}{Style.RESET}")
    print(f"{Style.BOLD}Component Analysis: {Style.CYAN}{node.get('label')}{Style.RESET}")
    print(f"{Style.BOLD}{'='*60}{Style.RESET}")
    print(f"File:         {node.get('source_file')}:{node.get('source_location')}")
    print(f"Type:         {node.get('file_type')} | Callable: {node.get('_callable')} | Class: {node.get('_callable_class')}")
    if node.get("community_name"):
        print(f"Community:    {node.get('community_name')} (Cluster #{node.get('community')})")
    print(f"Connectivity: {len(callers)} caller(s), {len(callees)} callee(s)")

    if callers:
        print(f"\n{Style.BOLD}Top Callers ({min(5, len(callers))} of {len(callers)}):{Style.RESET}")
        for c in callers[:5]:
            c_node = c["node"]
            rel = c["edge"].get("relation", "calls")
            print(f"  <- [{rel}] {c_node.get('label')} ({c_node.get('source_file')})")

    if callees:
        print(f"\n{Style.BOLD}Key Dependencies ({min(5, len(callees))} of {len(callees)}):{Style.RESET}")
        for c in callees[:5]:
            c_node = c["node"]
            rel = c["edge"].get("relation", "calls")
            print(f"  -> [{rel}] {c_node.get('label')} ({c_node.get('source_file')})")

    if line_no and abs_file.is_file():
        snippet = extract_code_snippet(abs_file, line_no, count=snippet_lines)
        if snippet:
            print(f"\n{Style.BOLD}Definition Snippet:{Style.RESET}")
            for lno, content in snippet:
                prefix = f"{Style.GREEN}>{Style.RESET}" if lno == line_no else " "
                print(f"  {prefix} {Style.DIM}{lno:4d} |{Style.RESET} {content}")
    print(f"{Style.BOLD}{'='*60}{Style.RESET}\n")


def main():
    args_list = sys.argv[1:]
    command_override = None

    if args_list and args_list[0] in ("callers", "callees", "path", "explain", "search"):
        command_override = args_list.pop(0)

    parser = argparse.ArgumentParser(
        description="Search existing implementations, functions, classes, and callers using graphify knowledge graphs."
    )
    parser.add_argument("query", nargs="?", help="Symbol name or implementation query (e.g., 'decrypt', 'auth', 'initModal')")
    parser.add_argument("target", nargs="?", help="Target symbol for pathfinding mode")
    parser.add_argument("--command", choices=["search", "callers", "callees", "path", "explain"], default="search", help="Action mode")
    parser.add_argument("--symbol", "-s-name", dest="symbol", help="Target symbol for callers/callees/explain")
    parser.add_argument("--graph", "-g", dest="graph_path", help="Path to graphify-out/graph.json")
    parser.add_argument("--snippet", "-s", action="store_true", help="Display code snippet from source file")
    parser.add_argument("--lines", "-l", type=int, default=20, help="Number of code lines to show in snippet")
    parser.add_argument("--callers", action="store_true", help="Include incoming callers in search results")
    parser.add_argument("--callees", action="store_true", help="Include outgoing callees in search results")
    parser.add_argument("--file", "-f", dest="file_filter", help="Filter by file pattern (glob/substring)")
    parser.add_argument("--type", "-t", dest="type_filter", choices=["func", "function", "class", "code", "doc"], help="Filter by node type")
    parser.add_argument("--exact", "-e", action="store_true", help="Exact symbol name match only")
    parser.add_argument("--limit", "-n", type=int, default=8, help="Maximum number of search results")
    parser.add_argument("--json", action="store_true", help="Output raw JSON for agent tools")
    parser.add_argument("--no-color", action="store_true", help="Disable colorized terminal output")

    args = parser.parse_args(args_list)

    if args.no_color or not sys.stdout.isatty():
        Style.disable()

    cmd = command_override or args.command
    query = args.query or args.symbol

    graph_file = Path(args.graph_path) if args.graph_path else find_graph_path()
    if not graph_file or not graph_file.is_file():
        print(f"{Style.RED}Error: graphify-out/graph.json not found.{Style.RESET}")
        print(f"{Style.YELLOW}To build the graph, run: graphify . (or .\\sync.ps1){Style.RESET}")
        sys.exit(1)

    index = GraphIndex(graph_file)

    if args.target and query and cmd != "path":
        cmd = "path"

    if cmd == "callers":
        if not query:
            print(f"{Style.RED}Error: callers mode requires a symbol name.{Style.RESET}")
            sys.exit(1)
        run_callers_command(index, query, file_filter=args.file_filter, limit=args.limit)
    elif cmd == "callees":
        if not query:
            print(f"{Style.RED}Error: callees mode requires a symbol name.{Style.RESET}")
            sys.exit(1)
        run_callees_command(index, query, file_filter=args.file_filter, limit=args.limit)
    elif cmd == "path":
        target = args.target
        if not query or not target:
            print(f"{Style.RED}Error: path mode requires both start and target.{Style.RESET}")
            sys.exit(1)
        run_path_command(index, query, target)
    elif cmd == "explain":
        if not query:
            print(f"{Style.RED}Error: explain mode requires a symbol name.{Style.RESET}")
            sys.exit(1)
        run_explain_command(index, query, file_filter=args.file_filter, snippet_lines=args.lines)
    else:
        if not query:
            parser.print_help()
            sys.exit(0)

        results = index.search(
            query=query,
            exact=args.exact,
            file_filter=args.file_filter,
            type_filter=args.type_filter,
            limit=args.limit,
        )

        if args.json:
            output_data = []
            for score, node in results:
                src_file = node.get("source_file")
                src_loc = node.get("source_location")
                line_no = parse_line_number(src_loc)
                abs_file = index.root_dir / (src_file or "")
                snippet_text = None
                if args.snippet and line_no and abs_file.is_file():
                    snip = extract_code_snippet(abs_file, line_no, count=args.lines)
                    snippet_text = "\n".join(f"{lno:4d} | {l}" for lno, l in snip)

                output_data.append({
                    "score": score,
                    "label": node.get("label"),
                    "id": node.get("id"),
                    "source_file": src_file,
                    "source_location": src_loc,
                    "line_number": line_no,
                    "callable": node.get("_callable"),
                    "callable_class": node.get("_callable_class"),
                    "community_name": node.get("community_name"),
                    "callers_count": len(index.get_callers(node["id"])),
                    "callees_count": len(index.get_callees(node["id"])),
                    "snippet": snippet_text,
                })
            print(json.dumps(output_data, indent=2))
        else:
            print_search_results(
                index=index,
                results=results,
                show_snippet=args.snippet,
                snippet_lines=args.lines,
                show_callers=args.callers,
                show_callees=args.callees,
            )


if __name__ == "__main__":
    main()
