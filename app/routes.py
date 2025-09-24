# Copyright (c) 2025 Stratoware LLC. All rights reserved.

"""Main routes for the Pocket DHF application."""

import os
import re
import subprocess
from datetime import datetime, timedelta

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for

from app.data_utils import DHFDataManager

main = Blueprint("main", __name__)
data_manager = DHFDataManager()


@main.route("/")
def index():
    """Home page route."""
    try:
        # Load project metadata
        data = data_manager.load_data()
        project_metadata = data.get("metadata", {})

        # Get user info from git config
        user_info = get_git_user_info()

        return render_template(
            "index.html",
            title="Pocket DHF",
            project_metadata=project_metadata,
            user_info=user_info,
        )
    except Exception as e:
        flash(f"Error loading project data: {str(e)}", "error")
        return render_template(
            "index.html",
            title="Pocket DHF",
            project_metadata={},
            user_info={"name": "Unknown User"},
        )


def get_git_user_info():
    """Get user information from git config."""
    try:
        name_result = subprocess.run(
            ["git", "config", "user.name"], capture_output=True, text=True, timeout=5
        )
        email_result = subprocess.run(
            ["git", "config", "user.email"], capture_output=True, text=True, timeout=5
        )

        name = (
            name_result.stdout.strip()
            if name_result.returncode == 0
            else "Unknown User"
        )
        email = email_result.stdout.strip() if email_result.returncode == 0 else ""

        return {"name": name, "email": email}
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        return {"name": "Unknown User", "email": ""}


@main.route("/browse")
def browse():
    """Browse DHF data with tree navigation and editing."""
    try:
        # Load all data for the tree navigation
        user_needs = data_manager.get_user_needs()
        risks = data_manager.get_risks()
        product_requirements = data_manager.get_product_requirements()
        software_specifications = data_manager.get_software_specifications()
        hardware_specifications = data_manager.get_hardware_specifications()
        mitigation_links = data_manager.get_mitigation_links()
        linkable_items = data_manager.get_linkable_items()
        config = data_manager.get_configuration()
        user_info = get_git_user_info()

        # Calculate counts for display
        user_needs_count = len(user_needs)

        # Count risks
        risk_count = 0
        for group in risks.values():
            if isinstance(group, dict) and "risks" in group:
                risk_count += len(group["risks"])
            else:
                risk_count += 1

        # Count product requirements
        product_requirements_count = 0
        for group in product_requirements.values():
            if "requirements" in group:
                product_requirements_count += len(group["requirements"])

        # Count software specifications
        software_specifications_count = 0
        for group in software_specifications.values():
            if "specifications" in group:
                software_specifications_count += len(group["specifications"])

        # Count hardware specifications
        hardware_specifications_count = 0
        for group in hardware_specifications.values():
            if "specifications" in group:
                hardware_specifications_count += len(group["specifications"])

        return render_template(
            "browse.html",
            title="Browse DHF Data",
            user_needs=user_needs,
            risks=risks,
            product_requirements=product_requirements,
            software_specifications=software_specifications,
            hardware_specifications=hardware_specifications,
            mitigation_links=mitigation_links,
            linkable_items=linkable_items,
            config=config,
            user_info=user_info,
            user_needs_count=user_needs_count,
            risk_count=risk_count,
            product_requirements_count=product_requirements_count,
            software_specifications_count=software_specifications_count,
            hardware_specifications_count=hardware_specifications_count,
        )
    except Exception as e:
        flash(f"Error loading DHF data: {str(e)}", "error")
        return redirect(url_for("main.index"))


@main.route("/configuration")
def configuration():
    """Configuration page for managing dropdown options."""
    try:
        # Get current configuration
        config = data_manager.get_configuration()
        user_info = get_git_user_info()

        return render_template(
            "configuration.html",
            title="Configuration",
            config=config,
            user_info=user_info,
        )
    except Exception as e:
        flash(f"Error loading configuration: {str(e)}", "error")
        return redirect(url_for("main.index"))


@main.route("/reports")
def reports():
    """Reports page for generating and viewing DHF reports."""
    try:
        # Get available report templates
        report_templates = get_report_templates()
        user_info = get_git_user_info()

        return render_template(
            "reports.html",
            title="Reports",
            report_templates=report_templates,
            user_info=user_info,
        )
    except Exception as e:
        flash(f"Error loading reports: {str(e)}", "error")
        return redirect(url_for("main.index"))


@main.route("/api/report/<report_name>")
def generate_report(report_name):
    """API endpoint to generate a specific report."""
    try:
        report_content = generate_report_content(report_name)
        if report_content:
            return jsonify(report_content)
        else:
            return jsonify({"error": "Report not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route("/api/item/<item_id>")
def get_item(item_id):
    """API endpoint to get item details by ID."""
    try:
        item = data_manager.get_item_by_id(item_id)
        if item:
            return jsonify(item)
        else:
            return jsonify({"error": "Item not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route("/api/item/<item_id>", methods=["PUT"])
def update_item(item_id):
    """API endpoint to update item by ID."""
    try:
        updated_data = request.get_json()
        if data_manager.update_item(item_id, updated_data):
            return jsonify({"success": True, "message": "Item updated successfully"})
        else:
            return jsonify({"error": "Item not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route("/api/folder-name", methods=["PUT"])
def update_folder_name():
    """API endpoint to update folder/group names."""
    try:
        data = request.get_json()
        group_type = data.get("group_type")
        group_key = data.get("group_key")
        new_name = data.get("new_name")

        if not all([group_type, group_key, new_name]):
            return jsonify({"error": "Missing required parameters"}), 400

        if data_manager.update_folder_name(group_type, group_key, new_name):
            return jsonify(
                {"success": True, "message": "Folder name updated successfully"}
            )
        else:
            return jsonify({"error": "Folder not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route("/api/mitigation-link", methods=["PUT"])
def update_mitigation_link():
    """API endpoint to update mitigation link effect."""
    try:
        data = request.get_json()
        link_id = data.get("link_id")
        effect = data.get("effect")

        if not link_id or not effect:
            return jsonify({"error": "Missing required parameters"}), 400

        # Update the mitigation link in the data
        dhf_data = data_manager.load_data()
        if "mitigation_links" in dhf_data and link_id in dhf_data["mitigation_links"]:
            dhf_data["mitigation_links"][link_id]["effect"] = effect
            data_manager.save_data(dhf_data)
            return jsonify(
                {"success": True, "message": "Mitigation link updated successfully"}
            )
        else:
            return jsonify({"error": "Mitigation link not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route("/api/configuration", methods=["PUT"])
def update_configuration():
    """API endpoint to update configuration settings."""
    try:
        data = request.get_json()
        config_type = data.get("config_type")  # 'severity' or 'probability'
        action = data.get("action")  # 'add', 'remove', 'rename'

        if config_type not in ["severity", "probability"]:
            return jsonify({"error": "Invalid config_type"}), 400

        if action == "add":
            name = data.get("name")
            description = data.get("description", "")
            if not name:
                return jsonify({"error": "Name is required for add action"}), 400
            new_id = data_manager.add_config_option(config_type, name, description)
            return jsonify(
                {
                    "success": True,
                    "message": f"Added new {config_type} option",
                    "new_id": new_id,
                }
            )

        elif action == "remove":
            option_id = data.get("option_id")
            if not option_id:
                return (
                    jsonify({"error": "Option ID is required for remove action"}),
                    400,
                )
            result = data_manager.remove_config_option(config_type, option_id)

        elif action == "update":
            option_id = data.get("option_id")
            name = data.get("name")
            description = data.get("description", "")
            if not option_id or not name:
                return (
                    jsonify(
                        {"error": "Option ID and name are required for update action"}
                    ),
                    400,
                )
            result = data_manager.update_config_option(
                config_type, option_id, name, description
            )

        else:
            return jsonify({"error": "Invalid action"}), 400

        if result:
            return jsonify(
                {"success": True, "message": "Configuration updated successfully"}
            )
        else:
            return jsonify({"error": "Failed to update configuration"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "pocket-dhf"}


def get_report_templates():
    """Get list of available report templates."""
    templates_dir = "sample-data/report-templates"
    templates = []

    if os.path.exists(templates_dir):
        for filename in os.listdir(templates_dir):
            if filename.endswith(".md"):
                template_name = filename[:-3]  # Remove .md extension
                template_path = os.path.join(templates_dir, filename)

                # Read the first few lines to get title and description
                try:
                    with open(template_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        lines = content.split("\n")
                        title = lines[0].strip("# ") if lines else template_name

                        # Extract description from purpose section
                        description = "Report template"
                        for i, line in enumerate(lines):
                            if line.strip() == "## Purpose":
                                if i + 2 < len(lines):
                                    description = lines[i + 2].strip()
                                break

                        templates.append(
                            {
                                "name": template_name,
                                "title": title,
                                "description": description,
                                "filename": filename,
                            }
                        )
                except Exception as e:
                    print(f"Error reading template {filename}: {e}")

    return templates


def generate_report_content(report_name):
    """Generate report content by processing template and inserting DHF data."""
    templates_dir = "sample-data/report-templates"
    template_path = os.path.join(templates_dir, f"{report_name}.md")

    if not os.path.exists(template_path):
        return None

    try:
        # Read template
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        # Get project metadata
        data = data_manager.load_data()
        metadata = data.get("metadata", {})

        # Replace template variables
        template_vars = {
            "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "project_name": metadata.get("project_name", "Unknown Project"),
            "device_type": metadata.get("device_type", "Unknown Device"),
            "version": metadata.get("version", "1.0"),
            "next_review_date": (datetime.now() + timedelta(days=90)).strftime(
                "%Y-%m-%d"
            ),
        }

        # Replace template variables
        for var, value in template_vars.items():
            template_content = template_content.replace("{{" + var + "}}", str(value))

        # Process AUTO_CONTENT tags
        template_content = process_auto_content(template_content, data)

        return {
            "title": template_vars["project_name"],
            "content": template_content,
            "generated_date": template_vars["generation_date"],
        }

    except Exception as e:
        print(f"Error generating report {report_name}: {e}")
        return None


def process_auto_content(content, data):
    """Process AUTO_CONTENT tags and replace with generated tables."""

    # Find all AUTO_CONTENT tags
    auto_content_pattern = r"<!-- AUTO_CONTENT: (\w+) -->"

    def replace_auto_content(match):
        content_type = match.group(1)

        if content_type == "user_needs_table":
            return generate_user_needs_table(data)
        elif content_type == "product_requirements_tables":
            return generate_product_requirements_tables(data)
        elif content_type == "software_specifications_tables":
            return generate_software_specifications_tables(data)
        elif content_type == "hardware_specifications_tables":
            return generate_hardware_specifications_tables(data)
        elif content_type == "traceability_matrix":
            return generate_traceability_matrix(data)
        elif content_type == "performance_summary":
            return generate_performance_summary(data)
        else:
            return f"*[{content_type} content would be generated here]*"

    return re.sub(auto_content_pattern, replace_auto_content, content)


def generate_user_needs_table(data):
    """Generate markdown table for user needs."""
    user_needs = data.get("user_needs", {})

    if not user_needs:
        return "*No user needs defined.*"

    table = "| ID | Title | Description |\n"
    table += "|----|----- |-------------|\n"

    for need_id, need in user_needs.items():
        title = need.get("title", "Untitled").replace("|", "\\|")
        description = need.get("description", "No description").replace("|", "\\|")
        # Truncate description if too long
        if len(description) > 100:
            description = description[:97] + "..."
        table += f"| {need_id} | {title} | {description} |\n"

    return table


def generate_product_requirements_tables(data):
    """Generate markdown tables for product requirements by group."""
    product_requirements = data.get("product_requirements", {})

    if not product_requirements:
        return "*No product requirements defined.*"

    output = ""

    for group_key, group in product_requirements.items():
        group_name = group.get("group_name", group_key)
        requirements = group.get("requirements", {})

        if requirements:
            output += f"### {group_name}\n\n"
            output += "| ID | Title | Description | Linked User Needs |\n"
            output += "|----|-------|-------------|-------------------|\n"

            for req_id, req in requirements.items():
                title = req.get("title", "Untitled").replace("|", "\\|")
                description = req.get("description", "No description").replace(
                    "|", "\\|"
                )
                if len(description) > 80:
                    description = description[:77] + "..."

                linked_needs = req.get("linked_user_needs", [])
                linked_str = ", ".join(linked_needs) if linked_needs else "None"

                output += f"| {req_id} | {title} | {description} | {linked_str} |\n"

            output += "\n"

    return output


def generate_software_specifications_tables(data):
    """Generate markdown tables for software specifications by group."""
    software_specs = data.get("software_specifications", {})

    if not software_specs:
        return "*No software specifications defined.*"

    output = ""

    for group_key, group in software_specs.items():
        group_name = group.get("group_name", group_key)
        specifications = group.get("specifications", {})

        if specifications:
            output += f"### {group_name}\n\n"
            output += "| ID | Title | Description | Linked Requirements |\n"
            output += "|----|-------|-------------|--------------------|\n"

            for spec_id, spec in specifications.items():
                title = spec.get("title", "Untitled").replace("|", "\\|")
                description = spec.get("description", "No description").replace(
                    "|", "\\|"
                )
                if len(description) > 80:
                    description = description[:77] + "..."

                linked_reqs = spec.get("linked_product_requirements", [])
                linked_str = ", ".join(linked_reqs) if linked_reqs else "None"

                output += f"| {spec_id} | {title} | {description} | {linked_str} |\n"

            output += "\n"

    return output


def generate_hardware_specifications_tables(data):
    """Generate markdown tables for hardware specifications by group."""
    hardware_specs = data.get("hardware_specifications", {})

    if not hardware_specs:
        return "*No hardware specifications defined.*"

    output = ""

    for group_key, group in hardware_specs.items():
        group_name = group.get("group_name", group_key)
        specifications = group.get("specifications", {})

        if specifications:
            output += f"### {group_name}\n\n"
            output += "| ID | Title | Description | Linked Requirements |\n"
            output += "|----|-------|-------------|--------------------|\n"

            for spec_id, spec in specifications.items():
                title = spec.get("title", "Untitled").replace("|", "\\|")
                description = spec.get("description", "No description").replace(
                    "|", "\\|"
                )
                if len(description) > 80:
                    description = description[:77] + "..."

                linked_reqs = spec.get("linked_product_requirements", [])
                linked_str = ", ".join(linked_reqs) if linked_reqs else "None"

                output += f"| {spec_id} | {title} | {description} | {linked_str} |\n"

            output += "\n"

    return output


def generate_traceability_matrix(data):
    """Generate traceability matrix showing relationships."""
    output = "| User Need | Product Requirements | Software Specs | Hardware Specs |\n"
    output += "|-----------|---------------------|----------------|----------------|\n"

    user_needs = data.get("user_needs", {})
    product_requirements = data.get("product_requirements", {})

    for need_id, need in user_needs.items():
        need_title = need.get("title", need_id)

        # Find linked requirements
        linked_reqs = []
        linked_sw_specs = []
        linked_hw_specs = []

        for group_key, group in product_requirements.items():
            for req_id, req in group.get("requirements", {}).items():
                if need_id in req.get("linked_user_needs", []):
                    linked_reqs.append(req_id)

        req_str = ", ".join(linked_reqs) if linked_reqs else "None"
        sw_str = ", ".join(linked_sw_specs) if linked_sw_specs else "None"
        hw_str = ", ".join(linked_hw_specs) if linked_hw_specs else "None"

        output += f"| {need_title} | {req_str} | {sw_str} | {hw_str} |\n"

    return output


def generate_performance_summary(data):
    """Generate performance requirements summary."""
    return "*Performance requirements would be extracted from specifications and presented in tabular format.*"
