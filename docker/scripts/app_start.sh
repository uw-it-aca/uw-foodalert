#export DB="sqlite3"
#export AUTH="SAML_MOCK"

echo "app_start actually ran."

/app/bin/python /app/manage.py migrate
