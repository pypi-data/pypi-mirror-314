import unittest
from unittest.mock import patch, MagicMock, Mock
from datetime import datetime
from src.inferent.ratings import (
    Glicko2,
    KalmanRating,
    Rating,
    BASE_RATING,
    TSRating,
)
import pandas as pd
import trueskill


class TestGlicko2(unittest.TestCase):

    @patch("src.inferent.ratings.Glicko2.Player")
    def test_update_method(self, mock_Player):
        mock_Player.return_value = Glicko2.Player()
        glicko = Glicko2()

        # Initialize players
        p1key = "player1"
        p2key = "player2"
        outcome = "win"
        date = datetime(2023, 1, 1)

        # Update ratings
        glicko.update(p1key, p2key, outcome, date)

        # Check if players are initialized and updated
        self.assertIn(p1key, glicko.players)
        self.assertIn(p2key, glicko.players)
        self.assertNotEqual(glicko.get_rating(p1key), BASE_RATING)
        self.assertNotEqual(glicko.get_rating(p2key), BASE_RATING)

    def test_g_function(self):
        rd_opp = 30.0
        g_value = Glicko2.g(rd_opp)
        self.assertAlmostEqual(g_value, 0.99549801)

    def test_win_proba(self):
        r = 1500.0
        r_opp = 1600.0
        rd_opp = 30.0
        expected = Glicko2.win_proba(r, r_opp, rd_opp)
        self.assertAlmostEqual(expected, 0.36053226)


class TestKalmanRating(unittest.TestCase):

    def test_update_method(self):
        kalman = KalmanRating(2.50, 1, 0.5, 4, 0.2)

        # Initialize players
        p1key = "player1"
        p2key = "player2"
        p1ortg = 0.8
        p2ortg = 0.7

        # Update ratings
        kalman.update(p1key, p2key, p1ortg, p2ortg)

        # Check if ratings are updated
        self.assertIn(p1key, kalman.players)
        self.assertIn(p2key, kalman.players)
        self.assertNotEqual(kalman.get_rating(p1key).o.score, kalman.avg_rtg)
        self.assertNotEqual(kalman.get_rating(p2key).o.score, kalman.avg_rtg)


class TestTSRating(unittest.TestCase):

    @patch("src.inferent.ratings.trueskill.TrueSkill")
    @patch("src.inferent.ratings.TSRating.Player")
    def test_init(self, mock_player, mock_trueskill):
        mock_env = MagicMock(spec=trueskill.TrueSkill)
        mock_trueskill.return_value = mock_env

        beta_adjustments = {"game1": 1.0}
        ts_rating = TSRating(
            draw_probability=0.1, beta_adjustments=beta_adjustments
        )

        mock_trueskill.assert_called_once_with(draw_probability=0.1)
        self.assertEqual(ts_rating.beta_adjustments, beta_adjustments)
        self.assertIsInstance(ts_rating.players, dict)

    def test_calc_ratings(self):
        mock_env = MagicMock(spec=trueskill.TrueSkill)
        ts_rating = TSRating(draw_probability=0.1, beta_adjustments={})
        ts_rating.env = mock_env

        row = pd.Series({"teams": [["Player1"], ["Player2"]], "ranks": [0, 1]})

        mock_env.rate.return_value = [
            [trueskill.Rating(mu=30)],
            [trueskill.Rating(mu=20)],
        ]

        ratings = ts_rating.calc_ratings(row)

        self.assertEqual(len(ratings), 2)
        self.assertEqual(ratings[0][0].rtg.mu, 30)
        self.assertEqual(ratings[1][0].rtg.mu, 20)
        mock_env.rate.assert_called_once()
        self.assertEqual(ts_rating.players["Player1"].rtg.mu, 30)
        self.assertEqual(ts_rating.players["Player2"].rtg.mu, 20)

    # This complex patch is required because of
    # https://github.com/pandas-dev/pandas/issues/45298
    @patch.object(TSRating, "calc_ratings", return_value=[["new_rating1"], ["new_rating2"]], new_callable=Mock)
    def test_enrich_update(self, mock_calc_ratings):
        df = pd.DataFrame(
            {"teams": [[["Player1"], ["Player2"]]], "ranks": [[0, 1]]}
        )

        ts_rating = TSRating(draw_probability=0.1, beta_adjustments={})
        ts_rating.calc_ratings = mock_calc_ratings

        updated_df = ts_rating.enrich_update(df)

        self.assertIn("ratings", updated_df.columns)
        mock_calc_ratings.assert_called_once()

if __name__ == "__main__":
    unittest.main()
