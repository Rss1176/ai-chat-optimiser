import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skill/chat-optimiser/scripts"))
import savings  # noqa: E402


class SavingsTest(unittest.TestCase):
    def test_cumulative_input_grows_with_turns(self):
        self.assertEqual(savings.cumulative_input(10_000, 1), 10_000)
        self.assertEqual(savings.cumulative_input(10_000, 9), 50_000)

    def test_zero_tokens(self):
        r = savings.estimate(0, 0, 0, "opus", "haiku", 1.0)
        self.assertEqual(r["spent"], 0)
        self.assertEqual(r["model_saving"], 0)

    def test_cost_uses_price_table(self):
        # 1M in + 1M out on Sonnet = $2 + $10
        self.assertAlmostEqual(savings.cost("sonnet", 1_000_000, 1_000_000), 12.0)

    def test_full_move_opus_to_sonnet_halves_cost(self):
        r = savings.estimate(100_000, 1, 10_000, "opus", "sonnet", 1.0)
        self.assertAlmostEqual(r["model_saving"], r["spent"] / 2)

    def test_same_model_saves_nothing(self):
        r = savings.estimate(50_000, 5, 5_000, "sonnet", "sonnet", 1.0)
        self.assertEqual(r["model_saving"], 0)

    def test_more_expensive_suggestion_never_negative(self):
        r = savings.estimate(50_000, 5, 5_000, "haiku", "opus", 1.0)
        self.assertEqual(r["model_saving"], 0)

    def test_fresh_start_saving(self):
        # 38k fewer tokens re-sent on each of 10 turns at Opus input price
        r = savings.estimate(40_000, 5, 0, "opus", fresh_start=2_000, future_turns=10)
        self.assertAlmostEqual(r["fresh_saving"], 380_000 * 4 / 1_000_000)

    def test_fresh_start_larger_than_context_saves_nothing(self):
        r = savings.estimate(1_000, 5, 0, "opus", fresh_start=2_000, future_turns=10)
        self.assertEqual(r["fresh_saving"], 0)

    def test_model_names_are_forgiving(self):
        self.assertEqual(savings.model_key("Claude Opus 5.5"), "opus")
        self.assertEqual(savings.model_key("claude-haiku-4-5"), "haiku")

    def test_unknown_model_rejected(self):
        with self.assertRaises(ValueError):
            savings.model_key("gpt-5")

    def test_movable_out_of_range_rejected(self):
        with self.assertRaises(ValueError):
            savings.estimate(1_000, 1, 0, "opus", "haiku", 1.5)

    def test_tiny_amounts_not_shown_as_zero_range(self):
        self.assertEqual(savings.fmt_money(0.001), "< $0.01")

    def test_cli_prints_labelled_estimates(self):
        out = io.StringIO()
        with redirect_stdout(out):
            savings.main(["--context", "40000", "--turns", "12", "--output", "9000",
                          "--current", "opus", "--suggested", "sonnet", "--movable", "0.7",
                          "--fresh-start", "2500", "--future-turns", "10"])
        text = out.getvalue()
        self.assertIn("≈ $", text)
        self.assertIn("Saved with sonnet", text)
        self.assertIn("Assumptions", text)


if __name__ == "__main__":
    unittest.main()
