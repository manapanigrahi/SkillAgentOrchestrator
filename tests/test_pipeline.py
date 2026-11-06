from pathlib import Path
import unittest

from src.testcycle.orchestrator import TestCycleOrchestrator


class PipelineTests(unittest.TestCase):
    def test_pipeline_creates_traceable_artifacts(self):
        import tempfile

        source = Path(r"D:\Project-Practice\AI\PromptEngineering\Data")
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            cycle = TestCycleOrchestrator().run(source / "RetailHub_SRS.docx", source / "RetailHub_SDS.docx", output)
            self.assertGreaterEqual(len(cycle.requirements), 45)
            self.assertEqual(len(cycle.cases), len(cycle.requirements) * 2)
            self.assertIn("FR-PAY-02", (output / "traceability.md").read_text(encoding="utf-8"))
            self.assertTrue((output / "scripts" / "test_retailhub_api.py").exists())
            pytest_suite = (output / "scripts" / "test_retailhub_cases.py").read_text(encoding="utf-8")
            self.assertEqual(pytest_suite.count("pytest.param("), len(cycle.cases))
