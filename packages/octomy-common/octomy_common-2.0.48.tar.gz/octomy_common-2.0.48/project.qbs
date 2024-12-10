Project {
    name: "octomy/common"
    Product {
    
        Group{
            name: "Code - Octomy"
            prefix: "src/octomy"
            excludeFiles: [
                "/**/internal/**/*",
                "/**/__pycache__/**/*",
                "/**/eggs/**/*",
                "/**/.eggs/**/*",
                "/**/.egg-info/**/*",
                "*.egg",
                "*.py[cod]",
            ]
            files: [
                "/**/*.html",
                "/**/*.py",
                "/**/*.sql",
            ]
        }
        Group{
            name: "Code quality"
            prefix: "./"
            excludeFiles: [
                "/**/internal/**/*",
                "/**/__pycache__/**/*",
                "/**/eggs/**/*",
                "/**/.eggs/**/*",
                "/**/.egg-info/**/*",
                "*.egg",
                "*.py[cod]",
            ]
            files: [
                // Code quality stuff
                "code_quality/Makefile",
                "code_quality/mypy.ini",
                "code_quality/pylintrc",
                // Code testing stuff
                "tests/Makefile",
                "tests/pytest.ini",
                "tests/**/*.html",
                "tests/**/*.sql",
                "tests/**/*.py",
            ]
        }
        Group{
            name: "Resources"
            prefix: "resources"
            excludeFiles: "/**/internal/**/*"
            files: [
                "/**/*.html",
                "/**/*.jpeg",
                "/**/*.js",
                "/**/*.mjs",
                "/**/*.md",
                "/**/*.mp4",
                "/**/*.ots",
                "/**/*.png",
                "/**/*.svg",
                "/**/*.ttf",
                "/**/*.woff*",
            ]
        }
        Group{
            name: "Meta"
            prefix: "./"
            excludeFiles: "/**/internal/**/*"
            files: [
                // Environment
                ".env",
                // Ignore files for docker context
                ".gitignore",
                // Ignore files for git staging
                ".dockerignore",
                // Gitlab files such as CI/CD yaml
                ".gitlab/*",
                // Changelog detailing development history of this project
                "CHANGELOG",
                // The dockerfile to build image for this project (needs to be in the root)
                "Dockerfile",
                // Make file with dependencies
                "Makefile*",
                // README generated from template
                "README.md",
                // Version source
                "VERSION",
                // License
                "LICENSE",
                // Resource files
                "resources/*",
                // Configuration files
                "config/*.yaml",
                // Docker & compose files
                "Dockerfile",
                "docker-*.yaml",
                "docker/*.yaml",
                "docker/Dockerfile*",
                // Local helpers to load virtual environment and environment variables
                "local-*.sh",
                //Entrypoint
                "entrypoint.sh",
                // Main project file for IDE
                "project.qbs",
                // Python package requirements
                "requirements/*.in",
                "requirements/*.txt",
                // Python package configuration
                "*setup.*",
                // README template
                "resources/templates/README.md",
            ]
        }
    }
}

