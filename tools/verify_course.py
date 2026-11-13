"""Verify both offline editions. Use --static-only without Playwright/browsers."""
import argparse
from verify_common import run_static


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--static-only', action='store_true', help='skip browser checks')
    args = parser.parse_args()
    run_static()
    if not args.static_only:
        from verify_browser import run_browser
        run_browser()


if __name__ == '__main__':
    main()
