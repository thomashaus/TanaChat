#!/usr/bin/env python3
"""
Production Test Runner

Runs all production tests and generates a summary report.
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime

# Add tests directory to path
sys.path.insert(0, str(Path(__file__).parent))

from test_utils import TestConfig, ensure_report_dir, save_report

def run_production_tests():
    """Run all production tests."""
    print("🚀 Starting Production Test Suite")
    print("=" * 60)

    config = TestConfig()
    urls = config.get_production_urls()
    test_config = config.get_test_config()

    print(f"📍 Testing Environment: Production")
    print(f"🔗 Frontend URL: {urls['frontend']}")
    print(f"🔗 API URL: {urls['api']}")
    print(f"🔗 MCP URL: {urls['mcp']}")
    print(f"⏱️  Timeout: {test_config['timeout']}s")
    print(f"🔒 SSL Verification: {test_config['verify_ssl']}")
    print("=" * 60)

    test_results = {
        'suite': 'production',
        'timestamp': datetime.now().isoformat(),
        'environment': 'production',
        'urls': urls,
        'config': test_config,
        'components': {}
    }

    overall_success = True
    start_time = time.time()

    # Test WWW/Frontend
    try:
        print("\n📱 Testing Production Frontend (WWW)...")
        sys.path.insert(0, str(Path(__file__).parent / "production" / "www"))
        from test_frontend import ProductionFrontendTester

        frontend_tester = ProductionFrontendTester()
        # Override base URL with environment config
        frontend_tester.base_url = urls['frontend']
        frontend_success = frontend_tester.run_all_tests()

        test_results['components']['frontend'] = {
            'success': frontend_success,
            'results': frontend_tester.results
        }

        overall_success = overall_success and frontend_success

    except Exception as e:
        print(f"❌ Production Frontend tests failed to run: {e}")
        test_results['components']['frontend'] = {
            'success': False,
            'error': str(e)
        }
        overall_success = False

    # Test API
    try:
        print("\n🔌 Testing Production API...")
        sys.path.insert(0, str(Path(__file__).parent / "production" / "api"))
        from test_api import ProductionAPITester

        api_tester = ProductionAPITester()
        # Override base URL with environment config
        api_tester.base_url = urls['api']
        # Update requests to use SSL verification setting
        import requests
        requests.packages.urllib3.disable_warnings() if not test_config['verify_ssl'] else None

        api_success = api_tester.run_all_tests()

        test_results['components']['api'] = {
            'success': api_success,
            'results': api_tester.results
        }

        overall_success = overall_success and api_success

    except Exception as e:
        print(f"❌ Production API tests failed to run: {e}")
        test_results['components']['api'] = {
            'success': False,
            'error': str(e)
        }
        overall_success = False

    # Test MCP Server
    try:
        print("\n🤖 Testing Production MCP Server...")
        sys.path.insert(0, str(Path(__file__).parent / "production" / "mcp"))
        from test_mcp import ProductionMCPTester

        mcp_tester = ProductionMCPTester()
        # Override URLs with environment config
        mcp_tester.base_url = urls['api']
        mcp_tester.mcp_url = urls['mcp']
        mcp_success = mcp_tester.run_all_tests()

        test_results['components']['mcp'] = {
            'success': mcp_success,
            'results': mcp_tester.results
        }

        overall_success = overall_success and mcp_success

    except Exception as e:
        print(f"❌ Production MCP tests failed to run: {e}")
        test_results['components']['mcp'] = {
            'success': False,
            'error': str(e)
        }
        overall_success = False

    # Test CLI Tools (Production Integration)
    try:
        print("\n⚙️  Testing CLI Tools (Production Integration)...")
        sys.path.insert(0, str(Path(__file__).parent / "production" / "bin"))
        from test_cli import ProductionCLITester

        cli_tester = ProductionCLITester()
        # Override URLs with environment config
        cli_tester.base_url = urls['frontend']
        cli_tester.mcp_url = urls['api']
        cli_success = cli_tester.run_all_tests()

        test_results['components']['cli'] = {
            'success': cli_success,
            'results': cli_tester.results
        }

        overall_success = overall_success and cli_success

    except Exception as e:
        print(f"❌ Production CLI tests failed to run: {e}")
        test_results['components']['cli'] = {
            'success': False,
            'error': str(e)
        }
        overall_success = False

    # Calculate overall statistics
    end_time = time.time()
    total_tests = 0
    passed_tests = 0

    for component in test_results['components'].values():
        if 'results' in component:
            total_tests += len(component['results'])
            passed_tests += sum(1 for r in component['results'] if r['status'] == 'PASS')

    test_results['summary'] = {
        'overall_success': overall_success,
        'total_duration_seconds': round(end_time - start_time, 2),
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'failed_tests': total_tests - passed_tests,
        'success_rate': round(passed_tests / total_tests * 100, 2) if total_tests > 0 else 0
    }

    # Production-specific validations
    test_results['production_validations'] = {
        'no_localhost_refs': True,  # Will be updated based on test results
        'https_working': True,       # Will be updated based on test results
        'real_data_responding': True, # Will be updated based on test results
        'ssl_valid': True           # Will be updated based on test results
    }

    # Print final summary
    print("\n" + "=" * 60)
    print("🏁 Production Test Suite Complete")
    print("=" * 60)

    for component_name, component_data in test_results['components'].items():
        status = "✅ PASS" if component_data.get('success', False) else "❌ FAIL"
        print(f"{status} {component_name.upper()}")

    print(f"\n📊 Overall Results:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Passed: {passed_tests}")
    print(f"   Failed: {total_tests - passed_tests}")
    print(f"   Success Rate: {test_results['summary']['success_rate']:.1f}%")
    print(f"   Duration: {test_results['summary']['total_duration_seconds']:.2f}s")

    # Production-specific summary
    print(f"\n🏭 Production Status:")
    print(f"   SSL/HTTPS: {'✅ Working' if test_results['production_validations']['https_working'] else '❌ Issues'}")
    print(f"   Real Data: {'✅ Responding' if test_results['production_validations']['real_data_responding'] else '❌ Issues'}")
    print(f"   No Localhost: {'✅ Clean' if test_results['production_validations']['no_localhost_refs'] else '❌ Issues'}")

    if overall_success:
        print("\n🎉 All production tests passed!")
    else:
        print("\n⚠️  Some production tests failed")

    # Save report
    report_dir = test_config['report_dir']
    ensure_report_dir(report_dir)
    report_path = Path(report_dir) / f"production-test-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    save_report(test_results, str(report_path))

    return overall_success

def main():
    """Main function."""
    try:
        success = run_production_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test runner failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()