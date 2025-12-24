"""
Prefect Proof of Concept: GitHub Actions to GitLab CI Workflow

This flow demonstrates workflow-to-workflow integration using Prefect.
"""

from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
import requests
import os
from dotenv import load_dotenv

load_dotenv()

@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(minutes=5))
def check_github_actions_status(repo: str, run_id: str) -> dict:
    """
    Check GitHub Actions workflow run status
    
    Args:
        repo: Repository in format 'owner/repo'
        run_id: GitHub Actions run ID
        
    Returns:
        Dictionary with workflow run status
    """
    token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }
    
    response = requests.get(
        f"https://api.github.com/repos/{repo}/actions/runs/{run_id}",
        headers=headers,
        timeout=10
    )
    response.raise_for_status()
    return response.json()

@task
def trigger_gitlab_ci(project_id: str, ref: str = "main", variables: dict = None) -> dict:
    """
    Trigger GitLab CI pipeline
    
    Args:
        project_id: GitLab project ID
        ref: Branch or tag to trigger
        variables: Optional CI/CD variables
        
    Returns:
        Dictionary with pipeline information
    """
    token = os.getenv("GITLAB_TOKEN")
    url = f"https://gitlab.com/api/v4/projects/{project_id}/trigger/pipeline"
    
    data = {
        "ref": ref,
        "token": token
    }
    
    if variables:
        data["variables"] = variables
    
    response = requests.post(url, data=data, timeout=30)
    response.raise_for_status()
    return response.json()

@task
def send_notification(message: str, status: str = "success"):
    """
    Send notification (e.g., to Slack, Discord)
    
    Args:
        message: Notification message
        status: Status (success, failure, info)
    """
    # Example: Slack webhook
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print(f"Notification: {status.upper()} - {message}")
        return
    
    payload = {
        "text": f"{status.upper()}: {message}",
        "username": "Workflow Orchestrator"
    }
    
    try:
        requests.post(webhook_url, json=payload, timeout=10)
    except Exception as e:
        print(f"Failed to send notification: {e}")

@flow(name="github-to-gitlab-workflow", log_prints=True)
def github_to_gitlab_workflow(
    github_repo: str,
    github_run_id: str,
    gitlab_project_id: str,
    gitlab_ref: str = "main"
) -> dict:
    """
    Main workflow: GitHub Actions → GitLab CI
    
    Args:
        github_repo: GitHub repository (owner/repo)
        github_run_id: GitHub Actions run ID
        gitlab_project_id: GitLab project ID
        gitlab_ref: GitLab branch/tag to trigger
        
    Returns:
        Dictionary with workflow result
    """
    print(f"Checking GitHub Actions status for {github_repo} run {github_run_id}")
    
    # Check GitHub Actions status
    github_status = check_github_actions_status(github_repo, github_run_id)
    
    status = github_status.get("status")
    conclusion = github_status.get("conclusion")
    
    print(f"GitHub Actions status: {status}, conclusion: {conclusion}")
    
    if status == "completed" and conclusion == "success":
        # Trigger GitLab CI
        print(f"Triggering GitLab CI for project {gitlab_project_id}")
        
        variables = {
            "GITHUB_REF": github_status.get("head_branch", gitlab_ref),
            "GITHUB_SHA": github_status.get("head_sha", "")
        }
        
        gitlab_result = trigger_gitlab_ci(
            project_id=gitlab_project_id,
            ref=gitlab_ref,
            variables=variables
        )
        
        pipeline_id = gitlab_result.get("id")
        print(f"GitLab CI pipeline triggered: {pipeline_id}")
        
        # Send notification
        send_notification(
            f"GitLab CI pipeline {pipeline_id} triggered successfully",
            "success"
        )
        
        return {
            "success": True,
            "gitlab_pipeline_id": pipeline_id,
            "github_run_id": github_run_id
        }
    else:
        message = f"GitHub Actions not completed or not successful (status: {status}, conclusion: {conclusion})"
        print(message)
        
        send_notification(message, "info")
        
        return {
            "success": False,
            "reason": message,
            "github_run_id": github_run_id
        }

if __name__ == "__main__":
    # Example usage
    result = github_to_gitlab_workflow(
        github_repo="owner/repo",
        github_run_id="123456789",
        gitlab_project_id="12345",
        gitlab_ref="main"
    )
    print(f"Workflow result: {result}")

