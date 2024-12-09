from pydantic import TypeAdapter

from mcp_server_memos import main
from mcp_server_memos.proto_gen.memos.api.v1 import ListMemoTagsRequest

if __name__ == "__main__":
    # main()
    print(TypeAdapter(ListMemoTagsRequest).json_schema())
