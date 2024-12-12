from typing import Dict, Any, Type, Optional, TypeVar, Generic

T = TypeVar('T')

class Container:
    """Dependency injection container"""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Any] = {}
        self._singletons: Dict[str, Any] = {}

    def register(self, interface: Type[T], implementation: Type[T]) -> None:
        """Register transient service"""
        self._services[interface.__name__] = implementation

    def register_singleton(self, interface: Type[T], implementation: Type[T]) -> None:
        """Register singleton service"""
        self._services[interface.__name__] = implementation
        self._singletons[interface.__name__] = None

    def register_factory(self, interface: Type[T], factory: Any) -> None:
        """Register factory"""
        self._factories[interface.__name__] = factory

    def resolve(self, interface: Type[T]) -> Optional[T]:
        """Resolve service"""
        name = interface.__name__

        # Check if singleton instance exists
        if name in self._singletons:
            if self._singletons[name] is None:
                self._singletons[name] = self._create_instance(name)
            return self._singletons[name]

        # Check if factory exists
        if name in self._factories:
            return self._factories[name]()

        # Create new instance
        return self._create_instance(name)

    def _create_instance(self, name: str) -> Any:
        """Create instance of service"""
        if name not in self._services:
            raise KeyError(f"No registration found for {name}")

        implementation = self._services[name]
        return implementation()

# Global container instance
container = Container()
