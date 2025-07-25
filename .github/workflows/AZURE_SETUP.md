# Azure Authentication Setup for GitHub Actions

This guide will help you set up Azure authentication for the GitHub workflow to access your Azure resources securely.

## Method 1: Service Principal with Federated Credentials (Recommended)

This is the most secure method as it doesn't require storing sensitive credentials as secrets.

### Step 1: Create a Service Principal

Run the following Azure CLI commands:

```bash
# Login to Azure
az login

# Set your subscription (replace with your subscription ID)
az account set --subscription "your-subscription-id"

# Create a service principal
az ad sp create-for-rbac --name "github-actions-fantasy-football" --role contributor --scopes /subscriptions/your-subscription-id --json-auth
```

Save the output - you'll need the `clientId`, `subscriptionId`, and `tenantId`.

### Step 2: Configure Federated Credentials

```bash
# Get your repository details
REPO_OWNER="sohamda"
REPO_NAME="fantasy-football"
SERVICE_PRINCIPAL_ID="your-client-id-from-step-1"

# Create federated credential for the main branch
az ad app federated-credential create \
  --id $SERVICE_PRINCIPAL_ID \
  --parameters '{
    "name": "github-actions-main",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:'$REPO_OWNER'/'$REPO_NAME':ref:refs/heads/main",
    "audiences": ["api://AzureADTokenExchange"]
  }'

# Optional: Create federated credential for all branches
az ad app federated-credential create \
  --id $SERVICE_PRINCIPAL_ID \
  --parameters '{
    "name": "github-actions-all-branches",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:'$REPO_OWNER'/'$REPO_NAME':ref:refs/heads/*",
    "audiences": ["api://AzureADTokenExchange"]
  }'
```

### Step 3: Grant Required Permissions

Ensure your service principal has the necessary permissions for your Azure resources:

```bash
# Example: Grant access to specific resource groups
az role assignment create \
  --assignee $SERVICE_PRINCIPAL_ID \
  --role "Contributor" \
  --scope "/subscriptions/your-subscription-id/resourceGroups/your-resource-group"

# Example: Grant specific permissions for Cosmos DB
az role assignment create \
  --assignee $SERVICE_PRINCIPAL_ID \
  --role "Cosmos DB Account Reader Role" \
  --scope "/subscriptions/your-subscription-id/resourceGroups/your-rg/providers/Microsoft.DocumentDB/databaseAccounts/your-cosmos-account"

# Example: Grant permissions for Log Analytics
az role assignment create \
  --assignee $SERVICE_PRINCIPAL_ID \
  --role "Log Analytics Contributor" \
  --scope "/subscriptions/your-subscription-id/resourceGroups/your-rg/providers/Microsoft.OperationalInsights/workspaces/your-workspace"
```

### Step 4: Configure GitHub Repository Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions, and add these secrets:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `AZURE_CLIENT_ID` | Client ID from Step 1 | Service Principal Application ID |
| `AZURE_TENANT_ID` | Tenant ID from Step 1 | Azure AD Tenant ID |
| `AZURE_SUBSCRIPTION_ID` | Your subscription ID | Azure Subscription ID |
| `AZURE_OPENAI_API_KEY` | Your Azure OpenAI key | API key for Azure OpenAI |
| `AZURE_OPENAI_ENDPOINT` | Your Azure OpenAI endpoint | Endpoint URL for Azure OpenAI |
| `COSMOS_DB_CONNECTION_STRING` | Cosmos DB connection string | Connection string for Cosmos DB |
| `LOG_ANALYTICS_WORKSPACE_ID` | Workspace ID | Log Analytics workspace identifier |
| `LOG_ANALYTICS_SHARED_KEY` | Shared key | Log Analytics shared access key |
| `BING_SEARCH_API_KEY` | Bing API key | Bing Search API key |

## Method 2: Service Principal with Client Secret (Alternative)

If you prefer using client secrets:

### Step 1: Create Service Principal with Secret

```bash
az ad sp create-for-rbac --name "github-actions-fantasy-football" --role contributor --scopes /subscriptions/your-subscription-id
```

### Step 2: Add Additional Secret

Add this secret to your GitHub repository:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `AZURE_CLIENT_SECRET` | Client secret from Step 1 | Service Principal secret |

### Step 3: Update Workflow

If using client secret method, update the Azure Login step in the workflow:

```yaml
- name: Azure Login
  uses: azure/login@v1
  with:
    creds: ${{ secrets.AZURE_CREDENTIALS }}
```

Where `AZURE_CREDENTIALS` is a JSON secret containing:
```json
{
  "clientId": "your-client-id",
  "clientSecret": "your-client-secret",
  "subscriptionId": "your-subscription-id",
  "tenantId": "your-tenant-id"
}
```

## Verification

To verify your setup works:

1. Go to your GitHub repository
2. Navigate to Actions → Run Scorito Agent
3. Click "Run workflow"
4. Check the logs for successful Azure authentication

## Troubleshooting

### Common Issues:

1. **Authentication failed**: Verify all secrets are correctly set
2. **Permission denied**: Ensure service principal has required roles
3. **Resource not found**: Check subscription ID and resource names
4. **Federated credential issues**: Verify the subject format matches your repository

### Debug Steps:

1. Check Azure CLI version in the workflow
2. Verify service principal permissions with `az role assignment list`
3. Test authentication locally with the same credentials
4. Review GitHub Actions logs for detailed error messages

## Security Best Practices

1. **Least Privilege**: Only grant minimum required permissions
2. **Resource Scoping**: Limit access to specific resource groups
3. **Regular Rotation**: Rotate secrets periodically
4. **Monitoring**: Set up alerts for service principal usage
5. **Federated Credentials**: Prefer OIDC over client secrets

## Additional Resources

- [Azure CLI documentation](https://docs.microsoft.com/en-us/cli/azure/)
- [GitHub Actions Azure integration](https://docs.github.com/en/actions/deployment/deploying-to-your-cloud-provider/deploying-to-azure)
- [Azure RBAC documentation](https://docs.microsoft.com/en-us/azure/role-based-access-control/)
