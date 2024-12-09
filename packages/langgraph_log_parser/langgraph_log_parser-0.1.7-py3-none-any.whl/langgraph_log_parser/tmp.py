import json
from pathlib import Path
import base64
import jinja2
from typing import Any, Dict, List


class MetricsFormatter:
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
                "path": MetricsFormatter.HTML_ARROW.join(steps)
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
                "path": MetricsFormatter.HTML_ARROW.join(sequence)
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
        activities_count = MetricsFormatter._context.get('activities_count', {})

        result = {}
        for activity, rework_count in counts.items():
            total_activity_count = activities_count.get(activity, 0)
            if total_activity_count > 0:
                percentage = (rework_count / total_activity_count) * 100
                result[activity] = f"{MetricsFormatter.format_count(rework_count)} ({percentage:.1f}% of activity)"
            else:
                result[activity] = f"{MetricsFormatter.format_count(rework_count)}"

        return result

    @staticmethod
    def format_metric(key: str, value: Any) -> Any:
        """Format a metric based on its key and value type."""
        if isinstance(value, dict):
            formatters = {
                "sequences": MetricsFormatter.format_sequences,
                "minimum_self_distances": MetricsFormatter.format_self_distances,
                "activities_count": MetricsFormatter.format_activities_count,
                "cases_durations": lambda v: {case: MetricsFormatter.format_time(duration)
                                              for case, duration in v.items()},
                "activities_mean_service_time": lambda v: {activity: MetricsFormatter.format_time(duration)
                                                           for activity, duration in v.items()},
                "rework_counts": MetricsFormatter.format_rework_counts,
                "avg_case_duration": lambda v: MetricsFormatter.format_time(v) if isinstance(v, (int, float)) else v
            }
            return formatters.get(key, lambda x: x)(value)
        elif isinstance(value, list) and key == "sequences_with_probabilities":
            return MetricsFormatter.format_sequences_with_probabilities(value)
        elif key == "avg_case_duration" and isinstance(value, (int, float)):
            return MetricsFormatter.format_time(value)
        return value

    # Class variable to store the context
    _context = {}

    @classmethod
    def set_context(cls, report_data: Dict):
        """Set the context for formatting metrics."""
        cls._context = report_data


class ArchitectureComparisonReport:
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
        self.formatter = MetricsFormatter()

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
                MetricsFormatter.set_context(report_data)
                self.infrastructures_data[infra_name]['main_report'] = {
                    key: self.formatter.format_metric(key, value)
                    for key, value in report_data.items()
                }

            # Load images
            img_path = base_path / "img"
            for img_file in img_path.glob("*.png"):
                with open(img_file, 'rb') as f:
                    self.images_data[infra_name][img_file.stem] = base64.b64encode(f.read()).decode('utf-8')

    def generate_report(self):
        self.report_dir.mkdir(exist_ok=True)

        first_infra = next(iter(self.infrastructures_data))
        metrics_comparison = {
            metric: [self.infrastructures_data[infra]['main_report'].get(metric)
                    for infra in self.infrastructures_data]
            for metric in self.infrastructures_data[first_infra]['main_report']
        }

        env = jinja2.Environment()
        html_content = env.from_string(self.get_template()).render(
            infrastructures_data=self.infrastructures_data,
            images_data=self.images_data,
            metrics_comparison=metrics_comparison
        )

        report_filename = self.generate_report_filename()
        report_path = self.report_dir / report_filename

        with open(report_path, 'w') as f:
            f.write(html_content)

        print(f"Report generated at {report_path}")

    @staticmethod
    def get_template():
        return """
<!DOCTYPE html>
<html>
<head>
    <title>Architecture Comparison Report</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            z-index: 1000;
        }

        .modal.show {
            display: block;
        }

        .modal-content {
            position: relative;
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: auto;
            padding: 20px;
        }

        .image-wrapper {
            min-width: min-content;
            display: inline-block;
        }

        .modal-image {
            max-height: 90vh;
            cursor: zoom-in;
            transition: transform 0.3s ease;
            transform-origin: left top;
        }

        .modal-image.zoomed {
            cursor: zoom-out;
        }

        .close-button {
            position: fixed;
            top: 15px;
            right: 35px;
            color: #f1f1f1;
            font-size: 40px;
            font-weight: bold;
            cursor: pointer;
            z-index: 1001;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        .zoom-hint {
            display: none;
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(255, 255, 255, 0.8);
            padding: 10px 20px;
            border-radius: 20px;
            color: black;
            z-index: 1001;
        }

        .modal.show .zoom-hint {
            display: block;
        }

        .metrics-table th {
            position: sticky;
            top: 0;
            background-color: #f8fafc;
            z-index: 10;
        }

        .metrics-row:nth-child(even) {
            background-color: #f8fafc;
        }

        .metrics-cell {
            max-width: 300px;
            overflow: auto;
        }
    </style>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto p-4">
        <h1 class="text-2xl font-bold mb-4">Architecture Comparison Report</h1>

        <!-- Tab Buttons -->
        <div class="mb-4">
            <button onclick="showTab('metrics')" class="px-4 py-2 bg-blue-500 text-white rounded mr-2">Metrics</button>
            <button onclick="showTab('visualizations')" class="px-4 py-2 bg-gray-200 rounded">Visualizations</button>
        </div>

        <!-- Metrics Tab -->
        <div id="metrics" class="tab-content active">
            <div class="bg-white rounded-lg shadow overflow-x-auto">
                <table class="w-full metrics-table">
                    <thead>
                        <tr>
                            <th class="px-4 py-2 text-left border-b">Metric</th>
                            {% for infra in infrastructures_data.keys() %}
                            <th class="px-4 py-2 text-left border-b">{{ infra }}</th>
                            {% endfor %}
                        </tr>
                    </thead>
                    <tbody>
                        {% for metric, values in metrics_comparison.items() %}
                        <tr class="metrics-row hover:bg-gray-50">
                            <td class="px-4 py-2 border-b font-medium">{{ metric }}</td>
                            {% for value in values %}
                            <td class="px-4 py-2 border-b metrics-cell">
                                {% if value is mapping %}
                                    {% for k, v in value.items() %}
                                    <div class="mb-2">
                                        <strong>{{ k }}:</strong>
                                        {% if v is mapping %}
                                            <div class="pl-4">
                                                {% for sub_k, sub_v in v.items() %}
                                                <div><em>{{ sub_k }}:</em> {{ sub_v }}</div>
                                                {% endfor %}
                                            </div>
                                        {% else %}
                                            {{ v }}
                                        {% endif %}
                                    </div>
                                    {% endfor %}
                                {% else %}
                                    {{ value }}
                                {% endif %}
                            </td>
                            {% endfor %}
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Visualizations Tab -->
        <div id="visualizations" class="tab-content">
            <div class="grid grid-cols-2 gap-4">
                {% for infra, images in images_data.items() %}
                <div class="bg-white p-4 rounded shadow">
                    <h2 class="text-xl font-bold mb-4">{{ infra }}</h2>
                    {% for img_name, img_data in images.items() %}
                    <div class="mb-4">
                        <h3 class="text-lg mb-2">{{ img_name }}</h3>
                        <img src="data:image/png;base64,{{ img_data }}"
                             alt="{{ img_name }}"
                             class="max-w-full cursor-pointer hover:opacity-80"
                             onclick="showImage('{{ img_data }}', '{{ img_name }}')">
                    </div>
                    {% endfor %}
                </div>
                {% endfor %}
            </div>
        </div>
    </div>

    <!-- Modal for image zoom -->
    <div id="imageModal" class="modal" onclick="handleModalClick(event)">
        <span class="close-button" onclick="hideModal()">&times;</span>
        <div class="modal-content">
            <div class="image-wrapper">
                <img id="modalImage" class="modal-image" alt="Zoomed image">
            </div>
        </div>
        <div class="zoom-hint">Click image to zoom in/out</div>
    </div>

    <script>
        let currentScale = 1;

        function showTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.getElementById(tabName).classList.add('active');
        }

        function calculateZoomLevel(img) {
            const imgWidth = img.naturalWidth;
            const imgHeight = img.naturalHeight;
            const aspectRatio = imgWidth / imgHeight;

            if (aspectRatio > 5) {
                return Math.min(8, Math.max(4, aspectRatio / 2));
            }
            return 2;
        }

        function showImage(imgData, imgName) {
            const modal = document.getElementById('imageModal');
            const modalImg = document.getElementById('modalImage');
            modal.classList.add('show');
            modalImg.src = 'data:image/png;base64,' + imgData;
            modalImg.alt = imgName;

            resetZoom();

            modalImg.onload = function() {
                currentScale = calculateZoomLevel(modalImg);
            };
        }

        function hideModal() {
            document.getElementById('imageModal').classList.remove('show');
            resetZoom();
        }

        function resetZoom() {
            const modalImg = document.getElementById('modalImage');
            modalImg.style.transform = 'scale(1)';
            modalImg.classList.remove('zoomed');
        }

        function toggleZoom(event) {
            const modalImg = document.getElementById('modalImage');
            const modalContent = document.querySelector('.modal-content');

            if (modalImg.classList.contains('zoomed')) {
                modalImg.style.transform = 'scale(1)';
                modalImg.classList.remove('zoomed');
            } else {
                modalImg.style.transform = `scale(${currentScale})`;
                modalImg.classList.add('zoomed');

                modalContent.scrollLeft = 0;
                modalContent.scrollTop = 0;
            }
            event.stopPropagation();
        }

        function handleModalClick(event) {
            if (event.target.classList.contains('modal')) {
                hideModal();
            }
        }

        document.getElementById('modalImage').addEventListener('click', toggleZoom);
    </script>
</body>
</html>
        """