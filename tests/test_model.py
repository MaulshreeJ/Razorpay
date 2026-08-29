import src.model as model_module
from src.data_gen import generate


def _patch_artifacts(tmp_path, monkeypatch):
    monkeypatch.setattr(model_module, "MODEL_PATH", tmp_path / "model.joblib")
    monkeypatch.setattr(model_module, "THRESHOLDS_PATH", tmp_path / "thresholds.json")
    monkeypatch.setattr(model_module, "ARTIFACT_DIR", tmp_path)


def test_train_returns_expected_metric_keys(tmp_path, monkeypatch):
    _patch_artifacts(tmp_path, monkeypatch)
    df = generate(n_transactions=1500, seed=7)
    metrics = model_module.train(df)

    for key in ("precision", "recall", "pr_auc", "roc_auc", "operating_threshold", "confusion_matrix"):
        assert key in metrics
    assert 0.0 <= metrics["precision"] <= 1.0
    assert 0.0 <= metrics["recall"] <= 1.0


def test_risk_model_scores_in_valid_range(tmp_path, monkeypatch):
    _patch_artifacts(tmp_path, monkeypatch)
    df = generate(n_transactions=1500, seed=7)
    model_module.train(df)

    risk_model = model_module.RiskModel()
    prob, band = risk_model.score(df.iloc[[0]])
    assert 0.0 <= prob <= 1.0
    assert band is not None
