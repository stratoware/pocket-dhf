# Security Policy

## Supported Versions

We release patches for security vulnerabilities. The following table shows which versions are currently being supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of pocket-dhf seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Please Do Not:

- Open a public GitHub issue for security vulnerabilities
- Disclose the vulnerability publicly before it has been addressed

### Please Do:

**Report security vulnerabilities privately using one of the following methods:**

1. **GitHub Security Advisories (Recommended)**
   - Navigate to the "Security" tab of this repository
   - Click "Report a vulnerability"
   - Fill out the vulnerability details form
   - Submit the report

2. **Email**
   - Send an email to the project maintainers (contact information can be found in the repository)
   - Include as much information as possible (see details below)

### What to Include in Your Report

To help us understand and resolve the issue quickly, please include the following information:

- **Type of vulnerability** (e.g., SQL injection, XSS, unauthorized access)
- **Full paths of source file(s)** related to the vulnerability
- **Location of the affected source code** (tag/branch/commit or direct URL)
- **Step-by-step instructions** to reproduce the issue
- **Proof-of-concept or exploit code** (if possible)
- **Impact of the vulnerability** and how an attacker might exploit it
- **Any potential mitigations** you've identified

### What to Expect

After you submit a vulnerability report, you can expect:

- **Initial Response**: Within 48-72 hours acknowledging receipt of your report
- **Assessment**: We will investigate and validate the vulnerability
- **Updates**: Regular updates on the progress of fixing the vulnerability
- **Resolution Timeline**: Most vulnerabilities will be addressed within 90 days
- **Credit**: If you wish, we will credit you in the security advisory and release notes

### Security Update Process

1. The vulnerability is received and assigned to a primary handler
2. The problem is confirmed and affected versions are identified
3. Code is audited to find any similar problems
4. Fixes are prepared for all supported releases
5. Fixes are released and a security advisory is published

## Security Best Practices for Users

When using pocket-dhf, we recommend:

- Keep your installation up to date with the latest version
- Review and follow the security guidelines in the documentation
- Use strong authentication mechanisms when deploying in production
- Regularly backup your data
- Monitor logs for suspicious activity
- Run the application with minimal required privileges

## Disclosure Policy

We follow the principle of **Coordinated Vulnerability Disclosure**:

- Vulnerabilities will be disclosed publicly only after:
  - A fix has been developed and released
  - Users have been given reasonable time to update (typically 30 days)
  - The reporter has been consulted on the disclosure timeline

## Comments on This Policy

If you have suggestions on how this process could be improved, please submit a pull request or open an issue to discuss.

---

Thank you for helping keep pocket-dhf and its users safe!

