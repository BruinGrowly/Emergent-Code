"""
Unit Tests for LJPW Vocabulary System

Comprehensive test suite for vocabulary.py module.

Author: Wellington Kwati Taureka
Date: December 4, 2025
"""

import unittest
import sys
import os
import numpy as np
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_nn.vocabulary import (
    WordEntry, CoordinateIndex, LJPWVocabulary, VocabularyLoader,
    ANCHOR_POINT, NATURAL_EQUILIBRIUM
)


class TestWordEntry(unittest.TestCase):
    """Test WordEntry dataclass"""
    
    def test_creation(self):
        """Test WordEntry creation"""
        coords = np.array([0.9, 0.5, 0.2, 0.7])
        entry = WordEntry(word="love", coords=coords, language="en")
        
        self.assertEqual(entry.word, "love")
        self.assertEqual(entry.language, "en")
        np.testing.assert_array_equal(entry.coords, coords)
    
    def test_harmony(self):
        """Test harmony calculation"""
        coords = np.array([1.0, 1.0, 1.0, 1.0])  # At anchor point
        entry = WordEntry(word="perfect", coords=coords)
        
        # At anchor point, distance=0, so H = 1/(1+0) = 1.0
        self.assertAlmostEqual(entry.harmony(), 1.0, places=5)
    
    def test_distance_to(self):
        """Test distance calculation"""
        coords1 = np.array([0.0, 0.0, 0.0, 0.0])
        coords2 = np.array([1.0, 0.0, 0.0, 0.0])
        
        entry = WordEntry(word="test", coords=coords1)
        distance = entry.distance_to(coords2)
        
        self.assertAlmostEqual(distance, 1.0, places=5)


class TestCoordinateIndex(unittest.TestCase):
    """Test CoordinateIndex class"""
    
    def setUp(self):
        """Set up test vocabulary"""
        self.word_coords = {
            'love': np.array([0.9, 0.5, 0.2, 0.7]),
            'justice': np.array([0.6, 0.9, 0.5, 0.8]),
            'power': np.array([0.4, 0.5, 0.9, 0.6]),
            'wisdom': np.array([0.7, 0.7, 0.4, 0.9])
        }
        self.index = CoordinateIndex()
        self.index.build_index(self.word_coords)
    
    def test_build_index(self):
        """Test index building"""
        self.assertIsNotNone(self.index.kdtree)
        self.assertEqual(len(self.index.word_list), 4)
    
    def test_query_single(self):
        """Test single nearest neighbor query"""
        # Query near 'love'
        coords = np.array([0.9, 0.5, 0.2, 0.7])
        nearest = self.index.query(coords, k=1)
        
        self.assertEqual(nearest, 'love')
    
    def test_query_multiple(self):
        """Test k-nearest neighbors query"""
        coords = np.array([0.9, 0.5, 0.2, 0.7])
        nearest = self.index.query(coords, k=2)
        
        self.assertEqual(len(nearest), 2)
        self.assertIn('love', nearest)
    
    def test_query_with_distances(self):
        """Test query with distance return"""
        coords = np.array([0.9, 0.5, 0.2, 0.7])
        words, distances = self.index.query(coords, k=1, return_distances=True)
        
        self.assertEqual(words, 'love')
        self.assertAlmostEqual(distances, 0.0, places=5)
    
    def test_query_radius(self):
        """Test radius query"""
        coords = np.array([0.9, 0.5, 0.2, 0.7])
        results = self.index.query_radius(coords, radius=0.5)
        
        self.assertGreater(len(results), 0)
        self.assertIsInstance(results[0], tuple)
        self.assertEqual(len(results[0]), 2)  # (word, distance)


class TestLJPWVocabulary(unittest.TestCase):
    """Test LJPWVocabulary class"""
    
    def setUp(self):
        """Set up test vocabulary"""
        self.vocab = LJPWVocabulary(vocab_size=100)
        
        # Add test words
        self.vocab.register('love', [0.9, 0.5, 0.2, 0.7], language='en')
        self.vocab.register('justice', [0.6, 0.9, 0.5, 0.8], language='en')
        self.vocab.register('power', [0.4, 0.5, 0.9, 0.6], language='en')
        self.vocab.register('wisdom', [0.7, 0.7, 0.4, 0.9], language='en')
    
    def test_register(self):
        """Test word registration"""
        self.assertEqual(len(self.vocab), 4)
        self.assertIn('love', self.vocab)
        self.assertNotIn('unknown', self.vocab)
    
    def test_get_coords(self):
        """Test coordinate retrieval"""
        coords = self.vocab.get_coords('love')
        
        self.assertIsNotNone(coords)
        self.assertEqual(len(coords), 4)
        np.testing.assert_array_almost_equal(coords, [0.9, 0.5, 0.2, 0.7])
    
    def test_get_coords_unknown(self):
        """Test unknown word handling"""
        coords = self.vocab.get_coords('unknown')
        
        # Should return Natural Equilibrium
        np.testing.assert_array_almost_equal(coords, NATURAL_EQUILIBRIUM)
    
    def test_get_entry(self):
        """Test entry retrieval"""
        entry = self.vocab.get_entry('love')
        
        self.assertIsNotNone(entry)
        self.assertEqual(entry.word, 'love')
        self.assertEqual(entry.language, 'en')
    
    def test_nearest_word(self):
        """Test nearest word search"""
        self.vocab.build_index()
        
        coords = np.array([0.9, 0.5, 0.2, 0.7])
        nearest = self.vocab.nearest_word(coords)
        
        self.assertEqual(nearest, 'love')
    
    def test_nearest_words_with_distances(self):
        """Test nearest words with distances"""
        self.vocab.build_index()
        
        coords = np.array([0.9, 0.5, 0.2, 0.7])
        results = self.vocab.nearest_words_with_distances(coords, k=2)
        
        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0], tuple)
        self.assertEqual(len(results[0]), 2)  # (word, distance)
    
    def test_words_in_radius(self):
        """Test radius search"""
        self.vocab.build_index()
        
        coords = np.array([0.9, 0.5, 0.2, 0.7])
        results = self.vocab.words_in_radius(coords, radius=0.5)
        
        self.assertGreater(len(results), 0)
    
    def test_save_load(self):
        """Test vocabulary persistence"""
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as f:
            temp_path = f.name
        
        try:
            # Save
            self.vocab.save(temp_path)
            
            # Load into new vocabulary
            new_vocab = LJPWVocabulary()
            new_vocab.load(temp_path)
            
            # Verify
            self.assertEqual(len(new_vocab), len(self.vocab))
            self.assertIn('love', new_vocab)
            
            coords1 = self.vocab.get_coords('love')
            coords2 = new_vocab.get_coords('love')
            np.testing.assert_array_almost_equal(coords1, coords2)
        
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_get_statistics(self):
        """Test statistics generation"""
        stats = self.vocab.get_statistics()
        
        self.assertEqual(stats['size'], 4)
        self.assertIn('languages', stats)
        self.assertIn('coord_stats', stats)
        self.assertIn('harmony_stats', stats)
        
        self.assertEqual(stats['languages']['en'], 4)


class TestVocabularyLoader(unittest.TestCase):
    """Test VocabularyLoader class"""
    
    def test_load_expansion_file(self):
        """Test loading expansion file"""
        # This test requires actual data files
        # Skip if not available
        data_dir = os.path.join('data', 'LJPW_Language_Data')
        test_file = os.path.join(data_dir, 'fifth_major_expansion.json')
        
        if not os.path.exists(test_file):
            self.skipTest("Test data file not available")
        
        entries = VocabularyLoader.load_expansion_file(test_file)
        
        self.assertGreater(len(entries), 0)
        self.assertIsInstance(entries[0], dict)
        self.assertIn('word', entries[0])
        self.assertIn('coords', entries[0])


def run_tests():
    """Run all tests"""
    print("=" * 70)
    print("Running LJPW Vocabulary Unit Tests")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestWordEntry))
    suite.addTests(loader.loadTestsFromTestCase(TestCoordinateIndex))
    suite.addTests(loader.loadTestsFromTestCase(TestLJPWVocabulary))
    suite.addTests(loader.loadTestsFromTestCase(TestVocabularyLoader))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print()
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print()
    
    if result.wasSuccessful():
        print("[OK] All tests passed!")
    else:
        print("[FAILED] Some tests failed")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
