#!/usr/bin/env python3
"""
GPT-Researcher HTTP API Test Client
This script demonstrates how to use the FastAPI endpoints for GPT-Researcher.

Usage:
    python tutorial_poc.py

The API server should be running at http://localhost:11250
"""

import json
import os
import time
import requests
from typing import Dict, List, Any, Optional


class GPTResearcherClient:
    """Client for interacting with the GPT-Researcher FastAPI server."""

    def __init__(self, base_url: str = "http://localhost:11250"):
        """
        Initialize the client with the server URL.

        Args:
            base_url: The base URL of the GPT-Researcher server
        """
        self.base_url = base_url
        self.session = requests.Session()

    def health_check(self) -> Dict[str, Any]:
        """Check if the server is running."""
        response = self.session.get(f"{self.base_url}/")
        return {"status": response.status_code, "headers": dict(response.headers)}

    def get_reports(self, report_ids: Optional[str] = None) -> Dict[str, Any]:
        """
        Get all reports or specific reports by ID.

        Args:
            report_ids: Comma-separated list of report IDs (optional)

        Returns:
            Dictionary containing the reports
        """
        url = f"{self.base_url}/api/reports"
        if report_ids:
            url += f"?report_ids={report_ids}"
        response = self.session.get(url)
        return response.json()

    def get_report_by_id(self, research_id: str) -> Dict[str, Any]:
        """
        Get a specific report by ID.

        Args:
            research_id: The ID of the report to retrieve

        Returns:
            Dictionary containing the report
        """
        response = self.session.get(f"{self.base_url}/api/reports/{research_id}")
        return response.json()

    def create_report(
        self,
        task: str,
        report_type: str = "research_report",
        report_source: str = "web",
        tone: str = "objective",
        headers: Optional[Dict] = None,
        repo_name: str = "default",
        branch_name: str = "main",
        generate_in_background: bool = True,
    ) -> Dict[str, Any]:
        """
        Create a new research report.

        Args:
            task: The research task/query
            report_type: Type of report (e.g., research_report, detailed_report)
            report_source: Source of information (web, local, hybrid, etc.)
            tone: Tone of the report (objective, formal, etc.)
            headers: Additional headers for the request
            repo_name: Name of the repository to use
            branch_name: Branch name to use
            generate_in_background: Whether to generate in background

        Returns:
            Dictionary with the report ID and status message
        """
        payload = {
            "task": task,
            "report_type": report_type,
            "report_source": report_source,
            "tone": tone,
            "headers": headers,
            "repo_name": repo_name,
            "branch_name": branch_name,
            "generate_in_background": generate_in_background,
        }

        response = self.session.post(
            f"{self.base_url}/report/",
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        return response.json()

    def update_report(self, research_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing report.

        Args:
            research_id: The ID of the report to update
            data: Dictionary containing the data to update

        Returns:
            Dictionary with update status
        """
        response = self.session.put(
            f"{self.base_url}/api/reports/{research_id}",
            json=data,
        )
        return response.json()

    def delete_report(self, research_id: str) -> Dict[str, Any]:
        """
        Delete a report.

        Args:
            research_id: The ID of the report to delete

        Returns:
            Dictionary with deletion status
        """
        response = self.session.delete(f"{self.base_url}/api/reports/{research_id}")
        return response.json()

    def get_report_chat(self, research_id: str) -> Dict[str, Any]:
        """
        Get chat messages for a report.

        Args:
            research_id: The ID of the report

        Returns:
            Dictionary containing chat messages
        """
        response = self.session.get(
            f"{self.base_url}/api/reports/{research_id}/chat"
        )
        return response.json()

    def add_chat_message(
        self, research_id: str, message: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Add a message to a report's chat history.

        Args:
            research_id: The ID of the report
            message: The message to add

        Returns:
            Dictionary with success status
        """
        response = self.session.post(
            f"{self.base_url}/api/reports/{research_id}/chat",
            json=message,
        )
        return response.json()

    def chat(
        self, report: str, messages: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Process a chat request with a report and message history.

        Args:
            report: The report text to chat about
            messages: List of message dictionaries with role and content

        Returns:
            Dictionary with assistant response
        """
        payload = {"report": report, "messages": messages}
        response = self.session.post(
            f"{self.base_url}/api/chat",
            json=payload,
        )
        return response.json()

    def list_files(self, doc_path: str = "./my-docs") -> Dict[str, Any]:
        """
        List files in a document directory.

        Args:
            doc_path: Path to the document directory

        Returns:
            Dictionary containing list of files
        """
        response = self.session.get(
            f"{self.base_url}/files/", params={"path": doc_path}
        )
        return response.json()

    def upload_file(self, file_path: str, doc_path: str = "./my-docs") -> Dict[str, Any]:
        """
        Upload a file to the document directory.

        Args:
            file_path: Path to the file to upload
            doc_path: Target directory path

        Returns:
            Dictionary with upload result
        """
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            response = self.session.post(
                f"{self.base_url}/upload/", files=files, params={"path": doc_path}
            )
        return response.json()

    def delete_file(self, filename: str, doc_path: str = "./my-docs") -> Dict[str, Any]:
        """
        Delete a file from the document directory.

        Args:
            filename: Name of the file to delete
            doc_path: Path to the document directory

        Returns:
            Dictionary with deletion result
        """
        response = self.session.delete(
            f"{self.base_url}/files/{filename}", params={"path": doc_path}
        )
        return response.json()

    def get_report_docx(self, research_id: str) -> Optional[bytes]:
        """
        Download a report as DOCX file.

        Args:
            research_id: The ID of the report

        Returns:
            DOCX file content as bytes, or None if not found
        """
        response = self.session.get(
            f"{self.base_url}/report/{research_id}", stream=True
        )
        if response.status_code == 200:
            return response.content
        return None


def demo_create_report(client: GPTResearcherClient) -> str:
    """
    Demonstrate creating a research report.

    Args:
        client: GPTResearcherClient instance

    Returns:
        The research ID of the created report
    """
    print("\n=== Creating a Research Report ===")
    print("This will create a new research task.")

    # Example: Create a research report about AI trends
    task = "What are the latest developments in large language models in 2024?"
    print(f"Task: {task}")

    response = client.create_report(
        task=task,
        report_type="research_report",
        report_source="web",
        tone="objective",
        generate_in_background=True,
    )

    print(f"Response: {json.dumps(response, indent=2)}")

    if "research_id" in response:
        return response["research_id"]
    return None


def demo_chat(client: GPTResearcherClient, report: str, research_id: str) -> None:
    """
    Demonstrate chat functionality with a report.

    Args:
        client: GPTResearcherClient instance
        report: The report text to chat about
        research_id: ID of the report
    """
    print("\n=== Chat with Report ===")
    print("This will chat about the report content.")

    messages = [
        {"role": "user", "content": "What is this report about?"},
        {"role": "assistant", "content": "This report covers the latest developments in large language models in 2024."},
        {"role": "user", "content": "Can you summarize the key points?"},
    ]

    response = client.chat(report=report, messages=messages)
    print(f"Response: {json.dumps(response, indent=2)}")


def demo_list_reports(client: GPTResearcherClient) -> None:
    """Demonstrate listing all reports."""
    print("\n=== Listing Reports ===")
    response = client.get_reports()
    print(f"Reports: {json.dumps(response, indent=2)}")


def demo_get_report(client: GPTResearcherClient, research_id: str) -> None:
    """Demonstrate getting a specific report."""
    print(f"\n=== Getting Report: {research_id} ===")
    response = client.get_report_by_id(research_id)
    print(f"Report: {json.dumps(response, indent=2)}")


def main():
    """Main function to demonstrate all API endpoints."""
    # Server URL (change if using a different port or host)
    base_url = os.getenv("GPTR_API_URL", "http://localhost:11250")
    print(f"Connecting to GPT-Researcher server at {base_url}")

    # Initialize the client
    client = GPTResearcherClient(base_url)

    # Check server health
    print("\n=== Health Check ===")
    health = client.health_check()
    print(f"Server Status: {health}")

    # Demo: List reports (empty initially)
    demo_list_reports(client)

    # Demo: Create a report
    research_id = demo_create_report(client)

    if research_id:
        print(f"\nReport created with ID: {research_id}")

        # Demo: Get the report by ID
        # Note: This may fail if the report is still being generated
        # time.sleep(5)  # Wait for background generation
        # demo_get_report(client, research_id)

        # Demo: List reports again
        demo_list_reports(client)

        # Demo: Delete the report (optional cleanup)
        # print(f"\n=== Deleting Report: {research_id} ===")
        # delete_response = client.delete_report(research_id)
        # print(f"Delete Response: {json.dumps(delete_response, indent=2)}")
    else:
        print("\nFailed to create report. Check the server logs for more information.")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()
