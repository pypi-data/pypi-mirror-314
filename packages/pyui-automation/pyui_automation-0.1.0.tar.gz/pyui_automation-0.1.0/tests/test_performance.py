import pytest
from unittest.mock import MagicMock, patch
import time
from pyui_automation.performance import PerformanceMonitor, PerformanceMetric


@pytest.fixture
def mock_process():
    """Create a mock process for testing"""
    process = MagicMock()
    process.pid = 12345
    process.name.return_value = "test_app.exe"
    process.cpu_percent.return_value = 5.0
    process.memory_info.return_value = MagicMock(rss=1024*1024*100)  # 100MB
    return process


@pytest.fixture
def perf_monitor(mock_process):
    """Create PerformanceMonitor instance"""
    monitor = PerformanceMonitor(mock_process)
    return monitor


def test_start_monitoring(perf_monitor):
    """Test starting performance monitoring"""
    perf_monitor.start_monitoring()
    assert perf_monitor.is_monitoring
    assert perf_monitor.start_time is not None


def test_stop_monitoring(perf_monitor):
    """Test stopping performance monitoring"""
    perf_monitor.start_monitoring()
    time.sleep(0.1)  # Small delay to ensure metrics are collected
    metrics = perf_monitor.stop_monitoring()
    
    assert not perf_monitor.is_monitoring
    assert isinstance(metrics, dict)
    assert "duration" in metrics
    assert metrics["duration"] > 0


def test_get_cpu_usage(perf_monitor, mock_process):
    """Test getting CPU usage"""
    mock_process.cpu_percent.return_value = 5.0
    
    cpu_usage = perf_monitor.get_cpu_usage()
    assert isinstance(cpu_usage, float)
    assert cpu_usage == 5.0
    mock_process.cpu_percent.assert_called_once()


def test_get_memory_usage(perf_monitor, mock_process):
    """Test getting memory usage"""
    memory_size = 100 * 1024 * 1024  # 100MB
    mock_process.memory_info.return_value = MagicMock(rss=memory_size)
    
    memory_usage = perf_monitor.get_memory_usage()
    assert isinstance(memory_usage, int)
    assert memory_usage == memory_size
    mock_process.memory_info.assert_called_once()


def test_get_response_time(perf_monitor):
    """Test measuring response time"""
    with patch('time.time', side_effect=[0, 1.5]):  # Mock 1.5 second delay
        response_time = perf_monitor.measure_response_time(lambda: None)
    
    assert isinstance(response_time, float)
    assert response_time == 1.5


def test_generate_report(perf_monitor, temp_dir):
    """Test generating performance report"""
    # Add some test metrics
    perf_monitor.metrics = [
        PerformanceMetric(
            timestamp=time.time(),
            cpu_usage=5.0,
            memory_usage=100 * 1024 * 1024,  # 100MB
            response_time=0.1
        ),
        PerformanceMetric(
            timestamp=time.time() + 1,
            cpu_usage=6.0,
            memory_usage=110 * 1024 * 1024,  # 110MB
            response_time=0.2
        )
    ]
    
    report_path = temp_dir / "performance_report.html"
    perf_monitor.generate_report(str(report_path))
    
    assert report_path.exists()
    assert report_path.with_suffix('.png').exists()


def test_collect_metrics(perf_monitor, mock_process):
    """Test collecting all performance metrics"""
    mock_process.cpu_percent.return_value = 5.0
    mock_process.memory_info.return_value = MagicMock(rss=100 * 1024 * 1024)  # 100MB
    
    metrics = perf_monitor.collect_metrics()
    
    assert isinstance(metrics, dict)
    assert "cpu_usage" in metrics
    assert "memory_usage" in metrics
    assert metrics["cpu_usage"] == 5.0
    assert metrics["memory_usage"] == 100 * 1024 * 1024


def test_measure_operation_time(perf_monitor):
    """Test measuring operation execution time"""
    def test_operation():
        time.sleep(0.1)
        return "test"
    
    result, duration = perf_monitor.measure_operation_time(test_operation)
    
    assert result == "test"
    assert duration >= 0.1


def test_monitor_resource_usage(perf_monitor):
    """Test monitoring resource usage over time"""
    perf_monitor.start_monitoring()
    time.sleep(0.2)  # Collect some data points
    metrics = perf_monitor.stop_monitoring()
    
    assert "cpu_usage_history" in metrics
    assert "memory_usage_history" in metrics
    assert len(metrics["cpu_usage_history"]) > 0
    assert len(metrics["memory_usage_history"]) > 0


def test_performance_threshold_check(perf_monitor):
    """Test checking performance against thresholds"""
    metrics = {
        "cpu_usage": 50.0,
        "memory_usage": 100 * 1024 * 1024,  # 100MB
        "response_time": 0.5
    }
    
    thresholds = {
        "cpu_usage": 80.0,  # 80% CPU threshold
        "memory_usage": 200 * 1024 * 1024,  # 200MB memory threshold
        "response_time": 1.0  # 1 second response time threshold
    }
    
    violations = perf_monitor.check_thresholds(metrics, thresholds)
    assert len(violations) == 0  # No violations expected
