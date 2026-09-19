#!/usr/bin/env python3

from graphlib import TopologicalSorter
from reference import Reference 
from typing import Any
from dataclasses import replace, is_dataclass, fields

def collect_dependencies(node) -> set[str]:
    deps = set()
    if isinstance(node, Reference):
        deps.add(node.target)
        for op, op_type, *rest in node.history:
            for node in rest:
                deps.update(collect_dependencies(rest))
    elif isinstance(node, dict):
        for v in node.values():
            deps.update(collect_dependencies(v))
    elif isinstance(node, (list, tuple, set)):
        for item in node:
            deps.update(collect_dependencies(item))
    elif is_dataclass(node):
        for field in fields(node):
            val = getattr(node, field.name)
            deps.update(collect_dependencies(val))
            
    return deps

def resolve_nested_structure(node, pool: dict, current_path: list[str] = None) -> Any:
    if current_path is None:
        current_path = []

    if isinstance(node, Reference):
        if not node.path and not node.history:
            return pool.get(node.target)
        else:
            return node.resolve(pool)
    elif hasattr(node, "resolve"):
        return node.resolve(pool)
    elif isinstance(node, dict):
        resolved_dict = {}
        for k, v in node.items():
            new_path = current_path + [k]
            
            pool_key = ".".join(new_path)
            if pool_key in pool:
                resolved_dict[k] = pool[pool_key]
            else:
                resolved_dict[k] = resolve_nested_structure(v, pool, new_path)
        return resolved_dict
    elif isinstance(node, (list, tuple, set)):
        resolved_list = [
            resolve_nested_structure(
                item, pool, current_path
            ) for item in node
        ]
        return type(node)(resolved_list)
    elif is_dataclass(node):
        changes = {}
        for field in fields(node):
            val = getattr(node, field.name)
            changes[field.name] = resolve_nested_structure(val, pool)
        return replace(node, **changes)

    return node

def flatten_data(data):
    flat_data = {}
    for section_key, section_dict in data.items():
        for element_key, value in section_dict.items():
            full_key = f"{section_key}.{element_key}"
            flat_data[full_key] = value
    return flat_data

def resolve_dependencies(data):
    flat_data = flatten_data(data)

    ts = TopologicalSorter()
    
    for full_key, value in flat_data.items():
        deps = collect_dependencies(value)
        ts.add(full_key, *deps)

    pool = {}
    ts.prepare()
    while ts.is_active():
        for r in ts.get_ready():
            if isinstance(flat_data[r], Reference):
                pool[r] = flat_data[r].resolve(pool)
            else:
                pool[r] = resolve_nested_structure(flat_data[r], pool)
                
            ts.done(r)

    return resolve_nested_structure(data, pool)

