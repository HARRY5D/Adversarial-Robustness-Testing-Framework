-- Adversarial Robustness Test Results Schema
-- This schema stores the results of adversarial attack tests

CREATE TABLE IF NOT EXISTS test_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    model_name TEXT NOT NULL,
    attack_type TEXT NOT NULL,
    epsilon REAL NOT NULL,
    clean_accuracy REAL NOT NULL,
    robust_accuracy REAL NOT NULL,
    attack_success_rate REAL NOT NULL,
    total_samples INTEGER NOT NULL,
    device TEXT,
    alpha REAL,
    iters INTEGER,
    notes TEXT,
    CONSTRAINT valid_attack CHECK (attack_type IN ('fgsm', 'pgd')),
    CONSTRAINT valid_model CHECK (model_name IN ('cifar10_resnet20', 'mnist_simplecnn')),
    CONSTRAINT valid_epsilon CHECK (epsilon >= 0),
    CONSTRAINT valid_accuracies CHECK (
        clean_accuracy >= 0 AND clean_accuracy <= 100 AND
        robust_accuracy >= 0 AND robust_accuracy <= 100 AND
        attack_success_rate >= 0 AND attack_success_rate <= 100
    )
);

-- Index for efficient querying by model and attack type
CREATE INDEX IF NOT EXISTS idx_model_attack ON test_results(model_name, attack_type);

-- Index for timestamp-based queries
CREATE INDEX IF NOT EXISTS idx_timestamp ON test_results(timestamp DESC);

-- Index for epsilon-based queries
CREATE INDEX IF NOT EXISTS idx_epsilon ON test_results(epsilon);
