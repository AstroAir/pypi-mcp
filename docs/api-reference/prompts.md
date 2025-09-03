# Prompts Reference

Complete reference for PyPI MCP Server prompts that provide structured templates for AI analysis tasks.

## Overview

Prompts in the PyPI MCP Server provide structured templates that guide AI models in performing comprehensive analysis tasks. These prompts are designed to generate detailed, actionable insights about Python packages.

The server provides 3 prompts:

1. **analyze_package** - Comprehensive package analysis
2. **compare_packages** - Package comparison analysis
3. **security_review** - Security-focused review

## Prompt Access

### Protocol

Prompts are accessed using the `prompts/get` method:

```json
{
  "jsonrpc": "2.0",
  "method": "prompts/get",
  "params": {
    "name": "analyze_package",
    "arguments": {
      "package_name": "requests"
    }
  },
  "id": 1
}
```

### Response Format

```json
{
  "jsonrpc": "2.0",
  "result": {
    "description": "Generate a comprehensive package analysis prompt",
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Please analyze the PyPI package 'requests'..."
        }
      }
    ]
  },
  "id": 1
}
```

## Available Prompts

### analyze_package

Generate a comprehensive package analysis prompt for detailed evaluation.

#### Parameters

| Parameter      | Type     | Required | Default | Description                                           |
| -------------- | -------- | -------- | ------- | ----------------------------------------------------- |
| `package_name` | `string` | Yes      | -       | Name of the package to analyze                        |
| `version`      | `string` | No       | `null`  | Specific version to analyze (latest if not specified) |

#### Generated Prompt

The prompt asks the AI to analyze the package considering:

1. **Package Purpose and Functionality**

   - What the package does
   - Primary use cases
   - Target audience

2. **Maintenance Status and Community Health**

   - Development activity
   - Community engagement
   - Maintainer responsiveness

3. **Security Considerations**

   - Known vulnerabilities
   - Security track record
   - Security best practices

4. **Dependencies and Implications**

   - Dependency tree analysis
   - Potential conflicts
   - Maintenance burden

5. **Compatibility**

   - Python version support
   - Platform compatibility
   - Breaking changes

6. **Documentation Quality**

   - Documentation completeness
   - Examples and tutorials
   - API reference quality

7. **Project Maturity**

   - Development stage
   - Stability indicators
   - Long-term viability

8. **Alternative Packages**

   - Similar packages
   - Comparative advantages
   - Migration considerations

9. **Usage Recommendations**
   - When to use
   - When to avoid
   - Best practices

#### Example Usage

=== "MCP Prompt Call"
`json
    {
      "jsonrpc": "2.0",
      "method": "prompts/get",
      "params": {
        "name": "analyze_package",
        "arguments": {
          "package_name": "fastapi",
          "version": "0.104.1"
        }
      },
      "id": 1
    }
    `

=== "Natural Language"
`    Generate a comprehensive analysis prompt for FastAPI version 0.104.1
   `

#### Sample Generated Prompt

```
Please analyze the PyPI package 'fastapi' version 0.104.1.

Consider the following aspects:
1. Package purpose and functionality
2. Maintenance status and community health
3. Security considerations and known vulnerabilities
4. Dependencies and their implications
5. Compatibility with different Python versions
6. Documentation quality and project maturity
7. Alternative packages and comparisons
8. Recommendations for usage

Use the available PyPI tools to gather detailed information about this package.
```

### compare_packages

Generate a package comparison prompt for technology selection decisions.

#### Parameters

| Parameter  | Type     | Required | Default | Description               |
| ---------- | -------- | -------- | ------- | ------------------------- |
| `package1` | `string` | Yes      | -       | First package to compare  |
| `package2` | `string` | Yes      | -       | Second package to compare |

#### Generated Prompt

The prompt asks the AI to compare packages across:

1. **Functionality and Feature Sets**

   - Core capabilities
   - Feature completeness
   - Unique features

2. **Performance Characteristics**

   - Speed and efficiency
   - Resource usage
   - Scalability

3. **Community Adoption and Popularity**

   - Download statistics
   - Community size
   - Industry adoption

4. **Maintenance and Development Activity**

   - Release frequency
   - Bug fix responsiveness
   - Feature development

5. **Security Track Record**

   - Vulnerability history
   - Security practices
   - Response to security issues

6. **Documentation Quality**

   - Documentation completeness
   - Learning resources
   - Community tutorials

7. **Dependencies and Ecosystem Impact**

   - Dependency requirements
   - Ecosystem integration
   - Compatibility

8. **Learning Curve and Ease of Use**

   - API design
   - Getting started experience
   - Development productivity

9. **License Compatibility**

   - License types
   - Commercial use
   - Legal considerations

10. **Use Case Recommendations**
    - When to choose each package
    - Specific scenarios
    - Migration considerations

#### Example Usage

=== "MCP Prompt Call"
`json
    {
      "jsonrpc": "2.0",
      "method": "prompts/get",
      "params": {
        "name": "compare_packages",
        "arguments": {
          "package1": "fastapi",
          "package2": "flask"
        }
      },
      "id": 1
    }
    `

=== "Natural Language"
`    Generate a comparison prompt for FastAPI vs Flask
   `

#### Sample Generated Prompt

```
Please compare the PyPI packages 'fastapi' and 'flask'.

Analyze and compare:
1. Functionality and feature sets
2. Performance characteristics
3. Community adoption and popularity
4. Maintenance and development activity
5. Security track record
6. Documentation quality
7. Dependencies and ecosystem impact
8. Learning curve and ease of use
9. License compatibility
10. Recommendations for different use cases

Use the PyPI tools to gather comprehensive information about both packages.
```

### security_review

Generate a security review prompt for comprehensive security assessment.

#### Parameters

| Parameter      | Type     | Required | Default | Description                   |
| -------------- | -------- | -------- | ------- | ----------------------------- |
| `package_name` | `string` | Yes      | -       | Name of the package to review |

#### Generated Prompt

The prompt asks the AI to conduct a security review focusing on:

1. **Known Vulnerabilities and CVEs**

   - Current vulnerability status
   - Historical security issues
   - Severity assessment

2. **Dependency Security Analysis**

   - Vulnerable dependencies
   - Transitive vulnerabilities
   - Dependency update practices

3. **Package Integrity and Authenticity**

   - Package signing
   - Source verification
   - Supply chain security

4. **Maintenance Status and Update Frequency**

   - Security patch responsiveness
   - Maintenance activity
   - End-of-life considerations

5. **Security Best Practices in Codebase**

   - Code quality indicators
   - Security-focused development
   - Testing practices

6. **Trust Indicators**

   - Maintainer reputation
   - Project maturity
   - Community oversight

7. **Potential Security Risks and Mitigations**

   - Risk assessment
   - Mitigation strategies
   - Monitoring recommendations

8. **Recommendations for Secure Usage**
   - Security configuration
   - Best practices
   - Monitoring and updates

#### Example Usage

=== "MCP Prompt Call"
`json
    {
      "jsonrpc": "2.0",
      "method": "prompts/get",
      "params": {
        "name": "security_review",
        "arguments": {
          "package_name": "django"
        }
      },
      "id": 1
    }
    `

=== "Natural Language"
`    Generate a security review prompt for Django
   `

#### Sample Generated Prompt

```
Please conduct a security review of the PyPI package 'django'.

Focus on:
1. Known vulnerabilities and CVEs
2. Dependency security analysis
3. Package integrity and authenticity
4. Maintenance status and update frequency
5. Security best practices in the codebase
6. Trust indicators (maintainer reputation, project maturity)
7. Potential security risks and mitigations
8. Recommendations for secure usage

Use the vulnerability checking and package analysis tools to gather security-relevant information.
```

## Prompt Listing

### List Available Prompts

Get a list of all available prompts:

```json
{
  "jsonrpc": "2.0",
  "method": "prompts/list",
  "params": {},
  "id": 1
}
```

#### Response

```json
{
  "jsonrpc": "2.0",
  "result": {
    "prompts": [
      {
        "name": "analyze_package",
        "description": "Generate a comprehensive package analysis prompt",
        "arguments": [
          {
            "name": "package_name",
            "description": "Name of the package to analyze",
            "required": true
          },
          {
            "name": "version",
            "description": "Specific version to analyze",
            "required": false
          }
        ]
      },
      {
        "name": "compare_packages",
        "description": "Generate a package comparison prompt",
        "arguments": [
          {
            "name": "package1",
            "description": "First package to compare",
            "required": true
          },
          {
            "name": "package2",
            "description": "Second package to compare",
            "required": true
          }
        ]
      },
      {
        "name": "security_review",
        "description": "Generate a security review prompt for a package",
        "arguments": [
          {
            "name": "package_name",
            "description": "Name of the package to review",
            "required": true
          }
        ]
      }
    ]
  },
  "id": 1
}
```

## Error Handling

### Error Response Format

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": {
      "parameter": "package_name",
      "details": "Package name is required"
    }
  },
  "id": 1
}
```

### Common Errors

| Error Code | Description        | Example                        |
| ---------- | ------------------ | ------------------------------ |
| `-32601`   | Prompt not found   | Invalid prompt name            |
| `-32602`   | Invalid parameters | Missing required parameter     |
| `-32603`   | Internal error     | Server error generating prompt |

## Use Cases

### AI-Assisted Package Evaluation

Use prompts to guide AI analysis:

```python
async def evaluate_package(package_name):
    """Get AI analysis of a package."""
    # Get analysis prompt
    prompt = await client.get_prompt("analyze_package", {
        "package_name": package_name
    })

    # Send to AI model for analysis
    analysis = await ai_model.complete(prompt['messages'][0]['content']['text'])

    return analysis
```

### Technology Selection

Compare packages for decision making:

```python
async def compare_for_selection(package1, package2):
    """Compare packages for technology selection."""
    prompt = await client.get_prompt("compare_packages", {
        "package1": package1,
        "package2": package2
    })

    comparison = await ai_model.complete(prompt['messages'][0]['content']['text'])

    return comparison
```

### Security Assessment

Conduct security reviews:

```python
async def security_assessment(package_name):
    """Conduct security assessment of a package."""
    prompt = await client.get_prompt("security_review", {
        "package_name": package_name
    })

    review = await ai_model.complete(prompt['messages'][0]['content']['text'])

    return review
```

## Best Practices

### Prompt Usage

- **Combine with Tools**: Use prompts alongside PyPI tools for comprehensive analysis
- **Iterative Analysis**: Use prompts to guide multi-step analysis processes
- **Context Awareness**: Provide additional context when using prompts

### Parameter Validation

- **Required Parameters**: Always provide required parameters
- **Package Names**: Validate package names before using in prompts
- **Version Specifications**: Use valid version strings when specified

### Integration Patterns

- **Structured Analysis**: Use prompts to ensure consistent analysis structure
- **Documentation Generation**: Generate documentation using prompt-guided analysis
- **Decision Support**: Use comparison prompts for technology decisions

## Integration Examples

### Claude Desktop

Prompts work seamlessly with Claude Desktop:

```
Use the analyze_package prompt to evaluate the requests library
```

### Custom AI Applications

```python
class PackageAnalyzer:
    def __init__(self, mcp_client, ai_client):
        self.mcp = mcp_client
        self.ai = ai_client

    async def analyze(self, package_name, version=None):
        """Perform comprehensive package analysis."""
        # Get structured prompt
        prompt_response = await self.mcp.get_prompt("analyze_package", {
            "package_name": package_name,
            "version": version
        })

        prompt_text = prompt_response['messages'][0]['content']['text']

        # Get AI analysis
        analysis = await self.ai.complete(prompt_text)

        return {
            "package": package_name,
            "version": version,
            "prompt": prompt_text,
            "analysis": analysis
        }

    async def compare(self, package1, package2):
        """Compare two packages."""
        prompt_response = await self.mcp.get_prompt("compare_packages", {
            "package1": package1,
            "package2": package2
        })

        prompt_text = prompt_response['messages'][0]['content']['text']
        comparison = await self.ai.complete(prompt_text)

        return {
            "packages": [package1, package2],
            "prompt": prompt_text,
            "comparison": comparison
        }

    async def security_review(self, package_name):
        """Conduct security review."""
        prompt_response = await self.mcp.get_prompt("security_review", {
            "package_name": package_name
        })

        prompt_text = prompt_response['messages'][0]['content']['text']
        review = await self.ai.complete(prompt_text)

        return {
            "package": package_name,
            "prompt": prompt_text,
            "security_review": review
        }
```

## Next Steps

- [Data Models](data-models.md) - Complete data structure reference
- [Tools Reference](tools.md) - Interactive tools for data gathering
- [Usage Examples](../user-guide/usage-examples.md) - Practical usage patterns
