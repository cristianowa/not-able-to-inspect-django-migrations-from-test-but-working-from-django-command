# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys

from django.core.management.base import BaseCommand

from django.db.migrations.loader import MigrationLoader


class Command(BaseCommand):
    help = "Check migrations"

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

    def handle(self, *args, **options):
        self.migration_loader = MigrationLoader(None)
        self.migration_loader.build_graph()
        error = False
        for root_node in self.migration_loader.graph.root_nodes():
            app_name = root_node[0]
            print(app_name, root_node[0])
            migrations = self.get_app_migrations(root_node, app_name)
            leafs = self.get_migrations_without_children(migrations, app_name)
            leaf_count = len(leafs)
            print(app_name, "Migrations:", len(migrations), "Leafs:", print(leaf_count))
            if leaf_count > 1:
                print("Problem found!")
                error = True
            print("------------------")
        sys.exit(error)