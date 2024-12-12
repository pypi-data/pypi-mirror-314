import time
from typing import Dict, List, Optional, Tuple, Callable, Any
import psutil
import json
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass

@dataclass
class PerformanceMetric:
    timestamp: float
    cpu_usage: float
    memory_usage: float
    response_time: float


class PerformanceMonitor:
    """Monitor and analyze application performance"""

    def __init__(self, application):
        self.application = application
        self.metrics: List[PerformanceMetric] = []
        self.start_time = time.time()
        self.is_monitoring = False

    def start_monitoring(self, interval: float = 1.0):
        """Start collecting performance metrics
        
        Args:
            interval: Time between metric collections in seconds
        """
        self.start_time = time.time()
        self.metrics.clear()
        self.is_monitoring = True
        
        # Start collecting metrics
        self.record_metric()
        
        # Schedule next metric collection if interval is specified
        if interval > 0:
            def collect_metrics():
                while self.is_monitoring:
                    time.sleep(interval)
                    self.record_metric()
            
            import threading
            self.monitor_thread = threading.Thread(target=collect_metrics)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()

    def record_metric(self, response_time: float = 0.0):
        """Record current performance metrics"""
        if self.application.is_running() and self.is_monitoring:
            self.metrics.append(PerformanceMetric(
                timestamp=time.time() - self.start_time,
                cpu_usage=self.get_cpu_usage(),
                memory_usage=self.get_memory_usage(),
                response_time=response_time
            ))

    def get_average_metrics(self) -> Dict[str, float]:
        """Get average performance metrics"""
        if not self.metrics:
            return {
                'cpu_usage': 0,
                'memory_usage': 0,
                'response_time': 0,
                'duration': time.time() - self.start_time
            }

        return {
            'cpu_usage': sum(m.cpu_usage for m in self.metrics) / len(self.metrics),
            'memory_usage': sum(m.memory_usage for m in self.metrics) / len(self.metrics),
            'response_time': sum(m.response_time for m in self.metrics) / len(self.metrics),
            'duration': time.time() - self.start_time
        }

    def get_metrics_history(self) -> Dict[str, List[float]]:
        """Get history of all recorded metrics"""
        if not self.metrics:
            return {
                'cpu_usage_history': [],
                'memory_usage_history': [],
                'response_time_history': [],
                'timestamps': []
            }
            
        return {
            'cpu_usage_history': [m.cpu_usage for m in self.metrics],
            'memory_usage_history': [m.memory_usage for m in self.metrics],
            'response_time_history': [m.response_time for m in self.metrics],
            'timestamps': [m.timestamp for m in self.metrics]
        }

    def stop_monitoring(self) -> Dict[str, Any]:
        """Stop monitoring and return metrics
        
        Returns:
            Dictionary containing:
            - Average metrics (cpu_usage, memory_usage, response_time)
            - Duration of monitoring session
            - History metrics (cpu_usage_history, memory_usage_history, etc.)
        """
        self.is_monitoring = False
        metrics = self.get_average_metrics()
        history = self.get_metrics_history()
        return {**metrics, **history}

    def get_cpu_usage(self) -> float:
        """Get current CPU usage percentage"""
        try:
            return self.application.cpu_percent()
        except (psutil.NoSuchProcess, AttributeError):
            return 0.0

    def get_memory_usage(self) -> int:
        """Get current memory usage in bytes"""
        try:
            return self.application.memory_info().rss
        except (psutil.NoSuchProcess, AttributeError):
            return 0

    def collect_metrics(self) -> Dict[str, Any]:
        """Collect all performance metrics"""
        metrics = {
            'cpu_usage': self.get_cpu_usage(),
            'memory_usage': self.get_memory_usage(),
            'timestamp': time.time()
        }
        return metrics

    def measure_response_time(self, action: Callable) -> float:
        """Measure response time of an action"""
        start_time = time.time()
        action()
        return time.time() - start_time

    def measure_operation_time(self, operation: Callable) -> Tuple[Any, float]:
        """Measure execution time of an operation"""
        start_time = time.time()
        result = operation()
        duration = time.time() - start_time
        return result, duration

    def check_thresholds(self, metrics: Dict[str, float], thresholds: Dict[str, float]) -> List[str]:
        """Check if metrics exceed specified thresholds"""
        violations = []
        for key, value in metrics.items():
            if value > thresholds.get(key, float('inf')):
                violations.append(f"{key} exceeds threshold")
        return violations

    def generate_report(self, output_path: str):
        """Generate HTML performance report"""
        if not self.metrics:
            return
            
        # Extract metrics for plotting
        timestamps = [m.timestamp - self.start_time for m in self.metrics]
        cpu_usage = [m.cpu_usage for m in self.metrics]
        memory_usage = [m.memory_usage / (1024 * 1024) for m in self.metrics]  # Convert to MB
        
        # Create plots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # CPU Usage plot
        ax1.plot(timestamps, cpu_usage, 'b-')
        ax1.set_title('CPU Usage Over Time')
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('CPU Usage (%)')
        
        # Memory Usage plot
        ax2.plot(timestamps, memory_usage, 'r-')
        ax2.set_title('Memory Usage Over Time')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Memory Usage (MB)')
        
        plt.tight_layout()
        
        # Save plots
        plot_path = str(Path(output_path).with_suffix('.png'))
        plt.savefig(plot_path)
        plt.close()
        
        # Generate HTML report
        html_content = f"""
        <html>
        <head>
            <title>Performance Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                .metrics {{ margin: 20px 0; }}
                img {{ max-width: 100%; }}
            </style>
        </head>
        <body>
            <h1>Performance Report</h1>
            <div class="metrics">
                <h2>Summary</h2>
                <p>Duration: {timestamps[-1]:.2f} seconds</p>
                <p>Average CPU Usage: {np.mean(cpu_usage):.1f}%</p>
                <p>Average Memory Usage: {np.mean(memory_usage):.1f} MB</p>
                <p>Peak CPU Usage: {max(cpu_usage):.1f}%</p>
                <p>Peak Memory Usage: {max(memory_usage):.1f} MB</p>
            </div>
            <div class="plots">
                <h2>Performance Graphs</h2>
                <img src="{plot_path}" alt="Performance Graphs">
            </div>
        </body>
        </html>
        """
        
        with open(output_path, 'w') as f:
            f.write(html_content)


class PerformanceTest:
    """Class for running performance tests"""

    def __init__(self, application):
        self.application = application
        self.monitor = PerformanceMonitor(application)

    def measure_action(self, action: Callable, name: str = None,
                      warmup_runs: int = 1, test_runs: int = 5) -> Dict[str, float]:
        """Measure performance of a specific action"""
        # Warmup runs
        for _ in range(warmup_runs):
            action()

        # Test runs
        times = []
        for _ in range(test_runs):
            start_time = time.time()
            action()
            end_time = time.time()
            times.append(end_time - start_time)
            self.monitor.record_metric(response_time=times[-1])

        return {
            'name': name or action.__name__,
            'min_time': min(times),
            'max_time': max(times),
            'avg_time': sum(times) / len(times),
            'std_dev': np.std(times)
        }

    def stress_test(self, action: Callable, duration: int = 60,
                   interval: float = 0.1) -> Dict[str, float]:
        """Run stress test for specified duration"""
        self.monitor.start_monitoring()
        end_time = time.time() + duration
        action_count = 0
        errors = 0

        while time.time() < end_time:
            try:
                start_time = time.time()
                action()
                self.monitor.record_metric(response_time=time.time() - start_time)
                action_count += 1
            except Exception:
                errors += 1
            time.sleep(interval)

        return {
            'duration': duration,
            'actions_performed': action_count,
            'errors': errors,
            'actions_per_second': action_count / duration,
            'error_rate': errors / action_count if action_count > 0 else 0,
            **self.monitor.get_average_metrics()
        }

    def memory_leak_test(self, action: Callable, iterations: int = 100,
                        threshold_mb: float = 10.0) -> Dict[str, bool]:
        """Test for memory leaks"""
        initial_memory = self.application.get_memory_usage()
        memory_usage = []

        for _ in range(iterations):
            action()
            current_memory = self.application.get_memory_usage()
            memory_usage.append(current_memory)
            self.monitor.record_metric()

        # Analyze memory growth
        memory_growth = memory_usage[-1] - initial_memory
        linear_growth = np.polyfit(range(len(memory_usage)), memory_usage, 1)[0]

        return {
            'has_leak': memory_growth > threshold_mb and linear_growth > 0,
            'memory_growth_mb': memory_growth,
            'growth_rate_mb_per_iteration': linear_growth,
            'initial_memory_mb': initial_memory,
            'final_memory_mb': memory_usage[-1]
        }
