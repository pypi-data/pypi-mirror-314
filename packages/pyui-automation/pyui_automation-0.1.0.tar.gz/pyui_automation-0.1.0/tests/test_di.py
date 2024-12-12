import pytest
from typing import Protocol
from pyui_automation.di import Container

class IService(Protocol):
    def do_something(self) -> str:
        ...

class ServiceA:
    def do_something(self) -> str:
        return "Service A"

class ServiceB:
    def do_something(self) -> str:
        return "Service B"

@pytest.fixture
def container():
    return Container()

def test_register_resolve(container):
    """Test registering and resolving service"""
    container.register(IService, ServiceA)
    service = container.resolve(IService)
    assert isinstance(service, ServiceA)
    assert service.do_something() == "Service A"

def test_register_singleton(container):
    """Test singleton registration"""
    container.register_singleton(IService, ServiceA)
    
    service1 = container.resolve(IService)
    service2 = container.resolve(IService)
    
    assert service1 is service2
    assert isinstance(service1, ServiceA)

def test_register_factory(container):
    """Test factory registration"""
    def factory():
        return ServiceB()
    
    container.register_factory(IService, factory)
    service = container.resolve(IService)
    
    assert isinstance(service, ServiceB)
    assert service.do_something() == "Service B"

def test_resolve_unregistered(container):
    """Test resolving unregistered service"""
    with pytest.raises(KeyError):
        container.resolve(IService)

def test_multiple_registrations(container):
    """Test multiple service registrations"""
    container.register(IService, ServiceA)
    container.register(IService, ServiceB)
    
    service = container.resolve(IService)
    assert isinstance(service, ServiceB)
    assert service.do_something() == "Service B"

def test_singleton_vs_transient(container):
    """Test difference between singleton and transient registration"""
    # Singleton
    container.register_singleton(IService, ServiceA)
    singleton1 = container.resolve(IService)
    singleton2 = container.resolve(IService)
    assert singleton1 is singleton2
    
    # Transient
    container = Container()  # Reset container
    container.register(IService, ServiceA)
    transient1 = container.resolve(IService)
    transient2 = container.resolve(IService)
    assert transient1 is not transient2
