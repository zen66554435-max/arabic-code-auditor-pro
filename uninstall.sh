#!/usr/bin/env bash
# Arabic Code Auditor Pro - Uninstaller

echo "Uninstalling Arabic Code Auditor Pro..."

# Remove installation directory
rm -rf "$HOME/arabic-code-auditor-pro"

# Remove shortcuts
rm -f "$HOME/.local/bin/aca"
rm -f "$HOME/.local/bin/aca-api"
rm -f "$HOME/.local/bin/aca-frontend"

echo "✅ Uninstalled successfully!"
