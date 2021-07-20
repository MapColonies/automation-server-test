{{- define "automation-server-test.fullname" -}}
{{- printf "%s" .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "automation-server-test.labels.app" -}}
{{- .Values.nameOverride | default .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "automation-server-test.labels.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "automation-server-test.serviceAccountName" -}}
{{- if .Values.app.serviceAccount.create -}}
{{- .Values.app.serviceAccount.name | default (include "automation-server-test.fullname" .) -}}
{{- else -}}
{{- .Values.app.serviceAccount.name | default "default" -}}
{{- end -}}
{{- end -}}

{{- define "automation-server-test.mapenvsecrets" -}}
{{- if .Values.global.cleanup.enabled }}
- name: CLEAN_UP
  valueFrom:
    secretKeyRef:
      name: {{ .Values.global.cleanup.varName }}
      key: {{ .Values.global.cleanup.enabled }}
{{- end }}
{{- end }}