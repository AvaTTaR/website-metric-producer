apiVersion: v1
kind: Secret
metadata:
  name: app-met-secret
  namespace: application-met
type: Opaque
stringData:
    POSTGRES_DB_USER: "<DB_USER>"
    POSTGRES_DB_PASSWORD: "<DB_PASSWORD>"