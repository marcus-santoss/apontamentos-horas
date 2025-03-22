from core.imp_clockfy import ClockifyAnnotation
from core.imp_jira import JiraAnnotation

if __name__ == '__main__':
    for provider in [JiraAnnotation, ClockifyAnnotation]:
        provider().fill_annotations(debug=True)
