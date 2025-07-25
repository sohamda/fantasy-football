# GitHub Workflows

This directory contains GitHub Actions workflows for the Fantasy Football project.

## Available Workflows

### Run Scorito Agent (`run-scorito-agent.yml`)

This workflow can be manually triggered to run the Scorito Agent for player data extraction.

#### How to Run

1. Go to the **Actions** tab in your GitHub repository
2. Select **Run Scorito Agent** from the workflow list
3. Click **Run workflow**
4. Configure the optional parameters:
   - **Log level**: Choose the logging verbosity (DEBUG, INFO, WARNING, ERROR)
   - **Dry run**: Enable to run without actual processing

#### Required Secrets

Before running this workflow, you need to set up the following repository secrets in your GitHub repository settings:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add the following secrets:

| Secret Name | Description |
|-------------|-------------|
| `AZURE_OPENAI_API_KEY` | Your Azure OpenAI API key |
| `AZURE_OPENAI_ENDPOINT` | Your Azure OpenAI endpoint URL |
| `COSMOS_DB_CONNECTION_STRING` | Connection string for Azure Cosmos DB |
| `LOG_ANALYTICS_WORKSPACE_ID` | Azure Log Analytics workspace ID |
| `LOG_ANALYTICS_SHARED_KEY` | Azure Log Analytics shared key |
| `BING_SEARCH_API_KEY` | Bing Search API key |

#### What the Workflow Does

1. **Setup**: Checks out the code and sets up Python 3.12
2. **Dependencies**: Installs required Python packages from `requirements.txt`
3. **Configuration**: Sets up environment variables based on input parameters
4. **Execution**: Runs the `main.py` script in the scoritoAgent directory
5. **Artifacts**: Uploads any generated logs as workflow artifacts

#### Output

- The workflow will show the execution logs in the GitHub Actions interface
- Any log files generated during execution will be uploaded as artifacts
- Artifacts are retained for 7 days and can be downloaded from the workflow run page

#### Troubleshooting

- **Missing secrets**: Ensure all required secrets are configured in repository settings
- **Permission errors**: Check that the workflow has the necessary permissions
- **Dependency issues**: Verify that `requirements.txt` contains all necessary packages
- **Runtime errors**: Check the workflow logs for detailed error messages

#### Customization

You can modify the workflow by:
- Adding more input parameters in the `workflow_dispatch` section
- Adjusting the Python version or runner OS
- Adding additional setup steps or post-processing
- Modifying environment variables or secrets
