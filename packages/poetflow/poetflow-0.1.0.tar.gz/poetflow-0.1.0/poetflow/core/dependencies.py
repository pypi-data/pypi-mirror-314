"""Dependency management module."""

from typing import Dict, List, Set

from poetflow.types.monorepo import MonoRepo


class DependencyManager:
    """Manages dependencies between packages."""

    def __init__(self, monorepo: MonoRepo) -> None:
        self.monorepo = monorepo
        self._dependency_graph: Dict[str, Set[str]] = {}
        self._build_dependency_graph()

    def _build_dependency_graph(self) -> None:
        """Build dependency graph from packages."""
        for package in self.monorepo.packages:
            info = self.monorepo.get_package_info(package)
            if info:
                self._dependency_graph[package] = set(info.get("dependencies", []))

    def get_dependencies(self, package: str) -> Set[str]:
        """Get direct dependencies of a package

        Args:
            package: Package name

        Returns:
            Set of package names
        """
        return self._dependency_graph.get(package, set())

    def get_all_dependents(self, package: str) -> Set[str]:
        """Get all packages that depend on this package."""
        dependents: Set[str] = set()
        for pkg, deps in self._dependency_graph.items():
            if package in deps:
                dependents.add(pkg)
                dependents.update(self.get_all_dependents(pkg))
        return dependents

    def get_build_order(self) -> List[str]:
        """Get packages in dependency order."""
        visited: Set[str] = set()
        order: List[str] = []

        def visit(pkg: str) -> None:
            if pkg in visited:
                return
            visited.add(pkg)
            for dep in self._dependency_graph.get(pkg, set()):
                visit(dep)
            order.append(pkg)

        for package in self.monorepo.packages:
            visit(package)

        return order

    def get_affected_packages(self) -> Set[str]:
        """Get packages affected by changes."""
        affected: Set[str] = set()
        for package in self.monorepo.packages:
            affected.add(package)
        return affected
