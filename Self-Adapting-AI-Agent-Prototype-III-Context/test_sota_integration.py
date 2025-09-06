"""
Test SOTA Evaluation Integration
Quick test to verify the integration is working properly.
"""

import sys
import os
from pathlib import Path

# Add SOTA_Evaluation to path
current_dir = Path(__file__).parent
sota_evaluation_path = current_dir.parent / "SOTA_Evaluation"
sys.path.insert(0, str(sota_evaluation_path))

def test_import_integration():
    """Test if SOTA evaluation modules can be imported."""
    try:
        from integration.prototype_iv_evaluator import PrototypeIVEvaluator
        print("✓ PrototypeIVEvaluator imported successfully")
        
        from metrics.mape_k_metrics import MAPEKAnalyzer
        print("✓ MAPEKAnalyzer imported successfully")
        
        from metrics.complexity_analyzer import ComplexityAnalyzer
        print("✓ ComplexityAnalyzer imported successfully")
        
        from metrics.statistical_tests import StatisticalAnalyzer
        print("✓ StatisticalAnalyzer imported successfully")
        
        from datasets.humaneval_loader import HumanEvalLoader
        print("✓ HumanEvalLoader imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_evaluator_initialization():
    """Test if the evaluator can be initialized."""
    try:
        from integration.prototype_iv_evaluator import PrototypeIVEvaluator
        
        prototype_path = str(Path(__file__).parent)
        evaluator = PrototypeIVEvaluator(prototype_path)
        print("✓ PrototypeIVEvaluator initialized successfully")
        
        # Test session start
        evaluator.start_evaluation_session("test_session")
        print("✓ Evaluation session started successfully")
        
        # Test decorators
        decorators = evaluator.get_decorators()
        print(f"✓ Decorators available: {list(decorators.keys())}")
        
        return True, evaluator
    except Exception as e:
        print(f"❌ Evaluator initialization failed: {e}")
        return False, None

def test_mape_k_timing():
    """Test MAPE-K timing functionality."""
    try:
        from integration.prototype_iv_evaluator import PrototypeIVEvaluator
        
        prototype_path = str(Path(__file__).parent)
        evaluator = PrototypeIVEvaluator(prototype_path)
        evaluator.start_evaluation_session("timing_test")
        
        # Simulate a complete MAPE-K cycle
        import time
        
        # Simulate monitor phase
        evaluator.mape_k_analyzer._update_current_cycle('monitor', 0.1, True, None)
        
        # Simulate analyze phase  
        evaluator.mape_k_analyzer._update_current_cycle('analyze', 0.2, True, None)
        
        # Simulate plan phase
        evaluator.mape_k_analyzer._update_current_cycle('plan', 0.15, True, None)
        
        # Simulate execute phase
        evaluator.mape_k_analyzer._update_current_cycle('execute', 0.05, True, None)
        
        # Complete the cycle
        test_code = '''
def test_function():
    return "Hello World"
'''
        evaluator.complete_iteration_cycle(1, test_code, "test_function", True)
        
        # Generate report
        report = evaluator.generate_comprehensive_report()
        
        print("✓ MAPE-K timing test completed successfully")
        print(f"  - Total cycles: {report['evaluation_summary']['total_cycles_completed']}")
        print(f"  - Session duration: {report['session_info']['duration']:.2f}s")
        
        return True
    except Exception as e:
        print(f"❌ MAPE-K timing test failed: {e}")
        return False

def test_complexity_analysis():
    """Test code complexity analysis."""
    try:
        from metrics.complexity_analyzer import ComplexityAnalyzer
        
        analyzer = ComplexityAnalyzer()
        
        # Test code sample
        test_code = '''
def factorial(n):
    if n < 0:
        raise ValueError("Negative numbers not allowed")
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
'''
        
        analysis = analyzer.analyze_code_complexity(test_code, "factorial")
        
        print("✓ Code complexity analysis completed")
        print(f"  - Lines of code: {analysis['lines_of_code']}")
        print(f"  - Function analyzed: {analysis['function_name']}")
        
        if 'ast_analysis' in analysis and analysis['ast_analysis']:
            ast_data = analysis['ast_analysis']
            if 'estimated_complexity' in ast_data:
                print(f"  - Estimated complexity: {ast_data['estimated_complexity']}")
        
        return True
    except Exception as e:
        print(f"❌ Complexity analysis test failed: {e}")
        return False

def test_statistical_analysis():
    """Test statistical analysis functionality."""
    try:
        from metrics.statistical_tests import StatisticalAnalyzer
        
        analyzer = StatisticalAnalyzer()
        
        # Test data for prototype progression
        test_data = {
            'Prototype_I': [4.8, 5.2, 4.5, 5.0, 4.7],
            'Prototype_II': [3.6, 3.8, 3.4, 3.5, 3.7],
            'Prototype_III': [2.9, 3.1, 2.8, 3.0, 2.7],
            'Prototype_IV': [2.2, 2.4, 2.1, 2.3, 2.0]
        }
        
        analysis = analyzer.analyze_prototype_progression(test_data)
        
        print("✓ Statistical analysis completed")
        
        # Check for trend analysis
        if 'trend_analysis' in analysis:
            improvement = analysis['trend_analysis'].get('overall_improvement_percent', 0)
            print(f"  - Overall improvement: {improvement:.1f}%")
        
        return True
    except Exception as e:
        print(f"❌ Statistical analysis test failed: {e}")
        return False

def test_paper_outputs():
    """Test paper output generation."""
    try:
        from reporting.nier_table_generator import NierTableGenerator
        
        # Create temporary output directory
        output_dir = Path(__file__).parent / "sota_evaluation_results" / "test_outputs"
        output_dir.mkdir(exist_ok=True)
        
        generator = NierTableGenerator(str(output_dir))
        
        # Generate a sample table
        table = generator.generate_prototype_comparison_table(None)  # Uses sample data
        
        print("✓ Paper output generation completed")
        print(f"  - Generated LaTeX table ({len(table)} characters)")
        print(f"  - Output directory: {output_dir}")
        
        return True
    except Exception as e:
        print(f"❌ Paper output test failed: {e}")
        return False

def main():
    """Run all integration tests."""
    print("SOTA Evaluation Integration Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Integration", test_import_integration),
        ("Evaluator Initialization", test_evaluator_initialization),
        ("MAPE-K Timing", test_mape_k_timing),
        ("Complexity Analysis", test_complexity_analysis),
        ("Statistical Analysis", test_statistical_analysis),
        ("Paper Outputs", test_paper_outputs),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if callable(test_func):
                result = test_func()
                if result and result != False:
                    passed += 1
                    print(f"✓ {test_name} PASSED")
                else:
                    print(f"❌ {test_name} FAILED")
            else:
                print(f"⚠ {test_name} SKIPPED (not callable)")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! SOTA evaluation integration is working correctly.")
        print("\nNext steps:")
        print("1. Run: python Core/main.py (to test with actual evaluation)")
        print("2. Run: python evaluation_runner.py (for comprehensive benchmark)")
    else:
        print("⚠ Some tests failed. Check the error messages above.")
        print("\nTroubleshooting:")
        print("1. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("2. Install additional tools: pip install radon mccabe datasets")
        print("3. Check that SOTA_Evaluation directory exists in parent folder")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)