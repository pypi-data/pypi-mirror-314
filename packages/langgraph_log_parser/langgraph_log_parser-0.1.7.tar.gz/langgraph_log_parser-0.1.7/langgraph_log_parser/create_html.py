import json
from pathlib import Path
import base64
import jinja2
from typing import Any, Dict, List
import webbrowser


class _MetricsFormatter:
    HTML_ARROW = " &rarr; "

    @staticmethod
    def format_time(seconds: float) -> str:
        """Format time in seconds to a readable string."""
        if seconds < 0.1:
            return f"{seconds * 1000:.2f} ms"
        return f"{seconds:.2f} s"

    @staticmethod
    def format_count(value: int) -> str:
        """Format count with a thousand separators."""
        return f"{value:,}"

    @staticmethod
    def format_sequences(sequences: Dict[str, list]) -> Dict[str, Any]:
        """Format sequences into a more readable structure."""
        return {
            f"Sequence {seq_id}": {
                "steps": len(steps),
                "path": _MetricsFormatter.HTML_ARROW.join(steps)
            }
            for seq_id, steps in sequences.items()
        }

    @staticmethod
    def format_sequences_with_probabilities(sequences: List) -> Dict[str, Any]:
        """Format sequences with probabilities into a readable structure."""
        return {
            f"Sequence {seq_id}": {
                "steps": len(sequence),
                "probability": f"{probability * 100:.1f}%",
                "path": _MetricsFormatter.HTML_ARROW.join(sequence)
            }
            for seq_id, sequence, probability in sequences
        }

    @staticmethod
    def format_self_distances(distances: Dict[str, Dict[str, int]]) -> Dict[str, Any]:
        """Format self distances into a more readable structure."""
        return {
            f"Sequence {seq_id}": {
                activity: f"{distance} steps"
                for activity, distance in activities.items()
            }
            for seq_id, activities in distances.items()
        }

    @staticmethod
    def format_activities_count(counts: Dict[str, int]) -> Dict[str, str]:
        """Format activity counts with percentage of total."""
        total = sum(counts.values())
        return {
            activity: f"{count:,} ({(count / total) * 100:.1f}%)"
            for activity, count in counts.items()
        }

    @staticmethod
    def format_rework_counts(counts: Dict[str, int]) -> str | dict[str, str]:
        """Format rework counts with percentages of total activities."""
        if not counts:
            return "No reworks"

        # Get activities count from context
        activities_count = _MetricsFormatter._context.get('activities_count', {})

        result = {}
        for activity, rework_count in counts.items():
            total_activity_count = activities_count.get(activity, 0)
            if total_activity_count > 0:
                percentage = (rework_count / total_activity_count) * 100
                result[activity] = f"{_MetricsFormatter.format_count(rework_count)} ({percentage:.1f}% of activity)"
            else:
                result[activity] = f"{_MetricsFormatter.format_count(rework_count)}"

        return result

    @staticmethod
    def format_metric(key: str, value: Any) -> Any:
        """Format a metric based on its key and value type."""
        if isinstance(value, dict):
            formatters = {
                "sequences": _MetricsFormatter.format_sequences,
                "minimum_self_distances": _MetricsFormatter.format_self_distances,
                "activities_count": _MetricsFormatter.format_activities_count,
                "cases_durations": lambda v: {case: _MetricsFormatter.format_time(duration)
                                              for case, duration in v.items()},
                "activities_mean_service_time": lambda v: {activity: _MetricsFormatter.format_time(duration)
                                                           for activity, duration in v.items()},
                "rework_counts": _MetricsFormatter.format_rework_counts,
                "avg_case_duration": lambda v: _MetricsFormatter.format_time(v) if isinstance(v, (int, float)) else v
            }
            return formatters.get(key, lambda x: x)(value)
        elif isinstance(value, list) and key == "sequences_with_probabilities":
            return _MetricsFormatter.format_sequences_with_probabilities(value)
        elif key == "avg_case_duration" and isinstance(value, (int, float)):
            return _MetricsFormatter.format_time(value)
        return value

    # Class variable to store the context
    _context = {}

    @classmethod
    def set_context(cls, report_data: Dict):
        """Set the context for formatting metrics."""
        cls._context = report_data


class _ArchitectureComparisonReport:
    DEFAULT_EXPERIMENTS_DIR = "experiments"

    def __init__(self, infrastructures, base_dir=None):
        self.base_dir = Path(base_dir) if base_dir else None
        self.base_paths = []
        self.infrastructures = infrastructures

        for infra in infrastructures:
            infra_path = Path(infra)

            # If it's just a name (no parent directory) and no base_dir was specified,
            # assume it's under the experiments directory
            if not infra_path.parent.name and not self.base_dir:
                self.base_paths.append(Path(self.DEFAULT_EXPERIMENTS_DIR) / infra_path)
            # If base_dir was specified, use it
            elif self.base_dir:
                self.base_paths.append(self.base_dir / infra_path)
            # Otherwise, use the path as-is
            else:
                self.base_paths.append(infra_path)

        self.infrastructures_data = {}
        self.images_data = {}
        self.report_dir = Path("comparison_reports")
        self.formatter = _MetricsFormatter()

    def generate_report_filename(self) -> str:
        """Generate a filename for the report based on compared infrastructures."""
        # Get infrastructure names without path
        infra_names = [Path(infra).name for infra in self.infrastructures]
        # Join with 'vs' and add .html extension
        return f"{'_vs_'.join(infra_names)}.html"

    def load_data(self):
        for base_path in self.base_paths:
            infra_name = base_path.name
            self.infrastructures_data[infra_name] = {}
            self.images_data[infra_name] = {}

            # Load report data
            report_path = base_path / "reports" / "all" / "report.json"
            with open(report_path) as f:
                report_data = json.load(f)
                # Set the context before formatting
                _MetricsFormatter.set_context(report_data)
                self.infrastructures_data[infra_name]['main_report'] = {
                    key: self.formatter.format_metric(key, value)
                    for key, value in report_data.items()
                }

            # Load images
            img_path = base_path / "img"
            for img_file in img_path.glob("*.png"):
                with open(img_file, 'rb') as f:
                    self.images_data[infra_name][img_file.stem] = base64.b64encode(f.read()).decode('utf-8')

    def generate_report(self, open_browser: bool = True):
        self.report_dir.mkdir(exist_ok=True)

        first_infra = next(iter(self.infrastructures_data))
        metrics_comparison = {
            metric: [self.infrastructures_data[infra]['main_report'].get(metric)
                     for infra in self.infrastructures_data]
            for metric in self.infrastructures_data[first_infra]['main_report']
        }

        template = self.get_template()
        html_content = template.render(
            infrastructures_data=self.infrastructures_data,
            images_data=self.images_data,
            metrics_comparison=metrics_comparison
        )

        report_filename = self.generate_report_filename()
        report_path = self.report_dir / report_filename

        with open(report_path, 'w') as f:
            f.write(html_content)

        print(f"Report generated at {report_path}")

        if open_browser:
            # Convert to absolute path and file URI format
            file_uri = f"file://{report_path.resolve().as_posix()}"
            webbrowser.open(file_uri)

    @staticmethod
    def get_template():
        """Load the HTML template from file."""
        current_dir = Path(__file__).parent
        template_path = current_dir / "templates" / "comparison_report.html"

        # Create Jinja environment with the template directory
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_path.parent),
            autoescape=True
        )

        return env.get_template("comparison_report.html")


def compare(infrastructures: list) -> None:
    """
    Generate and open HTML comparison report comparing multi-agent infrastructures.

    :param infrastructures: List of infrastructures to compare.
    :type infrastructures: list

    **Example:**

    .. code-block:: python

        # List the experiments you would like to compare
        infrastructures = ["test_1", "test_2"]

        # Run the function to generate comparison report
        compare(infrastructures)

        # Output:
        # Report generated at comparison_reports/test_1_vs_test_2.html

    """
    report_generator = _ArchitectureComparisonReport(infrastructures)
    report_generator.load_data()
    report_generator.generate_report()
