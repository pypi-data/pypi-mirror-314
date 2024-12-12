__all__ = ['starlake_dependencies', 'starlake_schedules', 'starlake_orchestration']

from .starlake_dependencies import StarlakeDependencies, StarlakeDependency, StarlakeDependencyType

from .starlake_schedules import StarlakeSchedules, StarlakeSchedule, StarlakeDomain, StarlakeTable

from .starlake_orchestration import AbstractDependency, AbstractTask, AbstractTaskGroup, AbstractPipeline, AbstractOrchestration, OrchestrationFactory, TaskGroupContext

import os
import importlib
import inspect

def register_orchestrations_from_package(package_name: str = "ai.starlake") -> None:
    """
    Dynamically load all classes implementing AbstractOrchestration from the given root package, including sub-packages,
    and register them in the OrchestrationRegistry.
    """
    print(f"Registering orchestrations from package {package_name}")
    package = importlib.import_module(package_name)
    package_path = os.path.dirname(package.__file__)

    for root, dirs, files in os.walk(package_path):
        # Convert the filesystem path back to a Python module path
        relative_path = os.path.relpath(root, package_path)
        if relative_path == ".":
            module_prefix = package_name
        else:
            module_prefix = f"{package_name}.{relative_path.replace(os.path.sep, '.')}"

        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                module_name = os.path.splitext(file)[0]
                full_module_name = f"{module_prefix}.{module_name}"

                try:
                    module = importlib.import_module(full_module_name)
                except ImportError as e:
                    print(f"Failed to import module {full_module_name}: {e}")
                    continue
                except AttributeError as e:
                    print(f"Failed to import module {full_module_name}: {e}")
                    continue

                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, AbstractOrchestration) and obj is not AbstractOrchestration:
                        OrchestrationFactory.register_orchestration(obj)

#FIXME register_orchestrations_from_package()
