from fastmcp import FastMCP

mcp = FastMCP("Account Status Service")

VALID_ACCOUNTS = {
    "ACC-001": {"status": "active", "name": "Acme Corp"},
    "ACC-002": {"status": "active", "name": "TechStart Inc"},
    "ACC-003": {"status": "suspended", "name": "Global Solutions"},
    "ACC-004": {"status": "active", "name": "Enterprise Systems"},
    "ACC-005": {"status": "closed", "name": "Legacy Partners"}
}

@mcp.tool(description="Get account status by account ID")
def account_status(account_id: str) -> dict:
    """Get account status and validate if account is active.
    
    Args:
        account_id: The account ID to check status for
        
    Returns:
        Dictionary with account status validation result and reason
    """
    if account_id in VALID_ACCOUNTS:
        account = VALID_ACCOUNTS[account_id]
        if account["status"] == "active":
            return {
                "account_id": account_id,
                "valid": True,
                "reason": f"Account '{account['name']}' is active and in good standing"
            }
        elif account["status"] == "suspended":
            return {
                "account_id": account_id,
                "valid": False,
                "reason": f"Account '{account['name']}' is suspended"
            }
        else:
            return {
                "account_id": account_id,
                "valid": False,
                "reason": f"Account '{account['name']}' is closed"
            }
    else:
        return {
            "account_id": account_id,
            "valid": False,
            "reason": "Account not found"
        }

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8002)
