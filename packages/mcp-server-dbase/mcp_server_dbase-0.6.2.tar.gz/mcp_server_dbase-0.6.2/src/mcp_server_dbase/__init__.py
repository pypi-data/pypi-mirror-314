from . import server
import asyncio
import argparse


def main():
    """Main entry point for the package."""
    parser = argparse.ArgumentParser(description='dbase MCP Server')
    parser.add_argument('--db-path', 
                       default="./dbase_mcp_server.db",
                       help='Path to dbase database file')
    
    args = parser.parse_args()
    asyncio.run(server.main(args.db_path))


# Optionally expose other important items at package level
__all__ = ["main", "server"]
