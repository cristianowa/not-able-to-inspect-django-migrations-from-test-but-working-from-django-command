# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.db.migrations.loader import MigrationLoader


class MigrationHelper:
    def get_children(self, node, app):
        app_nodes = filter(lambda nd: nd[0] == app,
               self.migration_loader.graph.node_map[
                   node].children)
        return [tuple(n) for n in app_nodes]

    def get_app_migrations(self, node, app):
        children_nodes = tuple(tuple(n) for n in filter(lambda node: node[0] == app,
                                                        self.migration_loader.graph.node_map[
                                                            node].children))
        processed_nodes = {node}
        while children_nodes:
            new_children_nodes = []
            for children_node in children_nodes:
                processed_nodes.add(children_node)
                new_children_nodes.extend(self.get_children(children_node, app))
            children_nodes = new_children_nodes
        return processed_nodes

    def get_migrations_without_children(self, migrations, app):
        result = set()
        for migration in migrations:
            if not self.get_children(migration, app):
                result.add(migration)
        return result

    def __init__(self):
        self.migration_loader = MigrationLoader(None)
        self.migration_loader.build_graph()

    def get_leaf_nodes_count_by_app(self):
        result = {}
        for root_node in self.migration_loader.graph.root_nodes():
            app_name = root_node[0]
            migrations = self.get_app_migrations(root_node, app_name)
            childless_migrations = self.get_migrations_without_children(migrations, app_name)
            result[app_name] = len(childless_migrations)
        return result


def test_multiple_leaf_nodes_in_migration_graph():
    migration_helper = MigrationHelper()
    print(migration_helper.migration_loader.graph.nodes)
    nodes = migration_helper.get_leaf_nodes_count_by_app()
    print(nodes)
    for app, count in nodes.items():
        print(app, count)
        assert count == 1, "Conflicting migrations detected; multiple leaf nodes in " + app