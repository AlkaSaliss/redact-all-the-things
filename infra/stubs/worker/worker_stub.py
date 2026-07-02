import json
import sys


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    print(json.dumps({"status": "ok", "worker_mode": mode}))


if __name__ == "__main__":
    main()
