# server_get.py
# ============================================================
# orchestrator_server から指定IDのリクエストを取得するCLI
#
# Usage:
#   python server_get.py --id XXX --url https://xxxx.trycloudflare.com
#   python server_get.py --id XXX --net-port "192.168.1.10:5000"
#
# 出力例:
#   {
#     "XXX": {
#       "実行コマンド": "echo helloworld",
#       "目的": "テスト",
#       "承認": false
#     }
#   }
#
# ※ サーバ(server.py)を先に起動しておくこと
#   python3 server.py
#   python3 server.py --net-port "0.0.0.0:5000"
# ============================================================

import argparse
import json
import requests

def get_request(server_id: str, base_url: str) -> dict:
    url = f"{base_url}/api/requests/{server_id}"
    response = requests.get(url)
    if response.status_code != 200:
        return {
            "error": True,
            "status_code": response.status_code,
            "detail": response.json() if response.content else None,
        }
    data = response.json()
    return {
        server_id: {
            "実行コマンド": data.get("command"),
            "目的": data.get("purpose"),
            "承認": data.get("status") == "承認済み",
        }
    }

def parse_net_port(value: str) -> str:
    host, port = value.rsplit(":", 1)
    return f"http://{host}:{int(port)}"

def parse_args():
    parser = argparse.ArgumentParser(description="orchestrator_server から指定IDのリクエストを取得するCLI")
    parser.add_argument("--id", required=True, help="取得するリクエストのID")
    connection = parser.add_mutually_exclusive_group(required=True)
    connection.add_argument("--url", help="サーバのベースURL (例: https://xxxx.trycloudflare.com)")
    connection.add_argument("--net-port", type=parse_net_port, help='ローカルネットワークのサーバアドレスとポート (例: "192.168.1.10:5000")')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    base_url = args.url if args.url else args.net_port
    result = get_request(server_id=args.id, base_url=base_url)
    print(json.dumps(result, ensure_ascii=False, indent=2))
