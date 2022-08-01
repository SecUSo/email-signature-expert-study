declare -a addresses=("alice@securepay24.de" "bob@code-audit.org" "bob@code-audil.org" "celine@example.org" "david@example.org" "ezra@code-audit.org" "farah@example.org" "garrett@code-audit.org" "hoy@example.org" "iva@example.org" "joon@code-audit.org" "kemina@example.org")

for address in "${addresses[@]}"; do
	gpg2 --export $address > "${address}.pub";
	gpg2 --export-secret-keys $address > "${address}.sec";
done
