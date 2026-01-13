"""
Database Module

Handles SQLite database operations for storing test results.
"""

import sqlite3
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Manages SQLite database for storing adversarial test results.
    
    This class provides methods to:
    - Initialize database schema
    - Store test results
    - Query historical results
    - Generate reports
    """
    
    def __init__(self, db_path: str = "results.db"):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.connection = None
        self._connect()
        self._initialize_schema()
    
    def _connect(self):
        """Establish database connection."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Enable dict-like access
            logger.info(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    def _initialize_schema(self):
        """Initialize database schema from SQL file."""
        schema_path = Path(__file__).parent / "schema.sql"
        
        try:
            with open(schema_path, 'r') as f:
                schema_sql = f.read()
            
            cursor = self.connection.cursor()
            cursor.executescript(schema_sql)
            self.connection.commit()
            logger.info("Database schema initialized")
            
        except Exception as e:
            logger.error(f"Schema initialization failed: {e}")
            raise
    
    def save_result(self, result: Dict) -> int:
        """
        Save a test result to the database.
        
        Args:
            result: Dictionary containing test results with keys:
                - model_name
                - attack
                - epsilon
                - clean_accuracy
                - robust_accuracy
                - attack_success_rate
                - total_samples
                - device (optional)
                - alpha (optional, for PGD)
                - iters (optional, for PGD)
                - notes (optional)
        
        Returns:
            ID of the inserted row
            
        Raises:
            ValueError: If required fields are missing
        """
        required_fields = [
            'model_name', 'attack', 'epsilon', 'clean_accuracy',
            'robust_accuracy', 'attack_success_rate', 'total_samples'
        ]
        
        # Validate required fields
        missing_fields = [f for f in required_fields if f not in result]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
        
        # Prepare insert statement
        sql = """
            INSERT INTO test_results (
                model_name, attack_type, epsilon,
                clean_accuracy, robust_accuracy, attack_success_rate,
                total_samples, device, alpha, iters, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        values = (
            result['model_name'],
            result['attack'],
            result['epsilon'],
            result['clean_accuracy'],
            result['robust_accuracy'],
            result['attack_success_rate'],
            result['total_samples'],
            result.get('device'),
            result.get('alpha'),
            result.get('iters'),
            result.get('notes')
        )
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, values)
            self.connection.commit()
            
            row_id = cursor.lastrowid
            logger.info(f"Saved test result with ID: {row_id}")
            return row_id
            
        except sqlite3.Error as e:
            logger.error(f"Failed to save result: {e}")
            self.connection.rollback()
            raise
    
    def get_recent_results(self, limit: int = 10) -> List[Dict]:
        """
        Get most recent test results.
        
        Args:
            limit: Maximum number of results to return
        
        Returns:
            List of result dictionaries
        """
        sql = """
            SELECT * FROM test_results
            ORDER BY timestamp DESC
            LIMIT ?
        """
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (limit,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        except sqlite3.Error as e:
            logger.error(f"Failed to fetch results: {e}")
            raise
    
    def get_results_by_model(self, model_name: str) -> List[Dict]:
        """
        Get all test results for a specific model.
        
        Args:
            model_name: Name of the model
        
        Returns:
            List of result dictionaries
        """
        sql = """
            SELECT * FROM test_results
            WHERE model_name = ?
            ORDER BY timestamp DESC
        """
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (model_name,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        except sqlite3.Error as e:
            logger.error(f"Failed to fetch results: {e}")
            raise
    
    def get_results_by_attack(
        self,
        model_name: str,
        attack_type: str,
        epsilon: Optional[float] = None
    ) -> List[Dict]:
        """
        Get test results for a specific model and attack combination.
        
        Args:
            model_name: Name of the model
            attack_type: Type of attack ('fgsm' or 'pgd')
            epsilon: Optional epsilon filter
        
        Returns:
            List of result dictionaries
        """
        if epsilon is not None:
            sql = """
                SELECT * FROM test_results
                WHERE model_name = ? AND attack_type = ? AND epsilon = ?
                ORDER BY timestamp DESC
            """
            params = (model_name, attack_type, epsilon)
        else:
            sql = """
                SELECT * FROM test_results
                WHERE model_name = ? AND attack_type = ?
                ORDER BY timestamp DESC
            """
            params = (model_name, attack_type)
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        except sqlite3.Error as e:
            logger.error(f"Failed to fetch results: {e}")
            raise
    
    def get_robustness_curve(self, model_name: str, attack_type: str) -> List[Dict]:
        """
        Get data for plotting robustness curve (accuracy vs epsilon).
        
        Args:
            model_name: Name of the model
            attack_type: Type of attack
        
        Returns:
            List of dictionaries with epsilon and accuracy data
        """
        sql = """
            SELECT 
                epsilon,
                AVG(clean_accuracy) as avg_clean_accuracy,
                AVG(robust_accuracy) as avg_robust_accuracy,
                AVG(attack_success_rate) as avg_attack_success_rate,
                COUNT(*) as num_tests
            FROM test_results
            WHERE model_name = ? AND attack_type = ?
            GROUP BY epsilon
            ORDER BY epsilon ASC
        """
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (model_name, attack_type))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        except sqlite3.Error as e:
            logger.error(f"Failed to fetch robustness curve data: {e}")
            raise
    
    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
